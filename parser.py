import math
import json
import os

from numpy import nan

from biothings.utils.dataload import dict_sweep


def extract_json(filename, data_dir=''):
    """Extracts data from a specified JSON file downloaded from the FooDB website and
    located in a specified directory containing the files and returns a dictionary
    storing the data for easy indexing.

    :param filename: Name of the JSON file to extract data from
    :type filename: str
    :param data_dir: Directory that the file is located in, defaults to empty string
    :type data_dir: str, optional
    :return: A dictionary with id's as keys and corresponding examples as values
    :rtype: dict of {int: dict}
    """
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
    """Extracts the data from the FooDB file Contents.json without reading
    the entire file (3.5 GB) at once. This data contains relations between
    food items and compound items in FooDB. Contents with null values for
    original content or source type other than 'Compound' are ignored. Only
    the food id, source id, original content, original unit, and citation
    are read.

    :param data_dir: Directory that the file is located in, defaults to empty string
    :type data_dir: str, optional
    :return: A dictionary with (food id, source id) pairs as keys and a list of
        contents corresponding to each food-compound relation as values
    :rtype: dict of {(int, int) tuple: list of dicts}
    """
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
    """Generates a contents object from a list of contents corresponding to a
    food-compound relation in the FooDB database if average of the content values
    is nonzero; otherwise returns None for the corresponding relation, which is
    assumed to not exist in this case.

    :param contents: A list of content objects corresponding to a food-compound
        relation
    :type contents: list of dicts
    :return: A dictionary containing minimum, maximum, and average values of
        contents along with original unit and reference, or None if average value
        is 0
    :rtype: dict or None
    """
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
    """Calculates the mean (average) of a list of numbers. This does not use NumPy.

    :param nums: a list of numbers to be averaged
    :type nums: list of numbers, int or float
    :return: average of nums
    :rtype: float
    """
    total = sum(nums)
    n = len(nums)
    return total / n


def load_data(data_folder):
    """Main code of the parser for the FooDB BioThings API. Generates a list of
    compound objects for each food object and their contents, then yields them.

    :param data_folder: A directory containing the FooDB JSON files. Required.
    :type data_folder: str
    :return: an iterator of dictionaries, one for each modified food item
    :rtype: iterator of dicts
    """
    content = extract_contents(data_folder)
    compound = extract_json('Compound.json', data_folder)
    food = extract_json('Food.json', data_folder)

    for food_id, compound_id in content.keys():
        try:
            compound_item = compound[compound_id].copy()
            content_match = compile_contents(content[(food_id, compound_id)])
            if not content_match:
                continue
            compound_item['orig_contents'] = content_match['orig_contents']
            compound_item['reference'] = content_match['reference']
            food_item = food[food_id]
            food_item.setdefault('compounds', []).append(compound_item)
        except KeyError:
            continue

    for doc in food.values():
        yield doc
