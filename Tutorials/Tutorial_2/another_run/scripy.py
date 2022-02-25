from PIL import Image
import pytesseract

img = Image.open('testocr.png')
text = pytesseract.image_to_string(img)
print(text)
