from functools import partial

from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd

from importPy.tkinterScrollbarFrameClass import *

class ElseList3Widget:
    def __init__(self, frame, decryptFile, else3List, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.else3List = else3List
        self.reloadFunc = reloadFunc

        self.elseLf = ttk.LabelFrame(self.frame, text="else3")
        self.elseLf.pack(anchor=NW, padx=10, expand=True, fill=BOTH)

        scrollbarFrame = ScrollbarFrame(self.elseLf)

        self.txtFrame = ttk.Frame(scrollbarFrame.frame)
        self.txtFrame.pack(anchor=NW)

        self.else3CntNameLb = Label(self.txtFrame, text="else3数", font=("", 20), width=7, borderwidth=1, relief="solid")
        self.else3CntNameLb.grid(row=0, column=0, sticky=W+E)
        self.varElse3Cnt = IntVar()
        self.varElse3Cnt.set(len(self.else3List))
        self.else3CntTextLb = Label(self.txtFrame, textvariable=self.varElse3Cnt, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.else3CntTextLb.grid(row=0, column=1, sticky=W+E)
        self.else3CntBtn = Button(self.txtFrame, text="修正", font=("", 14), command=lambda :self.editElse3Cnt(self.varElse3Cnt.get()))
        self.else3CntBtn.grid(row=0, column=2, sticky=W+E)

        self.txtFrame2 = ttk.Frame(scrollbarFrame.frame)
        self.txtFrame2.pack(anchor=NW, pady=5)
        rowNum = 0
        
        for i in range(len(self.else3List)):
            else3Info = self.else3List[i]
            
            self.tempBtn = Button(self.txtFrame2, text="修正", font=("", 14), command=partial(self.editElse3ListCnt, i, else3Info[0:2]))
            self.tempBtn.grid(row=rowNum, column=0, sticky=W+E)

            self.varRailNo = IntVar()
            self.varRailNo.set(int(else3Info[0]))
            self.tempfTextLb = Label(self.txtFrame2, textvariable=self.varRailNo, font=("", 20), width=7, borderwidth=1, relief="solid")
            self.tempfTextLb.grid(row=rowNum, column=1, sticky=W+E)

            self.varTemp = IntVar()
            self.varTemp.set(int(else3Info[1]))
            self.tempfTextLb = Label(self.txtFrame2, textvariable=self.varTemp, font=("", 20), width=7, borderwidth=1, relief="solid")
            self.tempfTextLb.grid(row=rowNum, column=2, sticky=W+E)

            rowNum += 1
            
            for j in range(else3Info[1]):
                for k in range(8):
                    self.varTemp = IntVar()
                    self.varTemp.set(int(else3Info[2+8*j+k]))
                    self.tempfTextLb = Label(self.txtFrame2, textvariable=self.varTemp, font=("", 20), width=7, borderwidth=1, relief="solid")
                    self.tempfTextLb.grid(row=rowNum, column=k+1, sticky=W+E)
                self.tempBtn = Button(self.txtFrame2, text="修正", font=("", 14), command=partial(self.editElse3List, i, j, else3Info))
                self.tempBtn.grid(row=rowNum, column=0, sticky=W+E)
                rowNum += 1
            

    def editElse3Cnt(self, val):
        result = EditElse3CntWidget(self.frame, "else3数の変更", self.decryptFile, val)
        if result.reloadFlag:
            if not self.decryptFile.saveElse3Cnt(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="else3数を修正しました")
            self.reloadFunc()

    def editElse3ListCnt(self, i, valList):
        result = EditElse3ListCntWidget(self.frame, "else3の変更", self.decryptFile, valList)
        if result.reloadFlag:
            for j in range(2):
                self.else3List[i][j] = result.resultValueList[j]
            if not self.decryptFile.saveElse3List(self.else3List):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="else3数を修正しました")
            self.reloadFunc()
            
    def editElse3List(self, i, j, valList):
        else3List = valList[2+8*j:10+8*j]
        result = EditElse3ListWidget(self.frame, "else3の変更", self.decryptFile, else3List)
        if result.reloadFlag:
            for k in range(8):
                self.else3List[i][2+8*j+k] = result.resultValueList[k]
            if not self.decryptFile.saveElse3List(self.else3List):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="else3情報を修正しました")
            self.reloadFunc()

