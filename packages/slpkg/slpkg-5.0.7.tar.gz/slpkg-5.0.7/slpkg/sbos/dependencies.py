#!/usr/bin/python3
# -*- coding: utf-8 -*-


from slpkg.utilities import Utilities


def resolve_requires(data: dict, name: str, flags: list) -> tuple:
    """ Resolve dependencies.

    Args:
        data (dict): Repository data.
        name (str): Slackbuild name.
        flags (list): List of options.

    Returns:
        tuple: Description
    """
    dependencies: tuple = tuple()
    utils = Utilities()

    if not utils.is_option(('-O', '--resolve-off'), flags):
        requires: list[str] = data[name]['requires']
        for require in requires:

            sub_requires: list[str] = data[require]['requires']
            for sub in sub_requires:
                if sub not in requires:
                    requires.append(sub)

        requires.reverse()
        dependencies: tuple = tuple(dict.fromkeys(requires))

    return dependencies
