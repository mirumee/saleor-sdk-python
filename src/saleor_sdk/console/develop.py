import subprocess
import sys

import click


@click.group
def develop():
    pass


@develop.command
def pre_commit():
    """
    Actually invoke the code cleanup as required by the maintainers.

    This is different than the check the pre-commit tool would do but should be
    leveraged by pre-commit as a local tool (it makes sense as all the tools 
    are distributed with the library).
    """
    subprocess.run(["black", "src"])
    subprocess.run(["isort", "src"])
    flake8_proc = subprocess.run(["flake8", "src"])
    if flake8_proc.returncode > 0:
        sys.exit(flake8_proc.returncode)
    mypy_proc = subprocess.run(["mypy", "src"])
    if mypy_proc.returncode > 0:
        sys.exitmypy_proc.returncode()
