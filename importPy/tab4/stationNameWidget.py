import copy

from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd

from importPy.tkinterScrollbarTreeview import *

class StationNameWidget:
    def __init__(self, frame, decryptFile, stationNameList, rowNum, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.stationNameList = stationNameList
        self.reloadFunc = reloadFunc
        self.copyStationNameInfo = []
        self.stationNameLf = ttk.LabelFrame(self.frame, text="駅名位置情報")
        self.stationNameLf.pack(anchor=NW, padx=10, pady=5)

        self.headerFrame = ttk.Frame(self.stationNameLf)
        self.headerFrame.pack()

        self.selectLbFrame = ttk.Frame(self.headerFrame)
        self.selectLbFrame.pack(anchor=NW, side=LEFT)
        
        selectLb = ttk.Label(self.selectLbFrame, text="選択した行番号：", font=("",14))
        selectLb.pack(side=LEFT, padx=15, pady=15)

        self.v_select = StringVar()
        selectEt = ttk.Entry(self.selectLbFrame, textvariable=self.v_select, font=("",14), width=5, state="readonly", justify="center")
        selectEt.pack(side=LEFT, padx=5, pady=15)

        self.btnFrame = ttk.Frame(self.headerFrame)
        self.btnFrame.pack(anchor=NE, padx=15)

        editLineBtn = ttk.Button(self.btnFrame, text="選択した行を修正する", width=25, state="disabled", command=self.editLine)
        editLineBtn.grid(row=0, column=0, padx=10, pady=15)

        insertLineBtn = ttk.Button(self.btnFrame, text="選択した行に挿入する", width=25, state="disabled", command=self.insertLine)
        insertLineBtn.grid(row=0, column=1, padx=10, pady=15)

        deleteLineBtn = ttk.Button(self.btnFrame, text="選択した行を削除する", width=25, state="disabled", command=self.deleteLine)
        deleteLineBtn.grid(row=0, column=2, padx=10, pady=15)

        copyLineBtn = ttk.Button(self.btnFrame, text="選択した行をコピーする", width=25, state="disabled", command=self.copyLine)
        copyLineBtn.grid(row=1, column=0, padx=10, pady=15)

        self.pasteLineBtn = ttk.Button(self.btnFrame, text="選択した行に貼り付けする", width=25, state="disabled", command=self.pasteLine)
        self.pasteLineBtn.grid(row=1, column=1, padx=10, pady=15)

        btnList = [
            editLineBtn,
            insertLineBtn,
            deleteLineBtn,
            copyLineBtn
        ]
        self.treeFrame = ttk.Frame(self.stationNameLf)
        self.treeFrame.pack(anchor=NW, fill=X)

        self.treeviewFrame = ScrollbarTreeview(self.treeFrame, rowNum, self.v_select, btnList)

        col_tuple = ("番号", "駅名", "駅フラグ", "レールNo", "f1", "f2", "f3", "e1", "e2", "e3", "e4")

        self.treeviewFrame.tree['columns'] = col_tuple
        self.treeviewFrame.tree.column("#0", width=0, stretch=False)
        self.treeviewFrame.tree.column("番号", anchor=CENTER, width=50, stretch=False)
        self.treeviewFrame.tree.column("駅名", anchor=CENTER, width=130)
        self.treeviewFrame.tree.column("駅フラグ", anchor=CENTER, width=50)
        self.treeviewFrame.tree.column("レールNo", anchor=CENTER, width=50)
        self.treeviewFrame.tree.column("f1", anchor=CENTER, width=50)
        self.treeviewFrame.tree.column("f2", anchor=CENTER, width=50)
        self.treeviewFrame.tree.column("f3", anchor=CENTER, width=50)
        self.treeviewFrame.tree.column("e1", anchor=CENTER, width=50)
        self.treeviewFrame.tree.column("e2", anchor=CENTER, width=50)
        self.treeviewFrame.tree.column("e3", anchor=CENTER, width=50)
        self.treeviewFrame.tree.column("e4", anchor=CENTER, width=50)

        self.treeviewFrame.tree.heading("番号", text="番号", anchor=CENTER)
        self.treeviewFrame.tree.heading("駅名", text="駅名", anchor=CENTER)
        self.treeviewFrame.tree.heading("駅フラグ", text="駅フラグ", anchor=CENTER)
        self.treeviewFrame.tree.heading("レールNo", text="レールNo", anchor=CENTER)
        self.treeviewFrame.tree.heading("f1", text="f1", anchor=CENTER)
        self.treeviewFrame.tree.heading("f2", text="f2", anchor=CENTER)
        self.treeviewFrame.tree.heading("f3", text="f3", anchor=CENTER)
        self.treeviewFrame.tree.heading("e1", text="e1", anchor=CENTER)
        self.treeviewFrame.tree.heading("e2", text="e2", anchor=CENTER)
        self.treeviewFrame.tree.heading("e3", text="e3", anchor=CENTER)
        self.treeviewFrame.tree.heading("e4", text="e4", anchor=CENTER)

        self.treeviewFrame.tree["displaycolumns"] = col_tuple

        index = 0
        for stNameInfo in self.stationNameList:
            data = (index,)
            data += (stNameInfo[0], stNameInfo[1], stNameInfo[2])
            data += (round(float(stNameInfo[3]), 3), round(float(stNameInfo[4]), 3), round(float(stNameInfo[5]), 3))
            data += (stNameInfo[6], stNameInfo[7], stNameInfo[8], stNameInfo[9])
            self.treeviewFrame.tree.insert(parent='', index='end', iid=index ,values=data)
            index += 1
        
    def editLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["番号"])
        result = EditStationNameListWidget(self.frame, "駅名位置修正", self.decryptFile, "modify", num, selectItem)
        if result.reloadFlag:
            if not self.decryptFile.saveStationNameInfo(num, "modify", result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="駅名位置情報を修正しました")
            self.reloadFunc()
        
    def insertLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["番号"])
        result = EditStationNameListWidget(self.frame, "駅名位置挿入", self.decryptFile, "insert", num, selectItem)
        if result.reloadFlag:
            if result.insert == 0:
                num += 1
            if not self.decryptFile.saveStationNameInfo(num, "insert", result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="駅名位置情報を修正しました")
            self.reloadFunc()
        
    def deleteLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["番号"])
        warnMsg = "選択した行を削除します。\nそれでもよろしいですか？"
        result = mb.askokcancel(title="警告", message=warnMsg, icon="warning")
        if result:
            if not self.decryptFile.saveStationNameInfo(num, "delete", []):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="駅名位置情報を修正しました")
            self.reloadFunc()

    def copyLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)

        stationNameInfoKeyList = list(selectItem.keys())
        stationNameInfoKeyList.pop(0)
        copyList = []
        for i in range(len(stationNameInfoKeyList)):
            key = stationNameInfoKeyList[i]
            copyList.append(selectItem[key])
        self.copyStationNameInfo = copyList
        mb.showinfo(title="成功", message="コピーしました")
        self.pasteLineBtn["state"] = "normal"

    def pasteLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        result = PasteStationNameDialog(self.frame, "駅名位置貼り付け", self.decryptFile, int(selectItem["番号"]), self.copyStationNameInfo)
        if result.reloadFlag:
            self.reloadFunc()

class EditStationNameListWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, mode, num, stationNameInfo):
        self.decryptFile = decryptFile
        self.mode = mode
        self.num = num
        self.stationNameInfo = stationNameInfo
        self.varList = []
        self.reloadFlag = False
        self.insert = 0
        self.resultValueList = []
        super(EditStationNameListWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        stationNameInfoKeyList = list(self.stationNameInfo.keys())
        stationNameInfoKeyList.pop(0)
        for i in range(len(stationNameInfoKeyList)):
            self.stationNameInfoLb = ttk.Label(master, text=stationNameInfoKeyList[i], font=("", 14))
            self.stationNameInfoLb.grid(row=i, column=0, sticky=W+E)
            if i == 0:
                self.varStationNameInfo = StringVar()
                self.varList.append(self.varStationNameInfo)
                self.stationNameInfoEt = ttk.Entry(master, textvariable=self.varStationNameInfo, font=("", 14))
                self.stationNameInfoEt.grid(row=i, column=1, sticky=W+E)

                if self.mode == "modify":
                    self.varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
            elif i in [3, 4, 5]:
                self.varStationNameInfo = DoubleVar()
                self.varList.append(self.varStationNameInfo)
                self.stationNameInfoEt = ttk.Entry(master, textvariable=self.varStationNameInfo, font=("", 14))
                self.stationNameInfoEt.grid(row=i, column=1, sticky=W+E)
                if self.mode == "modify":
                    self.varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])
            else:
                self.varStationNameInfo = IntVar()
                self.varList.append(self.varStationNameInfo)
                self.stationNameInfoEt = ttk.Entry(master, textvariable=self.varStationNameInfo, font=("", 14))
                self.stationNameInfoEt.grid(row=i, column=1, sticky=W+E)
                if self.mode == "modify":
                    self.varStationNameInfo.set(self.stationNameInfo[stationNameInfoKeyList[i]])

        if self.mode == "insert":
            self.setInsertWidget(master, len(stationNameInfoKeyList))

    def setInsertWidget(self, master, index):
        self.xLine = ttk.Separator(master, orient=HORIZONTAL)
        self.xLine.grid(row=index, column=0, columnspan=2, sticky=E+W, pady=10)

        self.insertLb = ttk.Label(master, text="挿入する位置", font=("", 12))
        self.insertLb.grid(row=index+1, column=0, sticky=W+E)
        self.v_insert = StringVar()
        self.insertCb = ttk.Combobox(master, state="readonly", font=("", 12), textvariable=self.v_insert, values=["後", "前"])
        self.insertCb.grid(row=index+1, column=1, sticky=W+E)
        self.insertCb.current(0)
        
    def validate(self):
        self.resultValueList = []
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)
        if result:
            try:
                try:
                    for i in range(len(self.varList)):
                        if i == 0:
                            res = self.varList[i].get()
                        elif i in [3, 4, 5]:
                            res = float(self.varList[i].get())
                        else:
                            res = int(self.varList[i].get())
                        self.resultValueList.append(res)
                    if self.mode == "insert":
                        self.insert = self.insertCb.current()
                            
                    return True
                except Exception as e:
                    errorMsg = "整数で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
            except Exception as e:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

    def apply(self):
        self.reloadFlag = True

