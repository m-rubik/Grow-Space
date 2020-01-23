"""!
Contains all pickling functions for database management.
"""

import pickle

def import_object(filename):
    try:
        with open(filename, 'rb+') as f:
            data = pickle.load(f)
    except Exception as e:
        print(e)
        return 1
    return data

def export_object(filename, data):
    try:
        with open(filename, 'wb+') as f:
            pickle.dump(data, f)
    except Exception as e:
        print(e)
        return 1
    return 0


if __name__ == "__main__":
    import os
    import random
    data = {str(k): random.random() for k in range(100)}
    export_object("./database/test_database", data)
    assert import_object("./database/test_database") == data
    os.remove("./database/test_database")