import os
from copy import copy

from decouple import config

from .gpt_engine import gpt_generation
from .manual_engine import manual_generation

INPUT_FORMAT = {
    "author_name": "",
    "art_name": "",
    "type": "",
    "style": "",
    "objects": [],
    "period": "",
    "date": "",
}


def describe(feature_dict: dict, engine: str = "manual"):
    input_features = copy(INPUT_FORMAT)
    input_features.update(feature_dict)

    output = ""
    if config("OPENAI_API_KEY"):
        output = gpt_generation(input_features)
    else:
        output = manual_generation(input_features)

    return {"description": output}
