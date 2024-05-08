import numpy as np
import scipy.io
from cfr import CFR

model_dim = 10

data = scipy.io.loadmat('./exampleData.mat')
dataTensor = data['dataTensor']

print(dataTensor.shape)
t = data['t']

mask = np.logical_and(t > - 50, t < 350)
CFR(dataTensor, mask, model_dim)