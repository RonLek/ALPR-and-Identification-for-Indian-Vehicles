import os

path = os.getcwd()

for i in range(967):
	if not os.path.exists(os.path.join(path,'images', 'obj'+str(i)+'.txt')):
                print(i,"doesn't exist")
