from distutils.command.build_py import build_py as _build_py
from setuptools import setup, find_packages
import pkginfo


version = '0.1.0'



setup(
    name="iot_order_system",
    version=version,
    packages=find_packages(),
    include_package_data=True,

    # This package_data include works only for 'install' and 'bdist' commands,
    # 'sdist' needs MANIFEST.in
    package_data={
        'tests': ['*.json', '*.txt']
    },

    author="Teodor Akov",
    install_requires=['boto3', 'pkginfo', 'semver'],
    python_requires='>=3',

    classifiers=[
        'branch::master',
        'commit_hash::hash_of_commit_here'
    ]
)
