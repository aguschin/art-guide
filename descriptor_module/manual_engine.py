def manual_generation(inputd: dict):

    name = inputd['art_name']
    name = name if name != '' else 'a piece of art'

    author = inputd['author_name']
    author = author if author != '' else 'some artist'

    types = inputd['type']
    name = f'{types} is called {name}' if types != '' else f'is {name}'

    style = inputd['style']
    style = f'It follows the {style} style. ' if style != '' else ''

    date = inputd['date']
    date = f', {date}' if date != '' else ''

    period = inputd['period']
    period = f' in the {period}' if period != '' else ''

    objects = inputd['objects']
    objects = 'It contains ' + ', '.join(objects) if len(objects) > 0 else ''

    ouput = f"""
        This {name}, created by {author}{period}{date}. {style}{objects}
    """

    return ouput
