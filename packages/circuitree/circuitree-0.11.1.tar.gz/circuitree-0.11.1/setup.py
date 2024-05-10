# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['circuitree']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=3.1,<4.0', 'numpy>=1.23.0,<2.0.0', 'pandas>=2.0.0,<3.0.0']

extras_require = \
{':python_version >= "3.10" and python_version < "3.13"': ['scipy>=1.11.3,<2.0.0'],
 'distributed': ['celery[redis]>=5.3.1,<6.0.0', 'gevent>=23.9.1,<24.0.0']}

setup_kwargs = {
    'name': 'circuitree',
    'version': '0.11.1',
    'description': 'Genetic circuit design using Monte Carlo tree search',
    'long_description': '<h1 align="center">\n<img src="https://raw.githubusercontent.com/pranav-bhamidipati/circuitree/main/logo.png" width="300">\n</h1><br>\n\nBiochemical circuit design using Monte Carlo tree search\n\n## Installation\n\n```pip install circuitree```\n\n## Getting Started\n\n[Getting started tutorial](https://githubtocolab.com/pranav-bhamidipati/circuitree-tutorial/blob/main/src/tutorial-1-getting-started.ipynb). \n\nSee the [`circuitree-tutorial`](https://github.com/pranav-bhamidipati/circuitree-tutorial) repo for additional tutorials and example scripts.\n\n## Documentation\n\nAPI docs coming soon\n\n\n© 2024 Pranav Bhamidipati\nLogo © 2024 Inna-Marie Strazhnik \n',
    'author': 'pranav-bhamidipati',
    'author_email': 'pbhamidi@usc.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
