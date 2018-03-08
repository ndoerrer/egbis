#!/usr/bin/python

import numpy as np

from segmentation import Segmentation

DEBUG = False

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
		if DEBUG:
			print "current edge weight is", w
		if not seg.issame(i, j):
			if w <= seg.MInt(V.index(v1), V.index(v2)):
				if DEBUG:
					print "merging", v1,"(", i, ") and", v2, "(", j, \
								") with weight", w, "MInt=", seg.MInt(i, j)
				seg.union(V.index(v1), V.index(v2), weight=w)
	return seg
			
