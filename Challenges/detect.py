import cv2 as cv
import numpy as np

class Detector:
	def __init__(self, img_name, img_path, debug=False):
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
		cv.drawContours(tempFrame,[box],0,(0,0,255),2)
		cv.imshow(self.winName,tempFrame)
		cv.imshow(self.winName+'1', self.plate)

	def detect_plate(self):
		'''
		This function detects the number plate in the image 
		and returns a cropped image focused on the number plate.
		'''
		self.coords = self.find_rect_contour()
		self.plate = self.get_perspective(self.coords)
	
	def get_perspective(self, contour, height = 500, width = 500):
		'''Get rectagular crop from a contour'''
		rect = cv.minAreaRect(contour)
		box = cv.boxPoints(rect)
		location = np.int0(box)
		pts1 = np.float32([location[0], location[3], location[1], location[2]])
		pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
		# Apply Perspective Transform Algorithm
		matrix = cv.getPerspectiveTransform(pts1, pts2)
		result = cv.warpPerspective(self.frame, matrix, (width, height))
		return result

		## Simple Method of cropping image
		# (x,y,w,h) = cv.boundingRect(box)
		# crop = self.frame[y:y+h,x:x+w]
		# return cv.resize(crop, (height,width))

	def find_rect_contour(self):
		'''Find the largest rectagular contour in the frame'''
		gray = cv.cvtColor(self.frame,cv.COLOR_BGR2GRAY)
		blur = cv.GaussianBlur(gray, (9,9), 0)
		canny = cv.Canny(blur,self.thres1, self.thres2)   # Detect edges
		contours, _ = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

		if not len(contours):
			print("No quadrilaterals found")
			return  np.array([ [-1, -1], [-1, -1], [-1, -1], [-1, -1] ])

		maxContour = None
		maxArea = 0

		#  Find largest rectangle
		for contour in contours:
			peri = cv.arcLength(contour, True)
			approx = cv.approxPolyDP(contour, 0.115*peri, True)
			
			if len(approx) != 4: # Next if not rectangular
				continue

			(_,_,w,h) = cv.boundingRect(contour) # width, height
			rect_area = w*h
			
			if rect_area > maxArea:
				maxArea = rect_area
				maxContour = contour

		return maxContour

def main():
	img1 = Detector('Delaware','Challenges/public/images/Delaware_Plate.png', True)
	img2 = Detector('Contrast','Challenges/public/images/Contrast.jpg', True)
	img3 = Detector('Arizonas','Challenges/public/images/Arizona_47.jpg', True)

	# img1.detect_plate()
	# img3.detect_plate()
	# img2.detect_plate()

	cv.waitKey(0)

if __name__ == '__main__':
	main()