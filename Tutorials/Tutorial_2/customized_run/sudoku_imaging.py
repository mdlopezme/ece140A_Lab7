# Import OpenCV
import cv2
import numpy as np
from PIL import Image
import pytesseract
import time

# Read the image
image_url = "Tutorials/Tutorial_2/sudoku_test.jpeg"
img = cv2.imread(image_url, 0)
# 0 is a simple alias for cv2.IMREAD_GRAYSCALE
# cv2.imshow('original image',img)
# cv2.waitKey(0)

# Preprocessing

# Add a Gaussian Blur to smoothen the noise
blur = cv2.GaussianBlur(img.copy(), (1, 1), 0)
# cv2.imwrite("Blur.png", blur)
# cv2.imshow('blur',blur)
# cv2.waitKey(0)

# Threshold the image to get a binary image
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
# cv2.imwrite("Threshold.png", thresh)
# cv2.imshow('thresh',thresh)
# cv2.waitKey(0)

# Invert the image to swap the foreground and background
invert = 255 - thresh
# cv2.imwrite("Inverted.png", invert)
# cv2.imshow('invert',invert)
# cv2.waitKey(0)

# Dilate the image to join disconnected fragments
kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)
dilated = cv2.dilate(invert, kernel)
# cv2.imwrite("Dilated.png", dilated)
# cv2.imshow('dilate',dilated)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


### Contours and Polygons

# Get contours
contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the largest 15 contours
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]

# Find best polygon and get location
location = None

# Finds rectangular contour
for contour in contours:
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02*peri, True) 
    if len(approx) == 4:
        location = approx
        break

# Handle cases when no quadrilaterals are found        
if type(location) != type(None):
    print("Corners of the contour are: ",location)
else:
    print("No quadrilaterals found")

# Sudoku Specific: Transform a skewed quadrilateral
def get_perspective(img, location, height = 900, width = 900):
    pts1 = np.float32([location[0], location[3], location[1], location[2]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (width, height))
    return result

if type(location) != type(None):
    result = get_perspective(img, location)
    result = cv2.rotate(result, cv2.ROTATE_90_CLOCKWISE)
    # cv2.imwrite("Result.png", result)
    # cv2.imshow('result',result)
    # cv2.waitKey(0)
    result = get_perspective(thresh, location)
    result = cv2.rotate(result, cv2.ROTATE_90_CLOCKWISE)
    # cv2.imshow('result',result)
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows()
    
print('Extracting the Numbers')

# pad numpy arrays helper from numpy.org
def pad_with(vector, pad_width, iaxis, kwargs):
    pad_value = kwargs.get('padder', 10)
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value

# Split the board into 81 blocks
def split_boxes(board, input_size=40):
  rows = np.vsplit(board,9)
  boxes = []
  n = 5
  for r in rows:
    cols = np.hsplit(r,9)
    for box in cols:
      # box = box[n:-n,n:-n]
      box = np.pad(box, 20, pad_with, padder=255)
      # box = cv2.resize(box, (input_size, input_size))/255.0
      box = cv2.GaussianBlur(box, (3, 3), 0)
      boxes.append(box)
  return boxes

ans = split_boxes(result)
# print(ans[0])
# for i in range(9):
#   cv2.imshow(f'{9*i+3}',ans[i*9+2])
  # cv2.waitKey(1)
# cv2.imshow(f'{i+1}',ans[80])
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.imshow('1,5',ans[4])
# cv2.waitKey(0)
# cv2.imshow('2,5',ans[9+4])
# cv2.waitKey(0)



# Get text from each box
# out = [[0]*9]*9 # weird output
out = np.zeros((9,9))

# print(out)
for i in range(9):
  print(f'row {i+1}')
  for j in range(9):

    cv2.imshow('image block', ans[9*i+j])

    text = pytesseract.image_to_string(
      Image.fromarray(ans[9*i+j].astype(np.uint8)),
      lang='eng', config='--psm 11')
    if not len(text):
      continue
    # print(text[0])
    if ord(text[0]) >= 48 and ord(text[0]) <= 57:
      print(f'adding {text[0]} to matrix at {(i,j)}')
      out[i][j] = text[0]
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
cv2.destroyAllWindows()
print("The grid detected is as follows:\n",out)
