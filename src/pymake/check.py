import subprocess
import os


def check(**kwargs):
    modules = {}
    debug_modules = []
    for i in subprocess.run(["pip", "freeze"], capture_output=True, text=True).stdout.splitlines():
        if i.startswith("WARNING:") or i.startswith('## '):
            pass
        elif i.startswith("-e "):
            debug_modules.append(i.removeprefix("-e "))
        elif '==' in i:
            modules.update({i.split('==')[0]: i.split('==')[1]})
        else:
            modules.update({i.split(' @ ')[0]: i.split(' @ ')[1]})
    for i in ['pymake', 'build', 'packaging', 'pyproject_hooks']:
        if i in modules:
            modules.pop(i)
    dependencies = {}
    if 'pyproject.toml' in os.listdir():
        with open('pyproject.toml', 'r') as f:
            for i in f.read().split('dependencies = [')[1].split(']')[0].split(', '):
                if '==' in i:
                    dependencies.update({
                        i.removeprefix('"').removesuffix('"').split('==')[0]: i.removeprefix('"').removesuffix('"').split('==')[1]
                    })
    elif 'requirements.txt' in os.listdir():
        with open('requirements.txt', 'r') as f:
            for i in f.read().split('\n'):
                if '==' in i:
                    dependencies.update({i.split('==')[0]: i.split('==')[1]})
                elif ' @ ' in i:
                    dependencies.update({i.split(' @ ')[0]: i.split(' @ ')[1]})
    else:
        print('pymake: error: folder unrecognized')
        return
    updates = {}
    for i in subprocess.run(["pip", "list", "--outdated"], capture_output=True, text=True).stdout.splitlines():
        if i.startswith("Package") or i.startswith("-------"):
            pass
        elif i.replace(' ', '') == '':
            break
        else:
            try:
                x = i.replace('  ', ' ').split(' ')
                updates.update({x[0]: x[2]})
            except IndexError:
                pass
    fixes = {
        'modules': {
            'reinstall': [],
            'update': [],
        },
    }
    print('\nModules:')
    all_ok = True
    if os.popen('pwd').read().replace('\n', '') in modules:
        modules.pop(os.popen('pwd').read().replace('\n', ''))
    for i in modules:
        if i not in dependencies:
            all_ok = False
            print(f"\t{i} is installed manually, reinstallation is recommended")
            fixes['modules']['reinstall'].append(f'{i}=={modules[i]}')
        elif modules[i] != dependencies[i]:
            all_ok = False
            print(f"\t{i} is upgraded/downgraded manually, reinstallation is recommended")
            fixes['modules']['reinstall'].append(f'{i}=={modules[i]}')
        elif i in updates:
            all_ok = False
            print(f"\t{i} is outdated, update is recommended")
            fixes['modules']['update'].append(i)
    for i in debug_modules:
        all_ok = False
        print(f"\t{i} is installed in editable mode, reinstallation must be done before build")
    if all_ok:
        print("\tAll modules are up-to-date")
    print()
    return fixes
