# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nadc_datahub']

package_data = \
{'': ['*']}

install_requires = \
['csdb==1.1.0']

setup_kwargs = {
    'name': 'nadc-datahub',
    'version': '0.1.0',
    'description': 'A Python package for accessing datasets from NADC DataHub',
    'long_description': None,
    'author': 'zhangzhen',
    'author_email': 'zhangzhen@nao.cas.cn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
