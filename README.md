# art-guide
Your guide in the world of art

## Environment

1. Create the environment file (on a `.env` file by using `.env.example` as template).
2. Set your own keys (telegram token).

### Build the Docker image

```shell
docker build -t art-guide-tg-bot .
```

### Run the docker image

```shell
docker run art-guide-tg-bot
```

### How to use the modules

```python
from descriptor_module import descriptor
from image_crop_module import croper

...

image = Image.open(path)

# input: Pilow image, output: np.array
image_croped = croper.crop_image(image)

...
description = descriptor.describe(features_dict)

print(description)
```

## Build and Deploy process

This repository contains the source code and configuration for automating the Continuous Integration and Continuous Deployment (CI/CD) process using GitHub Actions. The workflow is designed to build and deploy a Docker image of my project whenever changes are pushed to the `main` branch.

For more information read the [CI-CD README.md](.github/workflows/README.md) file in the `.github` folder.

## Description Generator Module


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
