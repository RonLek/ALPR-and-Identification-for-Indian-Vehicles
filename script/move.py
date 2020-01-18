import os, sys
import shutil
def move():
  path = (os.getcwd()+'/data')
  i=0
  for item in os.listdir(path):
    print(item)
    if i%2==0:
      	shutil.move('data/' +item, 'final')
      	print(item) 
    i+=1


move()
