
# Image Retrieval using ResNet-18 and Annoy Index

This folder contains code for performing reverse image search using the ResNet-18 neural network for feature extraction and the Annoy Index for efficient nearest neighbor search. The provided code allows you to generate embeddings for a collection of images, build an Annoy Index from those embeddings, and perform reverse image searches to find similar images from a dataset.


# Image Retrieval using ResNet-18 and Annoy Index

This repository contains code for performing reverse image search using the ResNet-18 neural network for feature extraction and the Annoy Index for efficient nearest neighbor search.

## Dependencies

To use the code in this repository, you will need the following dependencies:

- Python 3.x
- PyTorch
- torchvision
- numpy
- pandas
- matplotlib
- annoy

You can install these dependencies using the following command:

```
pip install torch torchvision numpy pandas matplotlib annoy
```
## Usage

Feature Extraction with ResNet-18

The Img2VecResnet18 class provides methods to extract image embeddings using the ResNet-18 neural network.

- getVec(img): Extracts the raw image embedding for a given image.
- getNormalizedVec(img): Extracts the normalized image embedding for a given image.

Example usage:

```
from resnet_image_search import Img2VecResnet18
import numpy as np
import matplotlib.pyplot as plt
import torchvision.transforms as transforms

# Initialize the Img2VecResnet18 instance
img2vec = Img2VecResnet18()

# Load an image and get its normalized embedding
image = plt.imread('path_to_your_image.jpg')
normalized_embedding = img2vec.getNormalizedVec(image)
```

## Building the Annoy Index

The Annoy Index is built using embeddings from a collection of images.

Embeddings should be stored in a .npy file, where each row represents an embedding.

The annoy_index is built using the embeddings and can be used for nearest neighbor search.

Example usage:


```
import numpy as np
from annoy import AnnoyIndex

# Load all embeddings from the .npy file
all_embeddings = np.load('path_to_embeddings.npy')
embedding_dim = all_embeddings.shape[1]

# Build Annoy index
annoy_index = AnnoyIndex(embedding_dim, metric='dot')

for idx, vec in enumerate(all_embeddings):
    vec = vec / np.linalg.norm(vec)
    annoy_index.add_item(idx, vec)
    
num_trees = 50
annoy_index.build(num_trees)
```
## Reverse Image Search

The find_image function performs reverse image search using the Annoy Index.

Example usage:

```
import matplotlib.pyplot as plt
from resnet_image_search import find_image

# Load the image you want to search for
query_image = plt.imread('path_to_query_image.jpg')

# Perform reverse image search
idx, dist, data = find_image(query_image)

# Display the search results
print(f"Most similar image: {data['title']} (Distance: {dist:.2f})")
```

## Dataset and Data Formatting


Here we get the dataset in a CSV file named wikiart_scraped.csv.
