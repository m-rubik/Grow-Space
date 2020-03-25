"""!
All functions providing plotting functionalities.
"""


import matplotlib.pylab as plt
import matplotlib.dates as mdates
import pandas as pd
import re
import datetime as dt


plt.rcParams.update({'font.size': 22})

environment_sensor_pattern = re.compile(r"([0-9-]+)\s([0-9:.]+):\stemperature:\s([0-9.]+),\sgas:\s([0-9]+),\shumidity:\s([0-9.]+),\spressure:\s([0-9.]+),\saltitude:\s([0-9.]+)", re.MULTILINE)
soil_moisture_pattern = re.compile(r"([0-9-]+)\s([0-9.:]+):\s\[([0-9]+),\s([0-9.]+),\s([0-9.]+)\]", re.MULTILINE)


def plot_soil_moisture(dict):
    """!
    Plots soil moisture data in simple line chart
    @param dict: Dicitonary containing timestamps and associated readings.
    """
   
    lists = sorted(dict.items()) 
    x, y = zip(*lists)
    fig, ax = plt.subplots()
    ax.plot(x, y, 'k', linewidth=2)
    fig.autofmt_xdate()
    hours = mdates.HourLocator(interval = 5)
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d - %H'))
    ax.grid()
    plt.title("Soil Moisture Sensor Readings Over Time")
    plt.ylabel("Moisture Percentage (%)")
    plt.xlabel("Time (Day - Hour)")
    plt.show()

def plot_temperature(dict):
    """!
    Plots temperature data in simple line chart
    @param dict: Dicitonary containing timestamps and associated readings.
    """

    lists = sorted(dict.items()) 
    x, y = zip(*lists)
    fig, ax = plt.subplots()
    ax.plot(x, y, 'k', linewidth=2)
    fig.autofmt_xdate()
    hours = mdates.HourLocator(interval = 5)
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d - %H'))
    ax.grid()
    plt.title("Temperature Over Time")
    plt.ylabel("Temperature (°C)")
    plt.xlabel("Time (Month-Day Hour)")
    plt.show()
    
def boxplot_environment(df):
    """!
    Creates a boxplot of all the relevant environment sensor data.

    What is a boxplot?
    Text from https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.boxplot.html:
    The box extends from the Q1 to Q3 quartile values of the data, with a line at the median (Q2). 
    The whiskers extend from the edges of box to show the range of the data. 
    The position of the whiskers is set by default to 1.5 * IQR (IQR = Q3 - Q1) from the edges of the box. 
    Outlier points are those past the end of the whiskers.

    @param df: dataframe object from which we generate a boxplot.
    """
    df['VOC'] = df['VOC'].div(1000)

    # with plt.style.context("seaborn"):
    fig, ax = plt.subplots(1, 3)
    fig.suptitle('Environment Sensor Data')
    df.boxplot('Temperature', ax=ax[0])
    df.boxplot('VOC', ax=ax[1], fontsize=12)
    df.boxplot('Humidity', ax=ax[2])
    ax[0].set_ylabel("Temperature (°C)")
    ax[1].set_ylabel("VOC (kΩ)")
    ax[2].set_ylabel("Humidity (%)")
    plt.show()

def extract_data_from_log(data, pattern):
    """!
    Function for extracting data out of a log file using regex matching.
    Returns all regex match objects.

    @param data: Raw data from the log file.
    @param pattern: Regex pattern to use for matching.
    """
    matches = list()
    for line in data:
        matches.append(re.match(pattern, line))
    return matches


if __name__ == "__main__":

    # Plot soil moisture data
    with open("./logs/Test_Results/soil_moisture_sensor_1.txt", "r") as myfile:
        data = myfile.readlines()
    matches = extract_data_from_log(data, soil_moisture_pattern)
    data_dict = dict()
    for match in matches:
        # current_val = float(match.group(4)) # Raw voltage reading
        current_val = float(match.group(5)) # Percentage reading
        index_time = match.group(1) + " " + match.group(2)
        index_dt = dt.datetime.strptime(index_time, "%Y-%m-%d %H:%M:%S.%f")
        data_dict[index_dt] = current_val
    plot_soil_moisture(data_dict)

    # Plot temperature data
    with open("./logs/Test_Results/environment_sensor.txt", "r") as myfile:
        data = myfile.readlines()
    matches = extract_data_from_log(data, environment_sensor_pattern)
    data_dict = dict()
    temperature_dict = dict()
    data_dict['Temperature'] = {}
    data_dict['VOC'] = {}
    data_dict['Humidity'] = {}
    for match in matches:
        index_time = match.group(1) + " " + match.group(2)
        index_dt = dt.datetime.strptime(index_time, "%Y-%m-%d %H:%M:%S.%f")
        data_dict['Temperature'][index_dt] = float(match.group(3))
        data_dict['VOC'][index_dt] = float(match.group(4))
        data_dict['Humidity'][index_dt] = float(match.group(5))
    plot_temperature(data_dict['Temperature'])

    # Plot environment sensor data
    df = pd.DataFrame.from_dict(data_dict, orient='columns')
    df.reset_index(inplace=True)
    boxplot_environment(df)

