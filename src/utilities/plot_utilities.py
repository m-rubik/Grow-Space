"""!
All functions providing plotting functionalities.
"""

import matplotlib.pylab as plt

def plot_dict(dict):
    lists = sorted(dict.items()) 
    x, y = zip(*lists)
    plt.plot(x, y)
    plt.show()

def plot_boxplot(df):
    with plt.style.context("seaborn"):
        boxplot = df.boxplot()
        plt.title("Test title")
        plt.show()
        
# There might be an "generate plot" button or something similar that will automatically
# Generate plots from the data that it has stored

if __name__ == "__main__":
    from src.utilities.pickle_utilities import import_object, export_object
    import random
    import datetime
    import time
    rand = random.Random()
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
    # export_object("test1", test_dict1)
    # export_object("test2", test_dict2)
    # export_object("test3", test_dict3)
    test_dict1 = import_object("test1")
    test_dict2 = import_object("test2")
    test_dict3 = import_object("test3")

    import pandas as pd
    df1 = pd.DataFrame.from_dict(test_dict1, orient='index', columns=['test1'])
    df2 = pd.DataFrame.from_dict(test_dict2, orient='index', columns=['test2'])
    df3 = pd.DataFrame.from_dict(test_dict3, orient='index', columns=['test3'])

    new_df = df1.join(df2, how='outer')
    new_df = new_df.join(df3, how='outer')
    new_df.reset_index(inplace=True)
    print(new_df)
    plot_boxplot(new_df)

