# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grasp_planning',
 'grasp_planning.constraints',
 'grasp_planning.cost',
 'grasp_planning.solver']

package_data = \
{'': ['*']}

install_requires = \
['casadi>3.5',
 'forwardkinematics>=1.1.3',
 'numpy>=1.15.3,<2.0.0',
 'scipy<=1.10.1',
 'spatial-casadi>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'grasp_planning',
    'version': '0.4.1',
    'description': '"Grasp and Motion Planning Python Package."',
    'author': 'Tomas Merva',
    'author_email': 'tmerva7@gmail.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)

