# Package to extend Klipper with my custom functionality
#
# Copyright (C) 2023  Jan Nakladal <mojeto1@gmail.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import importlib

# def load_config(config):
#     """place to store common configuration shared across extras"""
#     # todo


def load_config_prefix(config):
    """
    Use section name to match and load my_extras module
    This is a hack to extend klipper extras dynamically with custom modules
    I hope in more official way to do this in future e.g.
    https://klipper.discourse.group/t/adding-support-for-a-users-extras-directory/3175
    """
    name = config.get_name().split(maxsplit=2)[-1]
    try:
        my_module = importlib.import_module(f".{name}", package=__name__)
        if hasattr(my_module, "load_config") and callable(my_module.load_config):
            return my_module.load_config(config)
        else:  # raise import error to get proper error message to the end user.
            raise ImportError(f"`{name}.load_config()` function missing! Can't import")
    except ImportError:
        raise config.error(
            f"Section name {name!r} in [{config.get_name()}] section is not valid my_extras module "
            "Please choose a correct module name."
        )
