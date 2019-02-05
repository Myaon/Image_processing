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


# HIGH or LOWの時計測
def pulseIn(PIN, start=1, end=0):
    if start==0: end = 1
    t_start = 0
    t_end = 0
    # ECHO_PINがHIGHである時間を計測
    while GPIO.input(PIN) == end:
        t_start = time.time()
        
    while GPIO.input(PIN) == start:
        t_end = time.time()
    return t_end - t_start

# 距離計測
def calc_distance(TRIG_PIN, ECHO_PIN, num, v=34000): 
    for i in range(num):
        # TRIGピンを0.3[s]だけLOW
        GPIO.output(TRIG_PIN, GPIO.LOW)
        time.sleep(1)
        # TRIGピンを0.00001[s]だけ出力(超音波発射)        
        GPIO.output(TRIG_PIN, True)
        time.sleep(10)       
        GPIO.output(TRIG_PIN, False)
        # HIGHの時間計測
        t = pulseIn(ECHO_PIN)
        # 距離[cm] = 音速[cm/s] * 時間[s]/2
        distance = v * t/2
        if distance < 10:
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
                subprocess.call(["python","jtalk.py"])
                print(distance, "cm")
            if len(good) > MIN_MATCH_COUNT:
                print(distance, "cm")
        
        if distance > 10:
             print(distance, "cm")               

    # ピン設定解除
    GPIO.cleanup()

    
# TRIGとECHOのGPIO番号   
TRIG_PIN = 14
ECHO_PIN = 15
# ピン番号をGPIOで指定
GPIO.setmode(GPIO.BCM)
# TRIG_PINを出力, ECHO_PINを入力
GPIO.setup(TRIG_PIN,GPIO.OUT)
GPIO.setup(ECHO_PIN,GPIO.IN)
GPIO.setwarnings(False)

# 距離計測(TRIGピン番号, ECHO_PIN番号, 計測回数, 音速[cm/s])
calc_distance(TRIG_PIN, ECHO_PIN,10 , 34000)
