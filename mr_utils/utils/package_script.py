'''Package a script together with all its dependencies.

For example, on a remote computer I know for a fact that numpy and scipy are
available, but I cannot or cannot easily gaurantee that module x will be
installed.  I want to run script MyScript.py on this remote machine, but it
depends on module x.  package_script() will recurse through MyScript.py and
prepend module x (and all of module x's dependencies down to numpy, scipy, and
default python modules, assuming I've set existing_modules=['numpy', 'scipy']).
'''

import importlib
import os
import distutils.sysconfig as sysconfig
import re
import inspect

def get_std_lib():
    '''Get list of all Python standard library modules.'''
    ignored = set()
    std_lib = sysconfig.get_python_lib(standard_lib=True)
    for top, _dirs, files in os.walk(std_lib):
        for nm in files:
            prefix = top[len(std_lib)+1:]
            if prefix[:13] == 'site-packages':
                continue
            if nm == '__init__.py':
                ignored.add(top[len(std_lib)+1:].replace(
                    os.path.sep, '.').split('.')[0])
            elif nm[-3:] == '.py':
                ignored.add(os.path.join(
                    prefix, nm)[:-3].replace(os.path.sep, '.').split('.')[0])
            elif nm[-3:] == '.so' and top[-11:] == 'lib-dynload':
                ignored.add(nm[0:-3].split('.')[0])
    return list(ignored)

def get_imports(filename, existing_modules=None):
    '''Removes import statements and gets filenames of where imports are.'''

    if existing_modules is None:
        existing_modules = []

    stripped = ''
    keep_imports = []
    stdlib = get_std_lib()
    imports = set()
    files = set()
    with open(filename, 'r') as f:
        for line in f:

            # Remove lines we don't care for
            if '__all__' in line:
                continue

            if 'import' in line:

                # Remove comments
                im = line.split('#')[0]

                # Check to make sure we didn't kill the whole line
                if 'import' not in im:
                    continue

                # Remove test cases
                if '>>>' in im:
                    continue

                # Remove aliases
                # im = re.sub(r'\s+as\s+', '', im)
                im = re.split(r'\s+as\s+', im)[0]

                # Remove key words
                im = im.replace('from', '').replace('import', '')

                # Remove whitespace
                im = im.strip()

                # Make to look like mod.mody.mod function
                im = re.sub(r'\s+', ' ', im)


                # Add to set if it's not in the stdlib
                if im.split('.')[0] not in stdlib + existing_modules:
                    imports.add(im)

                    # Load in the module to get info about it
                    module = importlib.import_module(im.split(' ')[0])

                    # If there's more than one import, get files for all
                    if len(im.split(' ')) > 1:
                        for ii in range(1, len(im.split(' '))):
                            thing = getattr(module, im.split(' ')[ii])
                            for name, obj in inspect.getmembers(thing):
                                if name == '__code__':
                                    files.add(obj.co_filename)
                    else:
                        # If not, get the module's file
                        files.add(module.__file__)

                else:
                    keep_imports.append(line)
            else:
                stripped += line

    return(stripped, keep_imports, list(files))

def package_script(filename, existing_modules=None):
    '''Package a script together with all dependencies.

    filename -- Path to Python script we wish to package.
    existing_modules -- List of terminating modules.

    "Terminating module" is a module we assume is available on the machine we
    want to run the packaged script on.  These are python's built-in modules
    plus all existing_modules specified by caller.
    '''

    stripped_concat = ''
    files = set()
    keep_imports = set()
    prev_len = -1
    prev_files = set()
    prev_files.add(filename)
    while len(files) > prev_len:

        for prev_f in prev_files:
            stripped, keep, new_files = get_imports(prev_f, existing_modules)
            stripped_concat += '\n' + stripped

            # Add the imports we want to keep to the list
            for k in keep:
                keep_imports.add(k)

        prev_files = set()
        prev_len = len(files)
        for new_f in new_files:
            files.add(new_f)
            prev_files.add(new_f)

    # import json
    # print('FINAL TALLY:')
    # print(json.dumps(list(files), indent=4, sort_keys=True))

    # Append all the imports we wanted to keep to the top of the file
    stripped_concat = ''.join(list(keep_imports)) + stripped_concat

    return stripped_concat
