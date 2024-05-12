# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ai_alchemy', 'ai_alchemy.core']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=2.2.2,<3.0.0', 'pydantic>=2.7.1,<3.0.0', 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'ai-alchemy',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
