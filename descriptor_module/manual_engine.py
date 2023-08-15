def manual_generation(inputd: dict):

    name = inputd['art_name']
    name = name if name != '' else 'a piece of art'

    author = inputd['author_name']
    author = author if author != '' else 'some artist'

    types = inputd['type']
    types = types if types != '' else 'artwork'

    style = inputd['style']
    style = f'Falls under the {style} style. ' if style != '' else ''

    date = inputd['date']
    date = f', in {date}' if date != '' else ''

    period = inputd['period']
    period = f' during the {period} art period' if period != '' else ''

    objects = inputd['objects']
    objects = f'This {types} features ' + \
              ', '.join(objects) if len(objects) > 0 else ''

    ouput = f"""The artwork {name}, was created by {author}{period}{date}. {style}{objects}"""

    return ouput
