import cv2, os
import numpy as np


def captch_ex(file_name, file_name_original):
    img  = cv2.imread(file_name)
    img_original = cv2.imread(file_name_original)

    img2gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 125, 255, cv2.THRESH_BINARY)
    image_final = cv2.bitwise_and(img2gray , img2gray , mask =  mask)
    ret, new_img = cv2.threshold(image_final, 125 , 255, cv2.THRESH_BINARY)  # for black text , cv.THRESH_BINARY_INV
    cv2.imshow('new_img' , new_img)
    cv2.waitKey()    
    '''
            line  8 to 12  : Remove noisy portion 
    '''
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3 , 3)) # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more 
    dilated = cv2.dilate(new_img,kernel,iterations = 9) # dilate , more the iteration more the dilation
    cv2.imshow('dilated' , dilated)
    cv2.waitKey()
    contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours
    index = 0 
    for contour in contours:
        # get rectangle bounding contour
        [x,y,w,h] = cv2.boundingRect(contour)

        #Don't plot small false positives that aren't text
        if w < 35 and h<35:
            continue

        # draw rectangle around contour on original image
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)
        cv2.rectangle(img_original,(x,y),(x+w,y+h),(255,0,255),2)
        #you can crop image and send to OCR  , false detected will return no text :)
        cropped = img_original[y :y +  h , x : x + w]
        path = './crop/'+file_name[file_name.rfind('/') + 1:file_name.rfind('.')]+'/'
        if not os.path.exists(path):
            os.mkdir(path)
        s = path + 'crop_' + str(index) + '.jpg' 
        cv2.imwrite(s , cropped)
         
        index = index + 1  
    print index 
    # original image with added contours 
    cv2.imshow('captcha_result' , img)
    cv2.waitKey()
    cv2.imshow('captcha_result' , img_original)
    cv2.waitKey()


def main():
    extensions = {".jpg", ".png", ".gif"} #etc
    flowchart_data_set_path = './highlighted/'
    original_path = './resized/'
    dirs = os.listdir(flowchart_data_set_path)   
    for flowchart_image in dirs: 
        print flowchart_image
        # e.g. flowchart_image ='basic-flowchart.jpg'
        if any(flowchart_image.endswith(ext) for ext in extensions):
            file_name = flowchart_data_set_path + flowchart_image
            file_name_original = original_path + flowchart_image
            print file_name
            print file_name_original
            captch_ex(file_name, file_name_original) 
        else:
            print 'not an image'

if __name__ == "__main__":
    main()