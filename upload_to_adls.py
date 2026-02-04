from azure.storage.filedatalake import DataLakeServiceClient
import os

ACCOUNT_NAME = "bkadls02"
ACCOUNT_KEY = "qCXDy/PT+sRKWgTqn81IXaRmAyyw6GgHKU6kAwNApRgivnRoIlt8M3tGJ8CMnVcFlieExvMxxaQH+AStTjy61Q=="
FILE_SYSTEM = "bronze"
LOCAL_DIR = "data/incoming"

service_client = DataLakeServiceClient(
    account_url=f"https://{ACCOUNT_NAME}.dfs.core.windows.net",
    credential=ACCOUNT_KEY
)

fs_client = service_client.get_file_system_client(FILE_SYSTEM)

for file in os.listdir(LOCAL_DIR):
    local_path = os.path.join(LOCAL_DIR, file)
    adls_path = f"flight_statistics/{file}"

    file_client = fs_client.get_file_client(adls_path)

    with open(local_path, "rb") as data:
        file_client.upload_data(data, overwrite=True)

    os.remove(local_path)
    print(f"Uploaded: {file}")
