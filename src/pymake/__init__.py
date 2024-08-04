import os
import sys
import subprocess

import pymake.help_messages as help_messages
from pymake.init import init
from pymake.check import check
from pymake.update import update
from pymake.install import install
from pymake.fix import fix
from pymake.rollback import rollback
from pymake.create_checkpoint import create_checkpoint
from pymake.uninstall import uninstall
from pymake.restore import restore
from pymake.run import run
from pymake.build import build
from pymake.test import test


def main():
    raw_args = sys.argv[1:]
    args = []
    kwargs = {
        'help': False,
        'no-module': False
    }
    if raw_args:
        while raw_args and not raw_args[0].startswith('--'):
            args.append(raw_args.pop(0).replace('-', '_'))
        while raw_args:
            key = raw_args.pop(0).removeprefix('--')
            if not raw_args:
                kwargs[key] = True
            elif raw_args[0].startswith('--'):
                kwargs[key] = True
            else:
                value = raw_args.pop(0)
                kwargs[key] = value

    if kwargs['help']:
        if not args:
            lines = help_messages.main
        elif hasattr(help_messages, args[0]):
            lines = getattr(help_messages, args[0])
        else:
            lines = f"Unknown command: {args[0]}"
        print(lines)
    elif not args:
        print("Usage: pymake [OPTIONS]")
        print("For help: pymake --help")
        sys.exit(1)
    elif args[0] in globals() and callable(globals()[args[0]]):
        try:
            globals()[args[0]](*args[1:], **kwargs)
        except TypeError as e:
            if str(e).startswith(f'{args[0]}() takes ') and str(e).endswith(f'positional arguments but {len(args)-1} was given'):
                print(getattr(help_messages, args[0]).split('\n')[1])
            else:
                raise e
    else:
        print(f"Unknown command: {args[0]}")
