from elasticsearch import Elasticsearch
from google.cloud import storage
import pandas as pd
import io


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


def Elasticsearch_to_GCS_Connector(es_index_name, es_host, es_port, es_scheme, es_http_auth, es_size, gcs_file_name, gcs_bucket_name, gcs_bucket_name_prefix = None):
    
    # Access extracted data from Elastic search (assuming JSON format)
    extracted_data = connect_to_elasticsearch(index_name = es_index_name,
                host = es_host, 
                port = es_port, 
                scheme = es_scheme,
                http_auth = es_http_auth,
                size = es_size)
    
    # Create a dataframe of the extracted data
    df = pd.DataFrame(extracted_data)

    # Write the DataFrame to a BytesIO object
    csv_bytesio = io.BytesIO()
    df.to_csv(csv_bytesio, index=False)
    csv_bytesio.seek(0)

    # Create a client to interact with Google Cloud Storage
    client = storage.Client()


    # Create a client for the output bucket
    output_bucket = client.bucket(gcs_bucket_name)

    # Upload the  CSV file to the output bucket
    gcs_file_name = f"{gcs_bucket_name_prefix}/{gcs_file_name}"
    print("Output file name and location -> ", gcs_file_name)
    output_blob = output_bucket.blob(gcs_file_name)
    output_blob.upload_from_file(csv_bytesio, content_type='text/csv')

    print(f"Output CSV file saved as {gcs_file_name}")