import cv2
import uuid
import numpy as np
from pytesseract import pytesseract
#Passe o caminho do diretorio de onde o seu tesseract esta salvo:
pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

try:
    from PIL import Image
except ImportError:
    import Image



# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    canny_ = cv2.Canny(image, 100, 200)
    #save_path = r"C:\Users\Pedro\Desktop\TCC2C\license-plate-recognition-main\images"
    #outfile = save_path+'\%s.jpg' % (str(uuid.uuid4())+'"')
    save_path = r"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\images"
    edited_image = cv2.imwrite(save_path,image)
    return canny_ ,edited_image
