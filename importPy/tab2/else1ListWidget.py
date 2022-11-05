from functools import partial

from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd

class Else1ListWidget:
    def __init__(self, frame, decryptFile, else1List, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.else1List = else1List
        self.reloadFunc = reloadFunc

        self.else1Lf = ttk.LabelFrame(self.frame, text="else1")
        self.else1Lf.pack(anchor=NW, padx=10)

        self.txtFrame = ttk.Frame(self.else1Lf)
        self.txtFrame.pack(anchor=NW)

        self.varElse1 = DoubleVar()
        self.varElse1.set(round(float(self.else1List[0]), 3))
        self.else1TextLb = Label(self.txtFrame, textvariable=self.varElse1, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.else1TextLb.grid(row=0, column=0, sticky=W+E)
        self.else1Btn = Button(self.txtFrame, text="修正", font=("", 14), command=partial(self.editVarList, 0, [self.else1List[0]]))
        self.else1Btn.grid(row=0, column=1, sticky=W+E)

        self.txtFrame2 = ttk.Frame(self.else1Lf)
        self.txtFrame2.pack(anchor=NW, pady=5)
        
        for i in range(1, len(self.else1List)):
            else1Info = self.else1List[i]
            for j in range(len(else1Info)):
                if j in [0, 1]:
                    self.varTemp = IntVar()
                    self.varTemp.set(round(float(else1Info[j]), 3))
                else:
                    self.varTemp = IntVar()
                    self.varTemp.set(int(else1Info[j]))
                self.tempfTextLb = Label(self.txtFrame2, textvariable=self.varTemp, font=("", 20), width=7, borderwidth=1, relief="solid")
                self.tempfTextLb.grid(row=i, column=j, sticky=W+E)
                self.tempfBtn = Button(self.txtFrame2, text="修正", font=("", 14), command=partial(self.editVarList, i, else1Info))
                self.tempfBtn.grid(row=i, column=len(else1Info),  sticky=W+E)

    def editVarList(self, i, valList):
        result = EditElse1ListWidget(self.frame, "ele1の変更", self.decryptFile, valList)
        if result.reloadFlag:
            if i == 0:
                self.else1List[i] = result.resultValueList[0]
            else:
                self.else1List[i] = result.resultValueList
            if not self.decryptFile.saveEleList1(self.else1List):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="車両位置情報を修正しました")

            self.reloadFunc()


class EditElse1ListWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, valList):
        self.decryptFile = decryptFile
        self.valList = valList
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super(EditElse1ListWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text="値を入力してください", font=("", 14))
        self.valLb.grid(columnspan=2, row=0, column=0, sticky=W+E)

        for i in range(len(self.valList)):
            if i < 2:
                self.txtLb = ttk.Label(master, text="f{0}".format(i+1), font=("", 14))
                self.txtLb.grid(row=i, column=0, sticky=W+E)
            else:
                self.txtLb = ttk.Label(master, text="b{0}".format(i-1), font=("", 14))
                self.txtLb.grid(row=i, column=0, sticky=W+E)

            if i in [0, 1]:
                self.varTemp = DoubleVar()
                self.varTemp.set(round(float(self.valList[i]), 3))
            else:
                self.varTemp = IntVar()
                self.varTemp.set(int(self.valList[i]))
            self.varList.append(self.varTemp)
            self.txtEt = ttk.Entry(master, textvariable=self.varTemp, font=("", 14))
            self.txtEt.grid(row=i, column=1, sticky=W+E)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)
        if result:
            try:
                for i in range(len(self.valList)):
                    try:
                        if i in [0, 1]:
                            res = float(self.varList[i].get())
                        else:
                            res = int(self.varList[i].get())
                            
                        if res < 0:
                            errorMsg = "0以上の数字で入力してください。"
                            mb.showerror(title="数字エラー", message=errorMsg)
                            return False
                        self.resultValueList.append(res)
                    except:
                        errorMsg = "数字で入力してください。"
                        mb.showerror(title="エラー", message=errorMsg)
                return True
            except:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

    def apply(self):
        self.reloadFlag = True
