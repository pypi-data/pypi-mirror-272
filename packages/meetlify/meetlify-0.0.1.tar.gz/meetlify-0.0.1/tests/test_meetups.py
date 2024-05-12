from meetlify.api import initialize, Meetlify
from pathlib import Path
import os


def test_init():
    initialize(dest_=Path(os.path.dirname(os.path.realpath(__file__)), "results"))


def test_setup():
    Meetlify(dest_=Path(os.path.dirname(os.path.realpath(__file__)), "results")).setup()


def test_cleanup():
    Meetlify(dest_=Path(os.path.dirname(os.path.realpath(__file__)), "results")).clean()


def test_make():
    Meetlify(dest_=Path(os.path.dirname(os.path.realpath(__file__)), "results")).make()
