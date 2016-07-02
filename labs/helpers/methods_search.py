import os
import sys
import logging
import inspect
from .classes import Method
import constants

if sys.version_info[0] == 2:
    import imp
else:
    import importlib.util


def find_methods(file_path):
    def find_subclasses(module):
        return [cls for name, cls in inspect.getmembers(module) if inspect.isclass(cls) and issubclass(cls, Method)]

    cur_directory = os.path.dirname(file_path)
    methods = []
    for o in os.listdir(cur_directory):
        t = os.path.join(cur_directory, o)
        if os.path.isdir(t):
            method = os.path.join(t, 'method.py')
            if os.path.isfile(method):
                try:
                    if sys.version_info[0] == 2:
                        module = imp.load_source(o, method)
                    else:
                        spec = importlib.util.spec_from_file_location(o, method)
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                    logging.info('Imported %s' % o)
                    methods.extend(find_subclasses(module))
                except:
                    logging.warning('Failed to import %s' % o)
    print methods
    return methods
