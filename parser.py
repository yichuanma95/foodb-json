import math
import numpy as np
import pandas as pd
import json
import os
from biothings.utils.dataload import dict_sweep


def extract_json(filename, data_dir=''):
    '''
    Read data from a JSON file and put it into a Pandas DataFrame. The JSON file is assumed to have one object
    for each datapoint, one on each line.

    :param filename: Name of the file from the FooDB database (as of April 2020)
    :param data_dir: The directory containing the file
    :return: a Pandas dataframe containing the data in the specified file
    '''

    data_dir = os.path.join(data_dir, 'foodb_2020_04_07_json')
    infile = os.path.join(data_dir, filename)
    assert os.path.exists(infile)

    # First extract the column names from the file
    f = open(infile, 'r')
    line = f.readline()
    datapoint = json.loads(line)
    f.close()
    columns = list(datapoint.keys())

    # Then read all of the data and put it into a Pandas DataFrame
    data_list = []
    with open(infile) as f:
        for line in f:
            datapoint = json.loads(line)
            datavals = list(datapoint.values())
            data_list.append(datavals)

    return pd.DataFrame(np.array(data_list), columns=columns)


def extract_contents(data_dir=''):
    data_dir = os.path.join(data_dir, 'foodb_2020_04_07_json')
    infile = os.path.join(data_dir, 'Content.json')
    assert os.path.exists(infile)
    f = open(infile, 'r')
    line = f.readline()
    datapoint = json.loads(line)
    f.close()
    columns = list(datapoint.keys())

    data_list = []
    with open(infile) as f:
        for line in f:
            datapoint = json.loads(line)
            if not datapoint['orig_content'] or datapoint['source_type'] != 'Compound':
                continue
            datavals = list(datapoint.values())
            data_list.append(datavals)

    return pd.DataFrame(np.array(data_list), columns=columns)

def load_data(data_folder):
    infile = os.path.join(data_folder, 'FoodCompound.json')
    assert os.path.exists(infile)
    docs = []
    with open(infile) as f:
        for line in f:
            doc = json.loads(line)
            doc = dict_sweep(doc, vals=[np.nan, None])
            docs.append(doc)

    for doc in docs:
        yield doc


def load_food(data_folder):
    food = extract_json('Food.json', data_folder)
    food_ids = food['id'].to_list()
    food_data = []
    for food_id in food_ids:
        food_entry = list(food[food['id'] == food_id].to_dict('index').values())[0]
        food_entry['_id'] = food_entry.pop('public_id', None)
        food_entry.pop('id', None)
        food_entry = dict_sweep(food_entry, vals=[np.nan, None])
        food_data.append(food_entry)

    for doc in food_data:
        yield doc
