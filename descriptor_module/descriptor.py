from copy import copy
from manual_engine import manual_generation

INPUT_FORMAT = {
    'author_name': '',
    'art_name': '',
    'type': '',
    'style': '',
    'objects': [],
    'period': '',
    'date': ''
}


def describe(feature_dict: dict, engine: str = 'manual'):
    input_features = copy(INPUT_FORMAT)
    input_features.update(feature_dict)

    output = ''

    if engine == 'manual':
        output = manual_generation(input_features)
    else:
        assert False, f'engine value {engine} not found'

    return {'description': output}
