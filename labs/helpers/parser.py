import constants
from math import *


def parse_param(type_, data):
    if type_.startswith('function'):
        args = type_[9:].replace(';', ',') or 'x'
        func = 'def f(%s):\n return 0.0+%s\n' % (args, data)
        exec (func) in globals(), None  # TODO: resolve security issues
        # FIX: python 3.5 support
        return f
    elif type_ == 'float':
        data = data.replace(',', '.')
        return float(data)
    elif type_ == 'tuple':
        data = data.replace(';', ',').replace('(', '').replace(')', '')
        return tuple(float(x) for x in data.split(','))
    else:
        raise TypeError
