import json
import logging

from setuptools import setup, find_packages


logger = logging.getLogger()


def extract_metadata(file_path='.build.json'):
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


build_metadata = extract_metadata()

setup(
    name="project_name",
    version="0.1.0",
    packages=find_packages(),
    install_requires=['boto3', 'cerberus', 'requests'],
    python_requires='>=3',
    classifiers=[
        f"branch : {build_metadata.get('branch')}",
        f"commit_hash : {build_metadata.get('commit_hash')}",
        f"build_date : {build_metadata.get('build_date')}"
    ]
)
