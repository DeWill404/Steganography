# This code required Third party modlue
#	following code for line 1 to 7
# 	Check if required module is present in system or not...
from Dependencies import check_module
check_module({'cryptography', 'pillow'})
# Module Checking end...
# Remove This part if not required.... :)

import os
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import Encryption
import Steganography

######## ROOT WINDOW    ########
root = tk.Tk()
root.minsize(640, 450)
root.maxsize(640, 450)
root.title("Steganography")


######## Creating TABS    #########
current_dir = os.path.abspath(os.getcwd())
TAB_CONTROL = ttk.Notebook(root)
# Info Tab
DEFAULT = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(DEFAULT)
# Hide Tab
HIDE = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(HIDE)
# Retrive Tab
RETRIEVE = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(RETRIEVE)
TAB_CONTROL.place(width=600, height=350, x=20, y=80)


### Default Info Section
Button(DEFAULT, text="This project Steganography project......").place(x=10, y=20)
Button(DEFAULT, text="This will help to hide and retrive text in images...").place(x=10, y=60)

### Hide Section
# Variables
passwordState = BooleanVar(HIDE, value=False)
def resetH():
    textMsgRadio.invoke()
    msg = ""
    messageEntry.delete("1.0", END)
    passwordState.set(0)
    passwd = ""
    passwordEntry.delete(0, END)
    toggle_entry()
    inputImg = ""
    printIImg["text"] = ""
    outputDir = ""
    printOImg["text"] = ""
def open_tabh():
    TAB_CONTROL.select(HIDE)
    resetH()
hide = Button(root, text="HIDE", command=open_tabh).place(width=70, height=40, x=300, y=50)
# Functions
def open_text():
    file = filedialog.askopenfilename(initialdir=current_dir, filetypes=(("Text Files", "*.txt"), ("all Files", "*")))
    try:
        file = open(file, "r")
        msg = file.read()
        file.close()
    except:
        msg = ""
    messageEntry.delete('1.0', END)
    messageEntry.insert(tk.END, msg)
def toggle_entry():
    if passwordState.get():
        passwordEntry.config(state=NORMAL)
    else:
        passwordEntry.config(state=DISABLED)
def select_file():
    inputImg = filedialog.askopenfilename(initialdir=current_dir, filetypes=(
    ("PNG files", "*.png"), ("JPEG files", "*.jpeg"), ("JPG files", "*.jpg"), ("ICO files", "*.ico")))
    printIImg.config(text=inputImg)
def select_dir():
    outputDir = filedialog.askdirectory(initialdir=current_dir)
    printOImg.config(text=outputDir)
def hide():
    msg = ""
    passwd = ""
    inputImg = ""
    outputDir = ""
    msg = messageEntry.get('1.0', END)
    msg = msg[:-1]
    if passwordState.get():
        passwd = passwordEntry.get()
    inputImg = printIImg["text"]
    outputDir = printOImg["text"]
    if (msg == "") or (passwordState.get() and (passwd == "")) or (inputImg == "") or (outputDir == ""):
        messagebox.showerror("Error", "Incomplete information....")
        textMsgRadio.invoke()
    else:
        if passwordState.get():
            en = Encryption.Encrypt(msg, passwd)
            msg = en.encryptMessage()
            print(msg)
        sn = Steganography.Steg()
        sn.hide(inputImg, outputDir, msg)
        messagebox.showinfo("Successfull", "Information is hidden....")
        resetH()
