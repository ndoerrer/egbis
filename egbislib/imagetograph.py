#!/usr/bin/python

import numpy as np
import networkx as nx
import skimage
import skimage.io
import skimage.color
import skimage.transform
import skimage.filters
import matplotlib.pyplot as plt
import warnings

#IDEA: generally stretch grayscale images to range 0-1??
#IDEA: lowest weight edge instead of multigraph edges

def loadImage(filename):
	"""
	This method loads a file as image (np.ndarray)
	Args:
		filename: Name of the file to load (with optional path)
	Returns:
		image as np.ndarray
	"""
	print "loading image", filename
	img = skimage.io.imread(filename)
	return img

def saveImage(img, filename):
	"""
	This saves an image given as ndarray as file (extension determines format)
	Args:
		img:		image to be saved (np.ndarray)
		filename:	filename for the image file (with optional path)
	"""
	print "storing image as", filename
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")	#lossy conversion from float64 to uint16
		stretched = skimage.img_as_float(img)
		stretched = (stretched - np.amin(stretched)) / (np.amax(stretched) - np.amin(stretched))
		skimage.io.imsave(filename, stretched)

def imageToGray(img):
	"""
	Converts a given image to grayscale (intensity map)
	Args:
		img: image to convert
	Returns:
		grayscale representation of the image
	"""
	if img.ndim == 2:
		return img
	else:	# works for rgb and rgba
		result = skimage.color.rgb2gray(img)
	return result

def showImage(img):
	"""
	Displays the given image in matplotlib.pyplot figure.
	Args:
		img: image to be shown
	"""
	plt.imshow(img)
	plt.show()

def showStereo(img1, img2):
	"""
	Displays two images in a matplotlib.pyplot figure. Any zoom/selection
	performed in one of them will be also applied to the other.
	Args:
		img1:	left image to display
		img2:	right image to display
	"""
	if img1.shape[0] != img2.shape[0] or img1.shape[1] != img2.shape[1]:
		print "Images do not have the same shape!"
		return
	f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, sharex=True)
	#plt.title("dummytitle")
	ax1.imshow(img1, interpolation="none")	#, cmap = "gray"
	ax2.imshow(img2, interpolation="none")	#, cmap = "gray"
	plt.show()

def scaleImage(img, exponent):
	"""
	Scales a given image by the factor 2^exponent. For exponents < 0 the result
	will be smaller than the original.
	Args:
		img:		image to be scaled
		exponent:	exponent to determine amount of scaling (2^exponent)
	Returns:
		scaled image
	"""
	result = skimage.transform.rescale(img, 2**exponent, mode="constant")
	return result

def preprocess(img, sigma=0.8):
	"""
	Preprocesses an image by applying a gaussian filter. This is used to remove
	artifacts and improve the segmentation.
	Args:
		img: 	image to be smoothed
		sigma:	standard deviation of the gaussian kernel to apply
	Returns:
		smoothed image
	"""
	res = skimage.filters.gaussian(img, sigma=sigma)
	return res

def createNodes(img):
	"""
	Creates a list of vertice names (rownumber|colnumber) for all pixels of
	a given image.
	Args:
		img: image to get indexmap for
	Returns:
		list of vertice names for the image
	"""
	(x, y) = np.mgrid[0:img.shape[0], 0:img.shape[1]]
	x = list(x.flatten())
	y = list(y.flatten())
	nodes = ["{}|{}".format(x_, y_) for x_, y_ in zip(x, y)]
	return nodes

def directNeighborGraph(img):
	"""
	Creates an undirected graph from a grayscale image by using each pixel as a
	vertex. Edges are between vertices of neighboring pixels and their weight is
	their difference in intensity.
	Args:
		img: image to build a graph for
	Returns:
		graph with edges corresponding to intensity differences (1-neighborhood)
	"""
	nodes = createNodes(img)
	G = nx.Graph()
	print "STATUS: adding nodes"
	G.add_nodes_from(nodes)
	print "STATUS: adding edges"
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if i != 0:
				w = np.abs(img[i,j] - img[i-1,j])
				G.add_edge(str(i)+"|"+str(j), str(i-1)+"|"+str(j), weight=w)
			if i != img.shape[0]-1:
				w = np.abs(img[i,j] - img[i+1,j])
				G.add_edge(str(i)+"|"+str(j), str(i+1)+"|"+str(j), weight=w)
			if j != 0:
				w = np.abs(img[i,j] - img[i,j-1])
				G.add_edge(str(i)+"|"+str(j), str(i)+"|"+str(j-1), weight=w)
			if j != img.shape[1]-1:
				w = np.abs(img[i,j] - img[i,j+1])
				G.add_edge(str(i)+"|"+str(j), str(i)+"|"+str(j+1), weight=w)
	print "STATUS: finished Graph creation"
	return (G, nodes)

def distanceThresholdGraph(img, R=1):
	"""
	Creates an undirected graph from a grayscale image by using each pixel as a
	vertex. Edges are created for each pair of vertices with distance <= R
	and the weights are	their difference in intensity.
	For R=1 this should be the same as directNeighborGraph. (TODO: confirm)
	Args:
		img: image to build a graph for
	Returns:
		graph with edges corresponding to intensity differences
	"""
	nodes = createNodes(img)
	G = nx.MultiGraph()
	print "STATUS: adding nodes"
	G.add_nodes_from(nodes)
	print "STATUS: adding edges"
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			for i2 in range(int(i-R), int(i+R+1)):
				for j2 in range(int(j-R), int(j+R+1)):
					if (i2-i)*(i2-i)+(j2-j)*(j2-j) > R*R or (i==i2 and j==j2):
						continue
					if i2>0 and j2>0 and i2<img.shape[0] and j2<img.shape[1]:
						w = np.abs(img[i,j] - img[i2,j2])
						G.add_edge(str(i)+"|"+str(j), str(i2)+"|"+str(j2),
																weight=w)
	print "STATUS: finished Graph creation"
	return (G, nodes)

def distanceWeightedThresholdGraph(img, R=1):
	"""
	Creates an undirected graph from a grayscale image by using each pixel as a
	vertex. Edges are created for each pair of vertices with distance <= R
	and the weights are	their difference in intensity multiplied by the factor
	distance_square. This is 1 if distance = 1 and increases quadratically
	up to R.
	For R=1 this is the same as distanceThresholdGraph.
	Args:
		img: image to build a graph for
	Returns:
		graph with edges corresponding to intensity differences
	"""
	nodes = createNodes(img)
	G = nx.MultiGraph()
	print "STATUS: adding nodes"
	G.add_nodes_from(nodes)
	print "STATUS: adding edges"
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			for i2 in range(int(i-R), int(i+R+1)):
				for j2 in range(int(j-R), int(j+R+1)):
					distance_square = (i2-i)*(i2-i)+(j2-j)*(j2-j)
					if distance_square > R*R or (i==i2 and j==j2):
						continue
					if i2>0 and j2>0 and i2<img.shape[0] and j2<img.shape[1]:
						w = np.abs(img[i,j] - img[i2,j2])
						G.add_edge(str(i)+"|"+str(j), str(i2)+"|"+str(j2),
									weight=w*np.sqrt(distance_square))
	print "STATUS: finished Graph creation"
	return (G, nodes)

def showGraph(G):
	"""
	Displays a networkx graph in a matplotlib.pyplot figure.
	Args:
		G: the graph to be displayed
	"""
	nx.draw(G)
	plt.show()
