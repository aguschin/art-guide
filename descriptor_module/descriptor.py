from copy import copy
import os
from .manual_engine import manual_generation
from .gpt_engine import gpt_generation


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

    # if engine == 'manual':
    #     output = manual_generation(input_features)
    # else:
    #     assert False, f'engine value {engine} not found'

    if "OPENAI_API_KEY" in os.environ:
        output = gpt_generation(input_features)
    else:
        output = manual_generation(input_features)

    return {'description': output}
