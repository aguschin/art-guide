import numpy as np
import torch
from torchvision import transforms
import torchvision

torch.manual_seed(17)

class Img2VecResnet18():
    def __init__(self, batch_size=64):
        self.device = torch.device("cuda")
        self.numberFeatures = 512
        self.modelName = "resnet-18"
        self.model, self.featureLayer = self.getFeatureLayer()
        self.model = self.model.to(self.device)
        self.model.eval()
        self.normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        self.batch_size = batch_size

    def getFeatureLayer(self):
        cnnModel = torchvision.models.resnet18(pretrained=True)
        layer = cnnModel._modules.get('avgpool')
        self.layer_output_size = 512

        return cnnModel, layer

    def preprocess_image(self, image):
        transformationForCNNInput = transforms.Compose([transforms.Resize((224,224))])
        image = transformationForCNNInput(image)
        return self.normalize(self.toTensor(image)).unsqueeze(0).to(self.device)

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
