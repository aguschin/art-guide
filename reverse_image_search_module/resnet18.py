import os
import numpy as np
import torch
from PIL import Image
import pickle
from transformers import ViTFeatureExtractor, ViTModel
from torchvision import transforms  

torch.manual_seed(17)

class Img2VecViT():
    def __init__(self, batch_size=64):
        self.device = torch.device("cpu")  # Use CPU explicitly
        self.numberFeatures = 768 
        self.modelName = "google/vit-base-patch16-224-in21k"  
        self.model, self.featureLayer = self.getFeatureLayer()
        self.model = self.model.to(self.device)
        self.model.eval()
        self.toTensor = transforms.ToTensor()
        self.normalize = transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]) 
        self.batch_size = batch_size

    def getFeatureLayer(self):
        feature_extractor = ViTFeatureExtractor(model_name=self.modelName)
        model = ViTModel.from_pretrained(self.modelName)
        return model, feature_extractor

    def preprocess_image(self, image):
        transformationForCNNInput = transforms.Compose([transforms.Resize((224, 224))])
        if type(image) != torch.Tensor:
            image = self.toTensor(image)
        image = transformationForCNNInput(image)
        return self.normalize(image).unsqueeze(0).to(self.device)

    def getVectors(self, images):
        images = self.preprocess_image(images)
        with torch.no_grad():
            output = self.model(images)
            feature_vector = output.last_hidden_state.mean(dim=1)  # Take the mean over all tokens

        return feature_vector.numpy()


img2vec = Img2VecViT(batch_size=1)

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

        if counter % 1 == 0:
            print(counter)

    with open(output_file, 'wb') as output_f:
        pickle.dump(embeddings_dict, output_f)

    print(f"Successful images: {counter}")
    print(f"Failed images: {failed}")

if __name__ == "__main__":
    input_folder = '../data/img/full'
    output_file = '../data/embeddings_full.pkl'
    extract_and_save_embeddings(input_folder, output_file)
