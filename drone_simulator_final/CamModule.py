import numpy as np
import requests
import imutils
import cv2
import cv2.aruco as aruco
import sys, time, math

id_to_find = 1
marker_size = 10

def findArucoMarkers(img, markerSize=6, totalMarkers=250, draw=True):
	imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	key = getattr(aruco, 'DICT_6X6_250')
	arucoDict = aruco.Dictionary_get(key)
	arucoParam = aruco.DetectorParameters_create()
	bboxs, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)
	return bboxs, ids, rejected


def main_Loop(value):

	if value == "rpicam":
		cap = cv2.VideoCapture(0)
		cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
		cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
		while True:
			ret, frame = cap.read()

			corners, ids, rejected = findArucoMarkers(frame)

			if ids is not None and ids[0] == id_to_find:
				return True
	else:
		while True:
			print("Connecting TO Camera")
			cap = requests.get("http://"+value+":8080/shot.jpg")
			cap = np.array(bytearray(cap.content), dtype=np.uint8)
			cap = cv2.imdecode(cap, -1)
			frame = imutils.resize(cap, width=1000, height=1800)

			print("Trying to detect marker")
			corners, ids, rejected = findArucoMarkers(frame)

			if ids is not None and ids[0] == id_to_find:
				print("Marker Detected")
				return True
