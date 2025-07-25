import os
import click
from cli.openvpn import OpenVPNClient

@click.group()
def cli():
    """GRVPN CLI entry point."""
    pass

@cli.command()
def hello():
    """Prints hello message."""
    click.echo("Hello from GRVPN CLI!")

@cli.command()
@click.argument("path", type=click.Path(exists=True))
def test(path: str):
    """Test the CLI."""
    password = click.prompt("Enter your password", hide_input=True)
    os.environ["SUDO_PASSWORD"] = password
    vpn = OpenVPNClient(path)
    print(vpn.status)
    vpn.connect()
    print(vpn.status)

if __name__ == "__main__":
    cli()