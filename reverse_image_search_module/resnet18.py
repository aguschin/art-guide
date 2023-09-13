import os
import numpy as np
import torch
from torchvision import transforms
import torchvision
import PIL
from PIL import Image

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
        image = transformationForCNNInput(image)
        if type(image) != torch.Tensor:
            image = self.toTensor(image)
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
    save_interval = 3000000
    embeddings_chunk = []

    with open(output_file, 'wb') as output_f:
        for image_file in image_files:
            image_path = os.path.join(input_folder, image_file)
            try:
                image = Image.open(image_path)
                feature_vector = img2vec.getVectors(image)
            except Exception as e:
                print(f"Skipping image: {image_file} - Error: {e}")
                failed += 1
                embeddings = np.zeros((1, img2vec.numberFeatures))
                embeddings_chunk.append(embeddings)
                continue

            embeddings_chunk.append(feature_vector)
            counter += 1
            if counter % save_interval == 0:
                embeddings_chunk = np.vstack(embeddings_chunk)
                with open(output_file, 'ab') as output_f:
                    np.save(output_f, embeddings_chunk)
                embeddings_chunk = []

            if counter % 100 == 0:
                print(counter)

        if embeddings_chunk:
            embeddings_chunk = np.vstack(embeddings_chunk)
            np.save(output_f, embeddings_chunk)

    print(f"Successful images: {counter}")
    print(f"Failed images: {failed}")


if __name__ == "__main__":
    input_folder = '/root/art-guide/data/img/full'
    output_file = '/root/art-guide/image_search_modified/embeddings_full_v3.npy'
    # input_folder = '/Users/mohammadsanaee/Documents/harbour/art projrct/image/img2'
    # output_file = '/Users/mohammadsanaee/Documents/harbour/art projrct/image/img2/embeddings_test.npy'
    extract_and_save_embeddings(input_folder, output_file)
