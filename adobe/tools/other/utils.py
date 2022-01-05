import cv2
from pathlib import Path
import numpy as np


def write_img(path: Path, img: np.ndarray) -> None:
    """
    cv2.read()などで読み込んだimgをpathに保存する 
    """
    cv2.imwrite(path, img)
