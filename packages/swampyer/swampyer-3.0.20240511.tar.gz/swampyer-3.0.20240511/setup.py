# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swampyer']

package_data = \
{'': ['*']}

install_requires = \
['certifi>=2023.11.17,<2024.0.0',
 'six>=1.16.0,<2.0.0',
 'websocket-client>=0.59.0']

extras_require = \
{'all': ['cbor>=1.0.0,<2.0.0',
         'msgpack>=1.0.2,<2.0.0',
         'websockets>=11.0.3,<12.0.0'],
 'cbor': ['cbor>=1.0.0,<2.0.0'],
 'msgpack': ['msgpack>=1.0.2,<2.0.0'],
 'websockets': ['websockets>=11.0.3,<12.0.0']}

setup_kwargs = {
    'name': 'swampyer',
    'version': '3.0.20240511',
    'description': 'Simple WAMP library with minimal external dependencies',
    'long_description': 'None',
    'author': 'Aki Mimoto',
    'author_email': 'aki@zaber.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4.0',
}


setup(**setup_kwargs)
