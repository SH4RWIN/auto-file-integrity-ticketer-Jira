import os
import time
from datetime import datetime, timezone
from pathlib import Path
from crypto import *
from jira import *
import json  # Missing import for json
root_dir = Path('important_files')
CHECKSUM_FILE = "checksums.json"
intervel = 60


"""
1. Check hash
2. verify hash
3. Create hash for new files found
4. Raise Tickets for hash Mismatches
"""

def verify_integrity():
    """
    Verifies the integrity of files in the important_files directory.
    - Checks for modified files.
    - Checks for deleted files.
    - Checks for new files.
    """
    try:
        with open(CHECKSUM_FILE, "r") as f:
            checksum_list = json.load(f)
            expected_checksums = {list(item.keys())[0]: list(item.values())[0] for item in checksum_list}
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading checksums file: {e}")
        expected_checksums = {}

    current_files = {str(p) for p in root_dir.rglob('*') if p.is_file()}
    expected_files = set(expected_checksums.keys())

    # 1. Check for deleted files and Raise Tickets
    deleted_files = expected_files - current_files
    for file_path in deleted_files:
        print(f"File deleted!!!: {file_path}")
        ticket = raise_ticket_file_deleted(file_path, expected_checksums[file_path])
        print(f"Ticket ID: {ticket['id']}\nTicket Key: {ticket['key']}\nTicket Link: {ticket['self']}")

    # 2. Check for new files and Raise Tickets
    new_files = current_files - expected_files
    for file_path in new_files:
        print(f"New file created!!!: {file_path}")
        ticket = (raise_ticket_new_file(file_path))
        print(f"Ticket ID: {ticket['id']}\nTicket Key: {ticket['key']}\nTicket Link: {ticket['self']}")
        print("Adding hash to checksum file...")
        new_hash = get_hash(file_path)
        add_hash_to_checksum_file(file_path, new_hash)
        print(f"  -> New hash: {new_hash}\n")

    # 3. Check for modified files and Raise Tickets
    for file_path in expected_files.intersection(current_files):
        if not os.path.exists(file_path):
            # This case is handled by the deleted files check, but putting it for safety:
            print(f"File does not exist, but was expected: {file_path}")
            continue

        current_hash = get_hash(file_path)
        expected_hash = expected_checksums[file_path]

        print(f"File: {file_path}")
        # print(f" -> Expected Hash: {expected_hash}")
        # print(f" -> Current Hash:  {current_hash}")

        if current_hash != expected_hash:
            print("Tested Not OK!!! - File has been modified.")
            ticket = raise_ticket_file_modification(file_path, expected_hash=expected_hash, current_hash=current_hash)
            print(f"Ticket ID: {ticket['id']}\nTicket Key: {ticket['key']}\nTicket Link: {ticket['self']}")
        else:
            print("Tested OK")
        print("")

def add_hash_to_checksum_file(file_path, new_hash):
    """
    Adds a new file and its hash to the checksum file.
    """
    try:
        with open(CHECKSUM_FILE, "r+") as f:
            checksum_list = json.load(f)
            checksum_list.append({file_path: new_hash})
            f.seek(0)
            json.dump(checksum_list, f, indent=2)
            f.truncate()
    except (FileNotFoundError, json.JSONDecodeError) as e:
        # If the file doesn't exist or is empty, create a new list
        with open(CHECKSUM_FILE, "w") as f:
            json.dump([{file_path: new_hash}], f, indent=2)

if __name__ == "__main__":
    print("================= File Integrity Checker Version 1.0 =================")
    # intervel = 60 * 60 # 60 seconds times 60 minuts. Exactly One hour
    intervel = 15
    count = 0
    try:
        while True:
            now = datetime.now(timezone.utc).isoformat()
            print(f"\n\n[{now}] file integrity check. Count = {count}\n")
            verify_integrity()
            time.sleep(intervel)
            count += 1
    except KeyboardInterrupt:
        print("Keyboard Inturrupt detected Quiting...")
        exit()
    except Exception as e:
        print("An Unexpected Error occured", e)


# ============= CURRENT ISSUES =============

# If the problem isn't resolved within the next intervel, the same ticket will be raised again. A logic to solve that problem is required.
