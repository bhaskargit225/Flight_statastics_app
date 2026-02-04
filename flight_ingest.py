import requests
import json
import uuid
import time
from datetime import datetime
import os

DATA_DIR = "data/incoming"
os.makedirs(DATA_DIR, exist_ok=True)

OPENSKY_URL = "https://opensky-network.org/api/states/all"

def fetch_flight_data():
    response = requests.get(OPENSKY_URL, timeout=30)
    response.raise_for_status()
    data = response.json()

    record = {
        "batch_id": str(uuid.uuid4()),
        "ingestion_time": datetime.utcnow().isoformat(),
        "states": data.get("states", [])
    }

    file_name = f"flights_{int(time.time())}.json"

    with open(os.path.join(DATA_DIR, file_name), "w") as f:
        json.dump(record, f, indent=2)

    print(f"Saved {file_name}")


if __name__ == "__main__":
    while True:
        fetch_flight_data()
        time.sleep(60)   # every 1 minute


# to limit runs for testing
#if __name__ == "__main__":
#    max_files = 2
#    run_count = 0

#    while run_count < max_files:
#        fetch_flight_data()
#        run_count += 1
#        time.sleep(60)