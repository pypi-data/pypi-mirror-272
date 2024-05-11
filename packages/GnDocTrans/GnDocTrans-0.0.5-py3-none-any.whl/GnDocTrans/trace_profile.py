__all__ = [
    'gen_profile',
    'alignSize'
]


import cv2
import numpy as np
from numpy import ndarray
from typing import Iterable, Literal


def trace_profile(
    image: ndarray,
    color: Iterable = [0,0,255],
    thickness: int = -20,
    *,
    make_border: bool = True,
    ksize: int = None,
    margin: int = 5,
) -> ndarray:
    fg_u8 = None
    if image.ndim == 3:
        if image.shape[-1] == 4 and np.less(image[:,:,-1],128).any():
            fg_u8 = np.greater(image[:,:,-1], 127).astype(np.uint8)*255
        elif 3 <= image.shape[-1]:
            image = image[:,:,:3]
            bars = [image[:,:margin],image[:,-margin:],image[:margin,:],image[-margin,:]]
            bars = [bar.reshape((-1, 3)) for bar in bars]
            bar = np.concatenate(bars, axis=0)
            mean_val, std_val = np.mean(bar, axis=0), np.std(bar, axis=0)
            mean_val, std_val = mean_val.reshape((1,1,3)), std_val.reshape((1,1,3))
            fg_u8 = np.logical_and(np.greater_equal(image, mean_val-std_val), np.less_equal(image, mean_val+std_val))
            fg_u8 = np.logical_not(np.all(fg_u8, axis=2)).astype(np.uint8)*255
        else:
            image = image[:,:,0]
    if fg_u8 is None:
        bars = [image[:,:margin],image[:,-margin:],image[:margin,:],image[-margin,:]]
        bars = [bar.reshape(-1) for bar in bars]
        bar = np.concatenate(bars, axis=0)
        mean_val, std_val = np.mean(bar), np.std(bar)
        fg_u8 = np.logical_and(np.greater_equal(image, mean_val-std_val), np.less_equal(image, mean_val+std_val))
        fg_u8 = np.logical_not(fg_u8).astype(np.uint8)*255
    if ksize:
        closing_ksize = abs(ksize)
    else:
        closing_ksize = int((np.mean(fg_u8.shape) + np.sqrt(fg_u8.shape[0]*fg_u8.shape[1])) / 2 / 30)
    closing_ksize += 0 if closing_ksize % 2 else 1
    closing_element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (closing_ksize, closing_ksize))
    if make_border and thickness < 0:
        fg_u8 = cv2.copyMakeBorder(fg_u8, abs(thickness), abs(thickness), abs(thickness), abs(thickness), cv2.BORDER_CONSTANT, 0)
    dilated = cv2.dilate(fg_u8, closing_element)
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    redrawed = np.zeros(dilated.shape, np.uint8)
    cv2.drawContours(redrawed, contours, -1, 255, -1)
    eroded = cv2.erode(redrawed, closing_element)
    # cv2.imshow('show', eroded)
    # cv2.waitKey()
    if 0 != thickness:
        contours, hierarchy = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        redrawed = np.zeros(eroded.shape, np.uint8)
        cv2.drawContours(redrawed, contours, -1, 255, abs(thickness))
        # cv2.imshow('show', redrawed)
        # cv2.waitKey()
        profile = cv2.bitwise_and(eroded, redrawed)
        # cv2.imshow('show', profile)
        # cv2.waitKey()
        if thickness < 0:
            profile = cv2.bitwise_xor(profile, redrawed)
        # cv2.imshow('show', profile)
        # cv2.waitKey()
    else:
        profile = eroded
        
    return np.concatenate([np.full(profile.shape+(3,), color, np.uint8), np.expand_dims(profile, axis=2)], axis=2)


def gen_profile(white_image, thickness, color):
    white_image = cv2.copyMakeBorder(white_image, thickness, thickness, thickness, thickness, cv2.BORDER_CONSTANT, 0)
    profile_image = trace_profile(white_image, color, -thickness, make_border=False)
    filled_image = trace_profile(white_image, color, 0, make_border=False)
    # np.expand_dims(cv2.bitwise_or(profile_image[:,:,3], filled_image[:,:,3]), axis=2)
    filled_image = np.concatenate([profile_image[:,:,:3], np.expand_dims(cv2.bitwise_or(profile_image[:,:,3], filled_image[:,:,3]), axis=2)], axis=2)
    filled_image = cv2.add(cv2.bitwise_and(white_image, white_image, mask=white_image[:,:,3]),
                           cv2.bitwise_and(filled_image, filled_image, mask=cv2.bitwise_not(white_image[:,:,3])))
    profile_image = trace_profile(filled_image, color, thickness, make_border=False)
    return filled_image, profile_image


