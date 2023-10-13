from torch import nn

class MnistClassifier(nn.Module):
  def __init__(self):
    super(MnistClassifier, self).__init__()
    self.flatten = nn.Flatten(start_dim=1, end_dim=-1)
    self.layer1 = nn.Linear(784, 512)
    self.act1 = nn.ReLU()
    self.layer2 = nn.Linear(512, 256)
    self.act2 = nn.ReLU()
    self.layer3 = nn.Linear(256, 128)
    self.act3 = nn.ReLU()
    self.layer4 = nn.Linear(128, 64)
    self.act4 = nn.ReLU()
    self.layer5 = nn.Linear(64, 10)

  def forward(self, x):
    x = self.flatten(x)
    x = self.layer1(x)
    x = self.act1(x)
    x = self.layer2(x)
    x = self.act2(x)
    x = self.layer3(x)
    x = self.act3(x)
    x = self.layer4(x)
    x = self.act4(x)
    x = self.layer5(x)
    return x