class PasteStationNameDialog(sd.Dialog):
    def __init__(self, master, title, decryptFile, num, copyStationNameInfo):
        self.decryptFile = decryptFile
        self.num = num
        self.copyStationNameInfo = copyStationNameInfo
        self.reloadFlag = False
        super(PasteStationNameDialog, self).__init__(parent=master, title=title)
    def body(self, master):
        self.resizable(False, False)
        self.posLb = ttk.Label(master, text="挿入する位置を選んでください", font=("", 14))
        self.posLb.pack(padx=10, pady=10)
    def buttonbox(self):
        box = Frame(self, padx=5, pady=5)
        self.frontBtn = Button(box, text="前", font=("", 12), width=10, command=self.frontInsert)
        self.frontBtn.grid(row=0, column=0, padx=5)
        self.backBtn = Button(box, text="後", font=("", 12), width=10, command=self.backInsert)
        self.backBtn.grid(row=0, column=1, padx=5)
        self.cancelBtn = Button(box, text="Cancel", font=("", 12), width=10, command=self.cancel)
        self.cancelBtn.grid(row=0, column=2, padx=5)
        box.pack()
    def frontInsert(self):
        self.ok()
        if not self.decryptFile.saveStationNameInfo(self.num, "insert", self.copyStationNameInfo):
            self.decryptFile.printError()
            mb.showerror(title="エラー", message="予想外のエラーが発生しました")
            return
        mb.showinfo(title="成功", message="stationName情報を修正しました")
        self.reloadFlag = True
                
    def backInsert(self):
        self.ok()
        if not self.decryptFile.saveStationNameInfo(self.num + 1, "insert", self.copyStationNameInfo):
            self.decryptFile.printError()
            mb.showerror(title="エラー", message="予想外のエラーが発生しました")
            return
        mb.showinfo(title="成功", message="stationName情報を修正しました")
        self.reloadFlag = True
