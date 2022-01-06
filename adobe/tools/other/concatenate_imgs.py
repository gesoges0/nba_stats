from typing import List
from pathlib import Path
from PIL import Image
import cv2


def concatenate_images_with_PIL(paths: List[Path], output_file_path: Path, stride=0) -> None:
    """
    基本的にはコッチでOK、透歌画像を処理することができない
    """
    one_image = Image.open(paths[0])
    result_image = Image.new('RGB', (one_image.width * len(paths), one_image.height))
    _x = 0
    for path in paths:
        image = Image.open(path)
        result_image.paste(image, (_x, 0))
        _x += image.width
    result_image.save(output_file_path)


def concatenate_images_with_cv2(paths: List[Path], outupt_file_path: Path, mode: str = 'h', stride=0) -> None:
    """
    CV2.IMREAD_UNCHANGEDを使い, 透過画像もそのまま読み込める
    """
    result_image = None
    for path in paths:
        path = str(path)
        if result_image is None:
            result_image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        else:
            another_image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if mode == 'h':
                result_image = cv2.hconcat([result_image, another_image])
            if mode == 'v':
                result_image = cv2.vconcat([result_image, another_image])
    outupt_file_path = str(outupt_file_path)
    cv2.imwrite(outupt_file_path, result_image)
