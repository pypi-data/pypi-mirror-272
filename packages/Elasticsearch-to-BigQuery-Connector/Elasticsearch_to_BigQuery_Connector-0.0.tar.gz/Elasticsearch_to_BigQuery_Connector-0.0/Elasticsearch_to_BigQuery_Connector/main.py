from elasticsearch import Elasticsearch
from google.cloud import bigquery
from dateutil import tz
from datetime import datetime


def connect_to_elasticsearch(index_name, host, port, scheme, http_auth, size=10000):
    
    # Establish connection to Elasticsearch
    es = Elasticsearch([{'host': host, 'port': port, 'scheme': scheme}],
                        http_auth=http_auth)

    # Define an empty list to store extracted data
    extracted_data = []

    # Perform Elasticsearch search
    result = es.search(index=index_name, body={"query": {"match_all": {}}}, size=size)
    print("Index name -> ", index_name)
    print("Extraction result -> ", result)

    # Extract relevant data from the response (modify this based on your data structure)
    for item in result['hits']['hits']:
        extracted_data.append(item['_source'])  # Assuming data is in '_source'
    
    return extracted_data


def Elasticsearch_to_BigQuery_Connector(es_index_name, es_host, es_port, es_scheme, es_http_auth, es_size, bq_project_id, bq_dataset_id, bq_table_name, bq_add_record_addition_time = False):
    
    # Access extracted data from Elastic search (assuming JSON format)
    extracted_data = connect_to_elasticsearch(index_name = es_index_name,
                host = es_host, 
                port = es_port, 
                scheme = es_scheme,
                http_auth = es_http_auth,
                size = es_size)

    # Configure BigQuery client
    client = bigquery.Client()

    # Reference the existing BigQuery dataset and table
    try:
        dataset_ref = client.dataset(project=bq_project_id, dataset_id=bq_dataset_id)
        table_ref = dataset_ref.table(bq_table_name)

        tables = list(client.list_tables(dataset_ref))
        if tables:
            print(f"Found tables in dataset: {tables}")
        else:
            print("No tables found in the dataset.")
    except Exception as e:
        print(f"Error creating references: {e}")

    # Prepare data for insertion
    rows_to_insert = extracted_data
    print("Data prepared for insertion into BigQuery.")

    # Check if table exists before insertion
    tables = list(client.list_tables(dataset_ref))
    if any(table.table_id == bq_table_name for table in tables):
        print("Table ", bq_table_name, "found!")
    else:
        print("Table ", bq_table_name, " not found!")


    # Define the desired timezone (EST in this case)
    est_timezone = tz.gettz('US/Eastern')

    # Get current datetime with naive UTC timezone (no time zone info)
    current_datetime_naive = datetime.now()

    # Localize the naive datetime to EST
    current_datetime_est = current_datetime_naive.astimezone(est_timezone)

    # Format the datetime string in EST
    current_datetime = current_datetime_est.strftime("%Y-%m-%d %H:%M:%S")

    if bq_add_record_addition_time == True:
        # Add the current datetime to each record
        for record in rows_to_insert:
            record['record_addition_time'] = current_datetime

    # Insert data into the BigQuery table
    table = client.get_table(table_ref)
    errors = client.insert_rows(table=table, rows=rows_to_insert)


    # Handle potential errors during data insertion
    if errors:
        for err in errors:
            print(f"Error encountered while inserting row: {err}")

    print(f"Loaded {len(rows_to_insert)} rows to BigQuery table.")