#!/usr/bin/env python
# coding: utf-8

# get_ipython().system('pip install exif')
# get_ipython().system('pip install pillow')

from exif import *

save_dir = "./MetadataTest\\Output\\"


def dms(deg):
    import math
    f, d = math.modf(deg)
    s, m = math.modf(abs(f) * 60)
    return (d, m, s * 60)


def fix_exif(filename,latitude,longitude):
  print(filename)
  with open(filename, 'rb') as image_file:
    my_image = Image(filename)

  my_image.gps_latitude_ref = "N"
  my_image.gps_latitude = dms(float(latitude))
  my_image.gps_longitude_ref = "E"
  my_image.gps_longitude = dms(float(longitude))


  with open(filename, 'wb') as new_image_file:
    new_image_file.write(my_image.get_file())


def write_img(img, filename, latitude, longitude):
    img.save(save_dir + img_name)

    fix_exif(save_dir + img_name, latitude, longitude)


import glob
from exif import Image
from PIL import Image as PILIMG

root_dir = "MetadataTest/Input"
# meta_path = "./metadata\MetaData_0-490_eidted.csv"  # MetaData_0-11945.csv" ./metadata/MetaData_0-490_new.csv

for filename in glob.iglob(root_dir + '**/*.jpg', recursive=True):
    # print(filename.split("\\"))
    print(filename+"\n\n")
    img = PILIMG.open(filename)
    img = img.convert('RGB')
    # print(filename)
    img_name = (filename.split("\\")[2])
    # print(img_name)
    coordPart = img_name.split("-")[1]
    # print("Coordpart: "+coordPart)
    c1 = coordPart.split("_")[0]
    c2 = coordPart.split("_")[1]
    latitude = c1
    longitude = c2
    # print("Coord 1: "+c1+ "\nCoord 2: "+ c2)
    # write_img(img, filename, latitude, longitude)




