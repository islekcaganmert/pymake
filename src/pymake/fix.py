import os

from pymake.check import check
from pymake.create_checkpoint import create_checkpoint
from pymake.install import install
from pymake.update import update


def fix(**_):
    fixes = check()
    create_checkpoint()
    print('Running recommended actions:')
    for i in fixes['modules']['reinstall']:
        os.system(f'pip uninstall -y {i}')
        install(i)
    for i in fixes['modules']['update']:
        update(i)
