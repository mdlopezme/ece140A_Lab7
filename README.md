# Lab 7
## Information
Olivier Rogers: A16069362  
Moises Lopez: A14156109

## Tutorial 1: Say Cheese!
In this tutorial we learned to install opencv2 onto the raspberry pi. And learned how to capture a image from a webcam in python.  

![Our first image capture!](Tutorials/Tutorial_1/test.jpg)


## Tutorial 2: Sudoku Extractor  
Tesseract and PyTesseract were installed for OCR. PyTesseract was used with OpenCV to extract a sudoku puzzle from an image.  
The default settings did not result in any extracted values. Some things learned:  
- Tesseract does not work very well with single characters. Strings are better.
- The current version prefers black text on white backgrounds.
- The best results for this example were obtained on an image with minimal blurring, with threshold applied, and with a little bit of padding on each cropped segment.
- We tried removing the borders (from the Sudoku grid), but that resulted in worse number detection.


