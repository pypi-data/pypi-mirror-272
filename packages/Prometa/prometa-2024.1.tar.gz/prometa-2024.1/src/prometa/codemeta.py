#!/usr/bin/env python
'''
CodeMeta functions.
'''

import contextlib
import json
import logging
import pathlib
import shutil
import subprocess
import tempfile
import tomllib

import tomli_w
import tomli_w._writer

from .file import diff
from .id.orcid import get_orcid_url
from .python.common import get_version
from .python.venv import virtual_environment


LOGGER = logging.getLogger(__name__)


# https://codemeta.github.io/user-guide/
class CodeMeta():
    '''
    Wrapper around the codemetapy command-line executable.
    '''

    def __init__(self, project):
        '''
        Args:
            project:
                The project object.
        '''
        self.project = project
        self._data = None

    @property
    def data(self):
        '''
        The CodeMeta data.
        '''
        if self._data is None:
            try:
                with self.project.codemeta_json_path.open('rb') as handle:
                    self._data = json.load(handle)
            except FileNotFoundError:
                return None
        return self._data

    @property
    def name(self):
        '''
        The project name.
        '''
        try:
            return self.data['name']
        except TypeError:
            return None

    @contextlib.contextmanager
    def _modified_pyproject_toml(self):
        '''
        Context manager to create a temporary modified pyproject.toml file that
        works around current bugs in CodeMetaPy. The origin of the problem is
        that the project metadata now returns custom objects for the "readme"
        and "license" fields while CodeMetaPy still expects these to be strings.
        '''
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_dir = pathlib.Path(tmp_dir)
            git_dir = self.project.git_repo.path
            shutil.copytree(git_dir, tmp_dir, dirs_exist_ok=True, symlinks=True)
            ppt_path = git_dir / 'pyproject.toml'
            tmp_ppt_path = tmp_dir / ppt_path.name

            ppt_data = tomllib.loads(ppt_path.read_text(encoding='utf-8'))
            for field in ('license', 'readme'):
                try:
                    del ppt_data['project'][field]
                except KeyError:
                    pass
            content = tomli_w.dumps(ppt_data, multiline_strings=True)
            tmp_ppt_path.write_text(content, encoding='utf-8')

            yield tmp_ppt_path, ppt_data['project']['name']

    def from_pyproject_toml(self, version=None):
        '''
        Update from a pyproject.toml file.

        Args:
            version:
                The version to set. This is necessary due to SCM incrementing
                the version for unclean directories.
        '''
        author_data = []
        for author in self.project.config.config['authors']:
            data = {
                '@type': 'Person',
                'email': author['email'],
                'givenName': author['given-names'],
                'familyName': author['family-names']
            }
            orcid = author.get('orcid')
            if orcid:
                data['@id'] = get_orcid_url(orcid)
            author_data.append(data)

        codemeta_json_path = self.project.codemeta_json_path
        with self._modified_pyproject_toml() as (tmp_ppt_path, name):
            tmp_dir = tmp_ppt_path.parent
            tmp_path = tmp_dir / codemeta_json_path.name
            with virtual_environment(update_pip=True, inherit=False) as (_venv_dir, venv_exe):
                cmd = [
                    venv_exe,
                    '-m', 'pip',
                    'install', '-U',
                    str(tmp_dir),
                    # TODO
                    # Remove setuptools once CodeMetaPy is updated for Python >
                    # 3.12
                    'CodeMetaPy', 'setuptools'
                ]
                LOGGER.debug('Running command: %s', cmd)
                subprocess.run(cmd, check=True)
                cmd = [
                    venv_exe,
                    '-m',
                    'codemeta.codemeta',
                    '--enrich',
                    '-O', str(tmp_path)
                ]
                LOGGER.debug('Running command: %s', cmd)
                subprocess.run(cmd, check=True, cwd=str(tmp_dir))
            with tmp_path.open('rb') as handle:
                codemeta = json.load(handle)
            codemeta['name'] = name
            codemeta['author'] = author_data
            codemeta['readme'] = self.project.git_repo.readme_url
            codemeta['maintainer'] = author_data[0]
            for cont in codemeta.get('contributor', []):
                if all(
                    cont[key] == author_data[0][key]
                    for key in ('familyName', 'givenName')
                ):
                    cont.clear()
                    cont.update(author_data[0])
            if version:
                codemeta['version'] = version
            codemeta_text = json.dumps(codemeta, indent=2, sort_keys=True)
            if not codemeta_text.endswith('\n'):
                codemeta_text += '\n'
            tmp_path.write_text(codemeta_text, encoding='utf-8')
            diff(tmp_path, codemeta_json_path)
