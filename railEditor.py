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
            cb.current(0)
            cb["state"] = "readonly"
            selectInfo(cb.current())

def deleteAllWidget():
    children = tabFrame.winfo_children()
    for child in children:
        child.destroy()

def selectInfo(index):
    global decryptFile
    deleteAllWidget()
    
    if index == 0:
        tab1AllWidget(tabFrame, decryptFile, reloadWidget)
    elif index == 1:
        tab2AllWidget(tabFrame, decryptFile, reloadWidget)
    elif index == 2:
        tab3AllWidget(tabFrame, decryptFile, reloadWidget)
    elif index == 3:
        tab4AllWidget(tabFrame, decryptFile, reloadWidget)
    elif index == 4:
        tab5AllWidget(tabFrame, decryptFile, reloadWidget)
    elif index == 5:
        tab6AllWidget(tabFrame, decryptFile, reloadWidget)
    elif index == 6:
        tab7AllWidget(tabFrame, decryptFile, reloadWidget)
    elif index == 7:
        tab8AllWidget(tabFrame, decryptFile, reloadWidget)
    elif index == 8:
        tab9AllWidget(tabFrame, decryptFile, reloadWidget)
    elif index == 9:
        tab10AllWidget(tabFrame, decryptFile, reloadWidget)

def reloadWidget():
    global decryptFile
    decryptFile = decryptFile.reload()
    deleteAllWidget()
    selectInfo(cb.current())
    
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

info = [
    "BGM、配置情報",
    "要素1",
    "smf情報",
    "駅名位置情報",
    "要素2",
    "CPU情報",
    "Comic Script、土讃線",
    "レール情報",
    "要素3",
    "AMB情報"
]

cb = ttk.Combobox(root, width=31, values=info, state="disabled")
cb.bind('<<ComboboxSelected>>', lambda e: selectInfo(cb.current()))
cb.place(relx=0.05, rely=0.12)

tabFrame = ttk.Frame(root, borderwidth=1, relief="solid")
tabFrame.place(relx=0.05, rely=0.17, relwidth=0.90, relheight=0.80)

root.mainloop()
