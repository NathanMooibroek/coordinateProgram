#!/usr/bin/env python
# coding: utf-8

#get_ipython().system('pip install exif')
#get_ipython().system('pip install pillow')

from exif import *
save_dir = "./Output/"
def dms(deg):
  import math
  f,d = math.modf(deg)
  s,m = math.modf(abs(f)*60)
  return (d,m,s *60)

def fix_exif(filename,latitude,longitude,heading):
  print(filename)
  with open(filename, 'rb') as image_file:
    my_image = Image(filename)

  my_image.make = "Geoai"
  my_image.gps_latitude_ref = "N"
  my_image.gps_latitude = dms(float(latitude))
  my_image.gps_longitude_ref = "E"
  my_image.gps_longitude = dms(float(longitude))
  my_image.focal_length = 600
  my_image.gps_altitude = 14.4
  my_image.gps_altitude_ref = GpsAltitudeRef.ABOVE_SEA_LEVEL
  my_image.gps_img_direction = heading
  my_image.gps_map_datum ='WGS84'
  my_image.model="XT2"
  my_image.make="DJI"

  with open(filename, 'wb') as new_image_file:
    new_image_file.write(my_image.get_file())

def write_img(img,filename,latitude,longitude,heading):
  img.save(save_dir+ img_name)
  
  fix_exif(save_dir+ img_name,latitude,longitude,heading)



import glob
import csv
from exif import Image
from PIL import Image as PILIMG

root_dir = "./Input"
meta_path = "./metadata\MetaData_0-490_eidted.csv"#MetaData_0-11945.csv" ./metadata/MetaData_0-490_new.csv

for filename in glob.iglob(root_dir + '**/*.jpg', recursive=True):
  print(filename.split("\\"))
  img = PILIMG.open(filename)
  img = img.convert('RGB')
  img_name = (filename.split("\\")[2])
  #print(img_name)
  frame_id = img_name.split("_")[1]


  with open(meta_path) as f_obj:
    reader = csv.reader(f_obj, delimiter=';')
    #csv_headings = next(reader)

   
    for line in reader:      #Iterates through the rows of csv
        print((line[0]))
        print(type(frame_id))        #line here refers to a row in the csv
        if frame_id == str(line[0]):      #get first column of row
            latitude = line[4]
            longitude = line[5]
            heading = float(line[3])
            altitude = line[2]
            if heading > 270: #267
                heading = heading - 270.0 #267
            else:
                heading = heading + 90.0 #93
                
            write_img(img,filename,latitude,longitude,str(heading))





