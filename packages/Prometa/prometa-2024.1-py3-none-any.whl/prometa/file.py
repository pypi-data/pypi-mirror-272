#!/usr/bin/env python3
'''
File operations.
'''

import filecmp
import logging
import pathlib
import shutil
import subprocess
import tempfile


LOGGER = logging.getLogger(__name__)


def diff(path_1, path_2, differ='vimdiff'):
    '''
    Diff 2 paths.
    '''
    if not path_2.exists():
        shutil.copy(path_1, path_2)
        return
    if not filecmp.cmp(path_1, path_2, shallow=False):
        #  if path_1.read_bytes().rstrip(b'\n') == path_2.read_bytes().rstrip(b'\n'):
        #      return
        cmd = [differ, str(path_1), str(path_2)]
        LOGGER.info('Diffing %s and %s', path_1, path_2)
        subprocess.run(cmd, check=True)


def update_content(content, path, encoding='utf-8'):
    '''
    Interactively compare and merge new content.

    Args:
        content:
            The new content to merge.

        path:
            The target path.
    '''
    path = pathlib.Path(path).resolve()
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir = pathlib.Path(tmp_dir)
        tmp_path = tmp_dir / path.with_stem('new').name
        tmp_path.write_text(content, encoding=encoding)
        diff(tmp_path, path)
