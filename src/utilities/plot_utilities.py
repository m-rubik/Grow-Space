"""!
All functions providing plotting functionalities.
"""

import matplotlib.pylab as plt

def plot_dict(dict):
    lists = sorted(dict.items()) 
    x, y = zip(*lists)
    plt.plot(x, y)
    plt.xticks([])
    plt.yticks([])
    plt.show()

def plot_boxplot(df):
    with plt.style.context("seaborn"):
        boxplot = df.boxplot()
        plt.title("Example of what we could do for plotting")
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
    
        
# There might be an "generate plot" button or something similar that will automatically
# Generate plots from the data that it has stored

if __name__ == "__main__":
    from src.utilities.pickle_utilities import import_object, export_object
    import random
    import datetime
    import time

    max_volt = 3.292
    min_volt = 1.30

    with open("./logs/Test_Results/Watering Test (New)/soil_moisture_sensor_1.txt", "r") as myfile:
        data = myfile.readlines()
    matches = extract_soil_data(data)
    data_dict = dict()
    for match in matches:
        current_val= (-100/(max_volt-min_volt))*(float(match.group(4))-max_volt)
        if current_val > 99.7:
            current_val = 100.00
        elif current_val< 0.3:
            current_val = 0.00
        data_dict[match.group(2)] = current_val

    with open("./logs/Test_Results/Watering Test (New)/soil_moisture_sensor_2.txt", "r") as myfile:
        data2 = myfile.readlines()
    matches2 = extract_soil_data(data2)
    data_dict2 = dict()
    for match in matches2:
        current_val= (-100/(max_volt-min_volt))* (float(match.group(4))-max_volt)
        if current_val > 99.7:
            current_val = 100.00
        elif current_val< 0.3:
            current_val = 0.00
        data_dict2[match.group(2)] = current_val

    lists = sorted(data_dict.items()) 
    x, y = zip(*lists)

    lists2 = sorted(data_dict2.items()) 
    x2, y2 = zip(*lists2)

    plt.subplot(211)
    plt.title("Soil Moisture Sensor #1")
    plt.ylabel("Moisture")
    plt.xlabel("Time")
    plt.plot(y)
    plt.yticks([])
    plt.xticks([])
    plt.grid()
    plt.subplot(212)
    plt.title("Soil Moisture Sensor #2")
    plt.ylabel("Moisture")
    plt.xlabel("Time")
    plt.plot(y2)
    plt.yticks([])
    plt.xticks([])
    plt.grid()
    plt.show()

    # rand = random.Random()
    # test_dict1 = dict()
    # test_dict2 = dict()
    # test_dict3 = dict()
    # test_dict1[datetime.datetime.now()] = round(rand.random()*100,2)
    # test_dict2[datetime.datetime.now()] = round(rand.random()*100,2)
    # test_dict3[datetime.datetime.now()] = round(rand.random()*100,2)
    # time.sleep(1)
    # test_dict1[datetime.datetime.now()] = round(rand.random()*100,2)
    # test_dict2[datetime.datetime.now()] = round(rand.random()*100,2)
    # test_dict3[datetime.datetime.now()] = round(rand.random()*100,2)
    # time.sleep(1)
    # test_dict1[datetime.datetime.now()] = round(rand.random()*100,2)
    # test_dict2[datetime.datetime.now()] = round(rand.random()*100,2)
    # test_dict3[datetime.datetime.now()] = round(rand.random()*100,2)
    # time.sleep(1)
    # test_dict1[datetime.datetime.now()] = round(rand.random()*100,2)
    # test_dict2[datetime.datetime.now()] = round(rand.random()*100,2)
    # test_dict3[datetime.datetime.now()] = round(rand.random()*100,2)
    # time.sleep(1)
    # test_dict1[datetime.datetime.now()] = round(rand.random()*100,2)
    # test_dict2[datetime.datetime.now()] = round(rand.random()*100,2)
    # test_dict3[datetime.datetime.now()] = round(rand.random()*100,2)
    # time.sleep(1)
    # test_dict1[datetime.datetime.now()] = round(rand.random()*100,2)
    # test_dict2[datetime.datetime.now()] = round(rand.random()*100,2)
    # test_dict3[datetime.datetime.now()] = round(rand.random()*100,2)
    # time.sleep(1)
    # test_dict1[datetime.datetime.now()] = round(rand.random()*100,2)
    # test_dict2[datetime.datetime.now()] = round(rand.random()*100,2)
    # test_dict3[datetime.datetime.now()] = round(rand.random()*100,2)
    # export_object("plot_test1", test_dict1)
    # export_object("plot_test2", test_dict2)
    # export_object("plot_test3", test_dict3)

    # test_dict1 = import_object("plot_test1")
    # test_dict2 = import_object("plot_test2")
    # test_dict3 = import_object("plot_test3")

    # import pandas as pd

    # df = pd.DataFrame.from_dict(data_dict, orient='index', columns=['Test'])
    # df.reset_index(inplace=True)
    # plot_boxplot(df)


    # df1 = pd.DataFrame.from_dict(test_dict1, orient='index', columns=['sample_variable_1'])
    # df2 = pd.DataFrame.from_dict(test_dict2, orient='index', columns=['sample_variable_2'])
    # df3 = pd.DataFrame.from_dict(test_dict3, orient='index', columns=['sample_variable_3'])
    # plot_boxplot(df3)

    # new_df = df1.join(df2, how='outer')
    # new_df = new_df.join(df3, how='outer')
    # new_df.reset_index(inplace=True)
    # print(new_df)
    # plot_boxplot(new_df)

