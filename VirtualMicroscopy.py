#######################################################################
# Creates a virtual microscopy plot of the input particle trajectory. #
#######################################################################
import math, sys, re, os

import numpy as np
from PIL import Image

#extension for reading the head/tail of a file ########################
class File(file):
	def head(self, lines_2find=1):
		self.seek(0)                            #Rewind file
		return [self.next() for x in xrange(lines_2find)]

	def tail(self, lines_2find=1):  
		self.seek(0, 2)                         #go to end of file
		bytes_in_file = self.tell()             
		lines_found, total_bytes_scanned = 0, 0
		while (lines_2find+1 > lines_found and
			bytes_in_file > total_bytes_scanned): 
			byte_block = min(1024, bytes_in_file-total_bytes_scanned)
			self.seek(-(byte_block+total_bytes_scanned), 2)
			total_bytes_scanned += byte_block
			lines_found += self.read(1024).count('\n')
		self.seek(-total_bytes_scanned, 2)
		line_list = list(self.readlines())
		return line_list[-lines_2find:]

#loading last timestep ################################################
path1 = "./" + sys.argv[1] + "/" + sys.argv[2] + "-IN/variables";
path2 = "./" + sys.argv[1] + "/" + sys.argv[2] + "-IN/" + sys.argv[3] + "/variables"

if os.path.exists(path1):
	variables = open(path1)
else:
	variables = open(path2);

contents = variables.read()

values = [x.strip() for x in contents.split(",")[2:]];
#values contain [rand,vol,pml,sumo1,sumo2,sumo3,sp100,daxx, repulsor]

scale = 2.0*float(values[1])

datei = File("./" + sys.argv[1] + "/" + sys.argv[2] + "-OUT/" + sys.argv[2] + sys.argv[3] +".lammpstrj","r")


head = datei.head(4)
numofmols = int(head[-1])
data = datei.tail(2*numofmols)
print numofmols
#Preparing DATA#######################################################
pml_data=[];
flag = 0
for index in range(len(data)):
	data[index] = data[index].split()
	if data[index][0] == '1':
		flag = 1
	if flag : 
		data[index][2] = round(float(data[index][2])*scale - float(values[1]),4) 
		data[index][3] = round(float(data[index][3])*scale - float(values[1]),4) 
		data[index][4] = round(float(data[index][4])*scale - float(values[1]),4) 
		pml_data.append(data[index]);
	if (data[index][0] == `numofmols`) and flag:
		flag = 0

#analysing the data###################################################
aim = ["2","3","4"] #molecules of interest:sumo1/2/3, pml, sp100, daxx, repulsor
radius = {'1':14.20 , '2':14.20 , '3':14.20 , '4':30.00 , '5':25.80 , '6': 28.80 }
colors = {'1':(255,0,0),'2':(255,154,0),'3':(185,180,172),'4':(255,255,0),'5':(0,0,255),'6':(255,255,255)}

dz = 800. #thickness of the layer we are scanning
cz = 000. # center of the layer

dimx = 1000 #pixel dimension x
dimy = 1000 #pixel dimension y

widthx = scale / dimx ; #width that one pixel has to cover
widthy = scale / dimy ;

countmap = np.zeros([dimx, dimy]); #empty map, counting the particles overlapping this pixel

#loop through all particles, aim constructing the artifical volume around and count up

for i in range(len(pml_data)):
	particle_type = pml_data[i][1]
	if particle_type in aim : #check for the right protein
		if cz-dz/2.  < pml_data[i][4] < cz+dz/2. : #centering thickness around middlepoint
			pos = (pml_data[i][2], pml_data[i][3])
			ix = int((float(values[1]) - pos[0]) / widthx)
			iy = int((float(values[1]) - pos[1]) / widthy)
			spherex = int(math.ceil(radius[particle_type] / widthx)) #pixels that we have to look around the center of a molecule
			spherey = int(math.ceil(radius[particle_type] / widthy)) #to cover the whole proteins volume
			for j in range(-spherex, spherex + 1):
				for k in range(-spherey, spherey + 1):
					new_pos = (j * widthx, k * widthy)
					if 0 <= ix + j < dimx and 0 <= iy + k < dimy:
						if new_pos[0]**2 + new_pos[1]**2 <= radius[particle_type]**2:
							countmap[ix+j][iy+k] = particle_type;

img = Image.new( 'RGB', (dimx,dimy), "black") # create a new black image
pixels = img.load() # create the pixel map
for i in range(img.size[0]):    # for every pixel:
	for j in range(img.size[1]):
		if countmap[i][j] >= 1:
			value = colors[str(int(countmap[i][j]))]
		else:
			value = (0,0,0)
		pixels[i,j] = value 

img.show()
