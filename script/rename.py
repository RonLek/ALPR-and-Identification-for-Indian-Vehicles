import os
path = 'final/'
files = os.listdir(path)


for index, file in enumerate(files):
  os.rename(os.path.join(path, file), os.path.join(path, ''.join(['obj', str(index), '.jpg'])))
