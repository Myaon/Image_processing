#coding: utf-8

import cv2
import numpy as np
import subprocess

MIN_MATCH_COUNT = 10


template_path = "assets/img/template/"
template_filename = "neji.jpg"

sample_path = "assets/img/sample/"
sample_filename = "motoneji.jpg"

result_path = "assets/img/result_AKAZE/"
result_name = "perfect.jpg"


akaze = cv2.AKAZE_create() 


expand_template=2
whitespace = 20
template_temp = cv2.imread(template_path + template_filename, 0)
height, width = template_temp.shape[:2]
template_img=np.ones((height+whitespace*2, width+whitespace*2),np.uint8)*255
template_img[whitespace:whitespace + height, whitespace:whitespace+width] = template_temp
template_img = cv2.resize(template_img, None, fx = expand_template, fy = expand_template)
kp_temp, des_temp = akaze.detectAndCompute(template_img, None)


expand_sample = 2
sample_img = cv2.imread(sample_path + sample_filename, 0)
sample_img = cv2.resize(sample_img, None, fx = expand_sample, fy = expand_sample)
kp_samp, des_samp = akaze.detectAndCompute(sample_img, None)


bf = cv2.BFMatcher()
matches = bf.knnMatch(des_temp, des_samp, k=2)


ratio = 1
good = []
for m, n in matches:
    if m.distance < ratio * n.distance:
        good.append([m])

if len(good)>MIN_MATCH_COUNT:
    subprocess.call(["python","jtalkg4.py"])
    print ("enough matches are - %d/%d" % (len(good),MIN_MATCH_COUNT))
    matchesMask = None

else:
    print ("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
    matchesMask = None
