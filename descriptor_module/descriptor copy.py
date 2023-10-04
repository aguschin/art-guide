from copy import copy
from .manual_engine import manual_generation
from .auto_engine import ask_cohere_with_ai_snippets

INPUT_FORMAT = {
    'author_name': '',
    'art_name': '',
    'type': '',
    'style': '',
    'objects': [],
    'period': '',
    'date': ''
}


def describe(feature_dict, engine='auto'):
    if engine == 'auto':
        query = {
            'author_name': feature_dict['author_name'],
            'art_name': feature_dict['art_name'],
            'date': feature_dict['date']
        }
        return {'description': ask_cohere_with_ai_snippets(query)}
    elif engine == 'manual':
        return {'description': manual_generation(feature_dict)}
    else:
        assert False, f'engine value {engine} not found'
