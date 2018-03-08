#!/usr/bin/python

import numpy as np

DEBUG = False

#IDEA: path compression in union-find

class Segmentation:
	"""
	Class to handle segmentations. This implements a union-find data structure
	to be able to easily merge sets in an efficient way.
	The implementation is inspired by the unionfind module by Saito Tsutomu
		url: https://pypi.python.org/pypi/unionfind/0.0.10
	I taylored the class from this module to my needs and added fields
	holding values for cardinality and Int-values (see Felzenszwalb)
		paper: Efficient Graph-Based Image Segmentation
	"""
	def __init__(self, n, k=0.1):
		"""
		Constructor for Segmentation class. Creates a union-find structure
		where all components hold exactly one element. Also initializes
		cardinality and Int lists
		Args:
			n:	number of components in the data structure
			k:	parameter for the threshold function tau = k / |C|
		"""
		self.parent = list(range(n))
		self.Int = list(np.zeros(n))
		self.cardinality = list(np.ones(n))
		self.k = k
		self.n = n

	def find(self, i):
		"""
		Recursively walks up the tree containing i and gives root node
		Args:
			i:	node to which the root should be found
		Returns:
			root node number (find(root) = root itself)
		"""
		if self.parent[i] != i: self.parent[i] = self.find(self.parent[i])
		return self.parent[i]

	def union(self, i, j, weight=0):
		"""
		Unites two components in the union-find structure. Additionally it
		adjusts the cardinality and Int values such that they are correct for
		the root of each component after merging the components.
		Args:
			i:		node in first component to merge (not neccessarily root)
			j:		node in second component to merge (not neccessarily root)
			weight:	weight of the edge connecting them, needed to set Int value
		"""
		i = self.find(i)
		j = self.find(j)
		self.cardinality[j] += self.cardinality[i]
		if i != j:
			self.parent[i] = j
		self.Int[j] = max(self.Int[j], weight)

	def issame(self, i, j):
		"""
		Checks whether two nodes are in the same component, i.e. have same root.
		Args:
			i:	first node
			j:	second node
		Returns:
			true iff i and j are in the same component
		"""
		return self.find(i) == self.find(j)

	def MInt(self, i, j):
		"""
		Returns the MInt value between two components (reasonable iff disjoint)
		MInt = min( Int(C_i) + tau(C_i), Int(C_j) + tau(C_j) )
		Depends on tau function below.
		Args:
			i:	node in the first component
			j:	node in the second component
		Returns:
			MInt(C_i, C_j) value
		"""
		i = self.find(i)
		j = self.find(j)
		return min(self.Int[i] + self.tau(i), self.Int[j] + self.tau(j))

	def tau(self, i):
		"""
		Represents the threshold function which depends on the component size.
		Here it is set to k / |C| for some constant k.
		Args:
			i: root of a component (to get its cardinality)
		Returns:
			threshold-function value
		"""
		return self.k / self.cardinality[i]

	def toImage(self, shape):
		"""
		Converts the unionfind-structure to an Image of lables.
		For that the shape of the image has to be specified.
		This method only works if the labels correspond to the vertices
		increasing row by row and column by column (sorted Vertex set).
		Args:
			shape:	shape of the original image and also resulting label image
		Returns:
			image (np.ndarray) of the lables in current segmentation state
		"""
		labels = np.asarray([self.find(x) for x in range(self.n)]).reshape(shape)
		if DEBUG:
			print "labels"
			print labels
			print "cardinality"
			print np.asarray([self.cardinality[i] if i==self.find(i) else 0 for i in
								range(self.n)], dtype=np.int32).reshape(shape)
			print "Int"
			print np.asarray(self.Int).reshape(shape)
		return labels
