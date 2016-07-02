import os
import sys
if sys.version_info[0] == 2:
    import imp
else:
    import importlib.util
import logging

cur_directory = os.path.dirname(__file__)
labs = []
for directory in os.listdir(cur_directory):
    dir_ = os.path.join(cur_directory, directory)
    if os.path.isdir(dir_):
        if os.path.exists(os.path.join(dir_, 'lab.py')):
            try:
                if sys.version_info[0] == 2:
                    module = imp.load_source(directory, os.path.join(dir_, 'lab.py'))
                else:
                    spec = importlib.util.spec_from_file_location(directory, os.path.join(dir_, 'lab.py'))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                labs.append([directory,module])
                logging.info('Imported %s' % directory)
            except:
                logging.warning('Failed to import %s' % directory)
                raise
