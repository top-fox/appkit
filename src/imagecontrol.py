from PIL import Image
import numpy as np

def list_colours(image):
    npimage = np.array(image)
    colour_list = []
    for row in range(image.size[0]):
        for col in range(image.size[1]):
            if tuple(npimage[col][row]) not in colour_list:
                colour_list.append(tuple(npimage[col][row]))
    return colour_list

def combine_images_from_path(path_list, path_prefix='', path_suffix='.png'):
    image_list = []
    for path in path_list:
        image_list.append(Image.open(path_prefix + path + path_suffix))
    return combine_images(image_list)

def combine_images(image_list):
    '''
    Overlays images (PNG file in RGBA format) in order listed, with alpha channel.
    '''
    for index, image in enumerate(image_list):
        i = np.array(image)
        i = i.transpose(2, 0, 1)
        if index == 0:
            t = i
        else:
            for rgb in range(3):
                t[rgb] = t[rgb]*(1-i[3]/255) + i[rgb]*(i[3]/255)
            t[3] = 255*(1 - (1 - t[3]/255)*(1 - i[3]/255))
            t = t.transpose(1, 2, 0)
    return Image.fromarray(t)

def new_colour(image, new_white, new_black=[0,0,0,255]):
    '''
    Changes image (PNG file in RGBA format) to greyscale, then substitutes the new white and black colours.
    '''
    i = np.array(image)
    i = i.transpose(2,0,1)
    g = (i[0]/3 + i[1]/3 + i[2]/3)
    i = np.array([g, g, g, i[3]])
    for rgb in range(3):
        i[rgb] = new_white[rgb]*i[rgb]/255 + new_black[rgb]*(1 - i[rgb]/255)
    i = i.transpose(1, 2, 0)
    return Image.fromarray(i.astype(np.uint8))

def hex_to_rgba_1(hex, alpha=1):
    # Returns colours in RGBA format with scale 0 to 1
    return [int(hex[1:3] ,16)/255, int(hex[3:5], 16)/255, int(hex[5:7], 16)/255, alpha]

def hex_to_rgba_255(hex, alpha=1):
    # Returns colours in RGBA format with scale 0 to 255
    return [int(hex[1:3] ,16), int(hex[3:5], 16), int(hex[5:7], 16), 255*alpha]




