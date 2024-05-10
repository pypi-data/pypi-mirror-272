#!/usr/bin/env python
'''
Virtual environment functions.
'''

import contextlib
import logging
import pathlib
import sysconfig
import tempfile
import subprocess
import sys


LOGGER = logging.getLogger(__name__)


@contextlib.contextmanager
def virtual_environment(update_pip=False, inherit=False):
    '''
    Context manager for creating a temporary virtual environment.

    Args:
        update_pip:
            If True, update pip in the virtual environment.

        inherit:
            If True, create a .pth file to inherit packages from the parent
            environment.
    '''
    parent_purelib = sysconfig.get_paths()['purelib']

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir = pathlib.Path(tmp_dir)
        venv_dir = tmp_dir / 'venv'
        python_exe = pathlib.Path(sys.executable).resolve()
        cmd = [str(python_exe), '-m', 'venv', str(venv_dir)]
        LOGGER.debug('Creating temporary virtual environment: %s', cmd)
        subprocess.run(cmd, check=True)
        venv_exe = venv_dir / 'bin' / python_exe.name
        if update_pip:
            cmd = [str(venv_exe), '-m', 'pip', 'install', '-U', 'pip']
            LOGGER.debug('Updating pip in virtual environment: %s', cmd)
            subprocess.run(cmd, check=True)
        if inherit:
            cmd = [
                str(venv_exe), '-c',
                'import sysconfig; print(sysconfig.get_paths()["purelib"])'
            ]
            LOGGER.debug("Locating virtual environment's purelib directory.")
            child_purelib = subprocess.run(
                cmd, check=True, stdout=subprocess.PIPE
            ).stdout.decode().strip()
            pth_path = pathlib.Path(child_purelib) / 'parent.pth'
            pth_path.write_text(parent_purelib, encoding='utf-8')
        yield venv_dir, venv_exe
