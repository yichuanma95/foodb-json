import pytest
import math

from biothings.tests.web import BiothingsDataTest


class FooDBWebTest(BiothingsDataTest):
    host = 'localhost:8000'

    food_id = 'FOOD00914'
    prefix = ''
    compound_id = 'FDB023333'


class TestFooDBData(FooDBWebTest):
    def test_id(self):
        _id = self.request('food/' + self.food_id + '?fields=_id').json()
        assert _id['_id'] == self.food_id

    def test_name(self):
        name = self.request('food/' + self.food_id + '?fields=name').json()
        assert 'name' in name
        assert name['name'] == 'Soybean oil'

    def test_compounds(self):
        compounds = self.request('food/' + self.food_id + '?fields=compounds').json()
        assert 'compounds' in compounds
        assert len(compounds['compounds']) == 13

    def test_vitamin_k1(self):
        compounds = self.request('food/' + self.food_id + '?fields=compounds').json()
        compounds_dict = {}
        for compound in compounds['compounds']:
            compounds_dict[compound['_id']] = compound
        assert self.compound_id in compounds_dict
        vitamin_k1 = compounds_dict[self.compound_id]
        assert vitamin_k1['name'] == 'Vitamin K1 epoxide-1,4-diol'
        assert math.isclose(vitamin_k1['orig_contents']['avg'], 86.65)
        assert math.isclose(vitamin_k1['orig_contents']['min'], 82.35)
        assert math.isclose(vitamin_k1['orig_contents']['max'], 90.95)
        assert vitamin_k1['orig_contents']['unit'] == 'mg/100 g'
        assert vitamin_k1['reference'] == 'USDA'

    def test_metadata(self):
        metadata = self.request('metadata').json()
        assert metadata['biothing_type'] == 'food'
        assert metadata['stats']['total'] == 992
