from setuptools import setup, find_packages

with open('README.md', "r") as f:
    description = f.read()

setup(
    name = 'Elasticsearch_to_BigQuery_Connector',
    version = '0.1',
    packages = find_packages(),
    install_requires = ['elasticsearch', 'google-cloud-bigquery'],
    entry_points = {"console_scripts" : [
        "Elasticsearch_to_BigQuery_Connector = Elasticsearch_to_BigQuery_Connector:Elasticsearch_to_BigQuery_Connector",
    ],},
    long_description=description,
    long_description_content_type="text/markdown",
)