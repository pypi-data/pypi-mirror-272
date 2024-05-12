import numpy as np
import cv2
import string
from skimage.filters import threshold_otsu
from skimage.morphology import skeletonize
from skimage import morphology, measure
from skimage.morphology import medial_axis

def is_bool(param):
    return param.dtype == np.bool_

def bool2mask(matrix):
    """
    Convert Boolean matrix to 8-bit unsigned integer mask image
    """
    if is_bool(matrix):
        result_int = matrix.astype(int)
        _mask = result_int * 255
        return _mask.astype(np.uint8)
    else:
        raise ValueError("Input matrix must be of bool dtype.")

def medial_axis_mask(image):
    """
    The input must be a binary graph to obtain the axis image within it
    """
    result = medial_axis(image)
    return bool2mask(result)

def BinaryImg(image, min_value=127, max_value=255):
    """
    Convert image to binary image
    :param image: Original image. --- (BGR format)
    :param min_value: Minimum threshold, default to 127
    :param max_value: Maximum threshold, default to 225
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, min_value, max_value, cv2.THRESH_BINARY)
    return binary_image

def count_nonzero(thresh):
    """计算矩阵非0值"""
    nonzero_pixels = np.count_nonzero(thresh)
    return nonzero_pixels

def putBoxText(background_image, bbox, text, mode=1, rect=False, bboxcolor=(0, 255, 0), textcolor=(0, 0, 255),
               fontsize=1, thickness=2, bboxthickness=2,font=cv2.FONT_HERSHEY_SIMPLEX):
    """
    在给定的背景图像上绘制一个框，并在框的中心位置添加文本。获取文本的text_size，使文本居中。

    :param background_image: 背景图像，要在其上绘制框和文本的图像
    :param bbox: 框的边界框，表示为 [x1, y1, x2, y2]
    :param text: 要添加到框中心的文本
    :param mode: 模式0 表示框的中心位置，1 表示框的左上角
    :param rect: 是否绘制角标记框，导入的为 cornerRect 函数
    :param bboxcolor: 框的颜色，以 BGR 格式表示，例如 (0, 255, 0) 表示绿色
    :param textcolor: 文本的颜色，以 BGR 格式表示，例如 (0, 0, 255) 表示红色
    :param fontsize: 文本的字体大小
    :param thickness: 文本的线宽
    :param bboxthickness: 框的线宽，默认为 2
    :return: 绘制了框和文本的图像
    """
    text_x = text_y = None
    x1, y1, x2, y2 = bbox
    text_size, _ = cv2.getTextSize(text, font, fontsize, thickness)
    if rect:
        pass
    else:
        cv2.rectangle(background_image, (x1, y1), (x2, y2), bboxcolor, bboxthickness)
    if mode == 0:
        text_x = int((x1 + x2) / 2 - text_size[0] / 2)
        text_y = int((y1 + y2) / 2 + text_size[1] / 2)
    elif mode == 1:
        text_x = int(x1)
        text_y = int(y1 - text_size[1])
    cv2.putText(background_image, text, (text_x, text_y), font, fontsize, textcolor, thickness)

def SearchOutline(binary_image):
    """
    在给定图像中搜索轮廓并返回轮廓的坐标列表。
    :param binary_image: 要搜索轮廓的图像。
    :return: 包含轮廓坐标的列表，每个坐标表示裂缝的一个点，坐标格式为 [(x, y),...]。
    """
    contours = measure.find_contours(binary_image, level=128, fully_connected='low', positive_orientation='low')
    contours_xy = [np.fliplr(np.vstack(contour)).astype(np.int32) for contour in contours]
    return contours_xy

def is_gray_image(image):
    return (len(image.shape) == 2) or (len(image.shape) == 3 and image.shape[-1] == 1)

def drawOutline(blackbackground, contours, color=(255, 0, 255)):
    cv2.drawContours(blackbackground, contours, -1, color, thickness=1)


def SkeletonMap(target):
    """
    获取骨架图的信息
    :param target: 目标图
    :return: 骨架图与一个数组，其中每一行表示一个非零元素的索引(y,x)，包括行索引和列索引
    """
    if target.ndim == 2 or target.shape[2] == 1:
        gray = target
    else:
        gray = cv2.cvtColor(target, cv2.COLOR_RGB2GRAY)
    thresh = threshold_otsu(target)
    binary = gray > thresh
    skimage = skeletonize(binary)
    skepoints = np.argwhere(skimage)
    skimage = skimage.astype(np.uint8)
    return skimage, skepoints


def incircle(img, contours_arr, color=(0, 0, 255)):
    """
    轮廓最大内切圆算法,所有轮廓当中的内切圆
    :param img: 单通道图像
    :param contours_arr: ndarry的轮廓, 建议使用cv2.findContours,
                        contours_arr, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                        pyzjr也有SearchOutline可用,但要转换成ndarry的格式
    :example:
        contour = [np.array([point], dtype=np.int32) for point in contours]
        # 平铺的方法
        flatten_contours = np.concatenate([cnt.flatten() for cnt in contours_arr])
        flatten_contours = flatten_contours.reshape(-1, 2)
    :param color: 绘制内切圆颜色
    :return: 绘制在原图的内切圆,内切圆直径,绘制出的图像与轮廓直接差距一个像素，是因为cv2.circle的半径参数必须为int类型
    """
    if is_gray_image:
        result = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    raw_dist = np.zeros(img.shape, dtype=np.float32)
    letters = list(string.ascii_uppercase)
    label = {}
    k = 0
    for contours in contours_arr:
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                raw_dist[i, j] = cv2.pointPolygonTest(contours, (j, i), True)
        min_val, max_val, _, max_dist_pt = cv2.minMaxLoc(raw_dist)
        if max_val > .5:
            label[letters[k]] = max_val * 2
            k += 1
        cv2.circle(result, max_dist_pt, int(max_val), color, 1, 1, 0)

    return result, label


def outcircle(img, contours_arr, color=(0, 255, 0)):
    """
    轮廓外切圆算法,画出所有轮廓的外切圆
    :param img: 单通道图像
    :param contours_arr: ndarry的轮廓, 建议使用cv2.findContours,
                        contours_arr, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                        pyzjr也有SearchOutline可用,但要转换成ndarry的格式
    :example:
        contour = [np.array([point], dtype=np.int32) for point in contours]
    :param color: 绘制外切圆颜色
    :return:
    """
    radii = []
    result = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    for k, cnt in enumerate(contours_arr):
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        radii.append([(x,y),radius])
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(result, center, radius, color, 1)
        cv2.circle(result, center, 1, color, 1)

    return result, radii

def foreground_contour_length(binary_img, minArea=30):
    """
    计算前景的轮廓长度, 返回两个值, 每个轮廓的长度和总长度
    :param binary_img: 二值图
    :param minArea: 最小过滤面积
    """
    contours_xy = SearchOutline(binary_img)
    contour_lengths = []
    for contour in contours_xy:
        area = cv2.contourArea(contour)
        if area > minArea:
            length = cv2.arcLength(contour, False)
            contour_lengths.append(length)
    all_length = np.sum(contour_lengths)
    return contour_lengths, all_length


def each_crack_areas(mask, thresh, merge_threshold=3, area_threshold=50):
    """每条裂缝的面积,并用大写字母来进行标记"""
    connected_image = morphology.closing(thresh, morphology.disk(merge_threshold))
    labeled_image = measure.label(connected_image, connectivity=2)
    region_props = measure.regionprops(labeled_image)
    area = {}
    Bboxing = []
    crack_label = ord('A')
    for region in region_props:
        area_value = region.area
        if area_value >= area_threshold:
            minr, minc, maxr, maxc = region.bbox
            Bboxing.append([(minc, minr), (maxc, maxr)])
            putBoxText(mask, [minc, minr, maxc, maxr], chr(crack_label), mode=0, fontsize=.5)
            if crack_label <= ord('Z'):
                area[chr(crack_label)] = area_value
                crack_label += 1
    return area, Bboxing, mask

if __name__=="__main__":
    from pyzjr.augmentation.mask_ops import BinaryImg
    from pyzjr.measure.crack.skeleton_extraction import skeletoncv
    path = r'/models_img/1604.png'
    cv_image = cv2.imread(path)
    image = skeletoncv(path)
    # image = BinaryImg(cv_image)
    contour_lengths, all_length = foreground_contour_length(image)

    print(all_length)
    for i, length in enumerate(contour_lengths):
        print(f"Contour {i} length: {length}")