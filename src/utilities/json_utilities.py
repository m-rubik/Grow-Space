"""!
Contains all functions related to JSON operations.
"""


import json


def load_from_json(filename):
    """!
    Loads a json file into a python object
    @param filename: Path to the json object
    """

    with open(filename+".json", "r") as f:
        data = json.load(f)
    return data


def save_as_json(filename, data):
    """!
    Saves python object to a json object.
    @param filename: Name of the json object you wish to create/overwrite
    @param data: Python object you wish to save
    """

    try:
        with open(filename+".json", 'w+') as file:
            file.write(json.dumps(data, sort_keys=True, indent=4, default=str))
    except Exception as e:
        print(e)
        return 1
    return 0

def manually_generate_config_file(name):
    RGB_data = {}
    RGB_data['0'] = {"R": 100, "G": 0, "B": 100}
    RGB_data['1'] = {"R": 100, "G": 0, "B": 100}
    RGB_data['2'] = {"R": 100, "G": 0, "B": 100}
    RGB_data['3'] = {"R": 100, "G": 0, "B": 100}
    RGB_data['4'] = {"R": 100, "G": 0, "B": 100}
    RGB_data['5'] = {"R": 100, "G": 0, "B": 100}
    RGB_data['6'] = {"R": 100, "G": 25, "B": 100}
    RGB_data['7'] = {"R": 100, "G": 50, "B": 100}
    RGB_data['8'] = {"R": 100, "G": 75, "B": 100}
    RGB_data['9'] = {"R": 100, "G": 100, "B": 100}
    RGB_data['10'] = {"R": 100, "G": 100, "B": 100}
    RGB_data['11'] = {"R": 100, "G": 100, "B": 100}
    RGB_data['12'] = {"R": 100, "G": 100, "B": 100}
    RGB_data['13'] = {"R": 100, "G": 100, "B": 100}
    RGB_data['14'] = {"R": 100, "G": 100, "B": 100}
    RGB_data['15'] = {"R": 100, "G": 100, "B": 100}
    RGB_data['16'] = {"R": 100, "G": 100, "B": 100}
    RGB_data['17'] = {"R": 100, "G": 100, "B": 100}
    RGB_data['18'] = {"R": 100, "G": 75, "B": 100}
    RGB_data['19'] = {"R": 100, "G": 50, "B": 100}
    RGB_data['20'] = {"R": 100, "G": 25, "B": 100}
    RGB_data['21'] = {"R": 100, "G": 0, "B": 100}
    RGB_data['22'] = {"R": 100, "G": 0, "B": 100}
    RGB_data['23'] = {"R": 1000, "G": 0, "B": 100}

    UV_data = {}
    UV_data['0'] = 0
    UV_data['1'] = 0
    UV_data['2'] = 0
    UV_data['3'] = 0
    UV_data['4'] = 0
    UV_data['5'] = 0
    UV_data['6'] = 0
    UV_data['7'] = 0
    UV_data['8'] = 0
    UV_data['9'] = 0
    UV_data['10'] = 0
    UV_data['11'] = 0
    UV_data['12'] = 0
    UV_data['13'] = 0
    UV_data['14'] = 0
    UV_data['15'] = 0
    UV_data['16'] = 0
    UV_data['17'] = 0
    UV_data['18'] = 0
    UV_data['19'] = 0
    UV_data['20'] = 0
    UV_data['21'] = 0
    UV_data['22'] = 0
    UV_data['23'] = 0

    data = {}
    data['Temperature_Low'] = 20
    data['Temperature_High'] = 35
    data['Moisture_Low'] = 80
    data['Moisture_High'] = 100
    data['Humidity_Low'] = 60
    data['Humidity_High'] = 100
    data['VOC_Low'] = 10
    data['VOC_High'] = 100
    data['RGB_data'] = RGB_data
    data['UV_data'] = UV_data
    data['Soak_Minutes'] = 30

    save_as_json("./configuration_files/"+name, data)


if __name__ == "__main__":
    manually_generate_config_file("radishes")


