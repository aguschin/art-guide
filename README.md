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

[here](descriptor_module/README.md) for more details about the descriptor module.
