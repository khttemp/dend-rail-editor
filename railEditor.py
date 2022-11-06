import os

from tkinter import filedialog as fd
from tkinter import messagebox as mb

from importPy.tkinterTab import *
import dendDecrypt.RSdecrypt as dendRs

LS = 0
BS = 1
CS = 2
RS = 3

decryptFile = None

def openFile():
    global decryptFile

    errorMsg = "予想外のエラーが出ました。\n電車でDのファイルではない、またはファイルが壊れた可能性があります。"
    file_path = fd.askopenfilename(filetypes=[("TRAIN_DATA", "RAIL*.BIN")])
    if file_path:
        if v_radio.get() == RS:
            filename = os.path.basename(file_path)
            v_filename.set(filename)
            del decryptFile
            decryptFile = None
            decryptFile = dendRs.RailDecrypt(file_path)
            if not decryptFile.open():
                decryptFile.printError()
                mb.showerror(title="エラー", message=errorMsg)
                return

            deleteAllWidget()
            allTabWidget()

def deleteAllWidget():
    tabList = [
        tab_one,
        tab_two,
        tab_3,
        tab_4,
        tab_5,
        tab_6,
        tab_7,
        tab_8,
        tab_9
    ]

    for tab in tabList:
        children = tab.winfo_children()
        for child in children:
            child.destroy()

def allTabWidget():
    global decryptFile
    tab1AllWidget(tab_one, decryptFile, reloadWidget)
    tab2AllWidget(tab_two, decryptFile, reloadWidget)
    tab3AllWidget(tab_3, decryptFile, reloadWidget)
    tab4AllWidget(tab_4, decryptFile, reloadWidget)
    tab5AllWidget(tab_5, decryptFile, reloadWidget)
    tab6AllWidget(tab_6, decryptFile, reloadWidget)
    tab7AllWidget(tab_7, decryptFile, reloadWidget)
    tab8AllWidget(tab_8, decryptFile, reloadWidget)
    tab9AllWidget(tab_9, decryptFile, reloadWidget)

def reloadWidget():
    global decryptFile
    decryptFile = decryptFile.reload()
    deleteAllWidget()
    allTabWidget()
    
def selectGame():
    pass

root = Tk()
root.title("電車でD レール改造 1.0.0")
root.geometry("1024x768")

menubar = Menu(root)
menubar.add_cascade(label='ファイルを開く', command= lambda: openFile())
root.config(menu=menubar)

v_radio = IntVar()
v_radio.set(RS)

lsRb = Radiobutton(root, text="Lightning Stage", command = selectGame, variable=v_radio, value=LS, state="disabled")
lsRb.place(relx=0.05, rely=0.02)
bsRb = Radiobutton(root, text="Burning Stage", command = selectGame, variable=v_radio, value=BS, state="disabled")
bsRb.place(relx=0.32, rely=0.02)
csRb = Radiobutton(root, text="Climax Stage", command = selectGame, variable=v_radio, value=CS, state="disabled")
csRb.place(relx=0.59, rely=0.02)
rsRb = Radiobutton(root, text="Rising Stage", command = selectGame, variable=v_radio, value=RS)
rsRb.place(relx=0.86, rely=0.02)
rsRb.select()

v_filename = StringVar()
filenameEt = ttk.Entry(root, textvariable=v_filename, font=("", 14), width=20, state="readonly", justify="center")
filenameEt.place(relx=0.05, rely=0.07)

notebook = ttk.Notebook(root)
notebook.place(relx=0.02, rely=0.13, relwidth=0.96, relheight=0.82)

tab_one = ttk.Frame(notebook)
notebook.add(tab_one, text="BGM、配置情報")
tab_two = ttk.Frame(notebook)
notebook.add(tab_two, text="要素1")
tab_3 = ttk.Frame(notebook)
notebook.add(tab_3, text="smf情報")
tab_4 = ttk.Frame(notebook)
notebook.add(tab_4, text="駅名位置情報")
tab_5 = ttk.Frame(notebook)
notebook.add(tab_5, text="要素2")
tab_6 = ttk.Frame(notebook)
notebook.add(tab_6, text="CPU情報")
tab_7 = ttk.Frame(notebook)
notebook.add(tab_7, text="Comic Script、土讃線")
tab_8 = ttk.Frame(notebook)
notebook.add(tab_8, text="レール情報")
tab_9 = ttk.Frame(notebook)
notebook.add(tab_9, text="要素3")

root.mainloop()
