import tkinter as tk
from tkinter import *
from tkinter import filedialog

inputFolder = ""
outputFolder = ""
copy = True
master = tk.Tk()
def selectInput():
    file_path = filedialog.askdirectory()
    print(file_path)
    inputEntry.delete(0, "end")
    inputFolder=file_path
    inputEntry.insert(0, inputFolder)

#voor het selecteren van het pad van de map waarin de output moet komen
def selectOutput():
    file_path = filedialog.askdirectory()
    print(file_path)
    outputEntry.delete(0, "end")
    outputFolder=file_path
    outputEntry.insert(0, outputFolder)

def checkOutput():
    global copy
    if copy:
        print("output...")
        outputEntry.config(state="disabled")
        copy = False
    else:
        outputEntry.config(state="normal")
        copy = True

#zorgt ervoor dat de text boxes clickable worden
def handle_click(event):
    print("clicked!")
    if event.widget==inputEntry:
        selectInput()
    else:
        selectOutput()
#voor het converten van bitmap naar jpg en het toevoegen van metadata
def convert():
    print("converting...")


master.geometry("800x100")
tk.Label(master, text="Input Folder").grid(row=0)
tk.Label(master, text="Output Folder").grid(row=5)

inputEntry = tk.Entry(master, width=80)
outputEntry = tk.Entry(master, width=80)
inputEntry.insert(0, "-")
outputEntry.insert(0, "-")
inputEntry.bind("<1>", handle_click)
outputEntry.bind("<1>", handle_click)

tk.Checkbutton(command=checkOutput, text="Copy Files").grid(row=7)


inputEntry.grid(row=0, column=1)
outputEntry.grid(row=5, column=1)


tk.Button(master, text='Convert', command=convert).grid(row=10,column=1,sticky=tk.W,padx=350)

master.mainloop()