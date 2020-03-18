"""!
All functions providing plotting functionalities.
"""

# There might be an "generate plot" button or something similar that will automatically
# Generate plots from the data that it has stored

import matplotlib.pylab as plt
import pandas as pd

def plot_soil_moisture(dict):
    lists = sorted(dict.items()) 
    x, y = zip(*lists)
    plt.plot(x, y)
    plt.xticks([])
    plt.yticks([])
    plt.title("Soil Moisture Percentage Over Time")
    plt.ylabel("Moisture (%)")
    plt.xlabel("Time (s)")
    plt.show()

def plot_temperature(dict):
    lists = sorted(dict.items()) 
    x, y = zip(*lists)
    plt.plot(x, y)
    plt.xticks([])
    plt.yticks([])
    plt.title("Temperature Over Time")
    plt.ylabel("Temperature (°C)")
    plt.xlabel("Time (s)")
    plt.show()

def boxplot_environment(df):
    """!
    Text from https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.boxplot.html:
    The box extends from the Q1 to Q3 quartile values of the data, with a line at the median (Q2). 
    The whiskers extend from the edges of box to show the range of the data. 
    The position of the whiskers is set by default to 1.5 * IQR (IQR = Q3 - Q1) from the edges of the box. 
    Outlier points are those past the end of the whiskers.
    """

    with plt.style.context("seaborn"):
        fig, ax = plt.subplots(1, 3)
        fig.suptitle('Environment Sensor Data', fontsize=16)
        df.boxplot('Temperature', ax=ax[0])
        df.boxplot('VOC', ax=ax[1])
        df.boxplot('Humidity', ax=ax[2])
        plt.show()

def extract_environment_data(data):
    import re
    pattern = re.compile(r"([0-9-]+)\s([0-9:.]+)\stemperature:\s([0-9.]+),\sgas:\s([0-9]+),\shumidity:\s([0-9.]+),\spressure:\s([0-9.]+),\saltitude:\s([0-9.]+)", re.MULTILINE)
    matches = list()
    for line in data:
        matches.append(re.match(pattern, line))
    return matches

def extract_soil_data(data):
    import re
    pattern = re.compile(r"([0-9-]+)\s([0-9:.]+)\s\[([0-9]+),\s([0-9.]+),\s([0-9.]+)\]", re.MULTILINE)
    matches = list()
    for line in data:
        matches.append(re.match(pattern, line))
    return matches
    

if __name__ == "__main__":
    from src.utilities.pickle_utilities import import_object, export_object
    import random
    import datetime
    import time

    # Plot soil moisture data
    max_volt = 3.292
    min_volt = 1.30
    with open("./logs/Test_Results/Single_Soil_Sensor/soil_moisture_sensor_1.txt", "r") as myfile:
        data = myfile.readlines()
    matches = extract_soil_data(data)
    data_dict = dict()
    for match in matches:
        current_val= (-100/(max_volt-min_volt))*(float(match.group(4))-max_volt)
        if current_val > 99.7:
            current_val = 100.00
        elif current_val< 0.3:
            current_val = 0.00
        # print(match.group(2))
        data_dict[match.group(2)] = current_val
    plot_soil_moisture(data_dict)

    # Plot temperature data
    with open("./logs/Test_Results/Single_Soil_Sensor/environment_sensor.txt", "r") as myfile:
        data = myfile.readlines()
    matches = extract_environment_data(data)
    data_dict = dict()
    temperature_dict = dict()
    data_dict['Temperature'] = {}
    data_dict['VOC'] = {}
    data_dict['Humidity'] = {}
    for match in matches:
        data_dict['Temperature'][match.group(2)] = float(match.group(3))
        data_dict['VOC'][match.group(2)] = float(match.group(4))
        data_dict['Humidity'][match.group(2)] = float(match.group(5))
    plot_temperature(data_dict['Temperature'])

    # Plot environment sensor data
    df = pd.DataFrame.from_dict(data_dict, orient='columns')
    df.reset_index(inplace=True)
    boxplot_environment(df)

