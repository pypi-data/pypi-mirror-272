__all__ = [
    'hollowing_logo'
]


import cv2
import numpy as np
from numpy import ndarray
from typing import Iterable


def hollowing_logo(
    image: ndarray,
    color: Iterable = [0,0,255],
    thickness: int = 5,
    *,
    margin: int = 5,
) -> ndarray:
    fg_u8 = None
    if image.ndim == 3:
        if image.shape[-1] == 4 and np.less(image[:,:,-1],128).any():
            fg_u8 = np.greater(image[:,:,-1], 127).astype(np.uint8)*255
        elif 3 <= image.shape[-1]:
            image = image[:,:,:3]
            bars = [image[:,:margin],image[:,-margin:],image[:margin,:],image[-margin,:]]
            bars = [bar.reshape((-1, 3)) for bar in bars]
            bar = np.concatenate(bars, axis=0)
            mean_val, std_val = np.mean(bar, axis=0), np.std(bar, axis=0)
            mean_val, std_val = mean_val.reshape((1,1,3)), std_val.reshape((1,1,3))
            fg_u8 = np.logical_and(np.greater(image, mean_val-std_val), np.less(image, mean_val+std_val))
            fg_u8 = np.logical_not(np.all(fg_u8, axis=2)).astype(np.uint8)*255
        else:
            image = image[:,:,0]
    if fg_u8 is None:
        bars = [image[:,:margin],image[:,-margin:],image[:margin,:],image[-margin,:]]
        bars = [bar.reshape(-1) for bar in bars]
        bar = np.concatenate(bars, axis=0)
        mean_val, std_val = np.mean(bar), np.std(bar)
        fg_u8 = np.logical_and(np.greater(image, mean_val-std_val), np.less(image, mean_val+std_val))
        fg_u8 = np.logical_not(fg_u8).astype(np.uint8)*255
    contours, hierarchy = cv2.findContours(fg_u8, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    alpha_image = np.zeros(image.shape[:2], np.uint8)
    color_image = np.zeros(image.shape[:2]+(3,), np.uint8)
    cv2.drawContours(alpha_image, contours, -1, 255, thickness)
    cv2.drawContours(color_image, contours, -1, [int(val) for val in color], thickness)
    return np.concatenate([color_image, np.expand_dims(alpha_image, axis=2)], axis=2)


def test():
    img_path = '/home/fusen/图片/to家民/资源 1 4.png'
    image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    # image = cv2.imread(img_path, cv2.IMREAD_COLOR)
    # image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    cv2.imshow('image', image)
    # cv2.waitKey()
    hollowed_image = hollowing_logo(image)
    cv2.imshow('hollowed', hollowed_image)
    cv2.waitKey()


if '__main__' == __name__:
    test()