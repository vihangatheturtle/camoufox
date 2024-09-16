"""
Binary CLI manager for Camoufox.

Adapted from https://github.com/daijro/hrequests/blob/main/hrequests/__main__.py
"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as pkg_version

import click

from .pkgman import CamoufoxFetcher, installed_verstr, rprint


class CamoufoxUpdate(CamoufoxFetcher):
    """
    Checks & updates Camoufox
    """

    def __init__(self) -> None:
        """
        Initializes the CamoufoxUpdate class
        """
        super().__init__()
        try:
            self.current_verstr = installed_verstr()
        except FileNotFoundError:
            self.current_verstr = None

    def is_updated_needed(self) -> None:
        if self.current_verstr is None:
            return True
        # If the installed version is not the latest version
        if self.current_verstr != self.verstr:
            return True
        return False

    def update(self) -> None:
        """
        Updates the library if needed
        """
        # Check if the version is the same as the latest available version
        if not self.is_updated_needed():
            rprint("Camoufox binaries up to date!", fg="green")
            rprint(f"Current version: v{self.current_verstr}", fg="green")
            return

        # Download updated file
        if self.current_verstr is not None:
            # Display an updating message
            rprint(
                f"Updating Camoufox binaries from v{self.current_verstr} => v{self.verstr}",
                fg="yellow",
            )
        else:
            rprint(f"Fetching Camoufox binaries v{self.verstr}...", fg="yellow")
        # Install the new version
        self.install()


@click.group()
def cli() -> None:
    pass


@cli.command(name='fetch')
def fetch():
    """
    Fetch the latest version of Camoufox
    """
    CamoufoxUpdate().update()


@cli.command(name='remove')
def remove() -> None:
    """
    Remove all library files
    """
    if not CamoufoxUpdate().cleanup():
        rprint("Camoufox binaries not found!", fg="red")


@cli.command(name='version')
def version() -> None:
    """
    Display the current version
    """
    # python package version
    try:
        rprint(f"Pip package:\tv{pkg_version('camoufox')}", fg="green")
    except PackageNotFoundError:
        rprint("Pip package:\tNot installed!", fg="red")

    updater = CamoufoxUpdate()
    bin_ver = updater.current_verstr

    # If binaries are not downloaded
    if not bin_ver:
        rprint("Camoufox:\tNot downloaded!", fg="red")
        return
    # Print the base version
    rprint(f"Camoufox:\tv{bin_ver} ", fg="green", nl=False)

    # Check for library updates
    if updater.is_updated_needed():
        rprint(f"(Latest: v{updater.verstr})", fg="red")
    else:
        rprint("(Up to date!)", fg="yellow")


if __name__ == '__main__':
    cli()
