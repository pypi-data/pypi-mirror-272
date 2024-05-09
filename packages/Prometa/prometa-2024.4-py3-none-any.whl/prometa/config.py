#!/usr/bin/env python
'''
Configuration.
'''


import logging
import os
import pathlib
import shlex

import gitlab
import yaml

from .common import NAME

LOGGER = logging.getLogger(__name__)
CONFIG_FILE = f'{NAME}.yaml'

CONFIG_EXAMPLE = '''
# A list of authors. They will appear in various files (e.g. pyproject.toml,
# codemeta.json, CITATIONS.cff).
authors:
    # Given names (required)
  - given-names: John

    # Family names (required)
    family-names: Doe

    # Email (optional)
    email: john.doe@example.com

    # Affiliation (optional)
    affiliation: Example Institute

    # ORCID identifier (optional)
    orcid: XXXX-XXXX-XXXX-XXXX

    # HAL Open Science identifier (optional)
    hal: XXXXXXX

# If true, create missing CITATIONS.cff files.
citations_cff: true

# GitLab settings (optional)
gitlab:
  # Prometa uses python-gitlab to manage GitLab hooks that push code to other
  # open repositories (currently only Software Heritage). python-gitlab requires
  # both a configuration file and the name of the section in the configuration
  # file to use for a given project. For details, see the documentation:
  #
  # https://python-gitlab.readthedocs.io/en/stable/cli-usage.html#cli-configuration
  #
  # python-gitlab configuration file:
  config: path/to/python-gitlab.cfg

  # The section of the python-gitlab configuration file to use when retrieving
  # GitLab project data.
  section: somewhere

  # Map GitLab hosts to their corresponding GitLab Pages URL formats. This map
  # will be used to generate documentation links when a "pages" job is detected
  # in the CI configuration file. The namespace and name parameters correspond
  # to those of the GitLab project.
  pages_urls:
    gitlab.com: "https://{namespace}.gitlab.io/{name}"

  # The regular expression for matching release tags. If given, a CI release job
  # will be created for tags that match this pattern. Omit this or set it to
  # null to disable release jobs.
  release_tag_regex: "^v."

  # Configure tags for GitLab CI jobs. This is a mapping of Python regular
  # expressions to lists of tags. Jobs that match the regular expressions will
  # be tagged with the corresponding tags. If multiple regular expressions match
  # a job then it will accumulate the tags.
  #
  # To apply the same tags to all jobs, use the regular expression ".".
  ci_tags:
      ".":
        - tag1
        - tag2
        - tag3

# The utility to use when merging changes. It must accept two file paths (the
# modified file and the original) and return non-zero exit status to indicate an
# error or abort.
merger: vimdiff
'''.strip()


def _nested_values(data):
    '''
    A generator over all nested values in a dict.
    '''
    if not isinstance(data, dict):
        yield data
        return
    for value in data.values():
        if isinstance(value, dict):
            yield from _nested_values(value)
        else:
            yield value


def _nested_update(old_data, new_data, origin, new_path):
    '''
    Updated nested values in a configuration dict recursively.

    Args:
        old_data:
            The dict to update in place.

        new_data:
            The data to add to old_dict.

        origin:
            A dict of the same layout as old_data but the values are updated
            with the filenames that provided them.

        new_path:
            The path from which new_data was loaded.
    '''
    for key, new_value in new_data.items():
        old_value = old_data.get(key)
        if isinstance(new_value, dict) and isinstance(old_value, dict):
            _nested_update(old_value, new_value, origin[key], new_path)
        else:
            old_data[key] = new_value
            origin[key] = new_path


class Config():
    '''
    Common non-derivable configuration.
    '''
    def __init__(self, proj_path):
        '''
        Args:
            proj_path:
                The project path.
        '''
        self.proj_path = pathlib.Path(proj_path).resolve()
        self._config = None
        self._origin = None

    @property
    def config_paths(self):
        '''
        A generator over configuration file paths. The files are located by
        scanning the project directory and then all parent directories, with
        files closer to the project directory taking precedence. This allows
        common settings to be placed in a common root directory.
        '''
        path = self.proj_path / CONFIG_FILE
        while True:
            if path.exists():
                LOGGER.info('Found configuration file: %s', path)
                yield path
            next_path = path.parent.parent / CONFIG_FILE
            if path != next_path:
                path = next_path
            else:
                return

    @property
    def config(self):
        '''
        The configuration file object. If None, there is no configuration file.
        '''
        if self._config is None:
            configs = [
                (path, yaml.safe_load(path.read_text(encoding='utf-8')))
                for path in self.config_paths
            ]
            final_config = {}
            origin = {}
            for path, config in reversed(configs):
                _nested_update(final_config, config, origin, path)
            self._config = final_config
            self._origin = origin
        return self._config

    def get(self, *keys, default=None):
        '''
        Retrieve a configuration file value. This will scan the loaded
        configuration files in order and return the first match.

        Args:
            *keys:
                The keys to the field. For example, to retrieve the value of
                "bar" under "foo", call get("foo", "bar"). Integers may also be
                used to index lists.

            default:
                The default value to return if no value was found.

        Returns:
            The target value, or the default if no value was found.
        '''
        config = self.config
        origin = self._origin
        for i, key in enumerate(keys):
            try:
                config = config[key]
                try:
                    origin = origin[key]
                except TypeError:
                    pass
            except (KeyError, IndexError):
                return default
            except TypeError as err:
                paths = sorted(set(_nested_values(origin)))
                LOGGER.error(
                    'Failed to retrieve configuration value for %s: %s [%s]',
                    keys[:i + 1],
                    err,
                    ', '.join(shlex.quote(str(p)) for p in paths)
                )
                return default
        return config

    def _get_origin(self, *keys):
        '''
        Similar to get() but returns the origin path for the given keys.
        '''
        origin = self._origin
        if isinstance(origin, pathlib.Path):
            return origin
        for key in keys:
            origin = origin[key]
            if isinstance(origin, pathlib.Path):
                return origin
        return None

    @property
    def gitlab(self):
        '''
        The python-gitlab GitLab instance from the current configuration.
        '''
        path = self.get('gitlab', 'config')
        if path is None:
            LOGGER.warning('No python-gitlab configuration file specified.')
            path = os.getenv('PYTHON_GITLAB_CFG')
            if path is None:
                LOGGER.warning('PYTHON_GITLAB_CFG environment variable is unset.')
                return None
            path = pathlib.Path(path)
        else:
            path = self._get_origin('gitlab', 'config').parent.joinpath(path)
        path = path.resolve()
        section = self.get('gitlab', 'section')
        if not section:
            LOGGER.warning(
                'No section specified for the python-gitlab configuration file: %s',
                path
            )
        return gitlab.Gitlab.from_config(section, [str(path)])
