import click
from nipe_py import Stop, Start, Restart
from nipe_py import Status, Install
from rich import print
from rich.panel import Panel


@click.group()
def cli():
    pass


@cli.command()
def install():
    """Install dependencies"""
    Install()


@cli.command()
def start():
    """Start routing"""
    st = Start()
    st.start()
    print(Panel("[+] [green]nipe has been started...."))


@cli.command()
def stop():
    """Stop routing"""
    stop = Stop()
    stop.stop()
    print(Panel("[+] [red]nipe has been stopped...."))


@cli.command()
def restart():
    """Restart the Nipe circuit"""
    rst = Restart()
    rst.restart()
    print(Panel("[+] [red]nipe has been restated...."))


@cli.command()
def status():
    """See status"""
    Status()


if __name__ == "__main__":
    cli()
