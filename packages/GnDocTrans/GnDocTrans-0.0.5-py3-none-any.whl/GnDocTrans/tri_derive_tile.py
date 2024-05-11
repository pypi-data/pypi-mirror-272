__all__ = [
    'tileWithTri'
]


import cv2
import numpy as np
from numpy import ndarray
import base64
from typing import Literal
import math
import copy
import random
import time


def dictToSVG(element_name: str, properties: dict) -> str:

    internal_contents = ''
    internal_elements: list[str] = []
    header_string = element_name.strip('0123456789') + ' '
    for key, value in properties.items():
        if key is None:
            if isinstance(value, (bool, int, float, str)):
                internal_contents = str(value) + '\n'
            elif isinstance(value, (set, list, tuple)):
                internal_contents = ' '.join(
                    [str(val) for val in value]) + '\n'
            elif isinstance(value, np.ndarray):
                internal_contents = ' '.join(
                    [str(val) for val in value.reshape(-1)]) + '\n'
            elif isinstance(value, dict):
                internal_contents = ' '.join(
                    ['{}:{};'.format(k, v) for k, v in value.items()]) + '\n'
            continue

        if isinstance(value, dict):
            internal_elements.append(dictToSVG(key, value))
            continue

        if isinstance(value, (bool, int, float, str)):
            value_string = str(value)
        elif isinstance(value, (set, list, tuple)):
            value_string = ' '.join([str(val) for val in value])
        elif isinstance(value, np.ndarray):
            value_string = ' '.join([str(val) for val in value.reshape(-1)])
        else:
            value_string = ''
        header_string += str(key) + '="' + value_string + '" '

    if len(internal_contents) or len(internal_elements):
        head_string = '<' + header_string.rstrip() + '>\n'
        body_string = internal_contents + ''.join(internal_elements)
        foot_string = '</' + element_name.strip('0123456789') + '>\n'
    else:
        head_string = '<' + header_string.rstrip() + '/>\n'
        body_string = ''
        foot_string = ''
    return head_string + body_string + foot_string


def calcBoxes_old(
    cell_w: int, cell_h: int, on_left: bool,
    struct: Literal['2','7','lambda']
) -> dict[str, list[list]]:
    if on_left:
        sector_to_shift: list[list] = [
            [0.5, -1],
            [1, 0],
            [0.5, 1],
            [0, 2]
        ]
        struct_to_shift: dict[str, list] = {
            '2': [3, 1, 0],
            '7': [0, -1, 0],
            'lambda': [2, 1, 0],
        }
    else:
        sector_to_shift: list[list] = [
            [-0.5, -1],
            [-1, 0],
            [-0.5, 1],
            [0, 2]
        ]
        struct_to_shift: dict[str, list] = {
            '2': [3, -1, 0],
            '7': [0, 1, 0],
            'lambda': [2, -1, 0],
        }
    boxes_of_islet: list[list] = []
    boxes_of_islet.append([0, 0, cell_w, cell_h])
    boxes_of_sector: list[list] = []
    for sec2shif in sector_to_shift:
        box: list = [cell_w*sec2shif[0], cell_h*sec2shif[1], cell_w, cell_h]
        boxes_of_sector.append(box)
    stru2shif = struct_to_shift[struct]
    ref_box = boxes_of_sector[stru2shif[0]]
    boxes_of_sector.append([
        ref_box[0]+stru2shif[1]*cell_w,
        ref_box[1]+stru2shif[2]*cell_h,
        cell_w,
        cell_h
    ])
    return {
        'islet': boxes_of_islet,
        'sector': boxes_of_sector,
    }


