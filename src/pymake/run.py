import os


def run(**kwargs):
    if 'pyproject.toml' in os.listdir():
        if '__main__.py' in os.listdir(f"src/{os.listdir('src')[0].split('.')[0]}"):
            os.system(f"python3 -m {os.listdir('src')[0].split('.')[0]}")
        else:
            print("Module is not executable")
    elif 'requirements.txt' in os.listdir():
        os.system("python3 main.py")
    pass
