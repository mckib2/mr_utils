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

    # First of all, include a little blurb about how to install the thing
    docs += """## Installation

Say you want to use this package in one of your python scripts.  You can install it using pip like so:

```bash
git clone https://github.com/mckib2/mr_utils
cd mr_utils
pip3 install -e ./
```

You'll need to manually install the ismrmrd-python-tools as it's currently not available on pypi.
You can find it here: https://github.com/ismrmrd/ismrmrd-python-tools.git
"""

    # Now loop through all modules and add the docstrings to readme
    for m in all_modules:

        # Make the heading for the module
        docs += '\n## %s\n' % m[1]

        # Add a link to the module directory
        docs += '\n[Source](../blob/master/%s)\n\n' % '/'.join(m[1].split('.'))

        # Import the module so we can call help on it
        mod = importlib.import_module(m[1])
        strhelp = pydoc.render_doc(mod,renderer=pydoc.plaintext)

        # Remove the first line (says autodoc, blah, blah, blah)
        ii = strhelp.index('\n')
        docs += "```\n" + strhelp[ii+1:].lstrip() + "\n```\n\n"

    # Scrub string of all local file paths
    docs = re.sub(r'\s+FILE\s+(/\w+)+\.py','',docs)
    docs = re.sub(r"\s+DATA(\s+.+ = .+\n)+",'',docs)

    # Write it out!
    with open('README.md','w') as f:
        f.write(docs)
