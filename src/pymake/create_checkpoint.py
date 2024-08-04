import os
from datetime import datetime, UTC


def create_checkpoint(**_):
    print('Taking checkpoint...', end=' ', flush=True)
    if 'requirements.old' not in os.listdir():
        os.mkdir('requirements.old')
    with open(f'requirements.old/{datetime.now(UTC).strftime("%Y%m%d%H%M%S")}', 'w') as f:
        if 'pyproject.toml' in os.listdir():
            with open('pyproject.toml', 'r') as g:
                req = g.read().split('dependencies = [')[1].split(']')[0].split(', ')
            f.write('\n'.join([i.removeprefix('"').removesuffix('"') for i in req]))
        elif 'requirements.txt' in os.listdir():
            with open('requirements.txt', 'r') as g:
                f.write(g.read())
    print('Done!')
