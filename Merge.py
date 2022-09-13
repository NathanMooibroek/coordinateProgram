import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import aspose.words as aw
from exif import Image
from PIL import Image as PILIMG
import glob
from datetime import datetime

#Writen by Nathan Mooibroek 25-7-2022

def selectInput():
    global inputFolder
    global inputEntry
    file_path = filedialog.askdirectory()
    # print(file_path)
    inputEntry.delete(0, "end")
    inputFolder = file_path
    inputEntry.insert(0, inputFolder)
    inputFolder.replace("\\","\\\\")
    inputFolder += "\\"
    # print(inputFolder)

#voor het selecteren van het pad van de map waarin de output moet komen
def selectOutput():
    global outputFolder
    global outputEntry
    file_path = filedialog.askdirectory()
    # print(file_path)
    outputEntry.delete(0, "end")
    outputFolder=file_path
    outputEntry.insert(0, outputFolder)
    outputFolder.replace("\\","\\\\")
    outputFolder += "\\"


# zorgt ervoor dat de text boxes clickable worden
def handle_click(event):
    # print("clicked!")
    if event.widget == inputEntry:
        selectInput()
    else:
        selectOutput()


# voor het converten van bitmap naar jpg en het toevoegen van metadata
def addData(imgPath):
    # print(imgPath)
    img = PILIMG.open(imgPath)
    img = img.convert('RGB')
    # print(filename)
    img_name = (imgPath.split("\\"))
    img_name.reverse()
    img_name = img_name[0]
    # print(img_name)
    coordPart = img_name.split("-")[1]
    # print("Coordpart: "+coordPart)
    c1 = coordPart.split("_")[0]
    c2 = coordPart.split("_")[1]
    latitude = c1
    longitude = c2
    # print("Coord 1: "+c1+ "\nCoord 2: "+ c2)
    write_img(img, img_name, latitude, longitude)


def write_img(img, filename, latitude, longitude):
    global outputFolder
    img.save(outputFolder+"\\" + filename)
    fix_exif(outputFolder+"\\" + filename, latitude, longitude)



def fix_exif(filename,latitude,longitude):
    # print(filename)
    with open(filename, 'rb') as image_file:
        my_image = Image(filename)

    my_image.gps_latitude_ref = "N"
    my_image.gps_latitude = dms(float(latitude))
    my_image.gps_longitude_ref = "E"
    my_image.gps_longitude = dms(float(longitude))

    with open(filename, 'wb') as new_image_file:
        new_image_file.write(my_image.get_file())

    new_image_file.close()
    image_file.close()

# zorgt ervoor dat de coordinaten in het goede formaat staan
def dms(deg):
    import math
    f, d = math.modf(deg)
    s, m = math.modf(abs(f) * 60)
    return (d, m, s * 60)


# convert bmp naar .jpg
def bmp2jpg(imgName):
    global outputFolder
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)
    shape = builder.insert_image(imgName)
    imgName = imgName.split("\\")
    imgName.reverse()
    imgName = imgName[0]
    imgName = imgName.replace(".bmp", ".jpg")
    imgPath = outputFolder+"\\"+imgName
    shape.image_data.save(imgPath)


def jpg2jpg(imgName):
    global outputFolder
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)
    shape = builder.insert_image(imgName)
    imgName = imgName.split("\\")
    imgName.reverse()
    imgName = imgName[0]
    imgPath = outputFolder+"\\"+imgName
    shape.image_data.save(imgPath)


# functie voor het starten van het converteren en de coordinaten erbij doen
def convert():
    if(inputFolder=="" or outputFolder==""):
        tk.messagebox.showerror("Error", "Please enter both the input and output")
        return

    succesBMP2JPG = 0
    failBMP2JPG = 0
    succesJPG2JPG = 0
    failJPG2JPG = 0
    succesCoord = 0
    failCoord = 0

    # zoekt in de input folder naar bmp bestanden, convert ze naar jpg en slaat ze op in de output folder
    for filePath in glob.iglob(inputFolder + '**/*.bmp', recursive=True):
        try:
            bmp2jpg(filePath)
            succesBMP2JPG +=1
        except:
            failedConvert.append(filePath)
            failBMP2JPG+=1
            continue

    # zoekt in de input naar jpg bestanden en kopieert ze naar de output
    for filePath in glob.iglob(inputFolder + '**/*.jpg', recursive=True):
        try:
            jpg2jpg(filePath)
            succesJPG2JPG+=1
        except:
            failedCopy.append(filePath)
            failJPG2JPG+=1
            continue


    # zoekt in de output folder naar JPG en geeft ze waar mogelijk de coordinaten
    for filePath in glob.iglob(outputFolder + '**/*.jpg', recursive=True):
        try:
            addData(filePath)
            succesCoord+=1
        except:
            failedCoord.append(filePath)
            failCoord+=1
            continue

    # Error log writing
    if failBMP2JPG > 0 or failJPG2JPG > 0 or failCoord > 0:
        with open('./ErrorLog.txt', 'a') as log:
            try:
                log.write("\n["+str(datetime.now())+"]"+"\n\n")

                if(failBMP2JPG>0):
                    log.write("Files that failed to convert: ")
                    for path in failedConvert:
                        log.write(path+"\n")

                if(failJPG2JPG>0):
                    log.write("Files that failed to copy: ")
                    for path in failedCopy:
                        log.write(path+"\n")

                if(failCoord>0):
                    log.write("Files that failed to get Coordinates: ")
                    for path in failedCoord:
                        log.write(path+"\n")
                if(failBMP2JPG>0 or failJPG2JPG>0 or failCoord>0):
                    log.write("\n")
                log.close()
            except:
                log.close()




    succesBMP2JPG = str(succesBMP2JPG)
    failBMP2JPG = str(failBMP2JPG)
    succesJPG2JPG = str(succesJPG2JPG)
    failJPG2JPG = str(failJPG2JPG)
    succesCoord = str(succesCoord)
    failCoord = str(failCoord)

    message = "The operation has ended.\n\n"+succesBMP2JPG+" images have succesfully been converted\n"+failBMP2JPG+" images failed to convert\n\n"+succesJPG2JPG+" images have been copied\n"+failJPG2JPG+" images have failed to copy\n\n"+succesCoord+" images successfully been assigned coordinates\n"+failCoord+" images failed to get coordinates\n View Errorlog.txt for details"


    tk.messagebox.showinfo(title="Operation complete", message=message)



inputFolder = ""
outputFolder = ""

failedCopy = ['']
failedConvert = ['']
failedCoord = ['']


# copy = True
master = tk.Tk()

master.geometry("700x100")
master.title("Coordinate program")
tk.Label(master, text="Input Folder").grid(row=0)
tk.Label(master, text="Output Folder").grid(row=8)
master.resizable(False,False)

inputEntry = tk.Entry(master, width=80)
outputEntry = tk.Entry(master, width=80)
inputEntry.insert(0, "Click here")
outputEntry.insert(0, "Click here")
inputEntry.bind("<1>", handle_click)
outputEntry.bind("<1>", handle_click)

# tk.Checkbutton(command=checkOutput, text="Copy Files").grid(row=7)


inputEntry.grid(row=0, column=1, pady=12)
outputEntry.grid(row=8, column=1)

tk.Button(master, text='Convert', command=convert).grid(row=15, column=1, sticky=tk.W, padx=250, pady=5)

master.mainloop()