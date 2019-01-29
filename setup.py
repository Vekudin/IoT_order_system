from setuptools import setup, find_packages
import json


def get_build_metadata(file_path='build_state_metadata.json'):
    """Gets metadata from a json file and returns it as a python dictionary."""

    with open(file_path) as file:
        build_metadata = json.loads(file.read())

    return build_metadata


setup(
    name="iot_order_system",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.json']
    },
    install_requires=['boto3', 'cerberus', 'requests'],
    python_requires='>=3',
)
