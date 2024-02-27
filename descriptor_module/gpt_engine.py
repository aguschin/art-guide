from decouple import config
from openai import OpenAI


def generate_prompt(inputd: dict):
    # TODO: Eliminate fields if they are not present.
    # TODO: Think about some fields if they are needed: dimensions ?!
    # title = inputd.get('Title', 'Unknown Title')
    # original_title = inputd.get('OriginalTitle', 'Unknown')
    # date = inputd.get('Date', 'Date Unknown')
    # description = inputd.get('Description', None)
    # wiki_description = inputd.get('WikiDescription', None)
    # dimensions = inputd.get('Dimensions', 'Dimensions unknown')
    # genre = inputd.get('Genre', 'Unknown Genre')
    # location = inputd.get('Location', 'Unknown Location')
    # media = inputd.get('Media', 'Unknown Media')
    # series = inputd.get('Series', 'Not part of a series')
    # styles = inputd.get('Styles', 'Unknown Style')
    # tags = inputd.get('Tags', 'No Tags')
    #
    # author = inputd.get('Name_artist', 'Unknown Artist')
    # birth_date = inputd.get('BirthDate_artist', 'Unknown')
    # death_date = inputd.get('DeathDate_artist', 'Unknown')
    # birth_place = inputd.get('BirthPlace_artist', 'Unknown')
    # death_place = inputd.get('DeathPlace_artist', 'Unknown')
    # nationality = inputd.get('Nationality_artist', 'Unknown Nationality')
    # art_movements = inputd.get('ArtMovements_artist', 'Unknown Movements')
    # influenced_by = inputd.get('InfluencedBy_artist', 'No known influences')
    # pupils = inputd.get('Pupils_artist', 'Unknown')
    # artist_description = inputd.get('Description_artist', None)
    # artist_wiki_description = inputd.get('WikiDescription_artist', None)

    name = inputd.get("art_name", "a piece of art")
    author = inputd.get("author_name", "unknown artist")
    types = inputd.get("type", "")
    style = inputd.get("style", "")

    date = inputd.get("date", "")
    period = inputd.get("period", "")

    objects = inputd.get("objects", "")

    prompt = f"""Title: {name}
    Created by: {author}
    Types: {types}
    Date: {date}
    Style: {style}.
    Period: {period}
    objects: {objects}
    Please tell a coherent description that connects the painting's characteristics, the artist's life, and the historical and cultural context of the era."""

    return prompt


def gpt_generation(inputd: dict):
    client = OpenAI(api_key=config("OPENAI_API_KEY"))

    prompt = generate_prompt(inputd)

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    ouput = chat_completion.choices[0].message.content

    return ouput
