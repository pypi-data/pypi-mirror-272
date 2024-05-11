import time
from pathlib import Path
from .utils import *
import glob
import cv2
import numpy as np
from natsort import natsorted
from tqdm import tqdm

_sift = cv2.SIFT_create()

def crop_points(input_img):
    if not input_img.dtype == np.uint8:
        return
    height, width = input_img.shape[:2]
    full_area = height * width
    img_blur = cv2.medianBlur(input_img.copy(), ksize=5)
    img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
    img_binary = cv2.threshold(img_gray, thresh=3, maxval=255, type=cv2.THRESH_BINARY)[1]
    kernel = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(3, 3))
    img_open = cv2.morphologyEx(img_binary, cv2.MORPH_OPEN, kernel, iterations=1)
    contours, _ = cv2.findContours(img_open, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    corner = []
    for i, contour in enumerate(contours):
        arc_len = cv2.arcLength(contour, True)
        epsilon = max(3, np.int32(arc_len * 0.02))
        approx = cv2.approxPolyDP(contour, epsilon, True)
        area = cv2.contourArea(contour)
        rect = cv2.minAreaRect(contour)
        rect_h = np.int32(rect[1][0])
        rect_w = np.int32(rect[1][1])
        if min(rect_h, rect_w) == 0:
            rotation = 0
        else:
            rotation = max(rect_h, rect_w) / min(rect_h, rect_w)

        if rotation < 30 and full_area * 0.2 < area < full_area and approx.shape[0] == 4:
            corner.append([approx[0][0][0], approx[0][0][1]])
            corner.append([approx[1][0][0], approx[1][0][1]])
            corner.append([approx[2][0][0], approx[2][0][1]])
            corner.append([approx[3][0][0], approx[3][0][1]])
    if not len(corner):
        return

    c_p1 = {'x': np.int32(corner[0][0]), 'y': np.int32(corner[0][1])}
    c_p2 = {'x': np.int32(corner[1][0]), 'y': np.int32(corner[1][1])}
    c_p3 = {'x': np.int32(corner[2][0]), 'y': np.int32(corner[2][1])}
    c_p4 = {'x': np.int32(corner[3][0]), 'y': np.int32(corner[3][1])}

    if np.int32(c_p1['x']) < np.int32(width / 2) and np.int32(c_p1['y']) < np.int32(height / 2):
        l_t = {'x': max(c_p1['x'], c_p2['x']), 'y': max(c_p1['y'], c_p4['y'])}
        l_b = {'x': max(c_p1['x'], c_p2['x']), 'y': min(c_p2['y'], c_p3['y'])}
        # r_b = {'x': min(c_p3['x'], c_p4['x']), 'y': min(c_p2['y'], c_p3['y'])}
        r_t = {'x': min(c_p3['x'], c_p4['x']), 'y': max(c_p1['y'], c_p4['y'])}
        return l_t['y'], l_b['y'], l_t['x'], r_t['x']

    elif np.int32(c_p1['x']) > np.int32(width / 2) and np.int32(c_p1['y']) < np.int32(height / 2):
        l_t = {'x': max(c_p2['x'], c_p3['x']), 'y': max(c_p2['y'], c_p1['y'])}
        l_b = {'x': max(c_p2['x'], c_p3['x']), 'y': min(c_p3['y'], c_p4['y'])}
        # r_b = {'x': min(c_p1['x'], c_p4['x']), 'y': min(c_p3['y'], c_p4['y'])}
        r_t = {'x': min(c_p1['x'], c_p4['x']), 'y': max(c_p1['y'], c_p2['y'])}
        return l_t['y'], l_b['y'], l_t['x'], r_t['x']
    else:
        return


# @execution_time
def _register(source: str, target: str, sift_obj, match_factor: float = 0.6, thresh_area: float = 0.65, thresh_rotate: float = 0.89):
    """
    :param source: source image path
    :param target: target image path
    :param match_factor: match factor for good match, 0.4 means more accuracy, 0.6 means more quantity
    :param thresh_area: threshold for crop area
    :param thresh_rotate: threshold for rotation in perspective transformation
    :return:
    """
    src = image_load(source)
    dst = image_load(target)
    h, w = src.shape[:2]
    img_area = h * w
    img2_copy = dst.copy()

    kp1, des1 = sift_obj.detectAndCompute(src, None)
    kp2, des2 = sift_obj.detectAndCompute(dst, None)
    flann = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=50))
    matches = flann.knnMatch(des1, des2, k=2)

    good_matches = ([m] for m, n in matches if m.distance < match_factor * n.distance)
    points = [(kp1[match[0].queryIdx].pt, kp2[match[0].trainIdx].pt) for match in good_matches]
    pts1 = np.array([pts[0] for pts in points], dtype=np.float32).reshape(-1, 1, 2)
    pts2 = np.array([pts[1] for pts in points], dtype=np.float32).reshape(-1, 1, 2)
    try:
        homography_matrix, _ = cv2.findHomography(pts1, pts2, cv2.RANSAC, ransacReprojThreshold=4)
        warped_img = cv2.warpPerspective(img2_copy, homography_matrix, dsize=(w, h), flags=17)
        cp = crop_points(warped_img)
        if not isinstance(cp, tuple):
            return
        p1, p2, p3, p4 = cp
        remain_area = (p4 - p3) * (p2 - p1)
        if remain_area / img_area < thresh_area:
            return
        eye_m = np.eye(2, 2)
        matrix_similarity = 1 - np.linalg.norm(homography_matrix[:2, :2] - eye_m)
        if matrix_similarity < thresh_rotate:
            return
        empty_img = np.zeros_like(img2_copy)
        dst_reg = empty_img.copy()
        src_crop = empty_img.copy()

        dst_reg[p1:p2, p3:p4] = warped_img[p1:p2, p3:p4]
        src_crop[p1:p2, p3:p4] = src[p1:p2, p3:p4]

        return {'src_registration': src_crop, 'dst_registration': dst_reg, 'dst_warp': warped_img, 'crop_points': cp,
                'H': homography_matrix}
    except Exception as e:
        # print(e)
        return

