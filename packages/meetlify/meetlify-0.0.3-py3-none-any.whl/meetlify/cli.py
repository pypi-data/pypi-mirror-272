import click
import os
from .api import Meetlify, initialize
from pathlib import Path


@click.group()
def main():
    pass


@main.command("init", help="Initialize Meetlify Project")
def init():
    click.echo("Initialize Meetlify Project")
    initialize(dest_=Path(os.getcwd()))


@main.command("setup", help="Setup Project Structure")
def setup():
    click.echo("Setup Project Structure")
    Meetlify(dest_=Path(os.getcwd())).setup()


@main.command("clean", help="Clean Output Folder")
def clean():
    click.echo("clean")
    Meetlify(dest_=Path(os.getcwd())).clean()


@main.command("make", help="Make Current Project")
def make():
    click.echo("make")
    Meetlify(dest_=Path(os.getcwd())).make()
