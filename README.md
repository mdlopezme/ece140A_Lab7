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
- Changing the `psm` parameter to 10 instead of 11 improved the single character recognition.
- The current version prefers black text on white backgrounds.
- The best results were obtained on an image with minimal blurring and with threshold applied.