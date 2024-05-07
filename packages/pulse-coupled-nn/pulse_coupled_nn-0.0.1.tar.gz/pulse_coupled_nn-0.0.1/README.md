# PCNN
Python implementation of the Pulse Coupled Neural Network (PCNN) alongside multiple variations:
- Classical PCNN
- Feature Linking Model (FLM)
- Intersecting Cortical Model (ICM)
- Multi Linking Model (MLM)
- Spiking Cortical Model (SCM)
- Sigmoidal Linking Model (SLM)

Install:
```
pip install Pulse-Coupled-Neural-Networks
```

Usage example:
```
import numpy as np
import matplotlib.pyplot as plt

from pcnn import FLM
from pcnn import ICM
from pcnn import ClassicalPCNN
from pcnn import SCM
from pcnn import SLM


def run_image_segm(gamma=1, beta=2, v_theta=400, kernel_size=3, kernel='gaussian'):

    image = np.array(
        [[230, 230, 230, 230, 115, 115, 115, 115],
        [230, 230, 230, 230, 115, 115, 115, 115],
        [230, 230, 205, 205, 103, 103, 115, 115],
        [230, 230, 205, 205, 103, 103, 115, 115],
        [230, 230, 205, 205, 103, 103, 115, 115],
        [230, 230, 230, 230, 115, 115, 115, 115],
        [230, 230, 230, 230, 115, 115, 115, 115]]
    )

    model = ClassicalPCNN(image.shape, kernel, kernel_size=kernel_size)
    segm_image = model.segment_image(image, gamma=gamma, beta=beta, v_theta=v_theta, kernel_type='gaussian')

    plt.imshow(image)
    plt.colorbar()
    plt.show()

    plt.imshow(segm_image)
    plt.colorbar()
    plt.show()


run_image_segm()
```


