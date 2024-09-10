#classifying images of charts and graphs from tables and paragraphs
import os
import cv2
import numpy as np 

output_path='./final_images'

if not os.path.exists(output_path):
        os.mkdir(output_path)

for img in os.listdir("./saved"):
    image = cv2.imread(f"./saved/{img}", cv2.IMREAD_COLOR) 
    imgray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
    path=os.path.join(f'{output_path}',str(img))
#Using Threshold
    _,thresh = cv2.threshold(imgray, 250, 255, cv2.THRESH_BINARY)
#finding contours
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    # Save the cropped image
    final=image.astype(np.uint8)
    if len(contours)<300:
        cv2.imwrite(path,image)
    print(f"{img}:{len(contours)}")