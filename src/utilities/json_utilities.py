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
    data = {}
    data['Temperature_Low'] = 21
    data['Temperature_High'] = 35
    data['Sunlight_Low'] = 6
    data['Sunlight_High'] = 9
    data['Moisture_Low'] = 55
    data['Moisture_High'] = 80
    data['Humidity_Low'] = 60
    data['Humidity_High'] = 100
    data['VOC_Low'] = 400
    data['VOC_High'] = 800
    save_as_json("./configuration_files/Basil2ElectricBoogaloo", data)


