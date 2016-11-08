#!/usr/bin/python
from __future__ import print_function
import os, sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = 1000000000

iChartsDir = "charts"

for filename in os.listdir(iChartsDir):
    if filename.endswith(".tif"): 
		try:
			with Image.open(os.path.join(iChartsDir, filename)) as im:
				tilingFolder = iChartsDir+'/'+filename[0:-4]
				if not os.path.isdir(tilingFolder):
					os.makedirs(tilingFolder)
				
				imgQuality = 80 #Where 100 is no loss.
				resizeFactor = 10
				#Multiple resize algorithms as optional parameter, may want to experiment with
				resizedChart = im.resize( tuple(x/resizeFactor for x in im.size) )
				
				resizedChart.save(tilingFolder+"/"+filename)
				
		except IOError:
			pass
    else:
        continue

