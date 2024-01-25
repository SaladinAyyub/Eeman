from configparser import ConfigParser
from pathlib import Path

from gi.repository import GLib
import shutil
import os

config = ConfigParser()

datadir = Path(GLib.get_user_data_dir() + "/eeman")
user_path = Path(GLib.get_user_data_dir(), "eeman", "config.ini")
fallback_path = Path(__file__).parent.resolve() / "config.ini"

if not os.path.exists(datadir):
    os.makedirs(datadir)

shutil.copy(fallback_path, user_path)
config_path = user_path

if not config_path.is_file():
    # Fall back to default config file
    config_path = fallback_path


def get_conf():
    return config.read(config_path)
