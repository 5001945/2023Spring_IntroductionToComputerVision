import numpy as np
import cv2


def _get_white_area(img: cv2.Mat, thresh: int = 200) -> cv2.Mat:
    """R, G, B 값이 모두 thresh 이상인 픽셀을 1로 mask한다. Threshold method는 Otsu이다.

    Args:
        img (cv2.Mat): RGB image.
        thresh (int, optional): 기준 threshold. Defaults to 200.

    Returns:
        cv2.Mat: 0 또는 255 값을 갖는 bitmask.
    """
    # img는 RGB 순서로 가정. 사실 BGR이어도 큰 문제는 없다.
    _, r_thres = cv2.threshold(img[..., 0], thresh, maxval=255, type=cv2.THRESH_OTSU)
    _, g_thres = cv2.threshold(img[..., 1], thresh, maxval=255, type=cv2.THRESH_OTSU)
    _, b_thres = cv2.threshold(img[..., 2], thresh, maxval=255, type=cv2.THRESH_OTSU)
    return r_thres & g_thres & b_thres


def _sort_order(points: np.ndarray) -> np.ndarray:
    """좌상, 우상, 우하, 좌하 순서로 재정렬한다."""
    points = points[:, 0, :].astype(np.float32)
    med = np.median(points, axis=0)
    reordered = np.zeros_like(points, dtype=np.float32)
    for point in points:
        if (point[0] < med[0]) and (point[1] < med[0]):  # Top Left
            reordered[0, :] = point[:]
        if (point[0] >= med[0]) and (point[1] < med[0]):  # Top Right
            reordered[1, :] = point[:]
        if (point[0] >= med[0]) and (point[1] >= med[0]):  # Bottom Right
            reordered[2, :] = point[:]
        if (point[0] < med[0]) and (point[1] >= med[0]):  # Bottom Left
            reordered[3, :] = point[:]
    return reordered


def get_quadrilateral(img: cv2.Mat) -> np.ndarray:
    """사진에서 A4 영역의 위치를 찾는다.

    Parameters
    ----------
    img : cv2.Mat
        RGB image.

    Returns
    -------
    np.ndarray
        사각형의 x, y 좌표. shape는 (4, 2).
    """
    # R, G, B 값이 모두 200 이상인 점들만 흰색으로 표시한다.
    img_thres = _get_white_area(img)

    # 잔noise들을 없애기 위해 open 및 close를 해 준다.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    cv2.morphologyEx(img_thres, cv2.MORPH_OPEN, kernel, img_thres)
    cv2.morphologyEx(img_thres, cv2.MORPH_CLOSE, kernel, img_thres)

    # threshold image에서 일정 넓이 이상을 가진 사각형 contour를 찾는다.
    h, w, *_ = img.shape
    area_thres = h * w // 4

    approx = None
    contours, _ = cv2.findContours(img_thres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > area_thres:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, closed=True), closed=True)  # 다각형 폐곡선 찾기
            if len(approx) == 4:
                break  # 사각형을 뽑으면 stop
    if approx is None:
        raise ValueError("Cannot detect the paper.")
    
    return _sort_order(approx)


def get_a4(img: cv2.Mat, quadrilateral: np.ndarray, scale: float = 10) -> cv2.Mat:
    """사진에서 A4 영역을 뽑고 2970*2100 size로 변환한다.

    Parameters
    ----------
    img : cv2.Mat
        RGB image.
    quadrilateral : np.ndarray
        _description_
    scale : float, optional
        _description_, by default 10

    Returns
    -------
    cv2.Mat
        _description_
    """
    width = round(210 * scale)
    height = round(297 * scale)
    src_points = quadrilateral
    dst_points = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)

    H = cv2.getPerspectiveTransform(src_points, dst_points)
    a4 = cv2.warpPerspective(img, H, (width, height))
    a4_y = cv2.cvtColor(a4, cv2.COLOR_BGR2YCrCb)[..., 0]
    a4_blur = cv2.medianBlur(a4_y, 3)
    return cv2.addWeighted(a4_y, 2, a4_blur, -1, 0)
