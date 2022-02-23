import cv2
cam = cv2.VideoCapture(0) # Initialize the camera module
ret, image = cam.read() # Get the values (pixels) read by the camera
cv2.imwrite('./test.jpg', image) # Write these values to your Pi
cam.release() # Very Imp: Releasing the camera object
# It is necessary to release the object so that the camera does not keep running or crash because of an improper shutdown
