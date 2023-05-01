# Author: Burnside
# Time: 2023/05/01
# Function: Check the similarity of images in a directory and delete the similar ones
# Usage: python check.py
# Language: Python 3.10.5
# Encoding: utf-8

# Problems need to be solved:
# 1. The name of the image is not supported to contain Chinese characters.

import cv2
import os

class Color:
    RED = "\033[1;31m"                      # Red Color
    PURPLE = "\033[1;35m"                   # Purple Color
    END = '\033[0m'                         # Default Console Color

IMG_DIR = os.path.join('.', 'imgs')         # Dictory of images
DEL_THRES = 0.9                             # Threshold of similarity, if the similarity is greater than this value, the image will be deleted
TRASH_BIN = os.path.join('.', 'trash_bin')  # Use to store the deleted images
LOG_ALL = True                              # If True, print all the information, otherwise only print the information of the images amount.

# Code Start

img_list = [os.path.join(IMG_DIR, file) for file in os.listdir(IMG_DIR)]
imgs_num = len(img_list)
del_flag = [False for _ in range(imgs_num)]
 
if __name__ == '__main__':
    print('Find ' + Color.RED + str(imgs_num) + Color.END + ' images')
    for i in range(imgs_num):
        if LOG_ALL:
            print('Processing ' + Color.PURPLE + img_list[i] + Color.END + '...')
        if del_flag[i]:
            if LOG_ALL:
                print(Color.PURPLE + img_list[i] + Color.END + ' has been deleted, skip...')
            continue
        img1_hist = cv2.calcHist([cv2.imread(img_list[i])], [0], None, [255], [0, 256])
        for j in range(i + 1, imgs_num):
            if del_flag[j]:
                if LOG_ALL:
                    print(Color.PURPLE + img_list[j] + Color.END + ' has been deleted, skip...')
                continue
            img2_hist = cv2.calcHist([cv2.imread(img_list[j])], [0], None, [255], [0, 256])
            result = cv2.compareHist(img1_hist, img2_hist, method = cv2.HISTCMP_CORREL)
            if result > DEL_THRES:
                if LOG_ALL:
                    print(Color.PURPLE + img_list[i] + Color.END + ' and ' + Color.PURPLE + img_list[j] + Color.END + ' are similar, results = ' + Color.RED + str(result) + Color.END + ', delete ' + img_list[j] + '...')
                del_flag[j] = True
            elif LOG_ALL:
                print(Color.PURPLE + img_list[i] + Color.END + ' and ' + Color.PURPLE + img_list[j] + Color.END + ' are not similar, results = ' + Color.PURPLE + str(result) + Color.END)

    for i in range(imgs_num):
        if del_flag[i]:
            os.rename(img_list[i], os.path.join(TRASH_BIN, os.path.basename(img_list[i])))

# End of file

# TL; DR:
# There has some sample images in the imgs directory, you can run this script to test it.
# You can just use command 'python check.py' to run this script.
# This code is writen to delete the similar images in a directory, you can change the IMG_DIR to your own directory or put the images in the imgs directory.