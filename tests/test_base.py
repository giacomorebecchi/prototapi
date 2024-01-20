from importlib.metadata import version

from prototapi import __project_name__, __version__


def test_project_name():
    assert isinstance(__project_name__, str)


def test_version():
    assert isinstance(__version__, str)
    assert __version__ == version(__project_name__)
