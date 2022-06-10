import pandas as pd
import json
import numpy as np

def extract_json(filename):
    '''
    Read data from a JSON file and put it into a Pandas DataFrame. The JSON file is assumed to have one object
    for each datapoint, one on each line.

    :param filename: Name of the file from the FooDB database (as of April 2020)
    :return: a Pandas dataframe containing the data in the specified file
    '''

    data_dir = 'foodb_2020_04_07_json/'

    # First extract the column names from the file
    f = open(data_dir + filename, 'r')
    line = f.readline()
    datapoint = json.loads(line)
    f.close()
    columns = list(datapoint.keys())

    # Then read all of the data and put it into a Pandas DataFrame
    data_list = []
    with open(data_dir +filename) as f:
        while True:
            line = f.readline()
            if not line: break
            datapoint = json.loads(line)
            datavals = list(datapoint.values())
            data_list.append(datavals)

    return pd.DataFrame(np.array(data_list), columns=columns)
