Python Library for connecting to Elasticsearch and loading data into BigQuery.

This Python library provides utilities to extract data from Elasticsearch and load it directly into Google BigQuery. It simplifies the process of data migration between Elasticsearch and BigQuery by handling connection setup, data extraction, and data loading with optional timestamping.

**Features**

1. Connect to an Elasticsearch instance and fetch data.
2. Load data directly into a specified BigQuery table.
3. Optional timestamping for record insertion.


**Installation**
Install the package via pip:

```Bash
pip install Elasticsearch_to_BigQuery_Connector
```

**Dependencies**

1. elasticsearch: To connect and interact with Elasticsearch.
2. google-cloud-bigquery: To handle operations related to BigQuery.

Make sure to have these installed using:

```Bash
pip install elasticsearch google-cloud-bigquery
```


*Example Usage:*

```Python

from Elasticsearch_to_BigQuery_Connector import Elasticsearch_to_BigQuery_Connector

load_data_to_bigquery(
    es_index_name='your_index',
    es_host='localhost',
    es_port=port,
    es_scheme='http',
    es_http_auth=('user', 'pass'),
    es_size=size,
    bq_project_id='your_project_id',
    bq_dataset_id='your_dataset_id',
    bq_table_name='your_table_name',
    bq_add_record_addition_time=True
)

```


**Additional Notes:**

Ensure you have configured credentials for both Elasticsearch and Google Cloud (BigQuery):

1. For Elasticsearch, provide the host, port, scheme, and authentication details.
2. For BigQuery, ensure your environment is set up with the appropriate credentials (using Google Cloud SDK or setting the GOOGLE_APPLICATION_CREDENTIALS environment variable to your service account key file).

 
