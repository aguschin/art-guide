import os
import numpy as np
import torch
from torchvision import transforms
import torchvision
import PIL
from PIL import Image
import pickle
import random
from tqdm import tqdm
from decouple import config
import warnings

# Disable all warnings
warnings.filterwarnings("ignore")

MULTI_EMBEDDINGS = bool(config('MULTI_EMBEDDINGS'))

SINGLE_VALES_OUTPUT_FILE = config('SINGLE_VALES_OUTPUT_FILE')
SINGLE_KEYS_OUTPUT_FILE = config('SINGLE_KEYS_OUTPUT_FILE')

MULTI_VALES_OUTPUT_FILE = config('MULTI_VALES_OUTPUT_FILE')
MULTI_KEYS_OUTPUT_FILE = config('MULTI_KEYS_OUTPUT_FILE')


torch.manual_seed(17)

class Img2VecResnet18():
    def __init__(self, batch_size=64):
        self.device = torch.device("cpu")  # Use CPU explicitly
        self.numberFeatures = 512
        self.modelName = "resnet-18"
        self.model, self.featureLayer = self.getFeatureLayer()
        self.model = self.model.to(self.device)
        self.model.eval()
        self.toTensor = transforms.ToTensor()
        self.normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        self.batch_size = batch_size

    def getFeatureLayer(self):
        cnnModel = torchvision.models.resnet18(pretrained=True)
        layer = cnnModel._modules.get('avgpool')
        self.layer_output_size = 512

        return cnnModel, layer

    def preprocess_image(self, image):
        transformationForCNNInput = transforms.Compose([transforms.Resize((224, 224))])
        if type(image) != torch.Tensor:
            image = self.toTensor(image)
        image = transformationForCNNInput(image)
        return self.normalize(image).unsqueeze(0).to(self.device)

    def getVectors(self, images):
        images = self.preprocess_image(images)
        embedding = torch.zeros(self.batch_size, self.numberFeatures, 1, 1)

        def copyData(m, i, o):
            embedding.copy_(o.data)

        h = self.featureLayer.register_forward_hook(copyData)
        self.model(images)
        h.remove()
        return embedding.numpy()[:, :, 0, 0]

img2vec = Img2VecResnet18(batch_size=1)


def extract_and_save_embeddings(input_folder, output_file):
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))]

    counter = 0
    failed = 0
    embeddings_dict = {}

    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        try:
            image = Image.open(image_path)
            feature_vector = img2vec.getVectors(image)
        except Exception as e:
            print(f"Skipping image: {image_file} - Error: {e}")
            failed += 1
            embeddingzero = np.zeros((1, img2vec.numberFeatures))
            embeddings_dict[str(embeddingzero)] = image_file
            continue

        embeddings_dict[image_file] = np.asarray(feature_vector)
        counter += 1

        if counter % 1000 == 0:
            print(counter)

    with open(output_file, 'wb') as output_f:
        pickle.dump(embeddings_dict, output_f)

    print(f"Successful images: {counter}")
    print(f"Failed images: {failed}")


def make_points(point1, point2, width, height):
    return point1[0]*width, point1[1]*height, point2[0]*width, point2[1]*height


def gen_multi_cropping(width, height, k=6, min_size_random=128):
    '''
        6 default croppings are made by hand, the rest are random
    '''

    DEFAULT_CROPP = [
        [(0,0), (1,1)],
        [(0.25, 0.25), (0.75, 0.75)],
        [(0,0), (0.5,0.5)],
        [(0.5,0), (1,0.5)],
        [(0,0.5), (0.5,1)],
        [(0.5,0.5), (1,1)]
    ]

    for i in range(k):
        if i < 6:
            default_points = DEFAULT_CROPP[i]
            x, y, xend, yend = make_points(default_points[0], default_points[1], width, height)
        else:
            x = random.randint(0, width - min_size_random)
            y = random.randint(0, height - min_size_random)

            xend = random.randint(x + min_size_random, width)
            yend = random.randint(y + min_size_random, height)

        yield x, y, xend, yend


def extract_and_save_embeddings_multiple(input_folder, output_file, k=6):
    image_files = tqdm([f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))])

    counter = 0
    failed = 0
    embeddings_dict = {}

    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        
        try:
            image = Image.open(image_path)

            vectors= []

            for x, y, x_end, y_end in gen_multi_cropping(image.width, image.height, k=k, min_size_random=128):
                croped = image.crop((x, y, x_end, y_end))
                feature_vector = img2vec.getVectors(croped)

                vectors.append(feature_vector)
            
            embeddings_dict[image_file] = vectors

            counter += 1
        except Exception as e:
            print(f"Skipping image: {image_file} - Error: {str(e)}")
            failed += 1

    with open(output_file, 'wb') as output_f:
        pickle.dump(embeddings_dict, output_f)

    print(f"Successful images: {counter}")
    print(f"Failed images: {failed}")



if __name__ == "__main__":
    IMAGE_FOLDER = 'data'
    
    if not os.path.isdir(IMAGE_FOLDER):
        os.mkdir(IMAGE_FOLDER)
    
    input_folder = 'data/img/full'

    if MULTI_EMBEDDINGS:
        output_file = f'{IMAGE_FOLDER}/embeddings_full_multi.pkl'
        extract_and_save_embeddings_multiple(input_folder, output_file)
    else:
        output_file = f'{IMAGE_FOLDER}/embeddings_full.pkl'
        extract_and_save_embeddings(input_folder, output_file)
