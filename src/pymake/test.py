import os


def test(unit, **kwargs):
    if 'pyproject.toml' not in os.listdir():
        print('Tests are not available')
    if f"{unit}.py" not in os.listdir('tests'):
        if input('Unit not found. Create now? [y/N]').lower() == 'y':
            os.system(f"touch tests/{unit}.py")
            print(f"Unit '{unit}' created")
    else:
        os.system(f"cd tests; python3 {unit}.py")
