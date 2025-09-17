import hashlib
import json
from pathlib import Path

# Takes in one file object as input and returns its hash
def get_hash(path_obj):
    hasher = hashlib.new('sha256')
    try:
        with open(path_obj, 'rb') as file:
            while chunk := file.read(8912):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError as e:
        print(f"Error reading file '{path_obj}': {e}")
        return None
    except Exception as e:
        print("Unknown Exception occured: ", e)