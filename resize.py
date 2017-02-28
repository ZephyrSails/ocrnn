import cv2, os
import numpy as np
from PIL import Image, ImageDraw

def downscale_image(im, max_dim=500):
    """Shrink im until its longest dimension is <= max_dim.

    Returns new_image, scale (where scale <= 1).
    """
    a, b = im.size
    if max(a, b) <= max_dim:
        return 1.0, im

    scale = 1.0 * max_dim / max(a, b)
    new_im = im.resize((int(a * scale), int(b * scale)), Image.ANTIALIAS)
    return scale, new_im

def main():
    extensions = {".jpg", ".png", ".gif"} #etc
    flowchart_data_set_path = './flowchart_data_set/' # input flowchart folder
    dirs = os.listdir(flowchart_data_set_path)   
    path = './resized/' # resized image folder
    if not os.path.exists(path):
        os.mkdir(path)    
    for flowchart_image in dirs: 
        # print flowchart_image
        # e.g. flowchart_image ='basic-flowchart.jpg'
        if any(flowchart_image.endswith(ext) for ext in extensions):
            file_name = flowchart_data_set_path + flowchart_image
            img = Image.open(file_name)
            scale, resized = downscale_image(img)
            new_file_name = path + flowchart_image[0:flowchart_image.rfind('.')] + '.png'
            print new_file_name	 
            cv2.imwrite(new_file_name , np.asarray(resized))
        else:
            print 'not an image'

if __name__ == "__main__":
    main()