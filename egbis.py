#!/usr/bin/python

import egbislib
import sys

# falcon: exp=-4, sigma=0.8, k=3.0, R=1 -> runs 25 seconds
# falcon: exp=-4, sigma=1.3, k=2.5, R=3
# shapes: exp=-2, sigma=0.8, k=3.0, R=1 -> runs 3 minutes (10GB RAM!!)
# shapes: exp=-3, sigma=0.8, k=2.5, R=3

def runSegmentation(name, extension, exp=0, sigma=0, k=1.0, R=1):
	"""
	Method running the whole algorithm. Image is loaded, converted to grayscale
	and converted to a graph which is then used for the segmentation algorithm.
	Results are then shown and stored as image files.
	Args:
		name:		file name of the image (with optional path)
		extension:	file extension of the image file
		exp:		exponent for image scaling
		sigma:		standard deviation for image smoothing (gaussian)
		k:			factor for merging threshold function
		R:			neighborhood distance limit (in pixels)
	Returns: exit status
	"""
	print "running algorithm with settings:"
	print "\tfilename:", name+extension
	print "\texp:     ", exp
	print "\tsigma:   ", sigma
	print "\tk:       ", k
	print "\tR:       ", R

	img_raw = egbislib.imageToGray(egbislib.loadImage(name+extension))
	img_raw = egbislib.scaleImage(img_raw, exp)
	img = egbislib.preprocess(img_raw, sigma=sigma)
	#egbislib.showImage(img)
	if R == 0:
		(G, V) = egbislib.directNeighborGraph(img)
	else:
		(G, V) = egbislib.distanceThresholdGraph(img, R=R)
	#egbislib.showGraph(G)
	seg = egbislib.segmentate(G, V, k=k)
	segImage = seg.toImage(img.shape)
	egbislib.saveImage(segImage, name+"_e"+str(exp)+"_sigma"+str(sigma)+
							"_k"+str(k)+"_R"+str(R)+extension)
	egbislib.showStereo(img_raw, segImage)
	return 0

if __name__ == "__main__":
	"""
	Main method to handle help and parameter settings.
	"""
	if len(sys.argv) < 2 or "-h" in sys.argv or "--help" in sys.argv:
		print "usage: python egbis.py \n\t\t\t[--exp <exp>]\t\t(default: 0)\
									\n\t\t\t[--sigma <sigma>]\t(default: 0.0)\
									\n\t\t\t[--k <k>]\t\t(default: 1.0)\
									\n\t\t\t[--R <R>]\t\t(default: 1.0)\
									\n\t\t\t <image-file>\n"
		print "exp:\texponent for image scaling. Factor will be 2^exp\n"+\
				"\t\tfor negative exp the image size will be reduced.\n"+\
				"sigma:\tstandard deviation for gaussian image smoothing\n"+\
				"\t\tto reduce artifacts\n"+\
				"k:\tfactor for component merging threshold function. The\n"+\
				"\t\tlarger the value, the more likely is it for components\n"+\
				"\t\tto be merged.\n"+\
				"R:\trange of neighborhood relationships (in pixels)\n"+\
				"\t\tR=0 will enable simple neightborhood edges method."
		sys.exit(0)

	sigma = 0; exp = 0; k = 1; R = 1
	
	imagefile = sys.argv[-1].split(".")
	if len(imagefile) > 2:
		print "files with dots not supported!"
		sys.exit(0)
	name = imagefile[0]
	extension = "."+imagefile[1]

	if "--exp" in sys.argv:
		i = sys.argv.index("--exp")
		exp = int(sys.argv[i+1])
	if "--sigma" in sys.argv:
		i = sys.argv.index("--sigma")
		sigma = float(sys.argv[i+1])
	if "--k" in sys.argv:
		i = sys.argv.index("--k")
		k = float(sys.argv[i+1])
	if "--R" in sys.argv:
		i = sys.argv.index("--R")
		R = float(sys.argv[i+1])

	runSegmentation(name, extension, exp=exp, sigma=sigma, k=k, R=R)
