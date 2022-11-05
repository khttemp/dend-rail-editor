from functools import partial

from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd

class RailPosWidget:
    def __init__(self, frame, title, num, decryptFile, trainList, reloadFunc):
        self.frame = frame
        self.title = title
        self.railBtnList = []
        self.num = num
        self.decryptFile = decryptFile
        self.trainList = trainList
        self.reloadFunc = reloadFunc

        self.railPosLf = ttk.LabelFrame(self.frame, text=title)
        self.railPosLf.pack()

        self.playHeaderLb =  Label(self.railPosLf, text="player", font=("", 20), width=7, borderwidth=1, relief="solid")
        self.playHeaderLb.grid(row=0, column=0, sticky=W+E)

        self.railNoHeaderLb = Label(self.railPosLf, text="railNo", font=("", 20), width=7, borderwidth=1, relief="solid")
        self.railNoHeaderLb.grid(row=0, column=1, sticky=W+E)
        self.railPosHeaderLb = Label(self.railPosLf, text="railPos", font=("", 20), width=7, borderwidth=1, relief="solid")
        self.railPosHeaderLb.grid(row=0, column=2, sticky=W+E)
        self.ele1HeaderLb = Label(self.railPosLf, text="ele1", font=("", 20), width=5, borderwidth=1, relief="solid")
        self.ele1HeaderLb.grid(row=0, column=3, sticky=W+E)
        self.ele2HeaderLb = Label(self.railPosLf, text="ele2", font=("", 20), width=5, borderwidth=1, relief="solid")
        self.ele2HeaderLb.grid(row=0, column=4, sticky=W+E)
        self.ele3HeaderLb = Label(self.railPosLf, text="ele3", font=("", 20), width=5, borderwidth=1, relief="solid")
        self.ele3HeaderLb.grid(row=0, column=5, sticky=W+E)
            
        for i in range(len(self.trainList)):
            trainInfo = self.trainList[i]
            self.playLb = Label(self.railPosLf, text="{0}P".format(i+1), font=("", 20), borderwidth=1, relief="solid")
            self.playLb.grid(row=i+1, column=0, sticky=W+E)
            for j in range(len(trainInfo)):
                self.valLb = Label(self.railPosLf, text=trainInfo[j], font=("", 20), borderwidth=1, relief="solid")
                self.valLb.grid(row=i+1, column=j+1, sticky=W+E)

            self.railBtn = Button(self.railPosLf, text="修正", font=("", 14), command=partial(self.editVar, i, trainInfo))
            self.railBtn.grid(row=i+1, column=len(trainInfo)+1, sticky=W+E)

    def editVar(self, i, trainInfo):
        result = EditRailPosWidget(self.frame, self.title + "の変更", self.decryptFile, trainInfo)

        if result.reloadFlag:
            self.trainList[i] = result.resultValueList
            if not self.decryptFile.saveRailPos(self.num, self.trainList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="車両位置情報を修正しました")

            self.reloadFunc()

class EditRailPosWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, trainInfo):
        self.decryptFile = decryptFile
        self.trainInfo = trainInfo
        self.varList = []
        self.resultValueList = []
        self.reloadFlag = False
        super(EditRailPosWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text="値を入力してください", font=("", 14))
        self.valLb.grid(columnspan=2, row=0, column=0, sticky=W+E)

        trainInfoLbList = ["railNo", "railPos", "ele1", "ele2", "ele3"]
        for i in range(len(self.trainInfo)):
            self.railLb = ttk.Label(master, text=trainInfoLbList[i], font=("", 14))
            self.railLb.grid(row=i+1, column=0, sticky=W+E)
            self.varRail = IntVar()
            self.varRail.set(self.trainInfo[i])
            self.varList.append(self.varRail)
            self.railEt = ttk.Entry(master, textvariable=self.varRail, font=("", 14))
            self.railEt.grid(row=i+1, column=1, sticky=W+E)

    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)
        if result:
            try:
                try:
                    for i in range(len(self.varList)):
                        res = int(self.varList[i].get())
                        if res < 0:
                            errorMsg = "0以上の数字で入力してください。"
                            mb.showerror(title="数字エラー", message=errorMsg)
                            return False
                        self.resultValueList.append(res)
                    return True
                except:
                    errorMsg = "整数で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

    def apply(self):
        self.reloadFlag = True
