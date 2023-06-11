import numpy as np
from scipy.spatial import distance
import cv2
from PIL import Image, ImageFont, ImageDraw
import pandas as pd

import torch.cuda
import easyocr


scale = 10
font_paths = {
    "Arial": "fonts/arial.ttf",
    "Comic Sans MS": "fonts/comic.ttf",
    "Courier New": "fonts/cour.ttf",
    "Malgun Gothic": "fonts/malgun.ttf",
    "Times New Roman": "fonts/times.ttf",
}
fonts = {
    k: ImageFont.truetype(v, 50)
    for k, v
    in font_paths.items()
}


def _normalize(array: np.ndarray, inplace: bool = False) -> np.ndarray:
    if not inplace:
        array = array.copy()
    cv2.normalize(array, array, 0, 255, cv2.NORM_MINMAX)
    thres, _ = cv2.threshold(array, -1, maxval=255, type=cv2.THRESH_OTSU)
    array[array > thres] = 255
    return array


def _trunc_white(array: np.ndarray) -> np.ndarray:
    row, col = array.shape
    row_start, row_end = 0, row-1
    col_start, col_end = 0, col-1

    while row_start < row:
        if array[row_start].min() != 255:
            break
        row_start += 1
    while row_end >= 0:
        if array[row_end].min() != 255:
            break
        row_end -= 1
    while col_start < col:
        if array[:, col_start].min() != 255:
            break
        col_start += 1
    while col_end >= 0:
        if array[:, col_end].min() != 255:
            break
        col_end -= 1

    array = array[row_start:row_end+1, col_start:col_end+1]
    return array


def _sixteen_padding(array: np.ndarray) -> np.ndarray:
    x = array.shape[1]
    y = array.shape[0]
    x_pad = (x // 16 + 1) * 16 - x
    y_pad = (y // 16 + 1) * 16 - y
    array = np.pad(array, ((y_pad//2, y_pad//2 + y_pad%2),(x_pad//2, x_pad//2 + x_pad%2)), 'constant', constant_values=255)
    return array


def _get_descriptor(array: np.ndarray) -> cv2.HOGDescriptor:
    win_size = array.shape[::-1]
    block_size = (16, 16)
    block_stride = (8, 8)
    cell_size = (8, 8)
    nbins = 9
    return cv2.HOGDescriptor(win_size, block_size, block_stride, cell_size, nbins)



def get_ocr_results(a4: cv2.Mat) -> list[tuple[list[list[float]], str, float]]:
    reader = easyocr.Reader(lang_list=['en'], gpu=torch.cuda.is_available())
    return reader.readtext(a4, width_ths=0.2)


def get_corresponding_fonts(a4: cv2.Mat, results: list[tuple[list[list[float]], str, float]]) -> list[str]:
    distance_dict: dict[str, list[np.ndarray]] = {k: [] for k in font_paths.keys()}

    for (bbox, text, prob) in results:
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))

        image_text = _normalize(a4[tl[1]:bl[1], tl[0]:tr[0]], inplace=False)
        image_text = _trunc_white(image_text)
        image_text = _sixteen_padding(image_text)

        descriptor = _get_descriptor(image_text)
        image_hog: np.ndarray = descriptor.compute(image_text)

        for font_name, font in fonts.items():
            # canvas = Image.new('L', size=(tr[0]-tl[0], bl[1]-tl[1]), color='white')
            canvas = Image.new('L', size=(3000, 80), color='white')
            draw = ImageDraw.Draw(canvas)
            draw.text((0, 0), text, 'black', font=font)
            rendered_text = np.array(canvas)
            rendered_text = _trunc_white(rendered_text)
            rendered_text = _sixteen_padding(rendered_text)
            rendered_text = cv2.resize(rendered_text, image_text.shape[::-1], interpolation=cv2.INTER_CUBIC)

            text_hog: np.ndarray = descriptor.compute(rendered_text)
            dist = distance.euclidean(image_hog, text_hog)  # Euclidean
            # dist = distance.cityblock(image_hog, text_hog)  # 1-norm
            # dist = distance.chebyshev(image_hog, text_hog)  # inf-norm  # Danger!
            distance_dict[font_name].append(dist)

    distance_table = pd.DataFrame(distance_dict)
    most_close_fonts = distance_table.idxmin(axis='columns')
    return most_close_fonts.to_list()
