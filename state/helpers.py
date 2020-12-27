import os
from datetime import datetime, timedelta


def cleanup_states(root_dir: str):
    for file in os.listdir(root_dir):
        file_path = os.path.join(root_dir, file)
        last_mod = datetime.fromtimestamp(os.stat(file_path).st_mtime)
        time_since_mod = datetime.now() - last_mod
        expiry = timedelta(hours=1)
        if time_since_mod > expiry:
            os.remove(file_path)