def calcBoxes(
    cell_w: int, cell_h: int, on_left: bool,
    struct: Literal['2-1', '2-2', 'h-1', 'h-2', 'y-1', 'y-2', '7-1', '7-2'],
) -> dict[str, list[list]]:
    boxes_of_islet: list[list] = []
    boxes_of_islet.append([0, 0, cell_w, cell_h])
    sector_struct = {
        '2-1': [
            [-0.5,-1], [-1,0], [-0.5,1], [0,2], [-1,2]
        ],
        '2-2': [
            [0.5,-1], [-0.5,-1], [-1,0], [-0.5,1], [0,2], [-1,2]
        ],
        'h-1': [
            [-1,-2], [-0.5,-1], [-1,0], [-0.5,1], [-1,2], [0,2]
        ],
        'h-2': [
            [-1,-2], [-0.5,-1], [-1,0], [-0.5,1], [-1,2], [0,2], [-0.5,3]
        ],
        'y-1': [
            [-2,0], [-1,0], [-0.5,-1], [0.5,-1], [-0.5,1], [0,2]
        ],
        'y-2': [
            [-2,0], [-1,0], [-0.5,1], [0,2], [-0.5,-1], [0.5,-1], [1,2]
        ],
        '7-1': [
            [0.5,-1], [-0.5,-1], [-1,0], [-0.5,1], [0,2]
        ],
        '7-2': [
            [0.5,-1], [-0.5,-1], [-1,0], [-0.5,1], [0,2], [0.5,3]
        ]
    }
    struct_to_shift: list[list] = sector_struct[struct]
    if on_left:
        for sec2shif in struct_to_shift:
            sec2shif[0] = -sec2shif[0]
            # sec2shif[1] = -sec2shif[1]
    boxes_of_sector: list[list] = []
    for sec2shif in struct_to_shift:
        box: list = [cell_w*sec2shif[0], cell_h*sec2shif[1], cell_w, cell_h]
        boxes_of_sector.append(box)
    return {
        'islet': boxes_of_islet,
        'sector': boxes_of_sector,
    }


def randBoxes(cell_w: int, cell_h: int, rows: int, cols: int, probability: float, exist_boxes: dict[str, list[list]]) -> dict[str, list[list]]:
    random.seed(time.time())
    # random.seed(1)
    probability = 0 if probability < 0 else probability
    probability = 1 if probability > 1 else probability
    half_cell_w = cell_w / 2
    boxes_of_random: list[list] = []
    flags_dict: dict[str, list[bool]] = {
        'islet': [False]*len(exist_boxes['islet'])
    }
    for row in range(rows):
        col_shift = half_cell_w if row%2 else 0
        for col in range(cols+(row%2)):
            if random.random() <= probability:
                tl_x = col*cell_w - col_shift
                tl_y = row*cell_h
                center_x = tl_x + cell_w / 2
                center_y = tl_y + cell_h / 2
                is_in_box: bool = False
                for name, flag_list in flags_dict.items():
                    for index, flag in enumerate(flag_list):
                        if flag:
                            continue
                        is_in_box = (exist_boxes[name][index][0] < center_x and center_x < exist_boxes[name][index][0]+exist_boxes[name][index][2]) and \
                            (exist_boxes[name][index][1] < center_y and center_y < exist_boxes[name][index][1]+exist_boxes[name][index][3])
                        if is_in_box:
                            break
                    if is_in_box:
                        break
                if is_in_box:
                    print(f'It has hit the existed box: ["name":{name}, "index":{index}], location: ["row":{row}, "col":{col}]')
                if not is_in_box:
                    boxes_of_random.append([tl_x, tl_y, cell_w, cell_h])
    return {
        'random': boxes_of_random
    }
    

def shiftBoxes(boxes_dict: dict[str, list[list]], shift_x: int | float, shift_y: int | float) -> dict[str, list[list]]:
    boxes_copy = copy.deepcopy(boxes_dict)
    for name, boxes in boxes_copy.items():
        for box in boxes:
            box[0] += shift_x
            box[1] += shift_y
    return boxes_copy


