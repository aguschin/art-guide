# art-guide
Your guide in the world of art


## Description Generator Module

### How to use it

```python
from descriptor_module import descriptor

...
# features_dict its a dict with the fields described below

description = descriptor.describe(features_dict)

print(description)
```

### Expected Input

For the input the model expect the folllowing dictionary/json:

```python
{
    'author_name': 'Leonardo da Vinci',
    'art_name': 'Mona Lisa'
    'type': 'painting'
    'style': 'Renaissance',
    'objects': ['painting', 'Oil Paint'],
    'period': 'Renaissance',
    'date': '1503'
}
```

This is an example of what is expected, each field is described below:


*   **author_name** The name of the creator
*   **art_name** The name of the art piece
*   **type** Type of work. (e.g. painintg, mixography, sculpture, etc)
*   **style** The Style. (e.g Renaissance, Contemporany)
*   **objects** The structure of the workpiece. The better for the descriptor output in case that the art_name and author is unknown.
*   **period** The period
*   **date** The date, can be exact or aproximate.


The previous fileds can be empty, but the more the richer will be the descritor's output :)

### Expected Output

```python
{
    'description': 'some text'
}
```
