"""
.. module:: utils_loader.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Loads specialization from file system.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import imp
import json
import os
import glob



def get_modules(input_dir, typeof):
    """Returns specialization modules.

    :param str input_dir: Directory within which modules reside.
    :param str typeof: Type of specialization being processed.

    """
    # Load specialization modules.
    modules = _get_modules(input_dir, typeof)
    if not modules:
        raise KeyError("Specializations not found")

    # Set specializations.
    root = _get_module(modules, typeof)
    children = [_get_module(modules, i) for i in [
        '{}_key_properties'.format(typeof),
        '{}_grid'.format(typeof)
    ] + root.PROCESSES]

    return [root] + [i for i in children if i is not None]


def _get_modules(input_dir, typeof):
    """Returns a set of specialization modules.

    """
    def _is_target(fname):
        return not fname.startswith('_') and \
               fname.endswith('.py') and \
               fname.startswith(typeof)

    modules = sorted([i for i in os.listdir(input_dir) if _is_target(i)])
    modules = [os.path.join(input_dir, m) for m in modules]
    modules = [(m.split("/")[-1].split(".")[0], m) for m in modules]
    modules = [imp.load_source(i, j) for i, j in modules]

    return modules


def _get_module(modules, name):
    """Returns a specialization module.

    """
    for module in modules:
        if module.__name__ == name:
            return module
