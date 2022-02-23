# Import OpenCV
import cv2
import numpy as np
from PIL import Image
import pytesseract

# Read the image
image_url = "./sudoku_test.jpeg"
img = cv2.imread(image_url, cv2.IMREAD_GRAYSCALE)

# Preprocessing

# Add a Gaussin blur to smoothen the noise
blur = cv2.GaussianBlur(np.copy(img), (9,9), 0)
cv2.imwrite("Blur.png", blur)

# Threshold the image to get a binary image
_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cv2.imwrite("Threshold.png", thresh)

# Invert image to swap the foreground and background
invert = 255 - thresh
cv2.imwrite("Inverted.png", invert)

# Dilate the image to join disconnected fragments
kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)
dilated = cv2.dilate(invert, kernel)
cv2.imwrite("Dilated.png", dilated)

# Get contours
contours, hierarchy  = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the largest 15 contours
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]

# Find best polygon and get location
location = None

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
	cv2.imwrite("Result.png", result)

# Split the board into 81 blocks
def split_boxes(board, input_size=100):
	rows = np.vsplit(board,9)
	boxes = []
	for r in rows:
		cols = np.hsplit(r,9)
		for box in cols:
			box = cv2.resize(box, (input_size, input_size))/255.0
			boxes.append(box)
	return boxes

ans = split_boxes(result)


# Get text from each box
out = [[0]*9]*9
for i in range(9):
	for j in range(9):
		
		cv2.imshow('Analizing', ans[9*i+j])
		
		text = pytesseract.image_to_string(
			Image.fromarray(ans[9*i+j].astype(np.uint8)),
			lang='eng', config='--psm 11')

		if ord(text[0]) >= 48 and ord(text[0]) <= 57:
			out[i][j] = text[0]

		print(f'Processing box {(i+1,j+1)}, {ord(text[0])}', end='\r' )
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

print("The grid detected is as follows:\n",out)