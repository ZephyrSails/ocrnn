import os
from PIL import Image
import pytesseract

def image2Text(cropped_image):
	text = pytesseract.image_to_string(Image.open(cropped_image))
	# print (text)
	return text

def main():
    batches = ['2652515','2652805'] #etc
    crop_path = '/Users/xiaofengzhu/Documents/GitHub/ocrnn/crop_training/'

    ocr_label_txt = open('movie_lines.txt', 'w')  
    for batch in batches:
        training_label_file_name = 'training_label_' + batch
        training_label_file = open(training_label_file_name, 'r')
        for line in training_label_file.readlines():
        	image_label = line.split('\t')
        	image_name = image_label[0]
        	label = image_label[1].strip()
	        cropped_images_path = crop_path + image_name
	        text = image2Text(cropped_images_path).strip()
	        print text, label
	        ocr_label_txt.write('("' + text + '","' + label + '")\n')
	        ocr_label_txt.flush()               
    ocr_label_txt.close()

if __name__ == "__main__":
    main()