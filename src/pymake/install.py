import os
import json
import subprocess


def install(module, **kwargs):
    print()
    freeze_before = subprocess.run(['pip', 'freeze'], capture_output=True, text=True).stdout.split('\n')
    if '/' in module and 'https://' not in module:
        if '@' in module:
            h = f"@{module.split('@')[1]}"
            module = module.split('@')[0]
        else:
            h = ''
        os.system(f'pip install git+https://github.com/{module}.git{h} {"--upgrade" if kwargs.get("upgrade") else ""} {"--no-dependencies" if kwargs.get("no_dependencies") else ""}')
    else:
        if 'https://' in module:
            module = f"git+{module.removeprefix('git+')}"
        os.system(f'pip install {module} {"--upgrade" if kwargs.get("upgrade") else ""} {"--no-dependencies" if kwargs.get("no_dependencies") else ""}')
    freeze_after = subprocess.run(['pip', 'freeze'], capture_output=True, text=True).stdout.split('\n')
    modules = []
    for i in freeze_after:
        if i not in freeze_before:
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
                for m in modules:
                    if '@' in m:
                        l.append(m)
                    else:
                        l.append(f'{m}=={os.popen(f"pip show {m} | grep Version").read().split(': ')[1].removesuffix('\n')}')
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
        for m in modules:
            if '@' in m:
                lines.append(m)
            else:
                lines.append(f'{m}=={os.popen(f"pip show {m} | grep Version").read().split(": ")[1].removesuffix("\n")}')
        with open('requirements.txt', 'w') as f:
            f.write('\n'.join(lines))
    print('Done!\n')
