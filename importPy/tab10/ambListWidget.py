import traceback

from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
from tkinter import filedialog as fd

class AmbListWidget:
    def __init__(self, frame, decryptFile, ambList, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.smfList = [smfInfo[0] for smfInfo in decryptFile.smfList]
        self.ambList = ambList
        self.varList = []
        self.varChildList = []
        self.reloadFunc = reloadFunc

        self.smfList.extend(["モデル設定通り", "なし"])
        
        #
        self.ambNoFrame = ttk.Frame(self.frame)
        self.ambNoFrame.pack(anchor=NW, padx=30, pady=30)
        self.ambNoLb = ttk.Label(self.ambNoFrame, text="AMB No", font=("", 14))
        self.ambNoLb.grid(row=0, column=0, sticky=W+E)
        self.v_ambNo = IntVar()
        self.ambNoEt = ttk.Entry(self.ambNoFrame, textvariable=self.v_ambNo, font=("", 14), width=7, justify="center")
        self.ambNoEt.grid(row=0, column=1, sticky=W+E, padx=10)
        self.searchBtn = ttk.Button(self.ambNoFrame, text="照会", command=lambda: self.searchAmb(self.v_ambNo.get()))
        self.searchBtn.grid(row=0, column=2, sticky=W+E, padx=30)

        self.csvSaveBtn = ttk.Button(self.ambNoFrame, text="CSVで上書きする", command=self.saveCsv)
        self.csvSaveBtn.grid(row=0, column=3, sticky=W+E, padx=30)

        ###
        self.sidePackFrame = ttk.Frame(self.frame)
        self.sidePackFrame.pack(anchor=NW)

        #
        self.ambInfoLf = ttk.LabelFrame(self.sidePackFrame, text="AMB情報")
        self.ambInfoLf.pack(anchor=NW, side=LEFT, padx=30, pady=15)
        self.const0Lb = ttk.Label(self.ambInfoLf, text="const0", font=("", 14))
        self.const0Lb.grid(row=0, column=0, sticky=W+E, padx=10, pady=10)
        self.v_const0 = IntVar()
        self.const0Et = ttk.Entry(self.ambInfoLf, textvariable=self.v_const0, font=("", 14), width=7, justify="center", state="readonly")
        self.const0Et.grid(row=0, column=1, sticky=W+E, padx=10, pady=10)

        self.lengthLb = ttk.Label(self.ambInfoLf, text="長さ", font=("", 14))
        self.lengthLb.grid(row=1, column=0, sticky=W+E, padx=10, pady=10)
        self.v_length = IntVar()
        self.lengthEt = ttk.Entry(self.ambInfoLf, textvariable=self.v_length, font=("", 14), width=7, justify="center", state="readonly")
        self.lengthEt.grid(row=1, column=1, sticky=W+E, padx=10, pady=10)

        self.railNoLb = ttk.Label(self.ambInfoLf, text="配置レールNo", font=("", 14))
        self.railNoLb.grid(row=2, column=0, sticky=W+E, padx=10, pady=10)
        self.v_railNo = IntVar()
        self.railNoEt = ttk.Entry(self.ambInfoLf, textvariable=self.v_railNo, font=("", 14), width=7, justify="center", state="readonly")
        self.railNoEt.grid(row=2, column=1, sticky=W+E, padx=10, pady=10)

        self.railPosLb = ttk.Label(self.ambInfoLf, text="オフセット", font=("", 14))
        self.railPosLb.grid(row=3, column=0, sticky=W+E, padx=10, pady=10)
        self.v_railPos = IntVar()
        self.railPosEt = ttk.Entry(self.ambInfoLf, textvariable=self.v_railPos, font=("", 14), width=7, justify="center", state="readonly")
        self.railPosEt.grid(row=3, column=1, sticky=W+E, padx=10, pady=10)

        #
        self.xyzFrame = ttk.LabelFrame(self.sidePackFrame, text="BASE距離、向きXYZ情報")
        self.xyzFrame.pack(anchor=NW, side=LEFT, pady=15)
        self.xPosLb = ttk.Label(self.xyzFrame, text="xの距離", font=("", 14))
        self.xPosLb.grid(row=0, column=0, sticky=W+E, padx=10, pady=10)
        self.v_xPos = DoubleVar()
        self.xPosEt = ttk.Entry(self.xyzFrame, textvariable=self.v_xPos, font=("", 14), width=7, justify="center", state="readonly")
        self.xPosEt.grid(row=0, column=1, sticky=W+E, padx=10, pady=10)

        self.yPosLb = ttk.Label(self.xyzFrame, text="yの距離", font=("", 14))
        self.yPosLb.grid(row=1, column=0, sticky=W+E, padx=10, pady=10)
        self.v_yPos = DoubleVar()
        self.yPosEt = ttk.Entry(self.xyzFrame, textvariable=self.v_yPos, font=("", 14), width=7, justify="center", state="readonly")
        self.yPosEt.grid(row=1, column=1, sticky=W+E, padx=10, pady=10)

        self.zPosLb = ttk.Label(self.xyzFrame, text="zの距離", font=("", 14))
        self.zPosLb.grid(row=2, column=0, sticky=W+E, padx=10, pady=10)
        self.v_zPos = DoubleVar()
        self.zPosEt = ttk.Entry(self.xyzFrame, textvariable=self.v_zPos, font=("", 14), width=7, justify="center", state="readonly")
        self.zPosEt.grid(row=2, column=1, sticky=W+E, padx=10, pady=10)
        
        self.xRotLb = ttk.Label(self.xyzFrame, text="xの向き", font=("", 14))
        self.xRotLb.grid(row=0, column=2, sticky=W+E, padx=10, pady=10)
        self.v_xRot = DoubleVar()
        self.xRotEt = ttk.Entry(self.xyzFrame, textvariable=self.v_xRot, font=("", 14), width=7, justify="center", state="readonly")
        self.xRotEt.grid(row=0, column=3, sticky=W+E, padx=10, pady=10)

        self.yRotLb = ttk.Label(self.xyzFrame, text="yの向き", font=("", 14))
        self.yRotLb.grid(row=1, column=2, sticky=W+E, padx=10, pady=10)
        self.v_yRot = DoubleVar()
        self.yRotEt = ttk.Entry(self.xyzFrame, textvariable=self.v_yRot, font=("", 14), width=7, justify="center", state="readonly")
        self.yRotEt.grid(row=1, column=3, sticky=W+E, padx=10, pady=10)

        self.zRotLb = ttk.Label(self.xyzFrame, text="zの向き", font=("", 14))
        self.zRotLb.grid(row=2, column=2, sticky=W+E, padx=10, pady=10)
        self.v_zRot = DoubleVar()
        self.zRotEt = ttk.Entry(self.xyzFrame, textvariable=self.v_zRot, font=("", 14), width=7, justify="center", state="readonly")
        self.zRotEt.grid(row=2, column=3, sticky=W+E, padx=10, pady=10)

        #
        self.ambInfo2Frame = ttk.LabelFrame(self.sidePackFrame, text="AMB情報2")
        self.ambInfo2Frame.pack(anchor=NW, side=LEFT, padx=30, pady=15)
        self.priorityLb = ttk.Label(self.ambInfo2Frame, text="優先度", font=("", 14))
        self.priorityLb.grid(row=0, column=0, sticky=W+E, padx=10, pady=10)
        self.v_priority = IntVar()
        self.priorityEt = ttk.Entry(self.ambInfo2Frame, textvariable=self.v_priority, font=("", 14), width=7, justify="center", state="readonly")
        self.priorityEt.grid(row=0, column=1, sticky=W+E, padx=10, pady=10)

        self.fogLb = ttk.Label(self.ambInfo2Frame, text="フォグ", font=("", 14))
        self.fogLb.grid(row=1, column=0, sticky=W+E, padx=10, pady=10)
        self.v_fog = IntVar()
        self.fogEt = ttk.Entry(self.ambInfo2Frame, textvariable=self.v_fog, font=("", 14), width=7, justify="center", state="readonly")
        self.fogEt.grid(row=1, column=1, sticky=W+E, padx=10, pady=10)

        #
        self.ambModelLf = ttk.LabelFrame(self.frame, text="AMBモデル情報")
        self.ambModelLf.pack(anchor=NW, padx=30, pady=15)
        self.setAmbInfo(self.ambModelLf, True)

        #
        self.ambChildModelLf = ttk.LabelFrame(self.frame, text="AMB子モデル情報")
        self.ambChildModelLf.pack(anchor=NW, padx=30, pady=15)

        self.searchAmb(self.v_ambNo.get())

    def setAmbInfo(self, frame, flag):
        self.mdlNoFrame = ttk.Frame(frame)
        self.mdlNoFrame.pack(anchor=NW)
        self.mdlNoLb = ttk.Label(self.mdlNoFrame, text="モデル(smf)", font=("", 14))
        self.mdlNoLb.grid(row=0, column=0, sticky=W+E, padx=10, pady=10)
        self.mdlNoCb = ttk.Combobox(self.mdlNoFrame, width=40, values=self.smfList, state="disabled")
        self.mdlNoCb.grid(row=0, column=1, sticky=W+E, padx=10, pady=10)
        if flag:
            self.varList.append(self.mdlNoCb)
        else:
            self.varChildList.append(self.mdlNoCb)

        self.xyzFrame = ttk.Frame(frame)
        self.xyzFrame.pack(anchor=NW)
        self.xMdlPosLb = ttk.Label(self.xyzFrame, text="xの距離", font=("", 14))
        self.xMdlPosLb.grid(row=1, column=0, sticky=W+E, padx=10, pady=10)
        self.v_xMdlPos = DoubleVar()
        if flag:
            self.varList.append(self.v_xMdlPos)
        else:
            self.varChildList.append(self.v_xMdlPos)
        self.xMdlPosEt = ttk.Entry(self.xyzFrame, textvariable=self.v_xMdlPos, font=("", 14), width=7, justify="center", state="readonly")
        self.xMdlPosEt.grid(row=1, column=1, sticky=W+E, padx=10, pady=10)

        self.yMdlPosLb = ttk.Label(self.xyzFrame, text="yの距離", font=("", 14))
        self.yMdlPosLb.grid(row=1, column=2, sticky=W+E, padx=10, pady=10)
        self.v_yMdlPos = DoubleVar()
        if flag:
            self.varList.append(self.v_yMdlPos)
        else:
            self.varChildList.append(self.v_yMdlPos)
        self.yMdlPosEt = ttk.Entry(self.xyzFrame, textvariable=self.v_yMdlPos, font=("", 14), width=7, justify="center", state="readonly")
        self.yMdlPosEt.grid(row=1, column=3, sticky=W+E, padx=10, pady=10)

        self.zMdlPosLb = ttk.Label(self.xyzFrame, text="zの距離", font=("", 14))
        self.zMdlPosLb.grid(row=1, column=4, sticky=W+E, padx=10, pady=10)
        self.v_zMdlPos = DoubleVar()
        if flag:
            self.varList.append(self.v_zMdlPos)
        else:
            self.varChildList.append(self.v_zMdlPos)
        self.zMdlPosEt = ttk.Entry(self.xyzFrame, textvariable=self.v_zMdlPos, font=("", 14), width=7, justify="center", state="readonly")
        self.zMdlPosEt.grid(row=1, column=5, sticky=W+E, padx=10, pady=10)
        
        self.xMdlRotLb = ttk.Label(self.xyzFrame, text="xの向き", font=("", 14))
        self.xMdlRotLb.grid(row=2, column=0, sticky=W+E, padx=10, pady=10)
        self.v_xMdlRot = DoubleVar()
        if flag:
            self.varList.append(self.v_xMdlRot)
        else:
            self.varChildList.append(self.v_xMdlRot)
        self.xMdlRotEt = ttk.Entry(self.xyzFrame, textvariable=self.v_xMdlRot, font=("", 14), width=7, justify="center", state="readonly")
        self.xMdlRotEt.grid(row=2, column=1, sticky=W+E, padx=10, pady=10)

        self.yMdlRotLb = ttk.Label(self.xyzFrame, text="yの向き", font=("", 14))
        self.yMdlRotLb.grid(row=2, column=2, sticky=W+E, padx=10, pady=10)
        self.v_yMdlRot = DoubleVar()
        if flag:
            self.varList.append(self.v_yMdlRot)
        else:
            self.varChildList.append(self.v_yMdlRot)
        self.yMdlRotEt = ttk.Entry(self.xyzFrame, textvariable=self.v_yMdlRot, font=("", 14), width=7, justify="center", state="readonly")
        self.yMdlRotEt.grid(row=2, column=3, sticky=W+E, padx=10, pady=10)

        self.zMdlRotLb = ttk.Label(self.xyzFrame, text="zの向き", font=("", 14))
        self.zMdlRotLb.grid(row=2, column=4, sticky=W+E, padx=10, pady=10)
        self.v_zMdlRot = DoubleVar()
        if flag:
            self.varList.append(self.v_zMdlRot)
        else:
            self.varChildList.append(self.v_zMdlRot)
        self.zMdlRotEt = ttk.Entry(self.xyzFrame, textvariable=self.v_zMdlRot, font=("", 14), width=7, justify="center", state="readonly")
        self.zMdlRotEt.grid(row=2, column=5, sticky=W+E, padx=10, pady=10)

        self.xMdlRot2Lb = ttk.Label(self.xyzFrame, text="xの向き(終端)", font=("", 14))
        self.xMdlRot2Lb.grid(row=3, column=0, sticky=W+E, padx=10, pady=10)
        self.v_xMdlRot2 = DoubleVar()
        if flag:
            self.varList.append(self.v_xMdlRot2)
        else:
            self.varChildList.append(self.v_xMdlRot2)
        self.xMdlRot2Et = ttk.Entry(self.xyzFrame, textvariable=self.v_xMdlRot2, font=("", 14), width=7, justify="center", state="readonly")
        self.xMdlRot2Et.grid(row=3, column=1, sticky=W+E, padx=10, pady=10)

        self.yMdlRot2Lb = ttk.Label(self.xyzFrame, text="yの向き(終端)", font=("", 14))
        self.yMdlRot2Lb.grid(row=3, column=2, sticky=W+E, padx=10, pady=10)
        self.v_yMdlRot2 = DoubleVar()
        if flag:
            self.varList.append(self.v_yMdlRot2)
        else:
            self.varChildList.append(self.v_yMdlRot2)
        self.yMdlRot2Et = ttk.Entry(self.xyzFrame, textvariable=self.v_yMdlRot2, font=("", 14), width=7, justify="center", state="readonly")
        self.yMdlRot2Et.grid(row=3, column=3, sticky=W+E, padx=10, pady=10)

        self.zMdlRot2Lb = ttk.Label(self.xyzFrame, text="zの向き(終端)", font=("", 14))
        self.zMdlRot2Lb.grid(row=3, column=4, sticky=W+E, padx=10, pady=10)
        self.v_zMdlRot2 = DoubleVar()
        if flag:
            self.varList.append(self.v_zMdlRot2)
        else:
            self.varChildList.append(self.v_zMdlRot2)
        self.zMdlRot2Et = ttk.Entry(self.xyzFrame, textvariable=self.v_zMdlRot2, font=("", 14), width=7, justify="center", state="readonly")
        self.zMdlRot2Et.grid(row=3, column=5, sticky=W+E, padx=10, pady=10)
        
        self.perLb = ttk.Label(self.xyzFrame, text="per", font=("", 14))
        self.perLb.grid(row=4, column=0, sticky=W+E, padx=10, pady=10)
        self.v_per = DoubleVar()
        if flag:
            self.varList.append(self.v_per)
        else:
            self.varChildList.append(self.v_per)
        self.perEt = ttk.Entry(self.xyzFrame, textvariable=self.v_per, font=("", 14), width=7, justify="center", state="readonly")
        self.perEt.grid(row=4, column=1, sticky=W+E, padx=10, pady=10)

    def setAmbChildInfo(self, ambInfo):
        children = self.ambChildModelLf.winfo_children()
        for child in children:
            child.destroy()

        self.varChildList = []
        childCount = ambInfo[23]
        for i in range(childCount):
            self.ambChildFrame = ttk.Frame(self.ambChildModelLf)
            self.ambChildFrame.pack(anchor=NW)
            self.setAmbInfo(self.ambChildFrame, False)

    def searchAmb(self, ambNo):
        if ambNo < 0 or ambNo >= len(self.ambList):
            mb.showerror(title="エラー", message="存在しないAMBです")
            return
        ambInfo = self.ambList[ambNo]

        self.v_const0.set(ambInfo[0])
        self.v_length.set(ambInfo[1])
        self.v_railNo.set(ambInfo[2])
        self.v_railPos.set(ambInfo[3])
        self.v_xPos.set(round(ambInfo[4], 4))
        self.v_yPos.set(round(ambInfo[5], 4))
        self.v_zPos.set(round(ambInfo[6], 4))
        self.v_xRot.set(round(ambInfo[7], 4))
        self.v_yRot.set(round(ambInfo[8], 4))
        self.v_zRot.set(round(ambInfo[9], 4))
        self.v_priority.set(ambInfo[10])
        self.v_fog.set(ambInfo[11])

        self.varList[0].current(ambInfo[12])
        self.varList[1].set(round(ambInfo[13], 4))
        self.varList[2].set(round(ambInfo[14], 4))
        self.varList[3].set(round(ambInfo[15], 4))
        self.varList[4].set(round(ambInfo[16], 4))
        self.varList[5].set(round(ambInfo[17], 4))
        self.varList[6].set(round(ambInfo[18], 4))
        self.varList[7].set(round(ambInfo[19], 4))
        self.varList[8].set(round(ambInfo[20], 4))
        self.varList[9].set(round(ambInfo[21], 4))
        self.varList[10].set(round(ambInfo[22], 4))

        self.setAmbChildInfo(ambInfo)
        childCount = ambInfo[23]
        for i in range(childCount):
            self.varChildList[11*i+0].current(ambInfo[11*i+24])
            self.varChildList[11*i+1].set(round(ambInfo[11*i+25], 4))
            self.varChildList[11*i+2].set(round(ambInfo[11*i+26], 4))
            self.varChildList[11*i+3].set(round(ambInfo[11*i+27], 4))
            self.varChildList[11*i+4].set(round(ambInfo[11*i+28], 4))
            self.varChildList[11*i+5].set(round(ambInfo[11*i+29], 4))
            self.varChildList[11*i+6].set(round(ambInfo[11*i+30], 4))
            self.varChildList[11*i+7].set(round(ambInfo[11*i+31], 4))
            self.varChildList[11*i+8].set(round(ambInfo[11*i+32], 4))
            self.varChildList[11*i+9].set(round(ambInfo[11*i+33], 4))
            self.varChildList[11*i+10].set(round(ambInfo[11*i+34], 4))

    def saveCsv(self):
        errorMsg = "CSVで上書きが失敗しました。\n権限問題の可能性があります。"
        file_path = fd.askopenfilename(defaultextension='csv', filetypes=[("レールデータCSV", "*.csv")])
        if not file_path:
            return
        try:
            f = open(file_path)
            csvLines = f.readlines()
            f.close()
        except:
            errorMsg = "読み込み失敗しました。"
            mb.showerror(title="読み込みエラー", message=errorMsg)
            return

        try:
            csvLines.pop(0)
            ambList = []
            ambInfo = []
            count = 2
            childCount = 0
            childAllCount = 0
            childFlag = False
            for csv in csvLines:
                csv = csv.strip()
                arr = csv.split(",")
                if not childFlag:
                    ambInfo = []
                    
                    if len(arr) < 24:
                        print(arr)
                        raise Exception

                    const0 = int(float(arr[1]))
                    ambInfo.append(const0)

                    length = int(float(arr[2]))
                    ambInfo.append(length)

                    railNo = int(arr[3])
                    ambInfo.append(railNo)

                    railPos = int(arr[4])
                    ambInfo.append(railPos)

                    for i in range(6):
                        tempF = float(arr[5+i])
                        ambInfo.append(tempF)

                    priority = int(arr[11])
                    ambInfo.append(priority)

                    fog = int(arr[12])
                    ambInfo.append(fog)

                    #
                    mdl_no = int(arr[13])
                    ambInfo.append(mdl_no)

                    for i in range(10):
                        tempF = float(arr[14+i])
                        ambInfo.append(tempF)

                    childFlag = True
                    count += 1
                    continue

                if childCount == 0:
                    childAllCount = int(arr[12])
                    ambInfo.append(childAllCount)

                if childAllCount > 0:
                    mdl_no = int(arr[13])
                    ambInfo.append(mdl_no)

                    for i in range(10):
                        tempF = float(arr[14+i])
                        ambInfo.append(tempF)

                    childCount += 1
                    
                if childCount == childAllCount:
                    childFlag = False
                    childCount = 0
                    ambList.append(ambInfo)
                count += 1

            count -= 1
            msg = "{0}行のデータを読み込みしました。\n上書きしますか？".format(count)
            result = mb.askokcancel(title="警告", message=msg, icon="warning")

            if result:
                if not self.decryptFile.saveAmbCsv(ambList):
                    self.decryptFile.printError()
                    mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                    return
                mb.showinfo(title="成功", message="レール情報を修正しました")
                self.reloadFunc()
            
        except:
            print(traceback.format_exc())
            errorMsg = "{0}行のデータを読み込み失敗しました。".format(count)
            mb.showerror(title="読み込みエラー", message=errorMsg)
            return
