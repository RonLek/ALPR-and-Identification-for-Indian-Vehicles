import argparse
import sys
import re
import os
import requests
import cv2
import json 
import numpy as np
from time import sleep
from selenium import webdriver
try:
    import Image
except ImportError:
    from PIL import Image, ImageEnhance
from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import urlretrieve
from io import BytesIO

app_url = 'https://vahan.nic.in/nrservices/faces/user/searchstatus.xhtml'
captcha_image_url = 'https://vahan.nic.in/nrservices/cap_img.jsp'
number = sys.argv[1]

driver = webdriver.Chrome("C:\\Users\\hp\\Chrome WebDriver\\chromedriver.exe")
driver.get('https://vahan.nic.in/nrservices/faces/user/searchstatus.xhtml');

def detect_captcha(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    captcha = texts[0].description
    return captcha

# sleep(5)

#TODO: Add functionality to repeat detection in case of incorrect OCR
captcha_image = driver.find_elements_by_class_name("captcha-image")[0]
driver.save_screenshot('screenshot.png')
location = captcha_image.location
size = captcha_image.size

image = Image.open('screenshot.png')
left = location['x']
top = location['y'] 
right = location['x'] + size['width']
bottom = location['y'] + size['height'] 
image = image.crop((left, top, right, bottom))  # defines crop points
image.save('downloadedpng.png', 'png')  # saves new cropped image

print('Resolving Captcha')
extracted_text = detect_captcha('downloadedpng.png')
print("OCR Result => ", extracted_text)
print(extracted_text)

vehicle_number = driver.find_element_by_id('regn_no1_exact')
captcha_input = driver.find_element_by_id('txt_ALPHA_NUMERIC')
vehicle_number.send_keys(number)
captcha_input.send_keys(extracted_text)
button = driver.find_elements_by_tag_name('button')[1]
button.click()
