'''Generate all README files for all the modules.

We rely heavily on the pydoc.render_doc() method.
'''

from pkgutil import walk_packages
import ast,importlib,pydoc,re

if __name__ == '__main__':
    def top_level_functions(body):
        return (f for f in body if isinstance(f, ast.FunctionDef))

    def top_level_objects(body):
        return(o for o in body if isinstance(o,ast.ClassDef))

    def parse_ast(filename):
        with open(filename, "rt") as file:
            return ast.parse(file.read(), filename=filename)


    # Don't include setup, because it'll try to run it...
    all_modules = [ p for p in walk_packages('.') if not p[-1] and p[1] != 'setup' and p[1] != 'mr_utils.load_data.parsetab' ]
    docs = ''

    # First of all, a little orientation
    docs += """# mr_utils

mr_utils: magnetic resonance utilities. This repo is a collection of my
implementations of algorithms and tools for MR image reconstruction, mostly
in python.

## Orientation
There are few different things going on here.  There are algorithms, like the [geometric solution to the elliptical signal model](../master/mr_utils/recon/ssfp), as well as simulations, like [simulated bSSFP contrast](../master/mr_utils/sim/ssfp).

There's also some python functions and objects that interact with more polished tools such as [Gadgetron](../master/mr_utils/gadgetron) and [BART](../master/mr_utils/bart). You can use these python interfaces to easily write in Gadgetron, MATLAB, or BART functionality into your python scripts. These functions are written with the assumption of Gadgetron, MATLAB, etc. being run on some processing server (not necessarily on your local machine). If you use these, you'll want to create a [config file](../master/mr_utils/config) file.

## Documentation and Tests

Documentation is almost exclusively found in the docstrings of modules, functions, and classes.  This README file contains the output of help() for all the modules in the project.  README files can also be found in subdirectories containing only the help() output specific to that module.

Another great way to learn how things are used is by looking in the [examples](../master/examples).
Run examples from the root directory (same directory as setup.py) like this:

```bash
python3 examples/cs/reordering/cartesian_pe_fd_iht.py
```

If there's not an example, there might be some [tests](../master/mr_utils/tests). Individual tests can be run like this from the root directory (I recomment that you run tests from the home directory - imports will get messed up otherwise):

```bash
python3 -m unittest mr_utils/tests/recon/test_gs_recon.py
```

"""

    # Include a little blurb about how to install the thing
    docs += """# Installation

Say you want to use this package in one of your python scripts.  You can install it using pip like so:

```bash
git clone https://github.com/mckib2/mr_utils
cd mr_utils
pip3 install -e ./
```

You'll need to manually install the ismrmrd-python-tools as it's currently not available on pypi. You can find it here: https://github.com/ismrmrd/ismrmrd-python-tools.git
"""

    # Now loop through all modules and add the docstrings to readme
    readmes_already_seen = {}
    cur_module_docs = ''
    cur_module = ''
    for m in all_modules:

        # Group major modules
        splitted = m[1].split('.')
        if (len(splitted) >= 3) and (splitted[1] != cur_module):
            cur_module = splitted[1]
            cur_module_docs += '\n# %s' % splitted[1].upper()
        elif len(splitted) <= 2:
            cur_module_docs += '\n# %s' % splitted[-1].upper()

        # Make the heading for the module
        cur_module_docs += '\n## %s\n' % m[1]

        # Add a link to the module directory
        cur_module_docs += '\n[Source](https://github.com/mckib2/mr_utils/blob/master/%s.py)\n\n' % '/'.join(m[1].split('.'))

        # Import the module so we can call help on it
        mod = importlib.import_module(m[1])
        strhelp = pydoc.render_doc(mod,renderer=pydoc.plaintext)

        # Remove the first line (says autodoc, blah, blah, blah)
        ii = strhelp.index('\n')
        cur_module_docs += "```\n" + strhelp[ii+1:].lstrip() + "\n```\n\n"

        # Scrub string of all local file paths
        cur_module_docs = re.sub(r'\s+FILE\s+(/\w+)+\.py','',cur_module_docs)
        cur_module_docs = re.sub(r"\s+DATA(\s+.+ = .+\n)+",'',cur_module_docs)

        # Write the current module's doc out to the current module
        if m[0].path in readmes_already_seen:
            mode = 'a'
        else:
            readmes_already_seen[m[0].path] = None
            mode = 'w'
        with open(m[0].path + '/readme.md',mode) as f:
            f.write(cur_module_docs)

        # Add the current module's doc to the full doc
        docs += cur_module_docs
        cur_module_docs = ''

    # Write it out!
    with open('README.md','w') as f:
        f.write(docs)
