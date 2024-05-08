# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'source/packages'}

packages = \
['pycis',
 'pycis.cli',
 'pycis.cli.cmdtree',
 'pycis.cli.cmdtree.datastore',
 'pycis.cli.cmdtree.datastore.couchdb',
 'pycis.cli.cmdtree.datastore.mongodb',
 'pycis.cli.cmdtree.document',
 'pycis.cli.cmdtree.document.build',
 'pycis.cli.cmdtree.document.configuration',
 'pycis.cli.cmdtree.document.testrun',
 'pycis.cli.cmdtree.tracking',
 'pycis.cli.cmdtree.tracking.jira']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.4,<9.0.0',
 'mojo-config>=1.3.20,<1.4.0',
 'mojo-credentials>=1.3.10,<1.4.0',
 'mojo-xmodules>=1.3.0,<1.4.0']

extras_require = \
{'couchdb': ['couchdb>=1.2,<2.0'],
 'jira': ['jira>=3.8.0,<4.0.0'],
 'mongodb': ['pymongo>=4.0.0,<5.0.0']}

entry_points = \
{'console_scripts': ['pycis = pycis.cli.pycis_command:pycis_root_command']}

setup_kwargs = {
    'name': 'pycis-cli',
    'version': '0.1.5',
    'description': 'Python Continuous Integration System (PyCIS) - CLI Tools',
    'long_description': '========================================================\nPython Continuous Integration System (PyCIS) - CLI Tools\n========================================================\n\nProvides a set of CLI tools for working with the PyCIS continuous integration system.\n\n==========\nReferences\n==========\n\n- `User Guide <userguide/userguide.rst>`\n- `Coding Standards <userguide/10-00-coding-standards.rst>`\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
