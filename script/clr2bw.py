from PIL import Image
column = Image.open('test.jpg')
gray = column.convert('L')
blackwhite = gray.point(lambda x: 0 if x < 127 else 255, '1')
blackwhite.save("test_bw.jpg")
