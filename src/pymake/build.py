import subprocess


def build(**kwargs):
    print()
    print('Building package...', end=' ', flush=True)
    out = subprocess.run(['python3', '-m', 'build'], capture_output=True, text=True).stdout.split('\n')
    if out[-2].startswith('Successfully built'):
        print('\r' + out[-2])
    else:
        print('Failed!')
        for i in out:
            print(i)
        print('Failed to build package')
    print()