import json
import logging

from setuptools import setup, find_packages


logger = logging.getLogger()


def extract_metadata(file_path='metadata_vitals.json'):
    """Reads all of the data from JSON file and returns it as a dictionary."""

    try:
        with open(file_path) as file:
            metadata = json.loads(file.read())

    except FileNotFoundError as e:
        logger.warning(f"There was no '{e.filename}' file found!")
        return {}
    except json.JSONDecodeError as e:
        logger.warning(f"There was a JSONDecodeError: \n'{e.args[0]}'")
        return {}

    return metadata


setup(
    name="iot_order_system",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.json']
    },
    install_requires=['boto3', 'cerberus', 'requests'],
    python_requires='>=3',
)
