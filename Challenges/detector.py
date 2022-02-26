import cv2
import numpy as np
from PIL import Image
import pytesseract
import time

def get_perspective(img, location, height = 900, width = 900):
  # cv2.imshow('passed in image',img)
  pts1 = np.float32([location[0], location[3], location[1], location[2]])
  pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
  # Apply Perspective Transform Algorithm
  matrix = cv2.getPerspectiveTransform(pts1, pts2)
  result = cv2.warpPerspective(img, matrix, (width, height))
  cv2.imshow('get_perspective',result)
  cv2.waitKey(0)
  return result

def detect_plate(img):
  blur = cv2.GaussianBlur(img, (5, 5), 0)
  # cv2.imshow('blur',blur)
  # cv2.waitKey(0)
  thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
  cv2.imshow('thresh',thresh)
  # cv2.waitKey(0)
  invert = 255 - thresh
  # kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)
  # dilated = cv2.dilate(invert, kernel)
  # cv2.imshow('dilate',dilated)
  # cv2.waitKey(0)
  # contours, hierarchy = cv2.findContours(invert, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  contours, hierarchy = cv2.findContours(invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]
  location = None
  for contour in contours:
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.03*peri, True) 
    if len(approx) == 4:
      location = approx
      break
  if type(location) != type(None):
    print("Corners of the contour are: ",location)
    roi = get_perspective(img, location)
    roi = cv2.rotate(roi, cv2.ROTATE_90_CLOCKWISE)
    cv2.imshow('rotated image',roi)
  else:
    print("No quadrilaterals found")
    return
  coord=[]
  return (roi, coord)

def get_text(img):
  text=[]
  return text

if __name__ == "__main__":
  # image_url = "./public/images/Arizona_47.jpg"
  # image_url = "./public/images/Contrast.jpg"
  image_url = "./public/images/Delaware_Plate.png"
  img = cv2.imread(image_url, 0)
  cv2.normalize(img, img, 50, 255, cv2.NORM_MINMAX)
  detect_plate(img)