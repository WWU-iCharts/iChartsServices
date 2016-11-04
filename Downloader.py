import os.path
import urllib
import zipfile
from subprocess import call
import shutil


def downloader():
    database_path = "/home/chris/iCharts/iChartsServices/data/database"
    temp_path = "/home/chris/iCharts/Tools/WebScraper/temp"
    chart_path = "/home/chris/iCharts/iChartsServices/"
    did_update = False

    if not os.path.exists(database_path):
        print "databse file not found"
        return
    if not os.path.exists(temp_path):
        print "temp file not found"
        return

    database_file = open(database_path, 'r+')
    temp_file = open(temp_path, 'r')
    updated_file = open("updated", 'w+')
    updated_file.truncate()

    database = []
    temp = []

    #Read data and put into two arrays
    for line in database_file:
        split = line.split(',')

        row = []
        row.append(split[0])
        row.append(split[1])
        row.append(split[2].strip())

        database.append(row)

    for line in temp_file:
        split = line.split(',')

        row = []
        row.append(split[0])
        row.append(split[1])
        row.append(split[2].strip())

        temp.append(row)

    if not len(database) == len(temp):
        print "Database and Temp database do not match"

        #Compare version numbers between temp and the database
    for row1,row2 in zip(database,temp):
        #Download file if needed
        if row1[1] < row2[1]:
            row1[1] = row2[1]

            #Download File
            print "downloading"
            urllib.urlretrieve (row2[2], row1[2] +".zip")

            #unzip file
            print "unzipping"
            zip_ref = zipfile.ZipFile(row1[2]+ ".zip", 'r')
            zip_ref.extractall(row1[2])
            zip_ref.close()

            #Tile map
            print "Creating tiles"
            directory = row1[2]
            filename = row1[2]
            for files in os.listdir(directory):
                if files.endswith(".tif"):
                    os.rename(directory + "/" + files, directory + "/" + filename + ".tif")
                    call(["gdal_translate", "-of","vrt","-expand", "rgba",  directory + "/" + filename +  ".tif",  directory + "/temp.vrt"])
                    call(["gdal2tiles.py","-z","4-6", "-p", "raster", directory + "/temp.vrt", directory + "/" + filename])

            #Move tfw file into tiles folder
            for files in os.listdir(directory):
                if files.endswith(".tfw"):
                    os.rename(directory + "/" + files, directory + "/" + directory + "/" + filename + ".tfw")

            #Zip and move folder
            print "ziping tiles and moving files"
            zf = zipfile.ZipFile(filename + ".zip", "w")
            for dirname, subdirs, files in os.walk(directory + "/" + directory):
                zf.write(dirname)
                for filename in files:
                    zf.write(os.path.join(dirname,filename))
            zf.close()

            os.rename(row1[2] + ".zip", chart_path + row1[2] + "/" + row1[2] + ".zip")

            #clean up
            print "cleaning up"
            shutil.rmtree(directory)
            did_update = True

        updated_file.write(row1[0] + ',' + row1[1] + ',' + row1[2] + '\n')

    if did_update:
        print "updating database"
        #os.rename("updated", database_path)
    else:
        print "no charts to update"

downloader()
