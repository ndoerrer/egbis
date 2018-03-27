#!/usr/bin/python

import numpy as np

from segmentation import Segmentation

def segmentate(G, V, k=0.1):
	"""
	Method to segmentate a given weighted undirected Graph w.r.t a threshold
	function depending on the factor k.
	Args:
		G:	weighted undirected Graph
		V:	list of vertices (ordered!!)
		k:	threshold factor
	"""
	E = G.edges(data="weight")
	print "STATUS: sorting edges"
	E = sorted(E, key=lambda x: x[2])
	seg = Segmentation(len(V), k=k)
	print "STATUS: running segmentation"
	for e in E:
		(v1, v2, w) = e
		i = V.index(v1)
		j = V.index(v2)
		if w <= seg.MInt(i, j):
			seg.union(i, j, weight=w)
	return seg
			
