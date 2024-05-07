import click

from . import __version__


@click.version_option(version=__version__, help="Show version.")
# 老是变，等最后定下来再搞，目前也没啥用
def main():
    pass


