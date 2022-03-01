import cv2 as cv
from cv2 import WARP_INVERSE_MAP
import numpy as np
from PIL import Image
import time
import pytesseract

class Detector:
	def __init__(self, img_path, img_name='default', debug=False):
		# Set window name when showing the image
		self.__winName = img_name

		# Pre-process the image
		img = cv.imread(img_path)
		self.frame = cv.resize(img, (480,360))

		# This are some good edge detector threshold values I have found.
		self.__thres1 = 91
		self.__thres2 = 81
		# The approximate polygon
		self.__epsilon = 0.115

		# Create internal vars
		self.plate = None
		self.__coords = None

		# Create windows if in debugging mode
		self.__debug = debug
		if self.__debug:
			self.__create_trackbars()

	def __create_trackbars(self):
		cv.namedWindow(self.__winName)
		cv.createTrackbar('Threshold 1', self.__winName, self.__thres1, 1000, self.__update_thres1)
		cv.createTrackbar('Threshold 2', self.__winName, self.__thres2, 1000, self.__update_thres2)
		cv.createTrackbar('Epsilon', self.__winName, int(self.__epsilon*1000), 1000, self.__update_epsilon)

	def __update_thres1(self,value):  self.__thres1 = value; self.__on_change()
	def __update_thres2(self,value):  self.__thres2 = value; self.__on_change()
	def __update_epsilon(self,value):  self.__epsilon = value; self.__on_change()
	
	def __on_change(self):
		self.detect_plate()
		self.__draw_window()

	def __draw_window(self):
		tempFrame = np.copy(self.frame) # Make copy so we don't mod the orig
		rect = cv.minAreaRect(self.__coords)
		box = cv.boxPoints(rect)
		box = np.int0(box)
		cv.drawContours(tempFrame,[self.__coords],0,(0,0,255),2)
		cv.imshow(self.__winName,tempFrame)
		cv.imshow(self.__winName+'1', self.plate)
	
	def __calc_perspective(self, height = 300, width = 520):
		'''Get rectagular crop from a contour'''
		# FIXME: The images are coming out at random rotations. This needs to be fixed. Needs better algo?
		if self.__coords is None:
			self.__find_rect_contour()

		rect = cv.minAreaRect(self.__coords)
		peri=cv.arcLength(self.__coords, True)
		rect=cv.approxPolyDP(self.__coords, 0.02*peri, False)
		# box = cv.boxPoints(rect)
		location = np.int0(rect)

		# pts1 = np.float32([location[0], location[1], location[2], location[3]])
		pts1 = np.float32([location[0], location[3], location[2], location[1]])
		pts2 = np.float32([[0, 0], [width,0], [width,height], [0, height]])
		# Apply Perspective Transform Algorithm
		matrix = cv.getPerspectiveTransform(pts1, pts2)

		self.plate = cv.warpPerspective(np.copy(self.frame), matrix, (width, height))


	def __find_rect_contour(self):
		'''Find the largest rectagular contour in the frame'''
		# gray = cv.cvtColor(self.frame,cv.COLOR_BGR2GRAY)
		# blur = cv.GaussianBlur(gray, (9,9), 0)
		blur = cv.GaussianBlur(self.frame, (9,9), 0)
		canny = cv.Canny(blur,self.__thres1, self.__thres2)   # Detect edges
		contours, _ = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

		if not len(contours):
			print("No quadrilaterals found")
			return  np.array([ [-1, -1], [-1, -1], [-1, -1], [-1, -1] ])

		#  Find largest rectangle
		maxArea = 0
		for contour in contours:
			peri = cv.arcLength(contour, True)
			approx = cv.approxPolyDP(contour, self.__epsilon*peri, True)
			
			if len(approx) != 4: # Next if not rectangular
				continue

			(_,_,w,h) = cv.boundingRect(contour) # width, height
			rect_area = w*h
			
			if rect_area > maxArea:
				maxArea = rect_area
				self.__coords = contour

	def detect_plate(self):
		'''This function detects the number plate in the image.'''
		self.__find_rect_contour()
		self.__calc_perspective()

	# # pad numpy arrays helper from numpy.org
	# def __pad_with(self,vector, pad_width, iaxis, kwargs):
	# 		pad_value = kwargs.get('padder', 10)
	# 		vector[:pad_width[0]] = pad_value
	# 		vector[-pad_width[1]:] = pad_value

	def get_text(self):
		'''Get the lincense plate string from the crop image'''
		
		# Make a cropped image if not already done
		if self.plate is None:
			self.detect_plate()

		# roi = np.pad(self.plate, 20, self.__pad_with, padder=255)
		# roi = Image.fromarray(roi)

		pad=10
		# shade=200
		# roi = cv.copyMakeBorder(self.plate,pad,pad,pad,pad,cv.BORDER_CONSTANT,value=(shade,shade,shade))
		roi = cv.copyMakeBorder(self.plate,pad,pad,pad,pad,cv.BORDER_REPLICATE)
		text = pytesseract.image_to_string(roi, config='--psm 11')
		# cv.imshow('roi',roi)
		if not len(text):
			text = pytesseract.image_to_string(self.frame, config='--psm 11')
		for i in text.splitlines():
			if len(i) > 4 and True in [char.isdigit() for char in i]:
				print(i)
				self.text=i
				return
		# print(f'The text: {text}')
		for i in text.splitlines():
			if len(i) > 4:
				print(i)
				self.text=i
				return
		self.text = "Plate value not found."

def main():
	img1 = Detector('Challenges/public/images/Delaware_Plate.png','Delaware', True)
	img2 = Detector('Challenges/public/images/Contrast.jpg','Contrast', True)
	img3 = Detector('Challenges/public/images/Arizona_47.jpg','Arizonas', True)
	

	# new_img = img1.detect_plate()
	img1.get_text()
	img2.get_text()
	img3.get_text()
	cv.waitKey(0)

if __name__ == '__main__':
	main()