from PIL import Image
import os, sys
path = ('/home/controller/Downloads')

def resize():
  for item in os.listdir(path):
    if os.path.isfile(item):
      im = Image.open(item)
      f, e = os.path.splitext(item)
      imResize = im.resize((80,40), Image.ANTIALIAS)
      imResize.save('/home/controller/Downloads/' + ' resized.jpg', 'JPEG', quality=90)

resize()
