"""
.. module:: __main__.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Specialization validator.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import datetime
import glob
import operator
import os

import utils
import validate_root
import validate_short_table
import validate_topic


# Path to directory in which specializations reside.
_DIR = os.path.dirname(os.path.dirname(__file__))

# Name of associated project.
_PROJECT = __file__.split('/')[-3].split('-specializations-')[0]

# Name of associated specialization.
_TYPEOF = __file__.split('/')[-3].split('-specializations-')[-1]

# Report section break.
_REPORT_BREAK = "------------------------------------------------------------------------"


def _validate_definitions():
    """Validates py definitions.

    """
    # Set specialization modules.
    modules = utils.get_modules(_DIR, _TYPEOF)

    # Set validation context.
    ctx = utils.DefinitionsValidationContext(modules)

    # Validate.
    validate_root.validate(ctx)
    for module in [i for i in ctx.modules if i != ctx.root]:
        validate_topic.validate(ctx, module)

    # Set errors.
    errors = ctx.get_errors()

    # Set report.
    report = []
    if not errors:
        report.append(_REPORT_BREAK)
        report.append("{} {} specializations are valid.".format(_PROJECT.upper(), _TYPEOF))
        report.append(_REPORT_BREAK)
    else:
        error_count = len(reduce(operator.add, errors.values()))
        report.append(_REPORT_BREAK)
        report.append("SPECIALIZATIONS VALIDATION REPORT")
        report.append(_REPORT_BREAK)
        report.append("Specialization Type = {}".format(_TYPEOF))
        report.append("Generated @ {}".format(datetime.datetime.now()))
        report.append("Error count = {}".format(error_count))
        report.append(_REPORT_BREAK)

        # Set report errors.
        for module, errors in sorted(errors.items()):
            report.append("{}.py".format(module.__name__))
            for idx, err in enumerate(errors):
                report.append("Error #{}:\t{}.".format(idx + 1, err))
            report.append("")

    # Write to stdout.
    for l in report:
        print "ES-DOC :: {}".format(l)

    return len(errors) == 0

_validate_definitions()
