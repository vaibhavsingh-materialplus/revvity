import cv2
import numpy as np
import os
import glob
from pdf2images import convert_pdf_to_image
from prewitt import prewitt_edge_detection
from crop import crop_image
from iou import iou


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
    image = cv2.imread(f"./convert/{img}")
    image1 = cv2.GaussianBlur(image, (3, 3), 0)
    #imgray = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
    # Apply Prewitt edge detection
    edges = prewitt_edge_detection(image1)

#convert the edge detected image to the uint8 format
    image_uint8 = edges.astype(np.uint8)
#Using adaptiveThreshold
    thresh = cv2.adaptiveThreshold(image_uint8, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
#finding contours
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
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
                box1[2]=box1[0]+box1[2]
                box1[3]=box1[1]+box1[3]

                box2[2]=box2[0]+box2[2]
                box2[3]=box2[1]+box2[3]
                iou_value = iou(box1, box2)
                print(f"{i},{j},{iou_value}")
                if iou_value>0.5:
                    if i not in duplicate_set:
                        x,y,w,h = cv2.boundingRect(contours[list_of_contours[i]])
                        crop_image(path, os.path.join('./saved',f"{img}output{k}.jpg"), x, y, w, h)
                        k=k+1
                        duplicate_set.append(i)
                else:
                    if i not in duplicate_set:
                        x,y,w,h = cv2.boundingRect(contours[list_of_contours[i]])
                        crop_image(path, os.path.join('./saved',f"{img}output{k}.jpg"), x, y, w, h)
                        k=k+1
                        duplicate_set.append(i)
                    if j not in duplicate_set:
                        x,y,w,h = cv2.boundingRect(contours[list_of_contours[j]])    
                        crop_image(path, os.path.join('./saved',f"{img}output{k}.jpg"), x, y, w, h)
                        k=k+1
                        duplicate_set.append(j)
    else:
        try:
            x,y,w,h = cv2.boundingRect(contours[list_of_contours[1]])
            crop_image(path, os.path.join('./saved',f"{img}output{k}.jpg"), x, y, w, h)
            k=k+1
        except:
            pass
        
#print(list_of_contours)
            #x,y,w,h = cv2.boundingRect(cnt)
            #crop_image(path, os.path.join('./saved',f"{img}output{i}.jpg"), x, y, w, h)
            #i=i+1   





