from copy import copy
from manual_engyne import manual_generation

INPUT_FORMAT = {
    'author_name': '',
    'art_name': '',
    'type': '',
    'style': '',
    'objects': [],
    'period': '',
    'date': ''
}


def describe(feature_dict: dict, engyne: str = 'manual'):
    input_features = copy(INPUT_FORMAT)
    input_features.update(feature_dict)

    output = ''

    if engyne == 'manual':
        output = manual_generation(input_features)
    else:
        assert False, f'engyne value {engyne} not found'

    return {'description': output}
