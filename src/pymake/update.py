from pymake.install import install


def update(module, **kwargs):
    install(module, upgrade=True)
