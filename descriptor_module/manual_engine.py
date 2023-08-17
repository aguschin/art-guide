def manual_generation(inputd: dict):
    
    name = inputd['art_name']
    name = name if name != '' else 'a piece of art'

    author = inputd['artists_name']
    author = author if author != '' else 'some artist'


    style = inputd['style']
    style = f'It follows the {style} style. ' if style != '' else ''

    date = inputd['date']
    date = f' in the {date}' if date != '' else ''

    period = inputd['period']
    period = f' during the {period}' if period != '' else 'a period'

    objects = inputd['objects']
    objects = 'It contains ' + ', '.join(objects) if len(objects) > 0 else ''

    Dimensions=inputd['Dimensions']
    Dimensions = f' This art piece has Dimensions of {Dimensions}' if Dimensions != '' else ''

    Genre=inputd['Genre']
    Genre = f'The {name} is a {Genre} Genre.' if Genre != '' else 'is not classfied in any known Genre.'

    Series=inputd['Series']
    Series = f'belongs to the {Series} Series.' if Series != '' else 'is an individual art piece.'

    OriginalTitle=inputd['OriginalTitle']
    OriginalTitle = f'The OriginalTitle for {name} is {OriginalTitle}.' if OriginalTitle != '' else ''
    
    Nationality=inputd['Nationality']
    Nationality = f'{author} is {Nationality} citizen.' if Nationality != '' else ''
    
    Fields=inputd['Fields']
    Fields = f'The Fields in which the artist make art in includes {Fields}.' if Fields != '' else 'They artist Fields of art are unknown.'

    ArtInstitutions=inputd['ArtInstitutions']
    ArtInstitutions = f'They are related to {ArtInstitutions} ArtInstitution.' if ArtInstitutions != '' else 'They are not related to any ArtInstitutions.'

    artist_birth_date = inputd['BirthDate']
    birth_place = inputd['BirthPlace']
    artist_birth_info = f' The artist were born on {artist_birth_date} in {birth_place},' if artist_birth_date != '' else ''

    artist_death_date = inputd['DeathDate']
    death_place = inputd['DeathPlace']
    artist_death_info = f'They passed away on {artist_death_date} in {death_place}.' if artist_death_date != '' else 'With my last update the artist is still alive.'

    artist_movements = inputd['ArtMovements']
    artist_movements = f'associated with the {artist_movements}' if artist_movements != '' else 'not associated with'

    artist_influenced_by = inputd['InfluencedBy']
    artist_influenced_by = f' Their work was influenced by {artist_influenced_by}.' if artist_influenced_by != '' else ''

    artist_info = f' {Nationality}{artist_birth_info}{artist_death_info}They were {artist_movements}art movement.{artist_influenced_by}{Fields}{ArtInstitutions}'
    ouput = f"""
        This is {name}, created by {author}{period}{date}. {style}{objects}{Genre} It {Series}{OriginalTitle}{artist_info}
    """

    return ouput
