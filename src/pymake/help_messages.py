main = """
Usage: pymake [OPTIONS]

Options:
    init      Initialize a new project
    install   Install a package
    upgrade   Upgrade a package
    build     Build a package
    publish   Publish a package
"""

init = """
Usage: pymake init

--no-module
    Do not create a module, use project format instead

Initialize a new project in the current directory
A setup wizard will guide you through the process
"""

update = """
Usage: pymake update [PACKAGE]

Update a package to the latest version
"""

install = """
Usage: pymake install [PACKAGE]

Install a package
"""

check = """
Usage: pymake check

Check for outdated packages and dependencies
"""

build = """
Usage: pymake build

Build the module
"""
