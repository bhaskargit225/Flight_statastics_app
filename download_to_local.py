from azure.storage.filedatalake import DataLakeServiceClient
import os

# --------------------
# Config
# --------------------
ACCOUNT_NAME = "bkadls02"
ACCOUNT_KEY = "qCXDy/PT+sRKWgTqn81IXaRmAyyw6GgHKU6kAwNApRgivnRoIlt8M3tGJ8CMnVcFlieExvMxxaQH+AStTjy61Q=="
FILE_SYSTEM = "gold"

ADLS_BASE_PATH = "export/flight_positions_csv"
LOCAL_OUTPUT_DIR = "data/outgoing_csvs"

os.makedirs(LOCAL_OUTPUT_DIR, exist_ok=True)

# --------------------
# Connect to ADLS
# --------------------
service_client = DataLakeServiceClient(
    account_url=f"https://{ACCOUNT_NAME}.dfs.core.windows.net",
    credential=ACCOUNT_KEY
)

fs = service_client.get_file_system_client(FILE_SYSTEM)

# --------------------
# Download + Rename
# --------------------
paths = fs.get_paths(ADLS_BASE_PATH)

for path in paths:
    if path.name.endswith(".csv"):
        # Example path:
        # exports/flight_positions_csv/origin_country=India/part-0000.csv

        # Extract country name
        country_part = path.name.split("origin_country=")[1]
        country_name = country_part.split("/")[0]

        # Clean filename (spaces → underscores)
        safe_country = country_name.replace(" ", "_")

        local_filename = f"flight_positions_{safe_country}.csv"
        local_path = os.path.join(LOCAL_OUTPUT_DIR, local_filename)

        print(f"Downloading {path.name} → {local_filename}")

        file_client = fs.get_file_client(path.name)
        download = file_client.download_file()
        data = download.readall()

        with open(local_path, "wb") as f:
            f.write(data)

print("All CSVs downloaded successfully.")
