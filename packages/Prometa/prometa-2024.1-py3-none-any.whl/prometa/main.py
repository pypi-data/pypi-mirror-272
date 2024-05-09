#!/usr/bin/env python
'''\
Update project metadata.\
'''

import argparse
import logging
import pathlib
import subprocess
import sys

from .common import NAME
from .config import CONFIG_FILE, CONFIG_EXAMPLE
from .project import Project


LOGGER = logging.getLogger(__name__)


def main(args=None):
    '''
    Main function.
    '''
    parser = argparse.ArgumentParser(
        description=__doc__,
        prog=NAME
    )
    parser.add_argument(
        'path',
        nargs='*',
        help='Path to project directory.'
    )
    parser.add_argument(
        '--gen-config',
        metavar='PATH',
        help=f'''
            Generate a configuration file template at the given path. If the
            path is "-", the file will be printed to STDOUT. Note that %(prog)s
            will only look for files named {CONFIG_FILE}.
            '''
    )
    parser.add_argument(
        '--trust',
        action='store_true',
        help='''
            It is possible to insert arbitrary command output into the README
            file. By default, %(prog)s will prompt the user for confirmation
            before running the command to prevent arbitrary code execution in
            the context of a collaborative environment. This option can be used
            to disable the prompt if the user trusts all of the commands in the
            README.
            '''
    )
    pargs = parser.parse_args(args=args)

    if pargs.gen_config:
        if pargs.gen_config == '-':
            print(CONFIG_EXAMPLE)
        else:
            path = pathlib.Path(pargs.gen_config).resolve()
            LOGGER.info('Creating %s', path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(CONFIG_EXAMPLE, encoding='utf-8')

    for path in pargs.path:
        LOGGER.info('Updating %s', path)
        proj = Project(path, trust_commands=pargs.trust)
        proj.update()


def run_main(args=None):
    '''
    Wrapper around main for exception handling.
    '''
    logging.basicConfig(
        style='{',
        format='[{asctime}] {levelname} {message}',
        level=logging.INFO
    )
    try:
        main(args=args)
    except KeyboardInterrupt:
        pass
    except subprocess.CalledProcessError as err:
        sys.exit(err)


if __name__ == '__main__':
    run_main()
