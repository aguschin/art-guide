from copy import copy
import os
from decouple import config

from .manual_engine import manual_generation
from .gpt_engine import gpt_generation


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
