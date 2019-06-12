#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import picamera
import subprocess

import cv2
import numpy as np

from datetime import datetime

MIN_MATCH_COUNT = 8

camera = picamera.PiCamera()
camera.resolution = (640,400)
filename = datetime.now().strftime('assets/img/sample/test.jpg')


# 画像読み込み先のパス，結果保存用のパスの設定
template_path = "assets/img/template/"
template_filename = "maku.jpg"

sample_path = "assets/img/sample/"
sample_filename = "test.jpg"

result_path = "assets/img/result_AKAZE/"
result_name = "perfect.jpg"

akaze = cv2.AKAZE_create() 

camera.capture(filename)
# 文字画像を読み込んで特徴量計算
expand_template=2
whitespace = 20
template_temp = cv2.imread(template_path + template_filename, 0)
height, width = template_temp.shape[:2]
template_img=np.ones((height+whitespace*2, width+whitespace*2),np.uint8)*255
template_img[whitespace:whitespace + height, whitespace:whitespace+width] = template_temp
template_img = cv2.resize(template_img, None, fx = expand_template, fy = expand_template)
kp_temp, des_temp = akaze.detectAndCompute(template_img, None)

# 間取り図を読み込んで特徴量計算
expand_sample = 2
sample_img = cv2.imread(sample_path + sample_filename, 0)
sample_img = cv2.resize(sample_img, None, fx = expand_sample, fy = expand_sample)
kp_samp, des_samp = akaze.detectAndCompute(sample_img, None)

# 特徴量マッチング実行
bf = cv2.BFMatcher()
matches = bf.knnMatch(des_temp, des_samp, k=2)


# マッチング精度が高いもののみ抽出
ratio = 0.8
good = []
for m, n in matches:
    if m.distance < ratio * n.distance:
        good.append([m])
if len(good) < MIN_MATCH_COUNT:
    print("OFF")
if len(good) > MIN_MATCH_COUNT:
    print("ON")