def _register_single(path):
    src, tgt, cur_path = path
    name = Path(src).stem
    registration_result = _register(src, tgt, sift_obj=_sift)
    if not isinstance(registration_result, dict):
        return name
    Path(cur_path).mkdir(parents=True, exist_ok=True)
    p0, p1, p2, p3 = registration_result['crop_points']
    src_reg = registration_result['src_registration']
    dst_reg = registration_result['dst_registration']
    img_shape = src_reg.shape[:2]

    crop_mask = np.zeros((img_shape[0], img_shape[1], 1))
    crop_mask[p0:p1, p2:p3] = 1
    crop_mask = torch.tensor(crop_mask).unsqueeze(0)

    save_image_to_npy(src_reg, f'{cur_path}/{name}_source_sift.npy')
    save_image_to_npy(dst_reg, f'{cur_path}/{name}_target_sift.npy')
    save_image_to_pth(crop_mask, f'{cur_path}/{name}_crop_mask.pth')


class Register:
    def __init__(self):...

    def __call__(self, *args, **kwargs):
        self.run_register(*args, **kwargs)

    @execution_time
    def run_register(self, source_path, target_path, save_path=None, multiprocessing=False, processes=10):
        source_images = glob.glob(f'{source_path}/*.jpg')
        target_images = glob.glob(f'{target_path}/*.jpg')
        assert len(source_images) == len(target_images)
        if save_path is None:
            save_path = './preprocess_data/transfer_result'
        Path(save_path).mkdir(parents=True, exist_ok=True)
        source_images_sort = natsorted(source_images)
        target_images_sort = natsorted(target_images)
        cur_save_path = [f'{save_path}/{Path(name).stem}' for name in source_images_sort]
        zipped_path = zip(source_images_sort, target_images_sort, cur_save_path)
        num_items = len(source_images_sort)

        if not multiprocessing:
            failed = []
            item_bar = tqdm(zipped_path, total=num_items)
            item_bar.set_description('register')
            for src, tgt, cur_path in item_bar:
                failed.append(_register_single((src, tgt, cur_path)))
        else:
            failed = multiprocessor(processes=processes, obj_func=_register_single, items=zipped_path)
        return failed

def register(src, dst, save, multiprocessing=False, processes=10):
    registration = Register()
    return registration(source_path=src, target_path=dst, save_path=save, multiprocessing=multiprocessing, processes=processes)

