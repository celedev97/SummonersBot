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


def template_match(device, image, template) -> Optional[Tuple[int, int]]:
    if image is None or template is None:
        return None

    while not summonerGreedOn(device):
        time.sleep(1)

    # preparing template
    template_height, template_width, _ = template.shape[::]

    # template matching
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    amax = np.amax(res)
    if amax > 0.9:
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        return max_loc[0], max_loc[1]

    return None


def screenshot(device):
    while not summonerGreedOn(device):
        time.sleep(1)

    image = device.screenshot(format='opencv')
    # cv2.imwrite("last.png", image)
    return image


def show(image):
    height, width, _ = image.shape[::]
    imS = cv2.resize(image, ((int)(width / 3), (int)(height / 3)))
    cv2.imshow("last", imS)


def summonerGreedOn(device):
    return device.app_current()['package'] == "com.pixio.google.mtd"
