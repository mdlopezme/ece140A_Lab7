import cv2 as cv
import numpy as np

class Detector:
	def __init__(self, img_path, img_name='default', debug=False):
		# Set window name when showing the image
		self.winName = img_name

		# Pre-process the image
		img = cv.imread(img_path)
		self.frame = cv.resize(img, (480,360))

		# This are some good threshold values I have found.
		self.thres1 = 91
		self.thres2 = 81
		self.epsilon = 0.115

		# Create windows if in debugging mode
		self.debug = debug
		if self.debug:
			self.create_trackbars()

	def create_trackbars(self):
		cv.namedWindow(self.winName)
		cv.createTrackbar('Threshold 1', self.winName, self.thres1, 1000, self.update_thres1)
		cv.createTrackbar('Threshold 2', self.winName, self.thres2, 1000, self.update_thres2)
		cv.createTrackbar('Epsilon', self.winName, int(self.epsilon*1000), 1000, self.update_epsilon)

	def update_thres1(self,value):  self.thres1 = value; self.on_change()
	def update_thres2(self,value):  self.thres2 = value; self.on_change()
	def update_epsilon(self,value):  self.epsilon = value; self.on_change()
	
	def on_change(self):
		self.detect_plate()
		self.draw_window()

	def draw_window(self):
		tempFrame = np.copy(self.frame) # Make copy so we don't mod the orig
		rect = cv.minAreaRect(self.coords)
		box = cv.boxPoints(rect)
		box = np.int0(box)
		cv.drawContours(tempFrame,[self.coords],0,(0,0,255),2)
		cv.imshow(self.winName,tempFrame)
		cv.imshow(self.winName+'1', self.plate)

	def detect_plate(self):
		'''
		This function detects the number plate in the image 
		and returns a cropped image focused on the number plate.
		'''
		self.__find_rect_contour()
		self.__calc_perspective()

		return self.plate
	
	def __calc_perspective(self, height = 500, width = 500):
		'''Get rectagular crop from a contour'''
		# FIXME: The images are coming out at random rotations. This needs to be fixed. Needs better algo?
		if self.coords is None:
			self.__find_rect_contour()

		rect = cv.minAreaRect(self.coords)
		box = cv.boxPoints(rect)
		location = np.int0(box)
		pts1 = np.float32([location[0], location[3], location[1], location[2]])
		pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
		# Apply Perspective Transform Algorithm
		matrix = cv.getPerspectiveTransform(pts1, pts2)
		self.plate = cv.warpPerspective(np.copy(self.frame), matrix, (width, height))

	def __find_rect_contour(self):
		'''Find the largest rectagular contour in the frame'''
		gray = cv.cvtColor(self.frame,cv.COLOR_BGR2GRAY)
		blur = cv.GaussianBlur(gray, (9,9), 0)
		canny = cv.Canny(blur,self.thres1, self.thres2)   # Detect edges
		contours, _ = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

		if not len(contours):
			print("No quadrilaterals found")
			return  np.array([ [-1, -1], [-1, -1], [-1, -1], [-1, -1] ])

		#  Find largest rectangle
		maxArea = 0
		for contour in contours:
			peri = cv.arcLength(contour, True)
			approx = cv.approxPolyDP(contour, self.epsilon*peri, True)
			
			if len(approx) != 4: # Next if not rectangular
				continue

			(_,_,w,h) = cv.boundingRect(contour) # width, height
			rect_area = w*h
			
			if rect_area > maxArea:
				maxArea = rect_area
				self.coords = contour

	def get_text(self):
		'''Get the lincense plate string from the crop image'''
		
		# Make a cropped image if not already done
		if self.plate is None:
			self.detect_plate()

		roi = self.plate # :P
		self.text = 'UNDER DEVELOPMENT'

def main():
	img1 = Detector('Challenges/public/images/Delaware_Plate.png','Delaware', True)
	img2 = Detector('Challenges/public/images/Contrast.jpg','Contrast', True)
	img3 = Detector('Challenges/public/images/Arizona_47.jpg','Arizonas', True)

	cv.waitKey(0)

if __name__ == '__main__':
	main()