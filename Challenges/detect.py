import cv2 as cv
from cv2 import blur
import numpy as np

class Detector:
    def __init__(self, img_name, img_path):
        # Set window name when showing the image
        self.winName = img_name

        # Pre-process the image
        img = cv.imread(img_path)
        self.frame = cv.resize(img, (480,360))

    def detect_plate(self):
        '''
        This function detects the number plate in the image 
        and returns a cropped image focused on the number plate.
        '''
        self.coords = self.find_rect_contour()
        self.plate = self.get_perspective(self.coords)
    
    def get_perspective(self, contour, height = 500, width = 500):
        '''Get rectagular crop from a contour'''
        (x,y,w,h) = cv.boundingRect(contour)
        crop = self.frame[y:y+h,x:x+w]
        return cv.resize(crop, (height,width))

    def find_rect_contour(self):
        '''Find the largest rectagular contour in the frame'''
        gray = cv.cvtColor(self.frame,cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray, (9,9), 0)
        canny = cv.Canny(blur,91, 81)   # Detect edges
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
                maxContour = approx

        return maxContour

def main():
    img1 = Detector('Delaware','Challenges/public/images/Delaware_Plate.png')
    img2 = Detector('Contrast','Challenges/public/images/Contrast.jpg')
    img3 = Detector('Arizonas','Challenges/public/images/Arizona_47.jpg')

    img1.detect_plate()
    img3.detect_plate()
    img2.detect_plate()

    # Just for showing that it works
    cv.imshow('Test1', img1.plate)
    cv.imshow('Test2', img2.plate)
    cv.imshow('Test3', img3.plate)

    cv.waitKey(0)

if __name__ == '__main__':
    main()