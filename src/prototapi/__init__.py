from importlib.metadata import version
from pathlib import Path

__project_name__ = "prototapi"
__version__ = version(__project_name__)
__package_dir__ = Path(__file__).absolute().parent

__user_agent__ = {"prototapi": __version__}
