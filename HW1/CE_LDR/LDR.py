import sys
import math
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import time

def LDR(image_path, output_path, alpha=None, U=None):
    input_data = np.array(Image.open(image_path))
    
    start_time = time.time()
    if not U:
        U = np.zeros((255, 255))
        tmp_k = np.arange(255)
        for layer in range(255):
            U[:, layer] = np.minimum(tmp_k, 255 - layer) - np.maximum(tmp_k - layer, 0) + 1

    if not alpha:
        alpha = 2.5

    [HEIGHT, WIDTH, DEEP] = input_data.shape
    if (HEIGHT == 256) & ((WIDTH * DEEP) == 256):
        h2D_in = input_data
    else:
        in_Y = input_data

        h2D_in = np.zeros((256, 256))

        for i in range(HEIGHT):
            for j in range(WIDTH * DEEP):
                ref = in_Y[i, j % WIDTH, math.floor(j / WIDTH)]

                if i != HEIGHT - 1:
                    trg = in_Y[i + 1, j % WIDTH, math.floor(j / WIDTH)]
                    h2D_in[max(ref, trg), min(ref, trg)] = h2D_in[max(ref, trg), min(ref, trg)] + 1

                if j != (WIDTH * DEEP) - 1:
                    trg = in_Y[i, (j + 1) % WIDTH, math.floor((j + 1) / WIDTH)]
                    h2D_in[max(ref, trg), min(ref, trg)] = h2D_in[max(ref, trg), min(ref, trg)] + 1

    D = np.zeros((255, 255))
    s = np.zeros((255, 1))

    for layer in range(255):
        h_l = np.zeros((255 - layer, 1))

        tmp_idx = 0
        for i in range(1 + layer, 256):
            j = i - layer - 1

            h_l[tmp_idx, 0] = math.log(h2D_in[i, j] + 1)
            tmp_idx += 1

        s[layer, 0] = sum(h_l)

        if s[layer, 0] == 0:
            continue

        tmp_m_l = np.polymul(h_l.reshape(-1), np.ones((layer + 1, 1)).reshape(-1)).reshape(-1, 1)

        m_l = tmp_m_l if len(tmp_m_l) == 255 else np.insert(tmp_m_l, 0, np.zeros((255 - len(tmp_m_l),))).reshape(-1, 1)

        d_l = (m_l - min(m_l)) / U[:, layer].reshape(-1, 1)

        if sum(d_l) == 0:
            continue

        D[:, layer] = (d_l / sum(d_l)).reshape(-1)

    W = (s / max(s)) ** alpha
    d = np.matmul(D, W)

    d = d / sum(d)
    tmp = np.zeros((256, 1))

    for k in range(255):
        tmp[k + 1] = tmp[k] + d[k]

    x = 255 * tmp

    output = np.zeros((HEIGHT, WIDTH, DEEP))

    for i in range(HEIGHT):
        for j in range(WIDTH):
            for k in range(DEEP):
                output[i, j, k] = x[input_data[i, j, k]]

    CE_IMG = np.uint8(np.around(output))
    
    end_time = time.time()
    
    plt.imsave(output_path, CE_IMG)
    
    return (end_time - start_time) * 1000
