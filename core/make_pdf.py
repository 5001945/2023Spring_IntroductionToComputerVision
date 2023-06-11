import os
from datetime import datetime

import numpy as np
from scipy.spatial import distance
from PIL import ImageFont

from fpdf import FPDF

scale = 10
font_sizes = [8, 11, 15]
font_paths = {
    "Arial": "fonts/arial.ttf",
    "Comic Sans MS": "fonts/comic.ttf",
    "Courier New": "fonts/cour.ttf",
    "Malgun Gothic": "fonts/malgun.ttf",
    "Times New Roman": "fonts/times.ttf",
}
fonts = {
    font_name: {font_size: ImageFont.truetype(font_path, font_size) for font_size in font_sizes}
    for font_name, font_path
    in font_paths.items()
}


def _make_cell_with_box(pdf: FPDF, tl: tuple[float, float], br: tuple[float, float], font_name: str, text: str):
    """Make a new cell in pdf.

    Parameters
    ----------
    pdf : FPDF
        FPDF object
    tl : tuple[int, int]
        Coordinate of top-left corner (x, y)
    br : tuple[int, int]
        Coordinate of bottom-right corner (x, y)
    font : str
        Font of the cell.
    text : str
        Text of the cell.
    """
    pdf.set_xy(*tl)
    w, h = br[0] - tl[0], br[1] - tl[1]  # 단위: mm

    d = {}
    for point, font in fonts[font_name].items():
        bbox = font.getbbox(text)  # 단위: px
        rendered_w = (bbox[2] - bbox[0]) * 0.34  # px -> mm. 실제로는 0.352778이라는데 재 보니 0.34에 가깝다.
        rendered_h = (bbox[3] - bbox[1]) * 0.34
        if rendered_w > w * 1.05:
            continue
        d[point] = distance.euclidean([w, h], [rendered_w, rendered_h])
    size = min(d, key=d.get)
    pdf.set_font(font_name, size=size)
    pdf.cell(w, h, text, align='L')


def get_pdf(results: list[tuple[list[list[float]], str, float]], each_fonts: list[str]) -> str:
    pdf = FPDF(unit='mm')
    for font_name, font_path in font_paths.items():
        pdf.add_font(font_name, fname=font_path)
    pdf.add_page(format='A4')

    for (bbox, text, prob), font in zip(results, each_fonts):
        (tl, tr, br, bl) = bbox
        tl = (tl[0] / scale, tl[1] / scale)
        br = (br[0] / scale, br[1] / scale)
        _make_cell_with_box(pdf, tl, br, font_name=font, text=text)

    if not os.path.exists('__temp__'):
        os.mkdir('__temp__')
    current_time = datetime.now().isoformat().replace(':', '-')
    temp_filename = f"__temp__/__TempPDF__{current_time}.pdf"
    pdf.output(temp_filename)
    return temp_filename


if __name__ == '__main__':
    get_pdf()
