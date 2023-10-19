

# Image Retrieval using ResNet-18 and Annoy Index

This folder contains code for performing reverse image search using the ResNet-18 neural network for feature extraction and the Annoy Index for efficient nearest neighbor search.

## Dependencies

You can install the dependencies using the following command:

```shell
pip install -r requirements.txt
```
## Usage

Feature Extraction with ResNet-18

The Img2VecResnet18 class provides methods to extract image embeddings using the ResNet-18 neural network.

- getVec(img): Extracts the raw image embedding for a given image.
- getNormalizedVec(img): Extracts the normalized image embedding for a given image.

Example usage:

```python
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

## Reverse Image Search by Building the Annoy Index.

#### What is Annoy?
Annoy (Approximate Nearest Neighbors Oh Yeah) is a library that provides a data structure and algorithm for efficiently searching for approximate nearest neighbors in high-dimensional spaces.

#### Why Annoy?
We could have calculated the cosine similarities to find the nearest neighbor, as well as There are some other libraries to do nearest neighbor search. Annoy is almost as fast as the fastest libraries.
Visit: https://github.com/spotify/annoy

#### How it Works?
- The Annoy Index is built using embeddings from a collection of images stored in a .npy file.
- Initially, the dataset is divided into small clusters (called "forests" in Annoy). Each cluster contains a subset of data points.
- In each cluster, a binary tree is built to recursively partition the data points based on their feature values.
- When you query the Annoy index with a specific data point (query point), Annoy traverses the binary trees to find the cluster that is most likely to contain the nearest neighbors of the
  query point. Annoy narrows down the search space by traversing only the relevant branches of the binary trees.
- The Annoy Index performs approximate nearest neighbor search, meaning it might not always find the exact nearest neighbor but provides a good approximation.


#### Example usage:
**Build Annoy Index**

```python
import numpy as np
from annoy import AnnoyIndex
# Load all embeddings from the .npy file
all_embeddings = np.load('path_to_embeddings.npy')
embedding_dim = all_embeddings.shape[1]
# Build Annoy index
annoy_index = AnnoyIndex(embedding_dim, metric='dot')
for idx, vec in enumerate(all_embeddings):
    vec = vec / (np.linalg.norm(vec) + 1e-9)
    annoy_index.add_item(idx, vec)

num_trees = 50
annoy_index.build(num_trees)
```

#### Example usage:
**Reverse Image Search**

```python
import matplotlib.pyplot as plt
from resnet_image_search import find_image
# Load the image you want to search for
query_image = plt.imread('path_to_query_image.jpg')
# Perform reverse image search
idx, dist, data = find_image(query_image)
# Display the search results
print(f"Most similar image: {data['title']} (Distance: {dist:.2f})")
```

What can be improved in this section?

When performing a reverse image search using the `find_image` function, the returned results include an index (`idx`), a distance (`dist`), and data about the most similar image (`data`).

The distance (`dist`) represents the dissimilarity between the query image and the retrieved image embeddings. A lower distance indicates a higher degree of similarity. However, it's important to note that the distance's absolute value might not be as meaningful as its relative value compared to other distances in the result set.

To determine whether a retrieved image is a close match, you can compare the distance to a pre-defined threshold. If the distance is below the threshold, the retrieved image can be considered a relevant match. On the other hand, if the distance exceeds the threshold, it might indicate that the retrieved image is not a suitable match.

```python
# Example of using a distance threshold
if dist < threshold:
    print(f"Most similar image: {data['title']} (Distance: {dist:.2f})")
else:
    print("No close match found. Consider refining your search.")
```

## Dataset and Data Formatting


Here we get the dataset in a CSV file named wikiart_scraped.csv.

## Tests

To run the tests for the module use the following command

```shell
pytest reverse_image_search_module
```

## Possible Future Steps

### Explore Different Models:
While we are using ResNet-18 for feature extraction, we consider trying other pre-trained models (such as ResNet-50, VGG16, or Inception) to improve the quality of reverse image search results. Different models might capture different features and provide more accurate embeddings.

### Data Migration from a file to DataBase:
We are storing the embeddings in a single numpy file. we are planning to Extract the data from our numpy file, and then insert it into the database (Postgres/MYSQL). We will iterate through the numpy array and insert each embedding into the corresponding database table or collection.

### Automated Testing:
Implement automated tests to validate any changes you make to the code. Automated tests can ensure that your modifications don't introduce regressions and that the core functionality remains intact.

### Quality Metrics:
Develop ways to measure the quality of your reverse image search results. You could consider metrics like precision, recall, or F1-score to evaluate the accuracy of the retrieved images.

### Optimize Search Speed:
Investigate techniques to optimize the search speed further. This could involve adjusting parameters in the Annoy Index, experimenting with different distance metrics, or exploring GPU acceleration for feature extraction.

### Interactive Web Interface:
Extend the codebase to create an interactive web interface for users to upload images and perform reverse image searches. This could enhance user experience and make the tool more accessible.

### Parallel Processing:
Implement parallel processing techniques to speed up the extraction of embeddings and building of the Annoy Index, especially for large datasets.

### Fine-Tuning:
If you have a specific domain or dataset, consider fine-tuning the pre-trained model on your data to improve the relevance of search results within that domain.

