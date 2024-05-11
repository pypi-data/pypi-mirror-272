from PIL import Image, ImageOps
import numpy as np
import torch


def image_load(image_path):
    img = Image.open(image_path).convert('RGB')
    return np.array(ImageOps.exif_transpose(img))

def save_image_to_npy(input_numpy, save_path):
    np.save(save_path, input_numpy)

def save_image_to_pth(input_tensor, save_path):
    torch.save(input_tensor, save_path)

import multiprocessing as mp

def multiprocessor(processes, obj_func, items):
    with mp.Pool(processes=processes) as pool:
        result = pool.map(obj_func, items)
    pool.join()
    return result

import time

def execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'Execution time of "{func.__name__}": {float(end-start):.2f} seconds')
        return res
    return wrapper

