"""!
Contains all functions related to JSON operations.
"""

import json

def load_from_json(filename):
    with open(filename+".json", "r") as f:
        data = json.load(f)
    return data

def save_as_json(filename, data):
    try:
        with open(filename+".json", 'w+') as file:
            file.write(json.dumps(data, sort_keys=True, indent=4, default=str))
    except Exception as e:
        print(e)
        return 1
    return 0


if __name__ == "__main__":
    import os
    import random
    data = {str(k): random.random() for k in range(100)}
    save_as_json("./database/test", data)
    assert load_from_json("./database/test") == data
    os.remove("./database/test.json")

