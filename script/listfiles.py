textList = ["One", "Two", "Three", "Four", "Five"]
mypath='/myDrive/'

outF = open("a.txt", "a")
for index,line in enumerate(textList):
  # write line to output file
  outF.write(mypath+line+str(index))
  outF.write("\n")

outF.close() 
