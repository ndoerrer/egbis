#!/usr/bin/python

import numpy as np
import networkx as nx

def loadCSV(filename, skiphead=True, rows=-1):
	"""
	The method loads a .csv file from disk and converts it to a table
	(np.ndarray) of values. The first column corresponds to the unique id.
	All the other columns should hold attribute values.
	Args:
		filename:	name of the file to load (with optional path)
		skiphead:	if True the first line of the file is ignored
		rows:		sets a limit to the number of rows considered
					setting rows to -1 means using the whole file
	Returns:
		The table representation of the csv file.
	"""
	if skiphead:
		table = np.loadtxt(open(filename, "rb"), delimiter=",", skiprows=1,
													dtype=int)
	if rows == -1:
		return table
	else:
		return table[:rows,:]

def d(i, j, table):
	"""
	Distance function on the csv dataset. The first column is used as identifier
	but not as part of the sum. All the distances in the attributes are summed
	(their absolute values) and returned as distance value.
	Args:
		i:		identifier of the first datapoint
		j:		identifier of the second datapoint
		table:	table holding all the identifiers and attributes
	Returns:
		distance value which is sum of absolute differences in attributes
	"""
	return np.sum(np.absolute(table[i,1:] - table[j,1:]))
		

def csvToGraph(table, R=250):
	"""
	Converts a table (obtained from a csv file) to a networkx graph.
	To achive that the pairwise distances of the datapoints are computed
	and if this is below the distance threshold R an edge is added between
	the vertices corresponding to the identifiers of the data points.
	Args:
		table:	table holding all the identifiers and attributes
		R:		threshold value for the distance (default = 250)
	Returns:
		A pair of the resulting Graph G and the vertex set
	"""
	nodes = list(table[:,0])
	nodes.sort()						#not neccessary, but helpful for debug
	G = nx.Graph()
	print "STATUS: adding nodes"
	G.add_nodes_from(nodes)
	print "STATUS: adding edges"
	for v1 in nodes:					# python magic?
		for v2 in nodes:
			i = nodes.index(v1)
			j = nodes.index(v2)
			dist = d(i, j, table)		# hopefully table passed as pointer
			#print dist
			if dist < R:
				G.add_edge(v1, v2, weight=dist)
	print "STATUS: finished Graph creation"
	return (G, nodes)

def storeAllAttributeStatistics(name, table, label_list):
	"""
	This method creates two files (one for the means and one for variances)
	and stores the corresponding values there. One line in such an output file
	corresponds to one specific segmentation part (segmentation classes given
	as argument label_list). The first column depends on the unique id, all the
	following ones depend on the attribute values.
	Args:
		name:		identifier of the dataset/settings (with optional path)
					Created files will be name-means.csv and name-variances.csv
		table:		Full table (np.ndarray) of identifiers and attribute values
		label_list:	List of lists holding ids part of segmentation classes
	"""
	meansfile = open(name+"-means.csv", "w")
	variancesfile = open(name+"-variances.csv", "w")
	print "STATUS: storing result"
	meansfile.write("First line is over all players, following lines are values"
					+"for the single partitions in the segmentation\n")
	variancesfile.write("First line is over all players, following lines are"
					+"values for the single partitions in the segmentation\n")
	label_list = [[i for i in range(table.shape[0])]] + label_list

	for index_list in label_list:
		(means, variances) = getAttributeStatistics(table, index_list)
		meanstring = ""
		variancestring = ""
		for i in range(means.shape[0]):
			meanstring += str(means[i])
			meanstring += ","
			variancestring += str(variances[i])
			variancestring += ","
		meansfile.write(meanstring+"\n")
		variancesfile.write(variancestring+"\n")
	meansfile.close()
	variancesfile.close()

def getAttributeStatistics(table, index_list):
	"""
	Computes and returns means and variance values for the identifiers and
	all attributes of data points corresponding to ids in index_list.
	Args:
		table:		Full table (np.ndarray) of identifiers and attribute values
		index_list:	List of ids (those you want the statistics for)
	Returns:
		tuple of np.ndarray (1d) of means and np.ndarray (1d) of variance values
	"""
	selection = table[index_list]
	#print selection
	return (np.mean(selection, axis=0), np.var(selection, axis=0))

def printAttributeStatistics(table, attr_index, index_list):
	"""
	Method for debug purposes. Shows summary statistics for id list for given
	attribute.
	Args:
		table:		Full table (np.ndarray) of identifiers and attribute values
		attr_index:	Number/index of the attribute of interest (scalar)
		index_list:	List of ids (those you want the statistics for)
	"""
	selection = table[:,attr_index][index_list]
	print "index list =", index_list
	print "attribute index =", attr_index
	print "attribute values =", selection
	print "attribute minimum =", np.min(selection)
	print "attribute maximum =", np.max(selection)
	print "attribute mean =", np.mean(selection)
	print "attribute variance =", np.var(selection)
