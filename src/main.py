import os
import json
import cv2
import numpy as np
import pytesseract
from pytesseract import Output


def main():

    image_list = [img for img in os.listdir(os.getcwd()) if ".png" in img]

    if image_list:
        filename = image_list[0]

        raw_img = cv2.imread(filename)
        #transform rgb to hsv color
        hsv_img =  cv2.cvtColor(raw_img, cv2.COLOR_RGB2HSV)

        #red
        lower = np.array([0,255,255])
        upper = np.array([120,255,255])

        mask_1 = cv2.inRange(hsv_img, lower, upper)
        first_filter = cv2.bitwise_and(raw_img, raw_img, mask=mask_1)
        morph_filter = cv2.erode(first_filter,np.ones((3,3),np.uint8),iterations = 1)
        morph_filter = cv2.dilate(morph_filter,np.ones((3,3),np.uint8),iterations = 1)
        hsv_morph_filter =  cv2.cvtColor(morph_filter, cv2.COLOR_RGB2HSV)

        mask_red = cv2.inRange(hsv_morph_filter, lower, upper)
        bbox_red = cv2.boundingRect(mask_red)

        #blue
        lower = np.array([150,200,20])
        upper = np.array([200,255,255])

        mask_1 = cv2.inRange(hsv_img, lower, upper)
        first_filter = cv2.bitwise_and(raw_img, raw_img, mask=mask_1)
        morph_filter = cv2.erode(first_filter,np.ones((3,3),np.uint8),iterations = 2)
        morph_filter = cv2.dilate(morph_filter,np.ones((3,3),np.uint8),iterations = 2)
        hsv_morph_filter =  cv2.cvtColor(morph_filter, cv2.COLOR_RGB2HSV)

        mask_blue = cv2.inRange(hsv_morph_filter, lower, upper)
        bbox_blue = cv2.boundingRect(mask_blue)

        #white
        lower = np.array([0,0,20])
        upper = np.array([255,5,255])

        mask_1 = cv2.inRange(hsv_img, lower, upper)
        first_filter = cv2.bitwise_and(raw_img, raw_img, mask=mask_1)
        morph_filter = cv2.erode(first_filter,np.ones((5,5),np.uint8),iterations = 5)
        morph_filter = cv2.dilate(morph_filter,np.ones((5,5),np.uint8),iterations = 5)
        hsv_morph_filter =  cv2.cvtColor(morph_filter, cv2.COLOR_RGB2HSV)

        mask_white = cv2.inRange(hsv_morph_filter, lower, upper)
        bbox_white = cv2.boundingRect(mask_white)

        #applying tesseract to the white box
        crop_white = raw_img[bbox_white[1]:bbox_white[1]+bbox_white[3],bbox_white[0]:bbox_white[0]+bbox_white[2],:]
        
        #resizing the crop for better tesseract performance
        scale_percent = 50 
        dim = (int(crop_white.shape[1] * scale_percent / 100), int(crop_white.shape[0] * scale_percent / 100))
        rsz_crop_white = cv2.resize(crop_white, dim, interpolation = cv2.INTER_AREA)
        
        #extracting text
        text = pytesseract.image_to_string(rsz_crop_white)
        with open("text.json","w") as f:
            json.dump({"text":text},f)

        #highlight text
        highlighted_img = rsz_crop_white.copy()
        data = pytesseract.image_to_data(highlighted_img, output_type=Output.DICT)
        for i in range(len(data['level'])):
            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]
            cv2.rectangle(highlighted_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imwrite('highlighted.jpg', highlighted_img)

        #building json
        json_str = ""
        bbox_list = [bbox_red,bbox_blue,bbox_white]
        description_list = ["Rectangle","Circle","Rectangle"]
        for bbox,description in zip(bbox_list,description_list):

            json_dict = {
            "boundingPoly": {
                "vertices": [
                {
                    "x": bbox[0],
                    "y": bbox[1]
                },
                {
                    "x": bbox[0]+bbox[2],
                    "y": bbox[1]+bbox[3]
                }
                ]
            },
            "description": description
            }

            json_str += str(json_dict)

        #saving json
        with open("output.json","w") as f:
            json.dump(json_str,f)


 


    

    
            

