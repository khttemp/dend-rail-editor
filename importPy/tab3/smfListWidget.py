import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd

from importPy.tkinterScrollbarTreeview import ScrollbarTreeview


class SmfListWidget:
    def __init__(self, frame, decryptFile, smfList, rowNum, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.smfList = smfList
        self.reloadFunc = reloadFunc
        self.copySmfInfo = []

        self.swfListLf = ttk.LabelFrame(self.frame, text="smf情報")
        self.swfListLf.pack(anchor=tkinter.NW, padx=10, pady=5)

        self.headerFrame = ttk.Frame(self.swfListLf)
        self.headerFrame.pack()

        self.selectLbFrame = ttk.Frame(self.headerFrame)
        self.selectLbFrame.pack(anchor=tkinter.NW, side=tkinter.LEFT)

        selectLb = ttk.Label(self.selectLbFrame, text="選択した行番号：", font=("", 14))
        selectLb.pack(side=tkinter.LEFT, padx=15, pady=15)

        self.v_select = tkinter.StringVar()
        selectEt = ttk.Entry(self.selectLbFrame, textvariable=self.v_select, font=("", 14), width=5, state="readonly", justify="center")
        selectEt.pack(side=tkinter.LEFT, padx=5, pady=15)

        self.btnFrame = ttk.Frame(self.headerFrame)
        self.btnFrame.pack(anchor=tkinter.NE, padx=15)

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
        self.treeFrame = ttk.Frame(self.swfListLf)
        self.treeFrame.pack(anchor=tkinter.NW, fill=tkinter.X)

        self.treeviewFrame = ScrollbarTreeview(self.treeFrame, rowNum, self.v_select, btnList)

        col_tuple = ("番号", "smf名", "e1", "e2", "長さ", "e3", "e4", "架線柱No", "架線No")

        self.treeviewFrame.tree['columns'] = col_tuple
        self.treeviewFrame.tree.column("#0", width=0, stretch=False)
        self.treeviewFrame.tree.column("番号", anchor=tkinter.CENTER, width=50, stretch=False)
        self.treeviewFrame.tree.column("smf名", anchor=tkinter.CENTER, width=130)
        self.treeviewFrame.tree.column("e1", anchor=tkinter.CENTER, width=50)
        self.treeviewFrame.tree.column("e2", anchor=tkinter.CENTER, width=50)
        self.treeviewFrame.tree.column("長さ", anchor=tkinter.CENTER, width=50)
        self.treeviewFrame.tree.column("e3", anchor=tkinter.CENTER, width=50)
        self.treeviewFrame.tree.column("e4", anchor=tkinter.CENTER, width=50)
        self.treeviewFrame.tree.column("架線柱No", anchor=tkinter.CENTER, width=50)
        self.treeviewFrame.tree.column("架線No", anchor=tkinter.CENTER, width=50)

        self.treeviewFrame.tree.heading("番号", text="番号", anchor=tkinter.CENTER)
        self.treeviewFrame.tree.heading("smf名", text="smf名", anchor=tkinter.CENTER)
        self.treeviewFrame.tree.heading("e1", text="e1", anchor=tkinter.CENTER)
        self.treeviewFrame.tree.heading("e2", text="e2", anchor=tkinter.CENTER)
        self.treeviewFrame.tree.heading("長さ", text="長さ", anchor=tkinter.CENTER)
        self.treeviewFrame.tree.heading("e3", text="e3", anchor=tkinter.CENTER)
        self.treeviewFrame.tree.heading("e4", text="e4", anchor=tkinter.CENTER)
        self.treeviewFrame.tree.heading("架線柱No", text="架線柱No", anchor=tkinter.CENTER)
        self.treeviewFrame.tree.heading("架線No", text="架線No", anchor=tkinter.CENTER)

        self.treeviewFrame.tree["displaycolumns"] = col_tuple

        index = 0
        for smfInfo in self.smfList:
            data = (index,)
            data += (smfInfo[0], smfInfo[1], smfInfo[2], smfInfo[3], smfInfo[4], smfInfo[5])
            data += (smfInfo[6], smfInfo[7])
            self.treeviewFrame.tree.insert(parent='', index='end', iid=index, values=data)
            index += 1

    def editLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["番号"])
        result = EditSmfListWidget(self.frame, "smf修正", self.decryptFile, "modify", num, selectItem)
        if result.reloadFlag:
            if not self.decryptFile.saveSmfInfo(num, "modify", result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="smf情報を修正しました")
            self.reloadFunc()

    def insertLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["番号"])
        result = EditSmfListWidget(self.frame, "smf挿入", self.decryptFile, "insert", num, selectItem)
        if result.reloadFlag:
            if result.insert == 0:
                num += 1
            if not self.decryptFile.saveSmfInfo(num, "insert", result.resultValueList):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="smf情報を修正しました")
            self.reloadFunc()

    def deleteLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        num = int(selectItem["番号"])
        warnMsg = "選択した行を削除します。\nそれでもよろしいですか？"
        result = mb.askokcancel(title="警告", message=warnMsg, icon="warning")
        if result:
            if not self.decryptFile.saveSmfInfo(num, "delete", []):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="smf情報を修正しました")
            self.reloadFunc()

    def copyLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)

        smfInfoKeyList = list(selectItem.keys())
        smfInfoKeyList.pop(0)
        copyList = []
        for i in range(len(smfInfoKeyList)):
            key = smfInfoKeyList[i]
            if i == 0:
                copyList.append(selectItem[key])
            elif i in [1, 2, 4, 5]:
                copyList.append(int(selectItem[key], 16))
            else:
                copyList.append(int(selectItem[key]))
        self.copySmfInfo = copyList
        mb.showinfo(title="成功", message="コピーしました")
        self.pasteLineBtn["state"] = "normal"

    def pasteLine(self):
        selectId = self.treeviewFrame.tree.selection()[0]
        selectItem = self.treeviewFrame.tree.set(selectId)
        result = PasteSmfListDialog(self.frame, "smf貼り付け", self.decryptFile, int(selectItem["番号"]), self.copySmfInfo)
        if result.reloadFlag:
            self.reloadFunc()


