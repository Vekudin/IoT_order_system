import json
import logging
import os

from setuptools import setup, find_packages

from load_lazy import LoadLazy


logger = logging.getLogger()


@LoadLazy
def extract_metadata(file_name='.build.json'):
    """Reads a JSON file located in the same directory as 'setup.py' and returns
     the data from it as a dictionary."""

    file_path = os.path.dirname(os.path.realpath(__file__)) + '/' + file_name
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
    name="project_name-" + extract_metadata.branch,
    version="0.1.0-" + extract_metadata.commit_hash[0:7],
    packages=find_packages(),
    install_requires=['boto3', 'cerberus', 'requests'],
    python_requires='>=3'
)
