__all__ = [
    'boldInHollow'
]


import cv2
import time
import base64
import random
import numpy as np


def xywh2pathd(x: int | float, y: int | float, w: int | float, h: int | float) -> str:
    # return ' '.join(['M', f'{x},{y}', 'L', f'{x},{y+h}', 'L', f'{x+w},{y+h}', 'L', f'{x+w},{y}'])
    return ' '.join(['M', f'{x},{y}', 'v', f'{h}', 'h', f'{w}', 'v', f'{-h}'])


def dictToSVG(element_name: str, properties: dict) -> str:

    internal_contents = ''
    internal_elements: list[str] = []
    # header_string = element_name.rstrip('0123456789') + ' '
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


def boldInHollow(
    resolution_width: int, resolution_height: int,
    canvas_width: int, canvas_height: int,
    # image1_string: str, image1_width: int, image1_height: int,
    # image2_string: str, image2_width: int, image2_height: int,
    bg_img_str: str, fg_img_str: str,
    image_width: int, image_height: int,
    space_width: int, space_height: int,
) -> str:
    # if image1_width != image2_width or image1_height != image2_height:
    #     return "image1's size should equal with image2's size!"
    
    cell_width = image_width + space_width
    cell_height = image_height + space_height
    cell_height *= 2
    half_space_x = space_width / 2
    half_space_y = space_height / 2
    
    cell_num_x = canvas_width // cell_width + (1 if canvas_width % cell_width else 0)
    cell_num_x += 0 if cell_num_x % 2 else 1
    cell_num_y = canvas_height // cell_height + (1 if canvas_height % cell_height else 0)
    sandbox_width = cell_num_x * cell_width
    sandbox_height = cell_num_y * cell_height
    sandbox_rect = [0, 0, sandbox_width, sandbox_height]
    
    margin = 2
    bottom_x = cell_num_x // 2 * cell_width + half_space_x - margin
    bottom_y = sandbox_height - image_height - half_space_y - margin
    bottom_width = image_width + 2 * margin
    bottom_height = image_height + 2 * margin
    bottom_rect = [bottom_x, bottom_y, bottom_width, bottom_height]
    bottom_x = bottom_x + margin
    bottom_y = bottom_y + margin
    
    random.seed(time.time())
    random_x = random.randint(0, cell_num_x - 1) * cell_width + half_space_x - margin
    random_y = random.randint(0, cell_num_y - 1) * cell_height - half_space_y - image_height - margin
    random_rect = [random_x, random_y, bottom_width, bottom_height]
    random_x = random_x + margin
    random_y = random_y + margin
    
    viewbox_x = (sandbox_width - canvas_width) // 2
    viewbox_y = sandbox_height - canvas_height
    
    dict_bg_image = {
        'id': 'bg_img',
        'width': image_width,
        'height': image_height,
        'xlink:href': bg_img_str,
    }
    
    dict_fg_image = {
        'id': 'fg_img',
        'width': image_width,
        'height': image_height,
        'xlink:href': fg_img_str,
    }
    
    dict_pattern = {
        'id': 'tile',
        'patternUnits': 'userSpaceOnUse',
        'width': cell_width,
        'height': cell_height,
        'use1': {
            'x': -image_width / 2,
            'y': half_space_y,
            'xlink:href': '#bg_img',
        },
        'use2': {
            'x': image_width / 2 + space_width,
            'y': half_space_y,
            'xlink:href': '#bg_img',
        },
        'use3': {
            'x': half_space_x,
            'y': image_height + space_height + half_space_y,
            'xlink:href': '#bg_img',
        }
    }
    
    dict_defs = {
        'image1': dict_bg_image,
        'image2': dict_fg_image,
        'pattern': dict_pattern,
    }
    
    dict_path = {
        'd': ' '.join([xywh2pathd(*sandbox_rect), xywh2pathd(*bottom_rect), xywh2pathd(*random_rect), 'Z']),
        'fill': 'url(#tile)',
        'fill-rule': 'evenodd',
    }
    
    svg_name = 'svg'
    svg_attributes = {
        'width': resolution_width,
        'height': resolution_height,
        'viewBox': f'{viewbox_x} {viewbox_y} {canvas_width} {canvas_height}',
        'xmlns': "http://www.w3.org/2000/svg",
        'xmlns:xlink': "http://www.w3.org/1999/xlink",
        'defs': dict_defs,
        'path': dict_path,
        'use1': {
            'x': bottom_x,
            'y': bottom_y,
            'xlink:href': '#fg_img',
        },
        'use2': {
            'x': random_x,
            'y': random_y,
            'xlink:href': '#fg_img',
        },
    }
    
    return dictToSVG(svg_name, svg_attributes)


def opencv2base64(image:np.ndarray):
    data = cv2.imencode('.png', image)[1]
    image_bytes = data.tobytes()
    img_data = base64.b64encode(image_bytes).decode('utf8')
    result = "data:image/png;base64," + str(img_data)
    return result


def test():
    img1_path = '/media/fusen/datum/Project/Data/反白/png/Cluck2GO.png'
    img2_path = '/media/fusen/datum/Project/Data/反白/png/Cafe-Zella.png'
    image1 = cv2.imread(img1_path, cv2.IMREAD_UNCHANGED)
    image2 = cv2.imread(img2_path, cv2.IMREAD_UNCHANGED)
    svg_str = boldInHollow(
        resolution_width=4096, resolution_height=2048,
        canvas_width=4096, canvas_height=2048,
        bg_img_str=opencv2base64(image1), fg_img_str=opencv2base64(image2),
        image_width=image2.shape[1], image_height=image2.shape[0],
        space_width=10, space_height=10
    )
    with open('the-result.svg', 'w') as f:
        f.write(svg_str)


if '__main__' == __name__:
    test()