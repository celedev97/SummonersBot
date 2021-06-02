import os
import time

import images
import uiautomator2
import cv2
import numpy as np
from typing import Union, List, Optional, Tuple

def click(device: uiautomator2.Device, point: Tuple[int, int], post_sleep=0.2):
    while not summonerGreedOn(device):
        time.sleep(1)

    device.click(point[0], point[1])
    time.sleep(post_sleep)


def template_match(image, template, offset=None) -> Optional[Tuple[int, int]]:
    if offset is None:
        offset = [0, 0]
    if image is None or template is None:
        return None

    if True:
        cv2.imwrite("../tm_image.png", image)
        cv2.imwrite("../tm_templ.png", template)

    # preparing template
    template_height, template_width, _ = template.shape[::]

    # template matching
    res = cv2.matchTemplate(image, template, cv2.TM_SQDIFF_NORMED)
    amin = np.amin(res)
    if amin < 0.1:
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        return minLoc[0]+offset[0], minLoc[1]+offset[1]

    return None


def screenshot(device, filename=None):
    while not summonerGreedOn(device):
        time.sleep(1)

    image = device.screenshot(format='opencv')
    if filename is not None:
        cv2.imwrite(f"{filename}.png", image)
    return image


def percentage_crop(image, start_x, end_x, start_y, end_y, show = False):
    # getting image size
    height, width, _ = image.shape

    # calculating crop points in pixels
    start_x = start_x * width // 100
    end_x = end_x * width // 100
    start_y = start_y * height // 100
    end_y = end_y * height // 100

    # numpy slicing the array to crop the image
    cut = image[start_y:end_y, start_x:end_x]

    if show:
        cv2.imshow("TEMP", cut)
        cv2.waitKey(0)

    return cut, (start_x, start_y)


def show(image):
    height, width, _ = image.shape[::]
    imS = cv2.resize(image, ((int)(width / 3), (int)(height / 3)))
    cv2.imshow("last", imS)


def summonerGreedOn(device):
    return device.app_current()['package'] == "com.pixio.google.mtd"



from .match_images import *
