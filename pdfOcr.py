import pdf2image
from PIL import Image
import pytesseract
import numpy as np
import cv2
import tempfile
import cv2
import numpy as np
from PIL import Image
import checkEnv
import os
IMAGE_SIZE = 1800
BINARY_THREHOLD = 180

def tesseractProcess(img):
    os.getcwd()+"/data"
    os.environ['TESSDATA_PREFIX']= os.getcwd()+"/data"
    tessdata_dir_config = '--tessdata-dir \"'+os.getcwd()+"/data"+'\"'
    custom_config = r'--oem 3 --psm 6 '
    return pytesseract.image_to_string(img, config=custom_config,lang='fra')


def process_image_for_ocr(image):
    # TODO : Implement using opencv
    temp_filename = set_image_dpi(image)
    im_new = remove_noise_and_smooth(temp_filename)
    return im_new

def set_image_dpi(image):
    im = image
    length_x, width_y = im.size
    factor = max(1, int(IMAGE_SIZE / length_x))
    size = factor * length_x, factor * width_y
    # size = (1800, 1800)
    im_resized = im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))
    return temp_filename

def image_smoothening(img):
    ret1, th1 = cv2.threshold(img, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3

def remove_noise_and_smooth(file_name):
    img = cv2.imread(file_name, 0)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41,
                                     3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image

def rgb2gray(image):
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return img

def pdf_to_img(pdf_file):
    print(pdf_file)
    return pdf2image.convert_from_path(pdf_file)


async def OCRProcess(pdf_file):
    images = pdf_to_img(pdf_file)
    out={}
    out['pages'] = {}
    for pg, img in enumerate(images):
        res = process_image_for_ocr(img)
        result = tesseractProcess(res)
        out['pages'][str(pg)]=result
    return out

