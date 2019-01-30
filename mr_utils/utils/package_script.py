'''Package a script together with all its dependencies.

For example, on a remote computer I know for a fact that numpy and scipy are
available, but I cannot or cannot easily gaurantee that module x will be
installed.  I want to run script MyScript.py on this remote machine, but it
depends on module x.  package_script() will recurse through MyScript.py and
prepend module x (and all of module x's dependencies down to numpy, scipy, and
default python modules, assuming I've set existing_modules=['numpy', 'scipy']).
'''

import distutils.sysconfig as sysconfig
import os
import sys
from sys import builtin_module_names
from modulefinder import ModuleFinder

from pip._vendor import pkg_resources

def package_script(filename, existing_modules=None):
    '''Package a script together with all dependencies.

    filename -- Path to Python script we wish to package.
    existing_modules -- List of terminating modules.

    "Terminating module" is a module we assume is available on the machine we
    want to run the packaged script on.  These are python's built-in modules
    plus all existing_modules specified by caller.
    '''

    if existing_modules is None:
        existing_modules = []

    # Choose which modules to ignore
    ignored = []
    for name in existing_modules:
        _package = pkg_resources.working_set.by_key[name]
        ignored += [str(r.name) for r in _package.requires()]
    existing_modules += ignored


    std_lib = sysconfig.get_python_lib(standard_lib=True)

    for top, _dirs, files in os.walk(std_lib):
        for nm in files:
            prefix = top[len(std_lib)+1:]
            if prefix[:13] == 'site-packages':
                continue
            if nm == '__init__.py':
                print(top[len(std_lib)+1:].replace(os.path.sep, '.'))
            elif nm[-3:] == '.py':
                print(os.path.join(prefix, nm)[:-3].replace(os.path.sep, '.'))
            elif nm[-3:] == '.so' and top[-11:] == 'lib-dynload':
                print(nm[0:-3])

    for builtin in sys.builtin_module_names:
        print(builtin)


    existing_modules += builtin_module_names
    print(existing_modules)

    finder = ModuleFinder()
    finder.run_script(filename)
    # finder.report()
    print('Loaded modules:')
    for name, _mod in finder.modules.items():

        # If the module is an existing module, ignore it
        if name.split('.')[0] in existing_modules:
            continue
        print(name.split('.'))

        # print('%s: ' % name, end='')
        # print(','.join(list(mod.globalnames.keys())))