class EditSmfListWidget(sd.Dialog):
    def __init__(self, master, title, decryptFile, mode, num, smfInfo):
        self.decryptFile = decryptFile
        self.mode = mode
        self.num = num
        self.smfInfo = smfInfo
        self.varList = []
        self.reloadFlag = False
        self.insert = 0
        self.resultValueList = []
        super(EditSmfListWidget, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        smfInfoKeyList = list(self.smfInfo.keys())
        smfInfoKeyList.pop(0)
        for i in range(len(smfInfoKeyList)):
            self.smfInfoLb = ttk.Label(master, text=smfInfoKeyList[i], font=("", 14))
            self.smfInfoLb.grid(row=i, column=0, sticky=tkinter.W + tkinter.E)
            if i == 0:
                self.varSmfInfo = tkinter.StringVar()
                self.varList.append(self.varSmfInfo)
                self.smfInfoEt = ttk.Entry(master, textvariable=self.varSmfInfo, font=("", 14))
                self.smfInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)

                if self.mode == "modify":
                    self.varSmfInfo.set(self.smfInfo[smfInfoKeyList[i]])
            elif i in [1, 2, 4, 5]:
                mb = ttk.Menubutton(master, text="switch設定")
                menu = tkinter.Menu(mb)
                mb["menu"] = menu

                Flg0 = tkinter.BooleanVar()
                Flg1 = tkinter.BooleanVar()
                Flg2 = tkinter.BooleanVar()
                Flg3 = tkinter.BooleanVar()
                Flg4 = tkinter.BooleanVar()
                Flg5 = tkinter.BooleanVar()
                Flg6 = tkinter.BooleanVar()
                Flg7 = tkinter.BooleanVar()
                flagList = [Flg0, Flg1, Flg2, Flg3, Flg4, Flg5, Flg6, Flg7]
                self.varList.append(flagList)
                menu.add_checkbutton(label="フラグ0", variable=Flg7)
                menu.add_checkbutton(label="フラグ1", variable=Flg6)
                menu.add_checkbutton(label="フラグ2", variable=Flg5)
                menu.add_checkbutton(label="フラグ3", variable=Flg4)
                menu.add_checkbutton(label="フラグ4", variable=Flg3)
                menu.add_checkbutton(label="フラグ5", variable=Flg2)
                menu.add_checkbutton(label="フラグ6", variable=Flg1)
                menu.add_checkbutton(label="フラグ7", variable=Flg0)
                if self.mode == "modify":
                    val = int(self.smfInfo[smfInfoKeyList[i]], 16)
                    for j in range(8):
                        if val & (2**j) == 0:
                            flagList[j].set(False)
                        else:
                            flagList[j].set(True)

                mb.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
            else:
                self.varSmfInfo = tkinter.IntVar()
                self.varList.append(self.varSmfInfo)
                self.smfInfoEt = ttk.Entry(master, textvariable=self.varSmfInfo, font=("", 14))
                self.smfInfoEt.grid(row=i, column=1, sticky=tkinter.W + tkinter.E)
                if self.mode == "modify":
                    self.varSmfInfo.set(self.smfInfo[smfInfoKeyList[i]])
                elif self.mode == "insert":
                    if i == 3:
                        default = 8
                    else:
                        default = 255
                    self.varSmfInfo.set(default)

        if self.mode == "insert":
            self.setInsertWidget(master, len(smfInfoKeyList))

    def setInsertWidget(self, master, index):
        self.xLine = ttk.Separator(master, orient=tkinter.HORIZONTAL)
        self.xLine.grid(row=index, column=0, columnspan=2, sticky=tkinter.W + tkinter.E, pady=10)

        self.insertLb = ttk.Label(master, text="挿入する位置", font=("", 12))
        self.insertLb.grid(row=index + 1, column=0, sticky=tkinter.W + tkinter.E)
        self.v_insert = tkinter.StringVar()
        self.insertCb = ttk.Combobox(master, state="readonly", font=("", 12), textvariable=self.v_insert, values=["後", "前"])
        self.insertCb.grid(row=index + 1, column=1, sticky=tkinter.W + tkinter.E)
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
                        elif i in [1, 2, 4, 5]:
                            bitList = self.varList[i]
                            res = 0
                            for j in range(len(bitList)):
                                if bitList[j].get():
                                    res |= (2**j)
                        else:
                            res = int(self.varList[i].get())
                        self.resultValueList.append(res)
                    if self.mode == "insert":
                        self.insert = self.insertCb.current()

                    return True
                except Exception:
                    errorMsg = "整数で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

    def apply(self):
        self.reloadFlag = True


