#!/usr/bin/env python
'''
All things specific to Python (pyproject.toml, PyPI, etc.)
'''

import logging
import pathlib
import subprocess
import tomllib
from urllib.parse import quote as urlquote

import requests
import tomli_w
import tomli_w._writer
from spdx_license_list import LICENSES as SPDX_LICENSES

from ..file import update_content
from .venv import virtual_environment

LOGGER = logging.getLogger(__name__)


def get_pypi_url(name):
    '''
    Get the URL to the project's page on PyPI if it exists.

    Args:
        name:
            The project name.

    Returns:
        The project URL, or None if it does not exist.
    '''
    timeout = 5
    url = f'https://pypi.org/pypi/{urlquote(name)}/json'
    LOGGER.debug('Querying %s', url)
    resp = requests.get(url, timeout=timeout).json()
    try:
        return resp['info']['package_url']
    except KeyError:
        return None


def update_pyproject_toml(project):
    '''
    Update the URLs in a pyproject.toml file.

    Args:
        project:
            The Project instance.
    '''
    path = project.pyproject_toml_path
    data = tomllib.loads(path.read_text(encoding='utf-8'))

    urls = data['project']['urls']
    urls.clear()
    urls.update(project.urls)

    data['project']['authors'] = [
        {
            'name': f'{author["given-names"]} {author["family-names"]}',
            'email': author['email']
        }
        for author in project.config.config['authors']
    ]

    classifiers = set(
        classifier
        for classifier in data['project'].get('classifiers', [])
        if not classifier.startswith('License :: ')
    )
    # TODO
    # Make this more robust and find a way to validate the constructed
    # classifier strings. The recognized classifiers are listed on pypi.org:
    #
    # https://pypi.org/classifiers/
    #
    # Check if there is an API to retrieve them programmatically. If not, scrape
    # and cache the page with an HTML parser.
    found_license = False
    spdx_id = project.spdx_license
    if spdx_id:
        spdx_data = SPDX_LICENSES.get(spdx_id)
        if spdx_data:
            name = spdx_data.name
            if spdx_id not in name.split():
                name += f' ({spdx_id})'
            if spdx_data.osi_approved:
                classifiers.add(f'License :: OSI Approved :: {name}')
            else:
                classifiers.add(f'License :: {name}')
            found_license = True
    if not found_license:
        LOGGER.warning('Failed to detect SPDX-recognized license')

    data['project']['classifiers'] = sorted(classifiers)

    content = tomli_w.dumps(data, multiline_strings=True)
    update_content(content, path)
    return urls


def get_version(project_dir):
    '''
    Get the version of a project from its directory.

    This will create a temporary virtual environment and install the project in
    it to get the version. This ensures that VCS-versions are correctly handled.

    This should not be necessary but at the time or writing the current version
    of CodeMetaPy fails to detect versions.
    '''
    project_dir = pathlib.Path(project_dir).resolve()
    with virtual_environment() as (_venv_dir, python_exe):
        cmd = [python_exe, '-m', 'pip', 'install', '--no-deps', '-U', str(project_dir)]
        LOGGER.debug('Installing package in virtual environment: %s', cmd)
        subprocess.run(cmd, check=True)

        data = tomllib.loads((project_dir / 'pyproject.toml').read_text(encoding='utf-8'))
        name = data['project']['name']
        cmd = [
            python_exe, '-c',
            f'from importlib.metadata import version; print(version("{name}"))'
        ]
        LOGGER.debug('Getting version of %s: %s', name, cmd)
        return subprocess.run(cmd, check=True, capture_output=True).stdout.decode().strip()
