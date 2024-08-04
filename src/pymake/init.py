from datetime import datetime, UTC
import os
from pymake.licenses import (
    mit,
    gpl_3_0,
    lgpl_3_0,
    agpl_3_0,
    apache_2_0,
    bsd_3_clause,
    unlicense,
    cc_by_4_0,
    cc_by_sa_4_0,
    cc_by_nc_4_0,
    cc_by_nc_sa_4_0,
    cc_by_nd_4_0,
    cc_by_nc_nd_4_0,
    cc0
)

licenses_dict = {
    "MIT": mit,
    "GNU General Public License 3.0": gpl_3_0,
    "GNU Lesser General Public License 3.0": lgpl_3_0,
    "GNU Affero General Public License 3.0": agpl_3_0,
    "Apache License 2.0": apache_2_0,
    "The 3-Clause BSD License": bsd_3_clause,
    "Creative Commons Attribution 4.0": cc_by_4_0,
    "Creative Commons Attribution ShareAlike 4.0": cc_by_sa_4_0,
    "Creative Commons Attribution NonCommercial 4.0": cc_by_nc_4_0,
    "Creative Commons Attribution NonCommercial ShareAlike 4.0": cc_by_nc_sa_4_0,
    "Creative Commons Attribution NoDerivates 4.0": cc_by_nd_4_0,
    "Creative Commons Attribution NonCommercial NoDerivates 4.0": cc_by_nc_nd_4_0,
    "CC0": cc0,
    "Unlicense": unlicense
}


def licenses(name):
    return licenses_dict[name].text.removeprefix('\n')


def init(**kwargs):
    info = {
        "name": input("Name: "),
        "description": None if kwargs['no-module'] else input("Description: "),
        "license": "NOLICENSE",
        "maintainers": [],
        "python_version": None if kwargs['no-module'] else input("Python Version: "),
        "homepage_url": None if kwargs['no-module'] else input("Homepage URL: ")
    }
    print()
    print("Choose a license:")
    for i, j in enumerate(licenses_dict.keys()):
        print(f"{i+1}. {j}")
    print()
    info['license'] = licenses_dict.keys()[int(input("License: "))-1]
    print()
    if not kwargs['no-module']:
        print("Add maintainers in the format: Name <email>")
        print("Send blank line when you are finished")
        print()
        lines = []
        while not lines or lines[-1] != '':
            lines.append(input().replace('"', ''))
        for i in lines:
            if ' <' in i and '>' in i:
                info['maintainers'].append({'name': i.split(' <')[0], 'email': i.split(' <')[1].replace('>', '')})
        developer = info['maintainers'][0]['name']
    else:
        developer = input("Developer: ")
        print()

    print('Initializing project...', end=' ', flush=True)
    if kwargs['no-module']:
        with open('requirements.txt', 'w') as f:
            f.write('')
    else:
        with open('pyproject.toml', 'w') as f:
            f.write('''[project]
name = "''' + info['name'] + '''"
version = "0.1.0"
description = "''' + info['description'] + '''"
readme = "README.md"
license = {text = "''' + info['license'] + '''"}
maintainers = [''' + '' + ''']
requires-python = ">= ''' + info['python_version'] + '''"
dependencies = []

[project.urls]
Homepage = "''' + info['homepage_url'] + '''"

[build-system]
requires = ["setuptools","wheel"]
build-backend = "setuptools.build_meta"
''')
    with open('README.md', 'w') as f:
        f.write(f'# {info["name"]}\n\n{info["description"] if info["description"] else ""}')
    with open('LICENSE', 'w') as f:
        f.write(
            licenses(info['license'])
            .replace('???YEAR???', str(datetime.now(UTC).year))
            .replace('???HOLDER???', developer)
        )
    os.mkdir('src')
    if not kwargs['no-module']:
        os.mkdir('tests')
        os.mkdir(f'src/{info["name"]}')
    with open(f'src/main.py' if kwargs['no-module'] else f'src/{info["name"]}/__init__.py', 'w') as f:
        f.write('')
    with open('.gitignore', 'w') as f:
        f.write('__pycache__/\n.idea\n.code\n*.egg-info\ntests/\n.DS_Store\nrequirements.old\n')
    print('Done!\n')
    if not kwargs['no-module']:
        print('Installing package...', end=' ', flush=True)
        os.system('pip install -e . > /dev/null')
        print('Done!\n')
