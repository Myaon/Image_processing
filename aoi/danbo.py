# -*- coding: utf-8 -*-

import numpy as np
import cv2
from matplotlib import pyplot as plt

if __name__ == '__main__':

    img_src1 = cv2.imread('./image/dambo.jpg',0) # queryImage
    img_src2 = cv2.imread('./image/dambo_turn.jpg',0) # trainImage
    img_dst = img_src1

    # ORB(https://en.wikipedia.org/wiki/ORB_(feature_descriptcriptor))オブジェクトを生成する。
    orb = cv2.ORB_create()

    # img_src1とimg_src2の キーポイントと特徴量を抽出する。
    keypoint1, descript1 = orb.detectAndCompute(img_src1, None)
    keypoint2, descript2 = orb.detectAndCompute(img_src2, None)

    # BFMatcher オブジェクトを生成する。
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # 2つの特徴量をマッチングする。
    matches = bf.match(descript1, descript2)

    # マッチした特徴点の距離の短い順にソートする。
    matches = sorted(matches, key=lambda x:x.distance)

    # マッチングした特徴点同士を線で結ぶ
    img3 = cv2.drawMatches(img_src1, keypoint1, img_src2, keypoint2, matches, img_dst, flags=2)

    # 表示
    plt.imshow(img3),plt.show()
