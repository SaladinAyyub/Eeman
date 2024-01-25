from configparser import ConfigParser
from pathlib import Path

from gi.repository import GLib

config = ConfigParser()

config_path = Path(GLib.get_user_data_dir(), ".", "config.ini")

if not config_path.is_file():
    # Fall back to default config file
    config_path = Path(__file__).parent.resolve() / "config.ini"


def get_conf():
    return config.read(config_path)
