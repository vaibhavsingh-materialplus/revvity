import cv2
import numpy as np
import os
import glob
from pdf2images import convert_pdf_to_image
from prewitt import prewitt_edge_detection
from crop import crop_image
from iou import iou



def main(file_path):
#convert the pdf to images
    data_path = "./train"
    converted_path = "./convert"
    a=""
    print(file_path)
    print(file_path.split('/')[-1])
    print(a.join(file_path.split('/')))