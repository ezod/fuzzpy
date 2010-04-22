"""\
Helper function module.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

from decimal import Decimal, InvalidOperation

def convert_to_decimal(value):
    """\
    Convert a value to decimal type.

    @param value: The value to convert.
    @type value: C{object}
    @return: The converted value.
    @rtype: L{Decimal}
    """
    if not isinstance(value, Decimal):
        try:
            return Decimal(str(value))
        except InvalidOperation:
            raise TypeError, ("value must be numeric")
    return value