def boxesToPaths_old(boxes_dict: dict[str, list[list]], element_extend: int) -> list[list[list]]:
    xyxy_list: list[list] = []
    for name, boxes in boxes_dict.items():
        for box in boxes:
            xyxy_list.append([
                int(math.floor(box[0])),
                int(math.floor(box[1])),
                int(math.ceil(box[0]+box[2])),
                int(math.ceil(box[1]+box[3]))
            ])
    min_x, min_y = 100000, 100000
    max_x, max_y = -10000, -10000
    for box in xyxy_list:
        min_x = min(min_x, box[0])
        min_y = min(min_y, box[1])
        max_x = max(max_x, box[2])
        max_y = max(max_y, box[3])
    width = max_x - min_x + element_extend * 2
    height = max_y - min_y + element_extend * 2
    canvas = np.full((height, width), fill_value=0, dtype=np.uint8)
    shift_x = min_x - element_extend
    shift_y = min_y - element_extend
    for box in xyxy_list:
        cv2.rectangle(canvas, (box[0]-shift_x, box[1]-shift_y), (box[2]-shift_x, box[3]-shift_y), 255, -1)
    if 0 < element_extend:
        elem = cv2.getStructuringElement(cv2.MORPH_RECT, (element_extend*2+1, element_extend*2+1))
        # canvas = cv2.dilate(canvas, elem)
        canvas = cv2.morphologyEx(canvas, cv2.MORPH_CLOSE, elem)
    # tuple[ndarray][N,1,2], [1,N,4]
    contours, hierarchy = cv2.findContours(canvas, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    # hierarchy = hierarchy[0]
    # print(hierarchy)
    contours = list(contours)
    for index in range(len(contours)):
        contours[index] = np.squeeze(contours[index], axis=1).tolist()
        for point in contours[index]:
            point[0] += shift_x
            point[1] += shift_y
    return contours


def boxesToPaths(boxes_dict: dict[str, list[list]], element_extend: int) -> dict[str, list]:
    NEXT, PREVIOUS, CHILD_0, PARENT = 0, 1, 2, 3
    xyxy_list: list[list] = []
    for name, boxes in boxes_dict.items():
        for box in boxes:
            xyxy_list.append([
                int(math.floor(box[0])),
                int(math.floor(box[1])),
                int(math.ceil(box[0]+box[2])),
                int(math.ceil(box[1]+box[3]))
            ])
    min_x, min_y = 100000, 100000
    max_x, max_y = -10000, -10000
    for box in xyxy_list:
        min_x = min(min_x, box[0])
        min_y = min(min_y, box[1])
        max_x = max(max_x, box[2])
        max_y = max(max_y, box[3])
    width = max_x - min_x + element_extend * 2
    height = max_y - min_y + element_extend * 2
    canvas = np.full((height, width), fill_value=0, dtype=np.uint8)
    shift_x = min_x - element_extend
    shift_y = min_y - element_extend
    for box in xyxy_list:
        cv2.rectangle(canvas, (box[0]-shift_x, box[1]-shift_y), (box[2]-shift_x, box[3]-shift_y), 255, -1)
    if 0 < element_extend:
        elem = cv2.getStructuringElement(cv2.MORPH_RECT, (element_extend*2+1, element_extend*2+1))
        canvas = cv2.morphologyEx(canvas, cv2.MORPH_CLOSE, elem)
    contours, hierarchy = cv2.findContours(canvas, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    hierarchy = hierarchy[0]
    output_parent: list[list[list]] = []
    output_childs: list[list[list[list]]] = []
    index = 0
    while -1 != index:
        output_parent.append(np.squeeze(contours[index], axis=1).tolist())
        for point in output_parent[-1]:
            point[0] += shift_x
            point[1] += shift_y
        childs: list[list[list]] = []
        sub_index = hierarchy[index][CHILD_0]
        while -1 != sub_index:
            childs.append(np.squeeze(contours[sub_index], axis=1).tolist())
            for point in childs[-1]:
                point[0] += shift_x
                point[1] += shift_y
            sub_index = hierarchy[sub_index][NEXT]
        output_childs.append(childs)
        index = hierarchy[index][NEXT]
    return {
        'parent': output_parent,
        'childs': output_childs
    }


def boxesToPathsInvGlobal(boxes_dict: dict[str, list[list]], sandbox_width: int, sandbox_height: int, element_extend: int) -> dict[str, list]:
    NEXT, PREVIOUS, CHILD_0, PARENT = 0, 1, 2, 3
    xyxy_list: list[list] = []
    for name, boxes in boxes_dict.items():
        for box in boxes:
            xyxy_list.append([
                int(math.floor(box[0])),
                int(math.floor(box[1])),
                int(math.ceil(box[0]+box[2])),
                int(math.ceil(box[1]+box[3]))
            ])
    # min_x, min_y = 100000, 100000
    # max_x, max_y = -10000, -10000
    # for box in xyxy_list:
    #     min_x = min(min_x, box[0])
    #     min_y = min(min_y, box[1])
    #     max_x = max(max_x, box[2])
    #     max_y = max(max_y, box[3])
    # width = max_x - min_x + element_extend * 2
    # height = max_y - min_y + element_extend * 2
    # canvas = np.full((height, width), fill_value=0, dtype=np.uint8)
    canvas = np.full((sandbox_height, sandbox_width), fill_value=0, dtype=np.uint8)
    # shift_x = min_x - element_extend
    # shift_y = min_y - element_extend
    for box in xyxy_list:
        # cv2.rectangle(canvas, (box[0]-shift_x, box[1]-shift_y), (box[2]-shift_x, box[3]-shift_y), 255, -1)
        cv2.rectangle(canvas, (box[0], box[1]), (box[2], box[3]), 255, -1)
    if 0 < element_extend:
        elem = cv2.getStructuringElement(cv2.MORPH_RECT, (element_extend*2+1, element_extend*2+1))
        canvas = cv2.morphologyEx(canvas, cv2.MORPH_CLOSE, elem)
    # if inverse:
    canvas = cv2.bitwise_not(canvas)
    contours, hierarchy = cv2.findContours(canvas, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return {
            'parent': [],
            'childs': []
        }
    hierarchy = hierarchy[0]
    output_parent: list[list[list]] = []
    output_childs: list[list[list[list]]] = []
    index = 0
    while -1 != index:
        output_parent.append(np.squeeze(contours[index], axis=1).tolist())
        # for point in output_parent[-1]:
        #     point[0] += shift_x
        #     point[1] += shift_y
        childs: list[list[list]] = []
        sub_index = hierarchy[index][CHILD_0]
        while -1 != sub_index:
            childs.append(np.squeeze(contours[sub_index], axis=1).tolist())
            # for point in childs[-1]:
            #     point[0] += shift_x
            #     point[1] += shift_y
            sub_index = hierarchy[sub_index][NEXT]
        output_childs.append(childs)
        index = hierarchy[index][NEXT]
    return {
        'parent': output_parent,
        'childs': output_childs
    }


def pathToSVG(path: list[list]) -> str:
    fragments = ['M', f'{path[0][0]},{path[0][1]}']
    for p in path[1:]:
        # print(p)
        fragments.append('L')
        fragments.append(f'{p[0]},{p[1]}')
    # print(fragments)
    return ' '.join(fragments)


def pathsToSVG(paths: list[list[list]]) -> str:
    # print(paths)
    # print(len(paths))
    return ' '.join([pathToSVG(path) for path in paths])



def pathsToSVGs_old(paths: list[list[list]]) -> list[str]:
    return [pathToSVG(path)+' Z' for path in paths]


def pathsToSVGs(parent: list[list[list]], childs: list[list[list[list]]]) -> list[str]:
    str_list: list[str] = []
    for par, chi in zip(parent, childs):
        parts = [pathToSVG(par)]
        for box in chi:
            parts.append(pathToSVG(box))
        parts.append('Z')
        str_list.append(' '.join(parts))
    return str_list


def extendBoxes(boxes_dict: dict[str, list[list]], extend: int) -> dict[str, list[list]]:
    boxes_copy = copy.deepcopy(boxes_dict)
    extend_2 = 2*extend
    for name, boxes in boxes_copy.items():
        for box in boxes:
            box[0] -= extend
            box[1] -= extend
            box[2] += extend_2
            box[3] += extend_2
    return boxes_copy


def xywh2pathd(x: int | float, y: int | float, w: int | float, h: int | float) -> str:
    return ' '.join(['M', f'{x},{y}', 'v', f'{h}', 'h', f'{w}', 'v', f'{-h}'])


def tileWithTri(
    resolution_width: int, resolution_height: int,
    canvas_width: int, canvas_height: int,
    original_img_str: str, derive1_img_str, derive2_img_str: str,
    structure: Literal['2-1', '2-2', 'h-1', 'h-2', 'y-1', 'y-2', '7-1', '7-2'],
    direction: Literal['left', 'right'],
    location: Literal['islet', 'sector'],
    shift: Literal['2','3','4'],
    probability: float,
    reference_cx: float, reference_cy: float,
    image_width: int, image_height: int,
    space_width: int, space_height: int,
) -> str:
    if 'islet' == location:
        islet_img_str = original_img_str
        sector_img_str = derive1_img_str
    else:
        islet_img_str = derive1_img_str
        sector_img_str = original_img_str
    ocean_img_str = derive2_img_str
    cell_width = image_width + space_width
    cell_height = image_height + space_height
    half_cell_width = cell_width / 2
    half_cell_height = cell_height / 2
    half_space_width = space_width / 2
    half_space_height = space_height / 2
    cell_rows = canvas_height // cell_height + int(bool(canvas_height%cell_height))
    cell_cols = canvas_width // cell_width + int(bool(canvas_width%cell_width))
    sandbox_height = cell_rows * cell_height
    sandbox_width = cell_cols * cell_width
    sandbox_rect = [0, 0, sandbox_width, sandbox_height]
    sandbox_str = xywh2pathd(*sandbox_rect)
    boxes_raw = calcBoxes(cell_width, cell_height, 'left' == direction, structure)
    shift: int = int(shift)
    shift_y = (shift - 1) * cell_height
    shift_x = 0 if shift % 2 else half_cell_width
    if 'right' == direction:
        shift_x = sandbox_width - shift_x - cell_width
    shift_y = int(round(sandbox_height * reference_cy))
    shift_y = shift_y // cell_height * cell_height
    if (shift_y // cell_height)%2:
        shift_x = int(round(sandbox_width * reference_cx - half_cell_width))
        shift_x = shift_x // cell_width * cell_width + half_cell_width
    else:
        if 'left' == direction:
            shift_x = int(math.floor(sandbox_width * reference_cx))
        else:
            shift_x = int(math.ceil(sandbox_width * reference_cx))
        shift_x = shift_x // cell_width * cell_width
    boxes_raw = shiftBoxes(boxes_raw, shift_x, shift_y)
    boxes_rand = randBoxes(cell_width, cell_height, cell_rows, cell_cols, probability, boxes_raw)
    boxes_all = copy.deepcopy(boxes_raw)
    boxes_all.update(copy.deepcopy(boxes_rand))
    ocean_patch_list = pathsToSVGs(**boxesToPathsInvGlobal(boxes_all, sandbox_width, sandbox_height, element_extend=2))
    # boxes_str = pathsToSVG(boxesToPaths(boxes_all, element_extend=2))
    boxes_patch = copy.deepcopy(boxes_rand)
    boxes_patch['sector'] = copy.deepcopy(boxes_raw['sector'])
    derive_patch_list = pathsToSVGs(**boxesToPaths(boxes_patch, element_extend=2))
    # patch_str_list = pathsToSVGs(boxesToPaths(boxes_patch, element_extend=2))
    viewbox_x = 0 if 'left' == direction else sandbox_width - canvas_width
    viewbox_x = (sandbox_width - canvas_width) / 2
    viewbox_y = (sandbox_height - canvas_height) / 2
    if reference_cx < 0.3333:
        viewbox_x = 0
    elif reference_cx < 0.6667:
        viewbox_x = (sandbox_width - canvas_width) / 2
    else:
        viewbox_x = sandbox_width - canvas_width
    if reference_cy < 0.3333:
        viewbox_y = 0
    elif reference_cy < 0.6667:
        viewbox_y = (sandbox_height - canvas_height) / 2
    else:
        viewbox_y = sandbox_height - canvas_height
    dict_ocean_image = {
        'id': 'ocean_image',
        'width': image_width,
        'height': image_height,
        'xlink:href': ocean_img_str,
    }
    dict_sector_image = {
        'id': 'sector_image',
        'width': image_width,
        'height': image_height,
        'xlink:href': sector_img_str,
    }
    dict_islet_image = {
        'id': 'islet_image',
        'width': image_width,
        'height': image_height,
        'xlink:href': islet_img_str,
    }
    dict_ocean_pattern = {
        'id': 'ocean_pattern',
        'patternUnits': 'userSpaceOnUse',
        'width': cell_width,
        'height': cell_height*2,
        'use1': {
            'x': half_space_width,
            'y': half_space_height,
            'xlink:href': '#ocean_image',
        },
        'use2': {
            'x': -cell_width/2+half_space_width,
            'y': cell_height+half_space_height,
            'xlink:href': '#ocean_image',
        },
        'use3': {
            'x': cell_width/2+half_space_width,
            'y': cell_height+half_space_height,
            'xlink:href': '#ocean_image',
        }
    }
    dict_derive_pattern = {
        'id': 'derive_pattern',
        'patternUnits': 'userSpaceOnUse',
        'width': cell_width,
        'height': cell_height*2,
        'use1': {
            'x': half_space_width,
            'y': half_space_height,
            'xlink:href': '#sector_image',
        },
        'use2': {
            'x': -cell_width/2+half_space_width,
            'y': cell_height+half_space_height,
            'xlink:href': '#sector_image',
        },
        'use3': {
            'x': cell_width/2+half_space_width,
            'y': cell_height+half_space_height,
            'xlink:href': '#sector_image',
        }
    }
    dict_defs = {
        'image1': dict_ocean_image,
        'image2': dict_sector_image,
        'image3': dict_islet_image,
        'pattern1': dict_ocean_pattern,
        'pattern2': dict_derive_pattern,
    }
    # dict_derive_path = {
    #     'd': ' '.join([sandbox_str, xywh2pathd(*(boxes_raw['islet'][0])), 'Z']),
    #     'fill': 'url(#derive_pattern)',
    #     'fill-rule': 'evenodd'
    # }
    # dict_ocean_path = {
    #     'd': ' '.join([sandbox_str, boxes_str, 'Z']),
    #     'fill': 'url(#ocean_pattern)',
    #     'fill-rule': 'evenodd'
    # }
    svg_name = 'svg'
    svg_attributes = {
        'width': resolution_width,
        'height': resolution_height,
        'viewBox': f'{viewbox_x} {viewbox_y} {canvas_width} {canvas_height}',
        'xmlns': "http://www.w3.org/2000/svg",
        'xmlns:xlink': "http://www.w3.org/1999/xlink",
        'defs': dict_defs,
        # 'path1': dict_derive_path,
        # 'path': dict_ocean_path,
        'use': {
            'x': boxes_raw['islet'][0][0]+space_width/2,
            'y': boxes_raw['islet'][0][1]+space_height/2,
            'xlink:href': '#islet_image',
        }
    }
    svg_ele_index = 0
    for ocean_patch in ocean_patch_list:
        svg_attributes[f'path{svg_ele_index}'] = {
            'd': ocean_patch,
            'fill': 'url(#ocean_pattern)',
            'fill-rule': 'evenodd'
        }
        svg_ele_index += 1
    for derive_patch in derive_patch_list:
        svg_attributes[f'path{svg_ele_index}'] = {
            'd': derive_patch,
            'fill': 'url(#derive_pattern)',
            'fill-rule': 'evenodd'
        }
        svg_ele_index += 1
    # for index, patch_str in enumerate(patch_str_list):
    #     svg_attributes[f'path{index}'] = {
    #         'd': patch_str,
    #         'fill': 'url(#derive_pattern)',
    #         'fill-rule': 'evenodd'
    #     }
    # for index, box in enumerate(boxes_raw['sector']):
    #     svg_attributes[f'use{index+1}'] = {
    #         'x': box[0]+space_width/2,
    #         'y': box[1]+space_height/2,
    #         'xlink:href': '#sector_image',
    #     }
    # svg_attributes['viewBox'] = f'0 0 {sandbox_width} {sandbox_height}'
    return dictToSVG(svg_name, svg_attributes)



def opencv2base64(image:np.ndarray):
    data = cv2.imencode('.png', image)[1]
    image_bytes = data.tobytes()
    img_data = base64.b64encode(image_bytes).decode('utf8')
    result = "data:image/png;base64," + str(img_data)
    return result


def test():
    img_path = '/home/fusen/图片/20240424-165151.png'
    image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    cont = cv2.drawContours(np.full_like(binary, 0, np.uint8), cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0], -1, 255, 10)
    binary = np.stack([binary]*4, axis=2)
    cont = np.stack([cont]*4, axis=2)
    img_str = opencv2base64(image)
    con_str = opencv2base64(cont)
    bin_str = opencv2base64(binary)
    image_height, image_width = image.shape[:2]
    image_height, image_width = image_height // 15, image_width // 15
    svg_str = tileWithTri(
        resolution_width=1024, resolution_height=1024,
        canvas_width=1024, canvas_height=1024,
        original_img_str=img_str, derive1_img_str=bin_str, derive2_img_str=con_str,
        structure='2-1',
        direction='right',
        location='islet',
        shift='3',
        probability=1,
        reference_cx=0.5, reference_cy=0.4,
        image_width=image_width, image_height=image_height,
        space_width=image_width//10, space_height=image_width//12,
    )
    with open('result.svg', 'w') as fp:
        fp.write(svg_str)


if '__main__' == __name__:
    test()