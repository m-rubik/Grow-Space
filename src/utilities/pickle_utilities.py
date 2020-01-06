import pickle

def import_object(filename):
    return pickle.load(open(filename,'rb'))

def export_object(filename, data):
    pickle.dump(data, open(filename,'wb+'))


if __name__ == "__main__":
    pass
    # import src.utilities.plot_utilities as plot_utilities
    # plot_utilities.plot_dict(test_dict)