def unionRect(xywhs: ndarray, to_xyxy: bool = False) -> ndarray:
    xywhs[:,2] += xywhs[:,0]
    xywhs[:,3] += xywhs[:,1]
    xyxy = np.concatenate([np.min(xywhs[:,:2], axis=0), np.max(xywhs[:,2:4], axis=0)], axis=0)
    if to_xyxy:
        return xyxy
    xyxy[2] -= xyxy[0]
    xyxy[3] -= xyxy[1]
    return xyxy


def alignSize(*image_tuple: ndarray, remove_blank: bool = True,
              align_base: Literal['width', 'height', 'area', 'long', 'short'] = 'long',
              align_toward: Literal['min', 'max', 'middle', 'mean'] = 'min', ) -> list[ndarray]:
    if remove_blank:
        image_list: list[ndarray] = []
        for image in image_tuple:
            alpha_channel = image[:,:,-1]
            retval, labels, stats, centroids = cv2.connectedComponentsWithStats(cv2.reduce(alpha_channel, dim=0, rtype=cv2.REDUCE_MAX))
            stats = stats[1:,:4] if retval > 1 else stats[:,:4]
            x1, _, x2, _ = unionRect(stats, to_xyxy=True)
            retval, labels, stats, centroids = cv2.connectedComponentsWithStats(cv2.reduce(alpha_channel, dim=1, rtype=cv2.REDUCE_MAX))
            stats = stats[1:,:4] if retval > 1 else stats[:,:4]
            _, y1, _, y2 = unionRect(stats, to_xyxy=True)
            image_list.append(image[y1:y2,x1:x2])
    else:
        image_list = list(image_tuple)
    shape2_list: list[list] = []
    for image in image_list:
        shape2_list.append(list(image.shape[:2]))
    shape2_arr = np.array(shape2_list)
    if np.sum(np.greater(shape2_arr[:,0], shape2_arr[:,1])) > np.sum(np.greater(shape2_arr[:,1], shape2_arr[:,0])):
        long_id, short_id = 0, 1
    else:
        long_id, short_id = 1, 0
    base_arr = np.concatenate([shape2_arr, np.prod(shape2_arr, axis=1).reshape((-1, 1))], axis=1)
    base2index = {
        'width': 1, 'height': 0, 'area': 2, 'long': long_id, 'short': short_id
    }
    size_arr = base_arr[:,base2index[align_base]]
    toward2func = {
        'min': np.min, 'max': np.max, 'middle': np.median, 'mean': np.mean
    }
    base_size = toward2func[align_toward](size_arr)
    factor_arr = base_size/size_arr
    factor_list = factor_arr.tolist()
    return [cv2.resize(image, None, fx=factor, fy=factor) for image, factor in zip(image_list,factor_list)]


def test():
    img_path = '/home/fusen/图片/20240424-165151.png'
    image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    # image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # image = cv2.imread(img_path, cv2.IMREAD_COLOR)
    # cv2.imshow('image', image)
    # cv2.waitKey(10)
    # profile = trace_profile(image)
    # cv2.imwrite('result.png', profile)
    # im_show = cv2.vconcat(cv2.cvtColor(image,cv2.COLOR_GRAY2BGRA), profile)
    # cv2.namedWindow('show', cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('show', im_show)
    # cv2.waitKey()
    filled, profile = gen_profile(image, 20, [255, 23, 186])
    print(filled.shape)
    print(profile.shape)
    cv2.imwrite('fill.png', filled)
    cv2.imwrite('prof.png', profile)


def test2():
    img1 = np.zeros((500, 500), np.uint8)
    cv2.circle(img1, (200,200), 150, 255, -1)
    img1 = np.stack([img1]*4, axis=2)
    cv2.imshow('img1', img1)
    # cv2.waitKey()
    img2 = np.zeros((500, 500), np.uint8)
    cv2.rectangle(img2, (200,200), (400,450), 255, -1)
    img2 = np.stack([img2]*4, axis=2)
    cv2.imshow('img2', img2)
    # cv2.waitKey()
    img3 = np.zeros((500, 500), np.uint8)
    cv2.rectangle(img3, (100,50), (200,450), 255, -1)
    img3 = np.stack([img3]*4, axis=2)
    cv2.imshow('img3', img3)
    # cv2.waitKey()
    
    image_list = alignSize(img1, img2, img3, remove_blank=True, align_base='long', align_toward='middle')
    for index, image in enumerate(image_list, start=1):
        cv2.imshow(f're{index}', image)
        print(image.shape[:2])
    cv2.waitKey()


if '__main__' == __name__:
    test()
    # test2()