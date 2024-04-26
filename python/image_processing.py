import imageio as imio
from PIL import Image
import numpy as np

def open_img(img_path):
    img = imio.imread(img_path)
    return img

def convert_output(img):
    converted_img = []
    for r in img:
        new_row = []
        for p in r:
            if p == 3:
                new_row.append(255)
            elif p == 2:
                new_row.append(127)
            elif p == 1:
                new_row.append(63)
            else:
                new_row.append(0)
        converted_img.append(new_row)
    
    return converted_img

def save_img(img_data, save_path, f_name):
    img = Image.fromarray(np.asarray(img_data))
    img = img.convert('L')
    img.save("{}/{}.png".format(save_path, f_name))