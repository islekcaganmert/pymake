import os
import json
import subprocess


def uninstall(module, **kwargs):
    print()
    freeze_before = subprocess.run(['pip', 'freeze'], capture_output=True, text=True).stdout.split('\n')
    os.system(f'pip uninstall -y {module}')
    freeze_after = subprocess.run(['pip', 'freeze'], capture_output=True, text=True).stdout.split('\n')
    modules = []
    for i in freeze_before:
        if i not in freeze_after:
            modules.append(i.split('==')[0])
    print(f'\nUpdating dependencies...', end=' ', flush=True)
    if 'pyproject.toml' in os.listdir():
        with open('pyproject.toml', 'r') as f:
            data = f.read()
        lines = data.split('\n')
        for i in range(len(lines)):
            line = lines[i]
            if line.startswith('dependencies = '):
                l = json.loads(line.removeprefix('dependencies = '))
                for a in l:
                    for m in modules:
                        if a.startswith(m):
                            l.remove(a)
                lines[i] = f'dependencies = ["{"\", \"".join(l)}"]'
                lines[i] = lines[i].replace('""', '"')
        with open('pyproject.toml', 'w') as f:
            f.write('\n'.join(lines))
    elif 'requirements.txt' in os.listdir():
        with open('requirements.txt', 'r') as f:
            data = f.read()
        lines = data.split('\n')
        for line in lines:
            for m in modules:
                if line.startswith(m):
                    lines.remove(line)
        with open('requirements.txt', 'w') as f:
            f.write('\n'.join(lines))
    print('Done!\n')
