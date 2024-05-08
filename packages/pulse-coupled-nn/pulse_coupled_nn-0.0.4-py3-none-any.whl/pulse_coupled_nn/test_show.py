import numpy as np
import matplotlib.pyplot as plt

from .flm_model import FLM
from .icm_model import ICM
from .classic_model import ClassicalPCNN
from .scm_model import SCM
from .slm_model import SLM


def choose_pcnn_model(pcnn_type, input_shape, kernel_type):
    if pcnn_type == 'ICM':
        model = ICM(input_shape, kernel_type)
    elif pcnn_type == 'SCM':
        model = SCM(input_shape, kernel_type)
    elif pcnn_type == 'SLM':
        model = SLM(input_shape, kernel_type)
    elif pcnn_type == 'FLM':
        model = FLM(input_shape, kernel_type)
    elif pcnn_type == 'PCNN':
        model = ClassicalPCNN(input_shape, kernel_type)

    return model


def run_image_segm(gamma, beta, v_theta, kernel='gaussian'):

    image = np.array(
        [[230, 230, 230, 230, 115, 115, 115, 115],
        [230, 230, 230, 230, 115, 115, 115, 115],
        [230, 230, 205, 205, 103, 103, 115, 115],
        [230, 230, 205, 205, 103, 103, 115, 115],
        [230, 230, 205, 205, 103, 103, 115, 115],
        [230, 230, 230, 230, 115, 115, 115, 115],
        [230, 230, 230, 230, 115, 115, 115, 115]]
    )

    model = ClassicalPCNN(image.shape, kernel, kernel_size=3)
    # segm_image = classifier.segment_image(image, gamma, beta, v_theta, kernel_type='gaussian')
    segm_image = model.segment_image(image, gamma=1, beta=2, v_theta=400, kernel_type='gaussian')
    print(image)
    print(segm_image)

    plt.imshow(image)
    plt.colorbar()
    plt.show()

    plt.imshow(segm_image)
    plt.colorbar()
    plt.show()

def run_pcnn_model(pcnn_type):
    image = cv2.imread('./fish_wall.jpg')

    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 'ICM'
    # 'SCM'
    # 'SLM'
    # 'FLM'
    # 'PCNN'

    model = choose_pcnn_model(pcnn_type, input_shape=image.shape, kernel_type='gaussian')
    model.simulate(image)


# run_pcnn_model('SCM')
# run_pcnn_model('ICM')
# run_pcnn_model('SLM')
# run_pcnn_model('FLM')
# run_pcnn_model('PCNN')
# import time
# start = time.time()
run_image_segm(1, 1.1, 40)
# print(time.time() - start)
# plt.imshow(np.hstack((image, segm_image)))
# plt.show()

# image = np.uint8(image)
# segm_image = np.uint8(segm_image)
# cv2.imshow("aia e", np.hstack((image, segm_image)))
# cv2.waitKey(0)
