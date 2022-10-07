import os
import subprocess

if not os.path.isfile('data/fra.traineddata'):
    url = 'https://github.com/tesseract-ocr/tessdata/raw/main/fra.traineddata'
    subprocess.run(["wget", url]) 
    subprocess.run(["mv","fra.traineddata","data/fra.traineddata"]) 
