import cv2
import numpy
from pathlib import Path
from typing import Tuple

import numpy as np


def make_synthetic(bg_img: numpy.ndarray, fg_img: numpy.ndarray, coordinate: Tuple[int, int]) -> numpy.ndarray:
    """
    bg_imgにfg_imgをfg_imgの左上座標(x,y)で重ねて返す
    """
    x, y = coordinate
    fg_img_height, fg_img_width = fg_img.shape[0], fg_img.shape[1]
    bg_img_height, bg_img_width = bg_img.shape[0], bg_img.shape[1]

    y_plus_height, x_plus_width = -1, -1
    plus_height, plus_width = -1, -1

    # 右の座標を決める
    if bg_img_width >= x + fg_img_width:
        x_plus_width = x + fg_img_width
        plus_width = fg_img_width
    else:
        x_plus_width = bg_img_width
        plus_width = bg_img_width - x

    # 下の座標を決める
    if bg_img_height >= y + fg_img_height:
        y_plus_height = y + fg_img_height
        plus_height = bg_img_height
    else:
        y_plus_height = bg_img_height
        plus_height = bg_img_height - y

    # 前景画像の大きさを変更
    new_fg_img = fg_img[0: plus_height, 0: plus_width]

    # 背景画像を3チャネルに変更（透過合成ではマスク処理が必要となるため）
    bg_img = bg_img[:, :, :3]

    bg_img[y: y_plus_height, x: x_plus_width] = \
        bg_img[y: y_plus_height, x: x_plus_width] * (1 - new_fg_img[:, :, 3:] / 255) + \
        new_fg_img[:, :, :3] * (new_fg_img[:, :, 3:] / 255)

    # a = bg_img[y: y_plus_height, x: x_plus_width] * (1 - new_fg_img[:, :, 3:] / 255)
    # b = new_fg_img[:, :, :3] * (new_fg_img[:, :, 3:] / 255)
    # bg_img[y: y_plus_height, x: x_plus_width] = a + b

    return bg_img


def make_synthetic_by_image_path(bg_img_path: Path, fg_img_path: Path, coordinate: Tuple[int, int]) -> numpy.ndarray:
    """
    画像PATHと左上座標から画像を合成する
    """
    bg_img = cv2.imread(bg_img_path, cv2.IMREAD_UNCHANGED)
    fg_img = cv2.imread(fg_img_path, cv2.IMREAD_UNCHANGED)
    return make_synthetic(bg_img, fg_img, coordinate)
