import os
import glob

rootdir = './'
for file in os.listdir(rootdir):
    d = os.path.join(rootdir, file)
    if os.path.isdir(d):
        print(d)
directory = glob.iglob()
for filename in glob.iglob(rootdir + '**/*.jpg', recursive=True):
    print(filename)