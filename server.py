#By Erik Lanning, 2016
import os
import sys
import json
import uuid
import zipfile
import logging
import tempfile
from flask import Flask, send_file, request

try:
	import zlib
	compression = zipfile.ZIP_DEFLATED
except:
	compression = zipfile.ZIP_STORED

app = Flask(__name__)

defaultPort = 3333
mapExtension = ".zip"
tmpFolderPath = "./tmp/"
mapFolderPath = "./mapFiles/"

if os.path.isdir(tmpFolderPath) == False:
	os.mkdir(tmpFolderPath)
	
if os.path.isdir(mapFolderPath) == False:
	os.mkdir(mapFolderPath)

#@pre User has uploaded a JSON file of requested map files, or submitted a raw JSON string of map files directly.
#@post Maps that the user requested are returned as a bundled compressed archive.
@app.route('/getMaps', methods=['GET', 'POST'])
@app.route('/getMaps/<requestedMaps>')
def getMaps(requestedMaps=None):
	try:
		if requestedMaps == None:
			mapFile = json.load(request.files['mapFile'])
		else:
			mapFile = json.loads(requestedMaps)
			
		requestedMapsZip = buildMapZip(mapFile)

	except Exception,e:
		return logError(str(e))

	finally:
		return send_file(requestedMapsZip, as_attachment = True)
		
#@pre mapFile should be a json object containing the requested maps.
#		It should follow the format of "location name" : "version number".
#@post A zipfile object is returned that contains the requested maps in zip format, if they exist. 
def buildMapZip(mapFile):
	tmpZip = tmpFolderPath + genRandFileName(mapExtension)
	mapZip = zipfile.ZipFile(tmpZip, mode='w')
	
	for mapName, mapVersion in mapFile.iteritems():
		fileCompletePath = mapFolderPath + mapName + mapVersion + mapExtension
		if os.path.isfile(fileCompletePath):
			mapZip.write(fileCompletePath, compress_type=compression)	
	
	mapZip.close()
	
	return tmpZip

def genRandFileName(fileExtension):
	charsFromUUID = 5
	randUniqueName = uuid.uuid4().hex + fileExtension
	
	while (os.path.isfile(tmpFolderPath + randUniqueName)):
		randUniqueName = uuid.uuid4().urn[charsFromUUID:] + fileExtension
		
	return randUniqueName
	
def logError(error_str = ""):
	app.logger.error(error_str)
	return "Error processing request.\n"
	
if __name__ == "__main__":
	app.run(
		port=defaultPort,
		debug=True
	)