# Widgets
messageHead = Label(HIDE, text="MESSAGE")
messageHead.place(width=70, height=40, x=2, y=2)
textMsgRadio = Radiobutton(HIDE, text='Text', value=1)
textMsgRadio.place(width=70, height=20, x=2, y=42)
fileMsgRadio = Radiobutton(HIDE, text='File', value=2, command=open_text)
fileMsgRadio.place(width=70, height=20, x=72, y=42)
messageEntry = ScrolledText(HIDE, wrap=WORD)
messageEntry.place(height=100, width=550, x=5, y=60)
passwordEntry = Entry(HIDE, text="", show="*", width=20, state=DISABLED)
passwordEntry.place(x=95, y=165)
passwordLabel = Checkbutton(HIDE, text='Password', var=passwordState, command=toggle_entry)
passwordLabel.place(height=35, width=90, x=5, y=160)
selectInImg = Button(HIDE, text="Select Image", command=select_file)
selectInImg.place(x=5, y=200)
printIImg = Label(HIDE, text="")
printIImg.place(x=120, y=202)
selectOutImg = Button(HIDE, text="Select Folder", command=select_dir)
selectOutImg.place(x=5, y=235)
printOImg = Label(HIDE, text="")
printOImg.place(x=120, y=237)
Submit = Button(HIDE, text="Done !", command=hide).place(width=100, height=50, x=480, y=260)

### Retrive Section
# Variables
passwordStateR = BooleanVar(HIDE, value=False)
def resetR():
    passwordStateR.set(0)
    passwdR = ""
    passwordEntryR.delete(0, END)
    toggle_entryR()
    inputImgR = ""
    printIImgR["text"] = ""
def open_tabr():
    TAB_CONTROL.select(RETRIEVE)
    msgR = ""
    messageEntryR.delete("1.0", END)
    resetR()
retrieve = Button(root, text="RETRIVE", command=open_tabr).place(width=70, height=40, x=500, y=50)
# FUNCTIONS
def toggle_entryR():
    if passwordStateR.get():
        passwordEntryR.config(state=NORMAL)
    else:
        passwordEntryR.config(state=DISABLED)
def select_fileR():
    inputImgR = filedialog.askopenfilename(initialdir=current_dir, filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpeg"), ("JPG files", "*.jpg"), ("ICO files", "*.ico")))
    printIImgR.config(text=inputImgR)
def retrieve():
    msgR = ""
    passwdR = ""
    inputImgR = ""
    inputImgR = printIImgR["text"]
    if passwordStateR.get():
        passwdR = passwordEntryR.get()
    if (passwordStateR.get() and (passwdR == "")) or (inputImgR == ""):
        messagebox.showerror("Error", "Incomplete information....")
    else:
        sn = Steganography.Steg()
        try:
            msgR = sn.retr(inputImgR)
            if passwordStateR.get():
                en = Encryption.Encrypt(msgR, passwdR)
                msgR = en.decryptMessage()
            if (msgR == "!-)=~"):
                messagebox.showarning("Warning", "Incorrect password or image....")
            else:
                messageEntryR.delete('1.0', END)
                messageEntryR.insert(tk.END, msgR)
                messagebox.showinfo("Successfull", "Information is retrieved....")
        except:
            messagebox.showerror("Error", "Incorrect password or image....")
        resetR()
# Widgets
printIImgR = Label(RETRIEVE, text="")
printIImgR.place(x=15, y=10)
selectInImgR = Button(RETRIEVE, text="Select Image", command=select_fileR)
selectInImgR.place(x=10, y=40)
passwordEntryR = Entry(RETRIEVE, text="", show="*", width=20, state=DISABLED)
passwordEntryR.place(x=100, y=75)
passwordLabelR = Checkbutton(RETRIEVE, text='Password', var=passwordStateR, command=toggle_entryR)
passwordLabelR.place(height=35, width=90, x=10, y=70)
messageEntryR = ScrolledText(RETRIEVE, wrap=WORD)
messageEntryR.place(height=100, width=550, x=5, y=100)
Submit = Button(RETRIEVE, text="Done !", command=retrieve).place(width=100, height=50, x=480, y=260)


######## Logo    ########
logo = ImageTk.PhotoImage(Image.open("assets/logo.png"))
logoCon = Label(root, image=logo)
logoCon.place(x=0, y=0)

tk.mainloop()
