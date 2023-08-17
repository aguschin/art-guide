## Description Generator Module

This module was designed with two strategies in mind:

*   Use the input and manually return a response only by filling in a template with the values.

*   Use a transformer to create a text given the input in such a way that it sounds human.

The second one will be left for future work since for the moment, the input is too small and a generative or summary model is not necessary.

### Expected Input

For the input the model expect the folllowing dictionary/json:

```python
{
    'author_name': 'Leonardo da Vinci',
    'art_name': 'Mona Lisa',
    'type': 'painting',
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


The previous fileds are string type and can be empty, but the less empty ones the richer will be the descriptor's output :)

### Expected Output

```python
{
    'description': 'some text'
}
```
