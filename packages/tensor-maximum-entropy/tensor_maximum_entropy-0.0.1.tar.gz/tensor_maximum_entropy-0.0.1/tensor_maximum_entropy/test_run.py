import numpy as np
import scipy.io
from tme import TME

model_dim = 10

data = scipy.io.loadmat('./exampleData.mat')
dataTensor = data['dataTensor']

print(dataTensor.shape)
t = data['t']

mask = np.logical_and(t > - 50, t < 350)
TME(dataTensor, mask, model_dim)