# TME
Python implementation of Corrected Fisher Randomization (CFR)


Install:
```
pip install corrected-fisher-randomization
```

Usage example:
```
import numpy as np
import scipy.io
from corrected_fisher_randomization import CFR

model_dim = 10

data = scipy.io.loadmat('./exampleData.mat')
dataTensor = data['dataTensor']

print(dataTensor.shape)
t = data['t']

mask = np.logical_and(t > - 50, t < 350)
CFR(dataTensor, mask, model_dim)
```

The algorithm description can be found in the following article:
```
Elsayed, G.F.; Cunningham, J.P. Structure in Neural Population Recordings: An Expected Byproduct of Simpler Phenomena? Nat Neurosci 2017, 20, 1310–1318, doi:10.1038/nn.4617.
```

A matlab implementation can be found at the following link:
https://github.com/gamaleldin/CFR
