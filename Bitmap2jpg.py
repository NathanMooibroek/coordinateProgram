import aspose.words as aw
doc = aw.Document()
builder = aw.DocumentBuilder(doc)


#inputPath moet aan het fileDialog gekoppeld worden en de output moet dezelfde naam krijgen als de input file, maar dan als jpg en in de output map (geselecteerd door de user)

inputPath="Bitmap2jpgTest/Input/Snapshot-52.8977265_5.8565235-05_18_2021_10_53_07.bmp"
#eerste replace eruit halen bij het mergen
outputPath=inputPath.replace("Input","Output")
outputPath=outputPath.replace("bmp", "jpg")

shape = builder.insert_image(inputPath)
shape.image_data.save(outputPath)
