import torch
import torchvision.transforms as transforms
import numpy as np
from PIL import Image
from neural_net import MnistClassifier

model = MnistClassifier()
model.load_state_dict(torch.load("mnist_model_97.pt"))
model.eval()

def get_preds():
    image_path = "image.png"
    image = Image.open(image_path)

    preprocess = transforms.Compose([
        transforms.Grayscale(num_output_channels=1), # creates only one column for the color (because black/white image)
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])
    input_tensor = preprocess(image) # has shape [1, 28, 28] now

    with torch.no_grad():
        input_tensor = input_tensor.view(input_tensor.shape[0], -1) # keep first value, infer the rest, leads to  [1, 784]
        preds = model(input_tensor)

    softmax_preds = np.array(torch.softmax(preds, dim=1).numpy()).flatten()
    pred_order = np.argsort(softmax_preds)[::-1]
    #abs_pred = torch.argmax(preds, dim=1)

    return pred_order, softmax_preds
