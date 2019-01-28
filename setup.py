from setuptools import setup, find_packages
import json


def get_version_specifics(file_name='version_specifics.json'):
    """Gets all of the data from a json file and returns it as a dict type which
     is compatible with function setup's key word arguments."""

    with open(file_name) as file:
        data = json.loads(file.read())

    return {
        'version': data['version'],
        'author': data['author'],
        'classifiers': [
            'branch::' + data['branch'],
            'commit_hash::' + data['commit_hash'],
            'dist_timestamp::' + data['dist_timestamp']
        ]
    }


setup_args = {
    'name': "iot_order_system",
    'packages': find_packages(),
    'include_package_data': True,

    'package_data': {
        '': ['version_specifics.json']
    },

    'install_requires': ['boto3', 'cerberus', 'requests'],
    'python_requires=': '>=3',
    'branch=metadata': ['branch'],
}

# Get the needed version specific data and apply it on setup_args
version_specifics = get_version_specifics()
setup_args.update(version_specifics)

# Proceed the setup
setup(**setup_args)
