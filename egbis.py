#!/usr/bin/python
# -*- coding: utf_8 -*-

import egbislib
import sys
from skimage.segmentation import felzenszwalb

# falcon: exp=-4, sigma=0.8, k=3.0, R=1 -> runs 25 seconds
# falcon: exp=-4, sigma=1.3, k=2.5, R=3
# falcon: exp=-2, sigma=1.3, k=2.5, R=3 weighted -> runs 8 hours :/
# shapes: exp=-2, sigma=0.8, k=3.0, R=1 -> runs 3 minutes (10GB RAM!!)
# shapes: exp=-3, sigma=0.8, k=2.5, R=3

# fifastats.csv: R=200, k=4000, rows=2000 -> runs 45 minutes
# fifastats.csv: R=250, k=4000, rows=400 -> runs 15 seconds

#Remark: storing all pairwise differences would need 2474983368 Bytes ~ 2.5 GB
# of space and a veeeeery long time to compute

def runSegmentation(name, extension, exp=0, sigma=0, k=1.0, R=1,
								weighted=False, useskimage=False, rows=-1):
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
		weighted:	if a linear increase of weights with distance should be used
		rows:		(for CSV) how many rows should be processed (from start)
		useskimage:	whether to use the skimage implementation instead of this
	Returns: exit status
	"""
	if extension == ".jpg" or extension == ".png" or extension == ".tif":
		print "running algorithm on image with settings:"
		print "\tfilename:", name+extension
		print "\texp:     ", exp
		print "\tsigma:   ", sigma
		print "\tk:       ", k
		print "\tR:       ", R
		print "\tweighted:", weighted
		print "\tuseskimage:", useskimage

		img_raw = egbislib.imageToGray(egbislib.loadImage(name+extension))
		img_raw = egbislib.scaleImage(img_raw, exp)

		if useskimage:
			segImage = felzenszwalb(img_raw, scale=k, sigma=sigma, min_size=1)

		else:
			img = egbislib.preprocess(img_raw, sigma=sigma)

			if R == 0:
				(G, V) = egbislib.directNeighborGraph(img)
			else:
				if not weighted:
					(G, V) = egbislib.distanceThresholdGraph(img, R=R)
				else:
					(G, V) = egbislib.distanceWeightedThresholdGraph(img, R=R)

			seg = egbislib.segmentate(G, V, k=k)
			segImage = seg.toImage(img.shape)

		if not weighted:
			egbislib.saveImage(segImage, name+"_e"+str(exp)+"_sigma"+str(sigma)+
								"_k"+str(k)+"_R"+str(R)+extension)
		else:
			egbislib.saveImage(segImage, name+"_e"+str(exp)+"_sigma"+str(sigma)+
								"_k"+str(k)+"_R"+str(R)+"w"+extension)	
		egbislib.showStereo(img_raw, segImage)

	if extension == ".csv":
		print "running algorithm on csv with settings:"
		print "\tfilename:", name+extension
		print "\trows:     ", rows
		print "\tk:       ", k
		print "\tR:       ", R

		table = egbislib.loadCSV(name+extension, rows=rows)
		(G, V) = egbislib.csvToGraph(table, R=R)
		#egbislib.showGraph(G)
		seg = egbislib.segmentate(G, V, k=k)
		label_list = seg.toLabelList()
		#print label_list
		egbislib.storeAllAttributeStatistics(name,
										table, label_list)
		pca_data = egbislib.pcaTransform(table)
		egbislib.colorScatterPlot(pca_data, label_list, name)

if __name__ == "__main__":
	"""
	Main method to handle help and parameter settings.
	"""
	if len(sys.argv) < 2 or "-h" in sys.argv or "--help" in sys.argv:
		print "usage: python egbis.py \n\t\t\t[--exp <exp>]\t\t(default: 0)\
									\n\t\t\t[--sigma <sigma>]\t(default: 0.0)\
									\n\t\t\t[--k <k>]\t\t(default: 1.0)\
									\n\t\t\t[--R <R>]\t\t(default: 1.0)\
									\n\t\t\t[--rows <rows>]\t\t(default: all)\
									\n\t\t\t[--weighted]\t\t(default: not)\
									\n\t\t\t <image/csv-file>\n"
		print "exp:\t\t(for images) exponent for image scaling. Factor will\n"+\
				"\t\tbe 2^exp. For exp<0 the image size will be reduced.\n\n"+\
				"sigma:\t\t(for images)standard deviation for gaussian\n"+\
				"\t\timage smoothing to reduce artifacts\n\n"+\
				"k:\t\tfactor for component merging threshold function. The\n"+\
				"\t\tlarger the value, the more likely is it for components\n"+\
				"\t\tto be merged.\n\n"+\
				"R:\t\trange of neighborhood relationships (in pixels)\n"+\
				"\t\tR=0 will enable simple neightborhood edges method.\n\n"+\
				"rows:\t\t(for CSV) how many rows should be considered for\n"+\
				"\t\tthe segmentation algorithm.\n\n"+\
				"weighted:\t(for images)wheter or not to use linear\n"+\
				"\t\tincrease of weights with increasing distance.\n\n"+\
				"useskimage:\t(for images)wheter or not to use the skimage\n"+\
				"\t\felsenzwalb implementation instead of the manual one."
		sys.exit(0)

	sigma = 0; exp = 0; k = 1; R = 1
	weighted = False; useskimage = False; rows = -1
	
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
	if "--weighted" in sys.argv:
		weighted = True
	if "--useskimage" in sys.argv:
		useskimage = True
	if "--rows" in sys.argv:
		i = sys.argv.index("--rows")
		rows = int(sys.argv[i+1])

	runSegmentation(name, extension, exp=exp, sigma=sigma, k=k, R=R,
						weighted=weighted, useskimage=useskimage, rows=rows)
