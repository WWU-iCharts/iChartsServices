#By Erik Lanning, 2016
import os
import json
import server
import shutil
import zipfile
import unittest
import tempfile
from StringIO import StringIO

# List of resources created for unit testing.

jsonMapString = """{
	"Idaho" : "67",
	"Seattle" : "33",	
	"Alaska_Malbrook" : "42"
}
"""
jsonMapParsed = json.loads(jsonMapString)

exampleNames = ['Alaska_Malbrook42', 'Seattle33', 'Idaho67']
exampleMapZip1 = zipfile.ZipFile(server.mapFolderPath + exampleNames[0] + server.mapExtension, mode='w')
exampleMapZip2 = zipfile.ZipFile(server.mapFolderPath + exampleNames[1] + server.mapExtension, mode='w')
exampleMapZip3 = zipfile.ZipFile(server.mapFolderPath + exampleNames[2] + server.mapExtension, mode='w')
tmpMapZips = [exampleMapZip1, exampleMapZip2, exampleMapZip3]

tempMapDir =  "./tmpUnitTests/"
if os.path.isdir(tempMapDir) == False:
	os.mkdir(tempMapDir)

tempMapPath = tempMapDir + 'exampleFile.%s.json' % os.getpid()
tempMapFile = open(tempMapPath, 'w+b')
tempMapFile.write(jsonMapString)
tempMapFile.close()

class TestServer(unittest.TestCase):
	#@pre A json file named exampleMapFile.json should exist in the "tempMapDir" path,
	#		containing a valid iChart map request (given by Map Name as the key, and version as the value).
	#@post A zip file containing zips of all the requested maps should be returned.
	def testFileReturn(self):
		client = server.app.test_client()
		serverResponse = client.post(
			'/getMaps',
			content_type='multipart/form-data',			
			data = {
				'mapFile': (StringIO(open(tempMapPath, 'r').read()), 'exampleMapFile.json')
			},
			follow_redirects=True	
		)

		open(tempMapDir + 'testFile.zip', 'w+b').write(serverResponse.data)
		responseToZip = zipfile.ZipFile(tempMapDir + 'testFile.zip', mode='r')
		self.assertEqual(exampleNames <= responseToZip.namelist(), True)

	#@pre jsonMapParsed should be an initialized json object with proper map request formatting.
	#		This is given as "location name" : "version number".
	#		The temporary test zip files should be created in the server.mapFolderPath.
	#@post A zip file of the requested maps should all be archived in one zip and returned.
	def testBuildMapZip(self):
		loc = server.buildMapZip(jsonMapParsed)
		exampleZipFile = zipfile.ZipFile(loc, 'r')
		listOfFiles = exampleZipFile.namelist()
		
		exampleZipFile.close()
		os.remove(loc)
		
		self.assertEqual(exampleNames <= listOfFiles, True)
	
def cleanUpGlobalFiles():
	for i in tmpMapZips:
		i.close()
		
	for i in exampleNames:
		os.remove(server.mapFolderPath + i + server.mapExtension)

	os.remove(tempMapPath)
	shutil.rmtree(tempMapDir, ignore_errors=True)
	
if __name__ == "__main__":
	unittest.main(exit=False)
	cleanUpGlobalFiles()

	
	
	

