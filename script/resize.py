from PIL import Image
import os, sys
path = ('/home/controller/Desktop/vid2img/data/')

def resize():
  for item in os.listdir(path):
    if os.path.isfile(item):
      im = Image.open(item)
      f, e = os.path.splitext(item)
      imResize = im.resize((480,720), Image.ANTIALIAS)
      imResize.save('/home/controller/Desktop/vid2img/resized/' + ' resized.jpg', 'JPEG', quality=90)

resize()
