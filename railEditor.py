import os
import tkinter
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

from importPy.tkinterTab import tab1AllWidget, tab2AllWidget, tab3AllWidget, tab4AllWidget, tab5AllWidget, tab6AllWidget, tab7AllWidget, tab8AllWidget, tab9AllWidget, tab10AllWidget, tab11AllWidget
import dendDecrypt.RSdecrypt as dendRs
import dendDecrypt.CSdecrypt as dendCs
import dendDecrypt.BSdecrypt as dendBs
import dendDecrypt.LSdecrypt as dendLs

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
        filename = os.path.basename(file_path)
        v_filename.set(filename)
        del decryptFile
        decryptFile = None

        if v_radio.get() == RS:
            decryptFile = dendRs.RailDecrypt(file_path)
        elif v_radio.get() == CS:
            decryptFile = dendCs.RailDecrypt(file_path)
        elif v_radio.get() == BS:
            decryptFile = dendBs.RailDecrypt(file_path)
        elif v_radio.get() == LS:
            decryptFile = dendLs.RailDecrypt(file_path)

        if not decryptFile.open():
            if decryptFile.error == "":
                errorMsg = decryptFile.game + "のレールデータではありません"
                mb.showerror(title="エラー", message=errorMsg)
            else:
                decryptFile.printError()
                mb.showerror(title="エラー", message=errorMsg)
            return

        deleteAllWidget()
        if v_radio.get() == LS:
            cb["values"] = lsInfo
        else:
            cb["values"] = info
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
    elif index == 10:
        tab11AllWidget(tabFrame, decryptFile, reloadWidget)


def reloadWidget():
    global decryptFile
    decryptFile = decryptFile.reload()
    deleteAllWidget()
    selectInfo(cb.current())


def selectGame():
    v_filename.set("")
    cb.set("")
    cb["state"] = "disabled"
    deleteAllWidget()


root = tkinter.Tk()
root.title("電車でD レール改造 1.3.1")
root.geometry("1024x768")

menubar = tkinter.Menu(root)
menubar.add_cascade(label="ファイルを開く", command=lambda: openFile())
root.config(menu=menubar)

v_radio = tkinter.IntVar()
v_radio.set(RS)

lsRb = tkinter.Radiobutton(root, text="Lightning Stage", command=selectGame, variable=v_radio, value=LS)
lsRb.place(relx=0.05, rely=0.02)
bsRb = tkinter.Radiobutton(root, text="Burning Stage", command=selectGame, variable=v_radio, value=BS)
bsRb.place(relx=0.32, rely=0.02)
csRb = tkinter.Radiobutton(root, text="Climax Stage", command=selectGame, variable=v_radio, value=CS)
csRb.place(relx=0.59, rely=0.02)
rsRb = tkinter.Radiobutton(root, text="Rising Stage", command=selectGame, variable=v_radio, value=RS)
rsRb.place(relx=0.86, rely=0.02)
rsRb.select()

v_filename = tkinter.StringVar()
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
    "要素4",
    "AMB情報"
]

lsInfo = [
    "BGM、配置情報",
    "要素1",
    "smf情報",
    "駅名位置情報",
    "要素2",
    "CPU情報",
    "Comic Script、土讃線",
    "レール情報",
    "Cam",
    "要素4",
    "AMB情報"
]

cb = ttk.Combobox(root, width=31, values=info, state="disabled")
cb.bind("<<ComboboxSelected>>", lambda e: selectInfo(cb.current()))
cb.place(relx=0.05, rely=0.12)

tabFrame = ttk.Frame(root, borderwidth=1, relief="solid")
tabFrame.place(relx=0.05, rely=0.17, relwidth=0.90, relheight=0.80)

root.mainloop()
