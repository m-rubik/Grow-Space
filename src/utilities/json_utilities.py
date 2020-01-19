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
    # import random
    # data = {str(k): random.random() for k in range(100)}
    # save_as_json("./database/test", data)
    # assert load_from_json("./database/test") == data
    # os.remove("./database/test.json")
    data = {}
    data['Temperature_Low'] = 10
    data['Temperature_Medium_Low'] = 21
    data['Temperature_Median_High'] = 35
    data['Temperature__High'] = 37
    data['Temperature_Target'] = 29
    data['Sunlight_Low'] = 6
    data['Sunlight_High'] = 9
    data['Sunlight_Target'] = 8
    data['Moisture_Low'] = 55
    data['Moisture_High'] = 80
    data['Moisture_Target'] = 65
    save_as_json("./configuration_files/sample.cfg", data)
    # assert load_from_json("./database/test") == data
    # os.remove("./database/test.json")


