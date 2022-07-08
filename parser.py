import math
from numpy import nan
import json
import os
from biothings.utils.dataload import dict_sweep


def extract_json(filename, data_dir=''):
    data_dir = os.path.join(data_dir, 'foodb_2020_04_07_json')
    infile = os.path.join(data_dir, filename)
    assert os.path.exists(infile)

    data_table = {}
    with open(infile) as f:
        for line in f:
            datapoint = json.loads(line)
            datapoint = dict_sweep(datapoint, vals=[nan, None])
            public_id = datapoint.pop('public_id', None)
            datapoint['_id'] = public_id
            dbid = datapoint.pop('id', None)
            data_table[dbid] = datapoint
    return data_table


def extract_contents(data_dir=''):
    data_dir = os.path.join(data_dir, 'foodb_2020_04_07_json')
    infile = os.path.join(data_dir, 'Content.json')
    assert os.path.exists(infile)

    data_table = {}
    with open(infile) as f:
        for line in f:
            datapoint = json.loads(line)
            if not datapoint['orig_content'] or datapoint['source_type'] != 'Compound':
                continue
            food_id = datapoint['food_id']
            source_id = datapoint['source_id']
            item = {
                'orig_content': datapoint['orig_content'],
                'orig_unit': datapoint['orig_unit'],
                'citation': datapoint['citation']
            }
            data_table.setdefault((food_id, source_id), []).append(item)
    return data_table


def compile_contents(contents):
    unit = contents[0]['orig_unit']
    reference = contents[0]['citation']
    content_nums = []
    for content in contents:
        content_nums.append(float(content['orig_content']))
    content_min = min(content_nums)
    content_max = max(content_nums)
    content_avg = mean(content_nums)
    if math.isclose(content_avg, 0.0):
        return None
    return {
        'orig_contents': {
            'min': content_min,
            'max': content_max,
            'avg': content_avg,
            'unit': unit
        },
        'reference': reference
    }


def mean(nums):
    total = sum(nums)
    n = len(nums)
    return total / n


def load_data(data_folder):
    content = extract_json('Content.json', data_folder)
    compound = extract_json('Compound.json', data_folder)
    food = extract_json('Food.json', data_folder)

    for food_id, compound_id in content.keys():
        try:
            compound_item = compound[compound_id].copy()
            content_match = compile_contents(content[(food_id, compound_id)])
            if not content_match: continue
            compound_item['orig_contents'] = content_match['orig_contents']
            compound_item['reference'] = content_match['reference']
            food_item = food[food_id]
            food_item.setdefault('compounds', []).append(compound_item)
        except KeyError:
            continue

    for doc in food.values():
        yield doc


def load_food(data_folder):
    food = extract_json('Food.json', data_folder)
    food_ids = food['id'].to_list()
    food_data = []
    for food_id in food_ids:
        food_entry = list(food[food['id'] == food_id].to_dict('index').values())[0]
        food_entry['_id'] = food_entry.pop('public_id', None)
        food_entry.pop('id', None)
        food_entry = dict_sweep(food_entry, vals=[nan, None])
        food_data.append(food_entry)

    for doc in food_data:
        yield doc
