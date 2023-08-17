## Description Generator Module

This module will generate the images description by retrave the data from data.csv and artists.csv.

### manual_engine.py
The manual_engine.py file contains a function called manual_generation responsible for generating descriptions of artworks. The function takes an input dictionary containing various attributes. It then constructs a coherent description by combining these attributes.

### descriptor.py
The descriptor.py file defines an input format dictionary called INPUT_FORMAT, which provides default values for various attributes of an artwork's description. The describe function takes an input dictionary of feature information about an artwork. It then merges this input with the default input format and utilizes the manual description generation engine to create a description.

### t5_engine.py
Originally, there was an intention to use the T5 language model engine for generating descriptions. However, due to the high quality standards and training requirements of the T5 engine, it necessitates a substantial amount of data for training to achieve the desired level of description quality. Unfortunately, time constraints and resource limitations prevent us from gathering the necessary data for training the T5 engine to its fullest potential.



### Input Format


The model expects the input in the form of the following dictionary/json:

```python
INPUT_FORMAT = {
    'artists_name': '',
    'art_name': '',
    'Dimensions': '',
    'style': '',
    'objects': [],
    'period': '',
    'date': '',
    'Genre':'', 
    'Series':'',
    'OriginalTitle':'',
    #----------artist info
    'ArtMovements':'', 
    'BirthDate':'',
    'BirthPlace':'',
    'DeathPlace':'',
    'DeathDate' :'' , 
    'Fields':'',
    'Genres':'',  
    'Nationality':'',
    'ArtInstitutions' :'',
    'OriginalName':'',
    'InfluencedBy': ''
}
```

### Expected Output

```python
{
    'description': 'some text'
}
```
