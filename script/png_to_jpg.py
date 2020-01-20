from PIL import Image

for i in range(61):
	st='IIITA/obj'+str(i)+'.png'
	st1='obj'+str(i)+'.jpg'
	im = Image.open(st)
	rgb_im = im.convert('RGB')
	rgb_im.save(st1)
