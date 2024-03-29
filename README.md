# Art-guide

A telegram bot that can be your audio guide at Art Museums.
Send a photo of an artwork, and it will generate an audio description to which you can listen to.

<img width="360" alt="image" src="https://github.com/aguschin/art-guide/assets/6797716/2f668aba-963c-44be-81fb-97d91e67aeb9">

Try it out: https://t.me/harbour_art_guide_bot

We developed this project during [the class in Harbour.Space](https://harbour.space/data-science/courses/practicing-ds-skills-in-ml-competitions-alexander-guschin-875).

---

## How it works?

<img src="https://i.imgur.com/vRb0alE.jpg"  alt="Flow Diagram"/>

[Read a HackMD article about the project](https://hackmd.io/@aniervs/ryQt5Jlph)

## Modules:

### Image Cropper
This module is in charge of segmenting the image and cropping the relevant part of the image (for e.g. the painting in the image).

You can go [here](image_crop_module/README.md) for more details about the image crop module or read [this blog post](https://medium.com/@mjason98/paintings-extraction-from-images-art-guide-6002a749593e).


### Reverse Image Search
This module is in charge of finding the most similar image to the input image in the database and return the relevant information about the image.

You can go [here](reverse_image_search_module/README.md) for more details about the reverse image search module or read [this blog post](https://medium.com/@mohammadsanaee.n/your-ai-art-assistant-art-guide-9151433ab40a).


### Description Generation
This module receives the relevant information of the found image and generates a description of the image, in a specific format.
You can go [here](descriptor_module/README.md) for more details about the descriptor module or read [this blog post](https://medium.com/@ddunebari/your-guide-in-the-world-of-art-your-ai-museum-guide-1a087a132146).


### Text to Speech
This module receives the description and generates an audio file of the description.
You can go [here](text2speech_module/README.md) for more details about the text to speech module.

## Bot Flow

1. The bot receives the image from the user.
2. The bot sends the image to the image cropper module.
3. The bot sends the cropped image to the reverse image search module.
4. The reverse image search module finds the most similar image to the input image in the database, and returns it back to the bot with the relevant information.
5. The bot evaluates if the found image is similar enough to the input image. In case it isn't, the bot tells the user that it couldn't find the image. In case it is, the bot sends the relevant information of the found image to the description generation module.
6. The bot sends the description to the text to speech module.
7. The bot sends the audio file to the user.

---

## CI/CD

This project uses GitHub Actions for CI/CD. The workflow is defined in `.github/workflows/main.yml`. The workflow is triggered on every push or merge request to the `main` branch. The workflow consists mainly in a `build` job that builds the docker image and pushes it to the GitHub Container Registry. For more information please read [CI/CD README](.github/workflows/README.md)

---
## Setting up the project

There are 3 ways to run the project:

1. Run the project directly running the python file.
2. Build the Docker image and run it.
3. Run the docker image from the GitHub Container Registry.

### Environment

For the first 2 options you need to set up the environment variables

1. Create the environment file (on a `.env` file by using `.env.example` as template).
2. Set your own keys (telegram token).


### Run the project directly running the python file

You need 2 concurrent terminals to run the project.

##### Terminal 1 (Rest API)

```shell
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

##### Terminal 2 (Telegram Bot)


```shell
python3 main.py
```


### Build and run the Docker image

```shell
docker build -t art-guide-tg-bot .
docker run art-guide-tg-bot
```

### Run the docker image from the GitHub Container Registry

```shell
docker pull arielxx/art-guide-tg-bot:latest
docker run arielxx/art-guide-tg-bot:latest
```
---
## How to use the modules

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
