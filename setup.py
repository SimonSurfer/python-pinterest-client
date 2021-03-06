import glob
import sys
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(here, 'src'))
version = __import__('pinterest').get_version()
with open('requirements.txt') as requirements:
    install_reqs = [r.strip('\n') for r in requirements]

setup(
    name='pinterest-client',
    version=version,
    url='',
    author='Karoly Nagy',
    author_email='dr.karoly.nagy@gmail.com',
    description=('Python client for public Pinterest API'),
    license='GPL-3.0',
    packages=find_packages(os.path.join(here, 'src'), exclude=['contrib', 'docs', 'tests']),
    package_dir={'':'src'},
    scripts=glob.glob('bin/*'),
    install_requires=install_reqs,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ]
)