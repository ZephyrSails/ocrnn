import cv2, os, math
import numpy as np
from PIL import Image, ImageDraw
import shutil

def downscale_image(im, max_dim=516708):
    """Shrink im until its longest dimension is <= max_dim.

    Returns new_image, scale (where scale <= 1).
    """
    a, b = im.size
    if (a + 6) * (b + 6) <= max_dim:
        return 1.0, im
    # print a, b
    # scale = 1.0 * max_dim / max(a, b)
    scale = 1.0 * (-6*(a + b) + math.sqrt(36*(a + b)*(a + b) + 4*a*b*(max_dim - 36)))/(2*a*b)
    # print scale
    new_im = im.resize((int(a * scale), int(b * scale)), Image.ANTIALIAS)
    return scale, new_im

def main():
    extensions = {".jpg", ".png"} #etc
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
            if scale == 1:
                shutil.move(file_name, path + flowchart_image)
            else:
                new_file_name = path + flowchart_image[0:flowchart_image.rfind('.')] + '.png'
                print new_file_name	 
                cv2.imwrite(new_file_name , np.asarray(resized))
        else:
            print 'not an image'

if __name__ == "__main__":
    main()