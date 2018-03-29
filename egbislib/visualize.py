#!/usr/bin/python

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def pcaTransform(table):
	"""
	This takes the attribute values (not the ids) and performs a 2-component
	principle component analysis on them. The result is 2 dimensional
	(so plottable).
	Args:
		table:	table holding all the identifiers and attributes
	Returns:
		array (np.ndarray) holding the transformed attribute values. (the two
		first principal component values explaining the most variance)
	"""
	X = table[:,1:]
	pca = PCA(n_components=2)
	pca.fit(X)
	W = pca.components_
	return X.dot(W.T)

def colorScatterPlot(data, color_labels, name):
	"""
	Method to plot data in different colors according to a list of lists
	distributing indices to color classes. The result is shown on screen
	and additionally saved as name-pcascatter.pdf.
	Args:
		data:			data to be plotted (nx2 array)
		color_labels:	list of lists holding ids part of color classes
		name:			name prefix of the output file
	"""
	fig, ax = plt.subplots()
	for i in range(len(color_labels)):
		ax.scatter(data[color_labels[i],0], data[color_labels[i],1], label=i)
	plt.legend(loc="upper left", prop={'size': 8})
	plt.title("scatterplot of pca of attribute values of different classes")
	ax.set_xlabel("pc1-values")
	ax.set_ylabel("pc2-values")
	plt.savefig(name+"-pcascatter.pdf")
	plt.show()
