# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xlstm_torch']

package_data = \
{'': ['*']}

install_requires = \
['swarms', 'zetascale']

setup_kwargs = {
    'name': 'xlstm-torch',
    'version': '0.0.2',
    'description': 'xLSTM - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# xLSTM\nImplementation of xLSTM in Pytorch from the paper: "xLSTM: Extended Long Short-Term Memory"\n\n\n\n\n# License\nMIT\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/xLSTM',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
