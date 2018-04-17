egbis - efficient graph based image segmentation

A	General information

Implementation of a method proposed in: Efficient Graph-Based Image Segmentation
by Pedro F. Felzenszwalb and Daniel P. Huttenlocher at International Journal of
Computer Vision 01.09.2004 https://doi.org/10.1023/B:VISI.0000022288.19776.77

My implementation of this is part of scientific computing practical
at NAM Göttingen

Basic tasks of this project are two things:
1. Converting a type of input data (image or csv table) into a weighted Graph
	using a neighborhood relationship based on some reasonable distance metric.
2. Applying the Felzenzwalb-Huttenlocher algorithm to the graph to generate
	a segmentation and vizualizing it.


B	Installation/Requirements

The code is written in Python2.7

Python libraries used:
matplotlib 2.2.0
networkx 2.1
numpy 1.14.2
scikit-image 0.13.1
scikit-learn 0.19.1

As for hardware, a lot of RAM may be needed if working with large images. e.g.
for uncompressed 480 x 270 Pixel image the programm needs approximately 9GB.


C	Execution

This repository contains two executable python main files.

test.py just contains a basic test. It loads the image falcon.jpg (located in
images directory), scales it down by a factor of 2^4 in width and height,
applies a gaussian filter with standard deviation 1.3 and
creates a graph from it using the distanceWeightedThresholdGraph method with a
maximal neighborhood distance of 3. After that the Felzenzwalb-Huttenlocher
algorithm is applied with the threshold parameter k=2. The result is transformed
back to an image and shown on screen as well as saved in images directory.


egbis.py offers the whole spectrum of functionality this repository contains.

	usage: python egbis.py [--exp <exp>][--sigma <sigma>][--k <k>][--R <R>]
					[--rows <rows>][--weighted][--useskimage] <image/csv-file>

With the exp parameter, the exponent for image scaling can be set. The factor
will be 2^exp. For exp<0 the image size will be reduced. (default 0)

sigma parameter sets the standard deviation for a gaussian filter to be applied
on the image for image smoothing to reduce artifacts in image data. (default 0)

k sets the factor for the component merging threshold function. The larger the
value, the more likely is it for components to be merged. (default 1.0)

R is the range of neighborhood relationships (in pixels). R=0 will enable simple
neightborhood edges method instead of distanceWeightedThresholdGraph method.
(default 1.0)

rows (for CSV) sets how many rows should be considered for the segmentation
algorithm. (default all rows)

weighted parameter sets (for images) whether or not to use linear increase of
weights with increasing distance. (default not)

useskimage parameter sets (for images) whether or not to use the skimage
felzenzwalb implementation instead of the self-implemented one (for
comparisson). (default not)


D	Examples

python test.py
	executes the test script which performs a segmentation of of the image
	falcon.jpg (downscaled by factor 2^4).

python egbis.py --exp -4 --weighted --R 3 images/falcon.jpg
	performs segmentation of falcon.jpg (downscaled by factor 2^4) using
	weightedDistanceThresholdGraph function with maximal neighbor distance 3
	pixels.

python egbis.py --k 2.5 --sigma 1.3 --exp -4 --weighted --R 3 images/falcon.jpg
	like the example above, only that the image is smoothed by a gaussian with
	standard deviation 1.3 and that the threshold parameter is 2.5 instead of 1.


python egbis.py --R 250 --k 4000 --rows 400 football-dataset/fifastats.csv
	performs segmentation of the first 400 rows of fifastats dataset in
	directory football-dataset. Neighborhood parameter R is 250 and threshold
	factor k is 4000. The result is shown as colored scatterplot of the PCA of
	attribute values (column entries in dataset).


A more detailed description of this project can be found in egbis-report.pdf
