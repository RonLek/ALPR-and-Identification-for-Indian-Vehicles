import pytesseract
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

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
app_url = 'https://vahan.nic.in/nrservices/faces/user/searchstatus.xhtml'
captcha_image_url = 'https://vahan.nic.in/nrservices/cap_img.jsp'
number = sys.argv[1]

driver = webdriver.Chrome("C:\\Users\\hp\\Chrome WebDriver\\chromedriver.exe")
driver.get('https://vahan.nic.in/nrservices/faces/user/searchstatus.xhtml');

def resolve():
	enhancedImage = enhance()
	return pytesseract.image_to_string(enhancedImage)

def enhance():
	img = cv2.imread('downloadedpng.png', 0)
	kernel = np.ones((2,2), np.uint8)
	img_erosion = cv2.erode(img, kernel, iterations=1)
	img_dilation = cv2.dilate(img, kernel, iterations=1)
	erosion_again = cv2.erode(img_dilation, kernel, iterations=1)
	final = cv2.GaussianBlur(erosion_again, (1, 1), 0)
	return final

# sleep(5)

#TODO: Add functionality to repeat detection in case of incorrect OCR
#while(driver.find_element_by_id('rcDetailsPanel') == None):
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
captcha_text = resolve()
extracted_text = captcha_text.replace(" ", "").replace("\n", "")
print("OCR Result => ", extracted_text)
print(extracted_text)

vehicle_number = driver.find_element_by_id('regn_no1_exact')
captcha_input = driver.find_element_by_id('txt_ALPHA_NUMERIC')
button = driver.find_element_by_id('j_idt47')
vehicle_number.send_keys(number)
captcha_input.send_keys(extracted_text)
button.click()

# with open('downloadedpng.png', 'wb') as file:
#     file.write(captcha_image.screenshot_as_png)

# #MARK: Get Request to get webpage elements like textFields, image, etc
# r = requests.get(url=app_url)
# cookies = r.cookies
# soup = BeautifulSoup(r.text, 'html.parser')

# #MARK: ViewState contains token which needs to be passed in POST Request
# # ViewState is a hidden element. Open debugger to inspect element 
# viewstate = soup.select('input[name="javax.faces.ViewState"]')[0]['value']

#MARK: Get Request to get Captcha Image from URL
## Captcha Image Changes each time the URL is fired
# iresponse = requests.get(captcha_image_url)
# img = Image.open(BytesIO(iresponse.content))
# img.save("downloadedpng.png")


# # MARK: Identifying Submit Button which will be responsible to make POST Request
# button = soup.find("button",{"type": "submit"})


# encodedViewState = viewstate.replace("/", "%2F").replace("+", "%2B").replace("=", "%3D")

# # MARK: Data, which needs to be passed in POST Request | Verify this manually in debugger
# data = {
# 	'javax.faces.partial.ajax':'true',
# 	'javax.faces.source': button['id'],
# 	'javax.faces.partial.execute':'@all',
# 	'javax.faces.partial.render': 'rcDetailsPanel resultPanel userMessages capatcha txt_ALPHA_NUMERIC',
# 	button['id']:button['id'],
# 	'masterLayout':'masterLayout',
# 	'regn_no1_exact': number,
# 	'txt_ALPHA_NUMERIC': extracted_text,
# 	'javax.faces.ViewState': viewstate,
# 	'j_idt32':''
# }
# # MARK: Data in Query format.. But not in use for now
# query = "javax.faces.partial.ajax=true&javax.faces.source=%s&javax.faces.partial.execute=%s&javax.faces.partial.render=rcDetailsPanel+resultPanel+userMessages+capatcha+txt_ALPHA_NUMERIC&j_idt42=j_idt42&masterLayout=masterLayout&j_idt32=&regn_no1_exact=%s&txt_ALPHA_NUMERIC=%s&javax.faces.ViewState=%s"%(button['id'], '%40all', number, extracted_text, encodedViewState)


# # MARK: Request Headers which may or may not needed to be passed in POST Request
# # Verify in debugger
# headers = {
# 	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
# 	'Accept': 'application/xml, text/xml, */*; q=0.01',
# 	'Accept-Language': 'en-us',
# 	'Accept-Encoding': 'gzip, deflate, br',
# 	'Host': 'vahan.nic.in',
# 	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15',
# 	'Cookie': 'JSESSIONID=%s; SERVERID_7081=vahanapi_7081; SERVERID_7082=nrservice_7082' % cookies['JSESSIONID'],
# 	'X-Requested-With':'XMLHttpRequest',
# 	'Faces-Request':'partial/ajax',
# 	'Origin':'https://vahan.nic.in',
# 	'Referer':'https://vahan.nic.in/nrservices/faces/user/searchstatus.xhtml',
#     'Connection':'keep-alive'
#     # 'User-Agent': 'python-requests/0.8.0',
#     # 'Access-Control-Allow-Origin':'*',
# }
# print(headers)

# print("\nCookie JSESSIONID => ", cookies['JSESSIONID'])
# print("\nData => \n")
# print(data)

# # MARK: Added delay
# sleep(2.0)



# #MARK: Send POST Request 
# postResponse = requests.post(url=app_url, data=data, headers=headers, cookies=cookies)
# print("\nPOST Request -> Response =>\n")
# print(postResponse)

# rsoup = BeautifulSoup(postResponse.text, 'html.parser')
# print("Mark: postResponse soup => ")
# print(rsoup.prettify())

# #MARK: Following code finds tr which means <table> element from html response
# # the required response is appended in <table> only. Verify it in debugger
# table = SoupStrainer('tr')
# tsoup = BeautifulSoup(rsoup.get_text(), 'html.parser', parse_only=table)

# print("Table Soup => ")
# print(tsoup.prettify())
# #MARK: Result Table not appending to the response data
# #Fix Needed
