from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import subprocess
import os

WATCH_DIR = "data/incoming"

class IncomingFileHandler(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.endswith(".json"):
            print(f"New file detected: {event.src_path}")

            # Wait to ensure file write is complete
            time.sleep(2)

            # Run upload_to_adls.py
            subprocess.run(
                ["python", "upload_to_adls.py"],
                check=True
            )

if __name__ == "__main__":
    if not os.path.exists(WATCH_DIR):
        os.makedirs(WATCH_DIR)

    observer = Observer()
    observer.schedule(IncomingFileHandler(), WATCH_DIR, recursive=False)
    observer.start()

    print("Watching data/incoming for new files...")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
