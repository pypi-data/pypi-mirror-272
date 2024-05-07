from MoonshotAI_Api.utils.output_enum import OutputFormat
from MoonshotAI_Api.utils.consts import CHUNK_SIZE, CSV_FILE
import requests
import os

def download_file(url, output_format, output_path, chunk_size=CHUNK_SIZE):
    try:
        response = requests.get(url)
        if response.status_code == 200:

            # Return the filename of the downloaded csv file
            #when I send path ltv_result/test.csv No such file or directory: 'ltv_result/test.csv'
            #overcome this error by creating the dir needed

            if output_format == OutputFormat.CSV.value:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                return output_path

            # Return the content of the downloaded file as a byte stream (can be divided into chunks if needed)
            if output_format == OutputFormat.STREAM.value:
                if chunk_size is None:
                    return response.iter_content()
                return response.iter_content(chunk_size=CHUNK_SIZE)

        raise Exception(f"Error downloading file. Status code: {response.status_code}")

    except Exception as e:
        raise Exception(f"Error downloading file: {e}")
