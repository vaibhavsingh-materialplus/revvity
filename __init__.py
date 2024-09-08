import cv2
import numpy as np
import os
import glob
from pdf2images import convert_pdf_to_image
from prewitt import prewitt_edge_detection
from crop import crop_image
from iou import calculate_iou

box_factor = 1.3

def convert_bbox(x, y, w, h):
    x_min = x
    y_min = y
    x_max = x + w
    y_max = y + h
    return x_min, y_min, x_max, y_max

def is_crop_rectangle_valid(x,y,width,height,img_width,img_height):

    x_end=x+width
    y_end=y+height

    if x<0 or y<0 or x_end> img_width or y_end>img_height:
        return False
    return True


#convert the pdf to images
data_path = "./train"
converted_path = "./convert"

dir = os.listdir(data_path)
for file in dir:
   pdf_name = file
   convert_pdf_to_image(data_path, pdf_name, converted_path)

if not os.path.exists("./saved"):
        os.mkdir("./saved")
else:
        files = glob.glob('saved_path/*')
        for f in files:
            os.remove(f)

#apply prewitt-edge detection
# Read the input image
for img in os.listdir(converted_path):
    image = cv2.imread(f"./convert/{img}", cv2.IMREAD_COLOR)
    img_width,img_height=image.shape[:2]
    
   # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #image1 = cv2.GaussianBlur(image, (3, 3), 0)
    # Apply Prewitt edge detection
    edges = prewitt_edge_detection(image)

#convert the edge detected image to the uint8 format
    image_uint8 = edges.astype(np.uint8)
#Using adaptiveThreshold
    thresh = cv2.adaptiveThreshold(image_uint8, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
#finding contours
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
# drawing contours over blank image
    ctr = np.zeros(image.shape, dtype=np.uint8)

    #converting the contours to a dictionary based on area
    dic=dict()
    for i,j in enumerate(contours):
        area = cv2.contourArea(j)
    #lst_per.append(cv2.arcLength(x, True))
        dic[i]=area

    #sorting this dictionary in descending order 
    sorted_dict1 = {k: v for k, v in sorted(dic.items(), key=lambda item: item[1],reverse=True)}
    #print(sorted_dict1)  # Output: {'apple': 1, 'cherry': 2, 'banana': 3}

    list_of_contours=[]
    #saving cropped images
    
    k=0
    duplicate_set=[]
    for p,y in sorted_dict1.items():
        path=os.path.join('./convert',str(img))
    
        if y>20000:
            cnt = contours[int(p)]
            list_of_contours.append(p)
            #print(type(cnt))

    print(list_of_contours)
    if len(list_of_contours)>2:
        for i in range(1,len(list_of_contours)):   
            for j in range(i+1,len(list_of_contours)):
                #print(i,j)
         
                box1 = np.array(list(cv2.boundingRect(contours[list_of_contours[i]])))
                box2 = np.array(list(cv2.boundingRect(contours[list_of_contours[j]])))
                bbox1 = convert_bbox(*box1)
                bbox2 = convert_bbox(*box2)
                iou_value = calculate_iou(bbox1, bbox2)
                #iou_value = iou(box1, box2)
                print(f"{i},{j},{iou_value}")
                if iou_value>0.5:
                    if i not in duplicate_set:
                        x,y,w,h = cv2.boundingRect(contours[list_of_contours[i]])
                        
                        center_x = x + w // 2
                        center_y = y + h // 2
                        # Compute the new width and height with the box factor
                        new_w = int(w * box_factor)
                        #new_h = int(h * box_factor)
                        new_h=h
                        # Compute the new top-left corner based on the center
                        #new_x = int(center_x - new_w // 2)
                        new_x = x
                        new_y = int(center_y - new_h // 2)

                        #if is_crop_rectangle_valid(new_x,new_y,new_w,new_h,img_width,img_height):
                           # crop_image(path, os.path.join('./saved',f"{img}output{k}.jpg"), new_x, new_y, new_w, new_h)
                       # else:
                       #     crop_image(path, os.path.join('./saved',f"{img}output{k}.jpg"), x, y,w, h)
                        crop_image(path, os.path.join('./saved',f"{img}output{k}.jpg"), new_x, new_y, new_w, new_h)
                        k=k+1
                        duplicate_set.append(i)
                else:
                    if i not in duplicate_set:
                        x,y,w,h = cv2.boundingRect(contours[list_of_contours[i]])
                        center_x = x + w // 2
                        center_y = y + h // 2
                        # Compute the new width and height with the box factor
                        new_w = int(w * box_factor)
                        #new_h = int(h * box_factor)
                        new_h=h
                        # Compute the new top-left corner based on the center
                        #new_x = int(center_x - new_w // 2)
                        new_x = x
                        new_y = int(center_y - new_h // 2)
                        #if is_crop_rectangle_valid(new_x,new_y,new_w,new_h,img_width,img_height):
                         #   crop_image(path, os.path.join('./saved',f"{img}output{k}.jpg"), new_x, new_y, new_w, new_h)
                            
                        #else:
                         #   crop_image(path, os.path.join('./saved',f"{img}output{k}.jpg"), x, y,w,h)
                        crop_image(path, os.path.join('./saved',f"{img}output{k}.jpg"), new_x, new_y, new_w, new_h)

                        k=k+1
                        duplicate_set.append(i)
                    if j not in duplicate_set:
                        x,y,w,h = cv2.boundingRect(contours[list_of_contours[j]]) 
                        center_x = x + w // 2
                        center_y = y + h // 2
                        # Compute the new width and height with the box factor
                        new_w = int(w * box_factor)
                        #new_h = int(h * box_factor)
                        new_h=h
                        # Compute the new top-left corner based on the center
                        #new_x = int(center_x - new_w // 2)
                        new_x = x
                        new_y = int(center_y - new_h // 2)   
                        
                        #if is_crop_rectangle_valid(new_x,new_y,new_w,new_h,img_width,img_height):
                         #   crop_image(path, os.path.join('./saved',f"{img}output{k}.jpg"), new_x, new_y, new_w, new_h)
                    
                        #else:
                         #   crop_image(path, os.path.join('./saved',f"{img}output{k}.jpg"), x, y, w,h)
                        crop_image(path, os.path.join('./saved',f"{img}output{k}.jpg"), new_x, new_y, new_w, new_h)
                        k=k+1
                        duplicate_set.append(j)
    else:
        try:
            x,y,w,h = cv2.boundingRect(contours[list_of_contours[1]])
            center_x = x + w // 2
            center_y = y + h // 2
            # Compute the new width and height with the box factor
            new_w = int(w * box_factor)
            #new_h = int(h * box_factor)
            new_h=h
            # Compute the new top-left corner based on the center
            #new_x = int(center_x - new_w // 2)
            new_x = x
            new_y = int(center_y - new_h // 2)
            
            #if is_crop_rectangle_valid(new_x,new_y,new_w,new_h,img_width,img_height):
             #   crop_image(path, os.path.join('./saved',f"{img}output{k}.jpg"), new_x, new_y, new_w,new_h)
            #else:
            #    crop_image(path, os.path.join('./saved',f"{img}output{k}.jpg"), x, y, w, h)
            crop_image(path, os.path.join('./saved',f"{img}output{k}.jpg"), new_x, new_y, new_w, new_h)
            k=k+1
        except:
            pass
        
#print(list_of_contours)
            #x,y,w,h = cv2.boundingRect(cnt)
            #crop_image(path, os.path.join('./saved',f"{img}output{i}.jpg"), x, y, w, h)
            #i=i+1   





