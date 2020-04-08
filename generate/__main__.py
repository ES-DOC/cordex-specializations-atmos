"""
.. module:: __main__.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: ES-DOC specialization validator.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import argparse
import os

from generate_js import Generator as JavascriptGenerator
from generate_json import Generator as JSONGenerator
from generate_mm import Generator as MindmapGenerator
from utils_factory import get_specialization
from utils_loader import get_modules



# Name of associated project.
_PROJECT = __file__.split('/')[-3].split('-')[0]

# Specializations type is derived from repo name.
_TYPEOF = os.path.dirname(os.path.dirname(__file__)).split("/")[-1].split("-")[-1]

# Map of generator types to generator.
_GENERATORS = {
    'js': JavascriptGenerator,
    'json': JSONGenerator,
    'mm': MindmapGenerator,
}

# Map of generator types to file prefixes.
_FILE_PREFIXES = {
    'js': '_',
    'json': '_',
    'mm': '_',
}

# Map of generator types to directories.
_DIRECTORIES = {
    'js': '',
    'json': '',
    'mm': '',
}

# Set directory from which module is being run.
_DIR = os.path.dirname(__file__)

# Set command line arguments.
_ARGS = argparse.ArgumentParser("Encodes a specialization.")
_ARGS.add_argument(
    "--type",
    help="Type of generator to be executed.",
    dest="typeof",
    type=str,
    default="all"
    )
_ARGS.add_argument(
    "-o", "--output-dir",
    help="Path to a directory into which generated content will be written.",
    dest="output_dir",
    type=str,
    default=os.path.dirname(_DIR)
    )
_ARGS.add_argument(
    "--scope",
    help="Name of specialization scope being processed.",
    dest="scope",
    type=str,
    default=_TYPEOF
    )
_ARGS.add_argument(
    "--input",
    help="Path to a directory in which specializations reside.",
    dest="input_dir",
    type=str,
    default=os.path.dirname(_DIR)
    )
_ARGS = _ARGS.parse_args()


# Validate inputs.
if _ARGS.typeof != 'all' and _ARGS.typeof not in _GENERATORS.keys():
    err = "Unknown generator type [{}].  Validate types = {}."
    err = err.format(_ARGS.typeof, " | ".join(sorted(_GENERATORS.keys())))
    raise ValueError(err)

# Set specialization filename prefix.
_FILENAME = _ARGS.scope

# Set target generators to be executed.
if _ARGS.typeof == 'all':
    targets = _GENERATORS
else:
    targets = {
        _ARGS.typeof: _GENERATORS[_ARGS.typeof]
    }

# Set specialization modules.
modules = get_modules(_ARGS.input_dir, _FILENAME)
specialization = get_specialization(modules)

logging_output = []
for generator_type, generator_cls in targets.iteritems():
    # Run generator
    generator = generator_cls(_PROJECT, specialization)
    generator.run()

    # Set output file name.
    fname = "{}{}.{}".format(
        _FILE_PREFIXES.get(generator_type, ''),
        _FILENAME,
        generator_type
        )
    if fname.endswith('.py'):
        fname = fname.replace("-", "_")

    # Set output file path.
    fpath = _ARGS.output_dir
    dpath = _DIRECTORIES.get(generator_type, '')
    for part in dpath.split('/'):
        fpath = os.path.join(fpath, part)
    fpath = os.path.join(fpath, fname)

    # Write generated output to file system.
    with open(fpath, 'w') as fstream:
        fstream.write(generator.get_output())

    logging_output.append((fname.split('.')[-1], fpath))


# Inform user.
for encoding, fpath in sorted(logging_output):
    print "ES-DOC :: generated {} file written to --> {}".format(encoding, fpath)
