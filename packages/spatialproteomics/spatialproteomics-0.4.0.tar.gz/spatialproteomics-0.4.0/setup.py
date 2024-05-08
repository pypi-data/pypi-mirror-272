# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spatialproteomics',
 'spatialproteomics.ext',
 'spatialproteomics.la',
 'spatialproteomics.pl',
 'spatialproteomics.pp',
 'spatialproteomics.tl']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.3,<4.0.0',
 'scikit-image>=0.19.3,<0.20.0',
 'scikit-learn>=1.2.2,<2.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'xarray>=2022.6.0,<2023.0.0',
 'zarr>=2.14.2,<3.0.0']

extras_require = \
{'docs': ['Sphinx==4.2.0',
          'sphinx-rtd-theme==1.0.0',
          'sphinxcontrib-napoleon==0.7',
          'nbsphinx==0.8.9']}

setup_kwargs = {
    'name': 'spatialproteomics',
    'version': '0.4.0',
    'description': '',
    'long_description': 'None',
    'author': 'Harald Vohringer',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
