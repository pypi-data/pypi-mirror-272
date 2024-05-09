# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csdb']

package_data = \
{'': ['*']}

install_requires = \
['click', 'click-completion', 'python-dateutil', 'requests']

entry_points = \
{'console_scripts': ['csdb = csdb.console:csdb']}

setup_kwargs = {
    'name': 'csdb',
    'version': '1.1.0',
    'description': 'csdb python sdk for ep csdb',
    'long_description': None,
    'author': 'zhangzhen',
    'author_email': 'zhangzhen@nao.cas.cn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
