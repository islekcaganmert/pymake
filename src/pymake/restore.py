import os
from pymake.install import install


def restore(**kwargs):
    modules = []
    if 'file' in kwargs:
        with open(kwargs['file'], 'r') as f:
            modules = f.read().removeprefix('\n').removesuffix('\n').split('\n')
    elif 'pyproject.toml' in os.listdir():
        with open('pyproject.toml', 'r') as f:
            data = f.read()
        lines = data.split('\n')
        for i in range(len(lines)):
            line = lines[i]
            if line.startswith('dependencies = '):
                modules = json.loads(line.removeprefix('dependencies = '))
    elif 'requirements.txt' in os.listdir():
        with open('requirements.txt', 'r') as f:
            modules = f.read().removesuffix('\n').removeprefix('\n').split('\n')
    for i in modules:
        install(i.split(' ')[-1], no_dependencies=True)
