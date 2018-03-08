#!/usr/bin/python

import egbislib

# falcon: exp=-4, sigma=0.8, k=3.0 -> runs 25 seconds
# shapes: exp=-2, sigma=0.8, k=3.0 -> runs 3 minutes (10GB RAM!!)

name = "shapes"
extension = ".png"
exp = -2
sigma = 0.8
k = 3.0


#name = "falcon"
#extension = ".jpg"
#exp = -4
#sigma = 0.8
#k = 3.0

img_raw = egbislib.imageToGray(egbislib.loadImage(name+extension))
img_raw = egbislib.scaleImage(img_raw, exp)
img = egbislib.preprocess(img_raw, sigma=sigma)
#egbislib.showImage(img)
(G, V) = egbislib.directNeighborGraph(img)
#egbislib.showGraph(G)
seg = egbislib.segmentate(G, V, k=k)
segImage = seg.toImage(img.shape)
egbislib.saveImage(img, name+"_e"+str(exp)+"_sigma"+str(sigma)+
											"_k"+str(k)+extension)
egbislib.showStereo(img_raw, segImage)
