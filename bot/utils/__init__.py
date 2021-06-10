

import numpy
import cv2
import numpy as np
from typing import Optional, Tuple


def template_match(image, template, offset=None) -> Optional[Tuple[int, int]]:
    if offset is None:
        offset = [0, 0]
    if image is None or template is None:
        return None

    # preparing template
    template_height, template_width, _ = template.shape[::]

    # template matching
    res = cv2.matchTemplate(image, template, cv2.TM_SQDIFF_NORMED)
    amin = np.amin(res)
    if amin < 0.1:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        return min_loc[0] + offset[0], min_loc[1] + offset[1]

    return None


def percentage_crop(image, start_x, end_x, start_y, end_y) -> Tuple[numpy.ndarray, Tuple[int, int]]:
    # getting image size
    height, width, _ = image.shape

    # calculating crop points in pixels
    start_x = start_x * width // 100
    end_x = end_x * width // 100
    start_y = start_y * height // 100
    end_y = end_y * height // 100

    # numpy slicing the array to crop the image
    cut = image[start_y:end_y, start_x:end_x]

    return cut, (start_x, start_y)


def show(image):
    height, width, _ = image.shape[::]
    scaled = cv2.resize(image, (width // 3, height // 3))
    cv2.imshow("last", scaled)
    cv2.waitKey(0)


def summoner_greed_on(device):
    return device.app_current()['package'] == "com.pixio.google.mtd"