class PasteSmfListDialog(sd.Dialog):
    def __init__(self, master, title, decryptFile, num, copySmfInfo):
        self.decryptFile = decryptFile
        self.num = num
        self.copySmfInfo = copySmfInfo
        self.reloadFlag = False
        super(PasteSmfListDialog, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)
        self.posLb = ttk.Label(master, text="挿入する位置を選んでください", font=("", 14))
        self.posLb.pack(padx=10, pady=10)

    def buttonbox(self):
        box = tkinter.Frame(self, padx=5, pady=5)
        self.frontBtn = tkinter.Button(box, text="前", font=("", 12), width=10, command=self.frontInsert)
        self.frontBtn.grid(row=0, column=0, padx=5)
        self.backBtn = tkinter.Button(box, text="後", font=("", 12), width=10, command=self.backInsert)
        self.backBtn.grid(row=0, column=1, padx=5)
        self.cancelBtn = tkinter.Button(box, text="Cancel", font=("", 12), width=10, command=self.cancel)
        self.cancelBtn.grid(row=0, column=2, padx=5)
        box.pack()

    def frontInsert(self):
        self.ok()
        if not self.decryptFile.saveSmfInfo(self.num, "insert", self.copySmfInfo):
            self.decryptFile.printError()
            mb.showerror(title="エラー", message="予想外のエラーが発生しました")
            return
        mb.showinfo(title="成功", message="smf情報を修正しました")
        self.reloadFlag = True

    def backInsert(self):
        self.ok()
        if not self.decryptFile.saveSmfInfo(self.num + 1, "insert", self.copySmfInfo):
            self.decryptFile.printError()
            mb.showerror(title="エラー", message="予想外のエラーが発生しました")
            return
        mb.showinfo(title="成功", message="smf情報を修正しました")
        self.reloadFlag = True
