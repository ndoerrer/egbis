#!/usr/bin/python

import egbislib

# falcon: exp=-4, sigma=0.8, k=3.0, R=1 -> runs 25 seconds
# falcon: exp=-4, sigma=1.3, k=2.5, R=3
# shapes: exp=-2, sigma=0.8, k=3.0, R=1 -> runs 3 minutes (10GB RAM!!)
# shapes: exp=-3, sigma=0.8, k=2.5, R=3

def runSegmentation(name, extension, exp, sigma, k, R=1):
	img_raw = egbislib.imageToGray(egbislib.loadImage(name+extension))
	img_raw = egbislib.scaleImage(img_raw, exp)
	img = egbislib.preprocess(img_raw, sigma=sigma)
	#egbislib.showImage(img)
#	(G, V) = egbislib.directNeighborGraph(img)
	(G, V) = egbislib.distanceThresholdGraph(img, R=R)
	#egbislib.showGraph(G)
	seg = egbislib.segmentate(G, V, k=k)
	segImage = seg.toImage(img.shape)
	egbislib.saveImage(img, name+"_e"+str(exp)+"_sigma"+str(sigma)+
							"_k"+str(k)+"_R"+str(R)+extension)
	egbislib.showStereo(img_raw, segImage)



if __name__ == "__main__":
#	name = "shapes"
#	extension = ".png"
#	exp = -3
#	sigma = 0.8
#	k = 2.5

	name = "falcon"
	extension = ".jpg"
	exp = -4
	sigma = 1.3
	k = 2.0

	R = 3

	runSegmentation(name, extension, exp, sigma, k, R=R)
