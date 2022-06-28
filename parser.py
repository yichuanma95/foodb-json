import math
import numpy as np
import pandas as pd
import json
import os


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
        while True:
            line = f.readline()
            if not line: break
            datapoint = json.loads(line)
            datavals = list(datapoint.values())
            data_list.append(datavals)

    return pd.DataFrame(np.array(data_list), columns=columns)


def load_data(data_folder):
    content = extract_json('Content.json', data_folder)
    content = content.dropna(subset=['orig_content'])
    compound = extract_json('Compound.json', data_folder)
    food = extract_json('Food.json', data_folder)
    food_ids = food['id'].to_list()
    food_data = []
    for food_id in food_ids:
        compound_ids = pd.unique(content[(content['food_id'] == food_id) &
                                         (content['source_type'] == 'Compound')]['source_id'])
        compound_list = []
        for cid in compound_ids:
            contents_dict = content[(content['food_id'] == food_id) & (content['source_id'] == cid) &
                                    (content['source_type'] == 'Compound')][
                ['orig_content', 'orig_unit', 'citation']].to_dict()
            content_nums = np.array(list(map(lambda x: float(x), contents_dict['orig_content'].values())))
            avg = np.mean(content_nums)
            if math.isclose(avg, 0.0): continue
            extras = {
                'orig_contents': {
                    'min': np.min(content_nums),
                    'max': np.max(content_nums),
                    'avg': avg,
                    'unit': list(set(contents_dict['orig_unit'].values()))[0],
                },
                'reference': list(set(contents_dict['citation'].values()))[0]
            }
            try:
                compound_entry = list(compound[compound['id'] == cid].to_dict('index').values())[0]
                compound_entry.update(extras)
                compound_entry['_id'] = compound_entry.pop('public_id')
                compound_entry.pop('public_id', None)
                compound_entry.pop('id', None)
                compound_list.append(compound_entry)
            except IndexError:
                continue

        food_entry = list(food[food['id'] == food_id].to_dict('index').values())[0]
        food_entry['compounds'] = compound_list
        food_entry['_id'] = food_entry['public_id']
        food_entry.pop('public_id', None)
        food_entry.pop('id', None)
        food_data.append(food_entry)

    for doc in food_data:
        yield doc