class EditElse3CntWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, val):
        self.decryptFile = decryptFile
        self.val = val
        self.resultValue = 0
        self.reloadFlag = False
        super(EditElse3CntWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text="値を入力してください", font=("", 14))
        self.valLb.pack()

        self.varElse3Cnt = IntVar()
        self.varElse3Cnt.set(self.val)
        self.valEt = ttk.Entry(master, textvariable=self.varElse3Cnt, font=("", 14), width=16)
        self.valEt.pack()

    def validate(self):
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)

        if result:
            try:
                try:
                    res = int(self.varElse3Cnt.get())
                    if res < 0:
                        errorMsg = "0以上の数字で入力してください。"
                        mb.showerror(title="数字エラー", message=errorMsg)
                        return False
                    self.resultValue = res
                except:
                    errorMsg = "整数で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

            if self.resultValue < self.val:
                msg = "設定した値は現在より少なく設定してます\nこの数で修正しますか？"
                result = mb.askokcancel(title="警告", message=msg, icon="warning", parent=self)
                if result:
                    return True
            else:
                return True

    def apply(self):
        self.reloadFlag = True

class EditElse3ListCntWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, else3Info):
        self.decryptFile = decryptFile
        self.else3Info = else3Info
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super(EditElse3ListCntWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        else3InfoLbList = ["レールNo", "数"]
        for i in range(len(self.else3Info)):
            self.else3Lb = ttk.Label(master, text=else3InfoLbList[i], font=("", 14))
            self.else3Lb.grid(row=i, column=0, sticky=W+E)
            self.varElse3 = IntVar()
            self.varElse3.set(self.else3Info[i])
            self.varList.append(self.varElse3)
            self.else3Et = ttk.Entry(master, textvariable=self.varElse3, font=("", 14))
            self.else3Et.grid(row=i, column=1, sticky=W+E)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)
        if result:
            try:
                try:
                    for i in range(len(self.varList)):
                        res = int(self.varList[i].get())
                        if res <= 0:
                            errorMsg = "1以上の数字で入力してください。"
                            mb.showerror(title="数字エラー", message=errorMsg)
                            return False
                        self.resultValueList.append(res)
                except:
                    errorMsg = "数字で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
            except Exception as e:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

            if self.resultValueList[1] < self.else3Info[1]:
                msg = "設定した値は現在より少なく設定してます\nこの数で修正しますか？"
                result = mb.askokcancel(title="警告", message=msg, icon="warning", parent=self)
                if result:
                    return True
            else:
                return True

    def apply(self):
        self.reloadFlag = True

class EditElse3ListWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, else3Info):
        self.decryptFile = decryptFile
        self.else3Info = else3Info
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super(EditElse3ListWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        else3InfoLbList = ["b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8"]
        for i in range(len(self.else3Info)):
            self.else3Lb = ttk.Label(master, text=else3InfoLbList[i], font=("", 14))
            self.else3Lb.grid(row=i, column=0, sticky=W+E)
            self.varElse3 = IntVar()
            self.varElse3.set(self.else3Info[i])
            self.varList.append(self.varElse3)
            self.else3Et = ttk.Entry(master, textvariable=self.varElse3, font=("", 14))
            self.else3Et.grid(row=i, column=1, sticky=W+E)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)
        if result:
            try:
                try:
                    for i in range(len(self.varList)):
                        res = int(self.varList[i].get())
                        self.resultValueList.append(res)
                    return True
                except:
                    errorMsg = "数字で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
            except Exception as e:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

    def apply(self):
        self.reloadFlag = True
