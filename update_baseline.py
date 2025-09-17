import hashlib
import json
from pathlib import Path
from crypto import get_hash
root_dir = Path('important_files')
checksum_file = 'checksums.json'

# Returns the hashes of each file as a json element in a list format: [{"filename":"hash"}]
def get_file_hashes():
    results = []
    if not root_dir.exists():
        print(f"Root directory does not exist: {root_dir}")
        return None
    for path_obj in root_dir.rglob('*'):    # the root_dir.rglob('*') will recursively find all the files in the directories
        if path_obj.is_file():
            try:
                hash = get_hash(path_obj)
                # print(f"{path_obj} : {hash}")
                results.append({str(path_obj):hash})
            except Exception as e:
                print("Unknown Exception occured: ", e)
    return results

def save_hashes(results):
    # Save the hashes to checksums.json
    with open(checksum_file, 'w', encoding='utf-8') as f:
        json.dump(results or [], f, indent=2)


if __name__=='__main__':
    hashes = get_file_hashes()
    save_hashes(hashes)