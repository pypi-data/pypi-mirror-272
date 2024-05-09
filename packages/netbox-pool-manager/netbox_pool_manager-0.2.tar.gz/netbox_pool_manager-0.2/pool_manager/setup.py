from setuptools import find_packages, setup
import os.path
import codecs


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()
    

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")
    

setup(
    name='netbox-pool-manager',
    version=get_version('pool_manager/version.py'),
    description='A NetBox plugin to manage pools.',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
