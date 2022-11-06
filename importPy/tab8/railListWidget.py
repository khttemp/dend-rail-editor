from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd

class RailListWidget:
    def __init__(self, frame, decryptFile, railList, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.smfList = [smfInfo[0] for smfInfo in decryptFile.smfList]
        self.railList = railList
        self.varRailList = []
        self.reloadFunc = reloadFunc

        self.smfList.extend(["モデル設定通り", "なし"])
        
        #
        self.railNoFrame = ttk.Frame(self.frame)
        self.railNoFrame.pack(anchor=NW, padx=30, pady=30)
        self.railNoLb = ttk.Label(self.railNoFrame, text="レールNo", font=("", 14))
        self.railNoLb.grid(row=0, column=0, sticky=W+E)
        self.v_railNo = IntVar()
        self.railNoEt = ttk.Entry(self.railNoFrame, textvariable=self.v_railNo, font=("", 14), width=7, justify="center")
        self.railNoEt.grid(row=0, column=1, sticky=W+E, padx=10)
        self.searchBtn = ttk.Button(self.railNoFrame, text="照会", command=lambda: self.searchRail(self.v_railNo.get()))
        self.searchBtn.grid(row=0, column=2, sticky=W+E, padx=30)

        ###
        self.sidePackFrame = ttk.Frame(self.frame)
        self.sidePackFrame.pack(anchor=NW)

        #
        self.blockFrameLf = ttk.LabelFrame(self.sidePackFrame, text="ブロック情報")
        self.blockFrameLf.pack(anchor=NW, side=LEFT, padx=30, pady=15)
        self.prevRailLb = ttk.Label(self.blockFrameLf, text="繋げるレールNo", font=("", 14))
        self.prevRailLb.grid(row=0, column=0, sticky=W+E, padx=10, pady=10)
        self.v_prevRail = IntVar()
        self.prevRailEt = ttk.Entry(self.blockFrameLf, textvariable=self.v_prevRail, font=("", 14), width=7, justify="center", state="readonly")
        self.prevRailEt.grid(row=0, column=1, sticky=W+E, padx=10, pady=10)

        self.blockLb = ttk.Label(self.blockFrameLf, text="ブロックNo", font=("", 14))
        self.blockLb.grid(row=1, column=0, sticky=W+E, padx=10, pady=10)
        self.v_block = IntVar()
        self.blockEt = ttk.Entry(self.blockFrameLf, textvariable=self.v_block, font=("", 14), width=7, justify="center", state="readonly")
        self.blockEt.grid(row=1, column=1, sticky=W+E, padx=10, pady=10)

        #
        self.xyzFrame = ttk.LabelFrame(self.sidePackFrame, text="向きXYZ情報")
        self.xyzFrame.pack(anchor=NW, side=LEFT, pady=15)
        self.xLb = ttk.Label(self.xyzFrame, text="xの向き", font=("", 14))
        self.xLb.grid(row=0, column=0, sticky=W+E, padx=10, pady=10)
        self.v_x = DoubleVar()
        self.xEt = ttk.Entry(self.xyzFrame, textvariable=self.v_x, font=("", 14), width=7, justify="center", state="readonly")
        self.xEt.grid(row=0, column=1, sticky=W+E, padx=10, pady=10)

        self.yLb = ttk.Label(self.xyzFrame, text="yの向き", font=("", 14))
        self.yLb.grid(row=1, column=0, sticky=W+E, padx=10, pady=10)
        self.v_y = DoubleVar()
        self.yEt = ttk.Entry(self.xyzFrame, textvariable=self.v_y, font=("", 14), width=7, justify="center", state="readonly")
        self.yEt.grid(row=1, column=1, sticky=W+E, padx=10, pady=10)

        self.zLb = ttk.Label(self.xyzFrame, text="zの向き", font=("", 14))
        self.zLb.grid(row=2, column=0, sticky=W+E, padx=10, pady=10)
        self.v_z = DoubleVar()
        self.zEt = ttk.Entry(self.xyzFrame, textvariable=self.v_z, font=("", 14), width=7, justify="center", state="readonly")
        self.zEt.grid(row=2, column=1, sticky=W+E, padx=10, pady=10)

        self.kasenFrame = ttk.LabelFrame(self.sidePackFrame, text="モデル、架線情報")
        self.kasenFrame.pack(anchor=NW, side=LEFT, padx=30, pady=15)
        self.mdlNoLb = ttk.Label(self.kasenFrame, text="モデル(smf)", font=("", 14))
        self.mdlNoLb.grid(row=0, column=0, sticky=W+E, padx=10, pady=10)
        self.mdlNoCb = ttk.Combobox(self.kasenFrame, width=40, values=self.smfList, state="disabled")
        self.mdlNoCb.grid(row=0, column=1, sticky=W+E, padx=10, pady=10)

        self.mdlKasenLb = ttk.Label(self.kasenFrame, text="【推測】架線", font=("", 14))
        self.mdlKasenLb.grid(row=1, column=0, sticky=W+E, padx=10, pady=10)
        self.v_mdlKasen = IntVar()
        self.mdlKasenEt = ttk.Entry(self.kasenFrame, textvariable=self.v_mdlKasen, font=("", 14), width=7, justify="center", state="readonly")
        self.mdlKasenEt.grid(row=1, column=1, sticky=W+E, padx=10, pady=10)
        
        self.mdlKasenchuLb = ttk.Label(self.kasenFrame, text="架線柱(smf)", font=("", 14))
        self.mdlKasenchuLb.grid(row=2, column=0, sticky=W+E, padx=10, pady=10)
        self.mdlKasenchuCb = ttk.Combobox(self.kasenFrame, width=40, values=self.smfList, state="disabled")
        self.mdlKasenchuCb.grid(row=2, column=1, sticky=W+E, padx=10, pady=10)

        self.perLb = ttk.Label(self.kasenFrame, text="per", font=("", 14))
        self.perLb.grid(row=3, column=0, sticky=W+E, padx=10, pady=10)
        self.v_per = DoubleVar()
        self.perEt = ttk.Entry(self.kasenFrame, textvariable=self.v_per, font=("", 14), width=7, justify="center", state="readonly")
        self.perEt.grid(row=3, column=1, sticky=W+E, padx=10, pady=10)
        
        ###
        self.flagFrameLf = ttk.LabelFrame(self.frame, text="フラグ情報")
        self.flagFrameLf.pack(anchor=NW, padx=30, pady=15)

        flagInfoList = [
            ["フラグ1", "フラグ2", "フラグ3", "フラグ4", "フラグ5", "フラグ6", "フラグ7", "フラグ8"],
            ["フラグ1", "フラグ2", "フラグ3", "フラグ4", "フラグ5", "フラグ6", "フラグ7", "フラグ8"],
            ["フラグ1", "フラグ2", "フラグ3", "フラグ4", "フラグ5", "フラグ6", "フラグ7", "フラグ8"],
            ["フラグ1", "フラグ2", "フラグ3", "フラグ4", "フラグ5", "フラグ6", "フラグ7", "フラグ8"]
        ]

        self.v_flagInfoList = []
        self.chkInfoList = []
        
        for i in range(len(flagInfoList)):
            v_flagInfo = []
            chkInfo = []
            self.flagFrame = ttk.Frame(self.flagFrameLf)
            self.flagFrame.pack(anchor=NW, pady=3)
            for j in range(len(flagInfoList[i])):
                self.v_flag = IntVar()
                self.v_flag.set(0)
                v_flagInfo.append(self.v_flag)
                self.flagChk = Checkbutton(self.flagFrame, text=flagInfoList[i][j], variable=self.v_flag, state="disabled", disabledforeground="black")
                self.flagChk.grid(row=0, column=j, sticky=W+E, padx=10, pady=10)
                chkInfo.append(self.flagChk)
            self.v_flagInfoList.append(v_flagInfo)
            self.chkInfoList.append(chkInfo)

        ###
        self.railFrameLf = ttk.LabelFrame(self.frame, text="レール情報")
        self.railFrameLf.pack(anchor=NW, padx=30, pady=15)
    
        self.railFrameCntFrame = ttk.Frame(self.railFrameLf)
        self.railFrameCntFrame.pack(anchor=NW, padx=10, pady=10)
        self.railDataCntLb = ttk.Label(self.railFrameCntFrame, text="レール本数", font=("", 14))
        self.railDataCntLb.grid(row=0, column=0, sticky=W+E, padx=10, pady=10)
        self.v_railDataCnt = IntVar()
        self.railDataCntEt = ttk.Entry(self.railFrameCntFrame, textvariable=self.v_railDataCnt, font=("", 14), width=7, justify="center", state="readonly")
        self.railDataCntEt.grid(row=0, column=1, sticky=W+E, padx=10, pady=10)

        self.changeRailBtn = ttk.Button(self.railFrameCntFrame, text="本数を変える", state="disabled", command=lambda :self.setRailInfo(self.v_railDataCnt.get()))
        self.changeRailBtn.grid(row=0, column=2, sticky=W+E, padx=10)
    
        self.railFrame = ttk.Frame(self.railFrameLf)
        self.railFrame.pack(anchor=NW, padx=10, pady=10)

        self.searchRail(self.v_railNo.get())
    def setRailInfo(self, cnt):
        self.varRailList = []
        children = self.railFrame.winfo_children()
        for child in children:
            child.destroy()
            
        for i in range(cnt):
            self.nextRailLb = ttk.Label(self.railFrame, text="次レール", font=("", 14))
            self.nextRailLb.grid(row=i, column=0, sticky=W+E, padx=10, pady=5)
            self.v_nextRailNo = IntVar()
            self.varRailList.append(self.v_nextRailNo)
            self.nextRailNoEt = ttk.Entry(self.railFrame, textvariable=self.v_nextRailNo, font=("", 14), width=7, justify="center", state="readonly")
            self.nextRailNoEt.grid(row=i, column=1, sticky=W+E, pady=5)
            self.v_nextRailPos = IntVar()
            self.varRailList.append(self.v_nextRailPos)
            self.nextRailPosEt = ttk.Entry(self.railFrame, textvariable=self.v_nextRailPos, font=("", 14), width=7, justify="center", state="readonly")
            self.nextRailPosEt.grid(row=i, column=2, sticky=W+E, pady=5)

            self.prevRailLb = ttk.Label(self.railFrame, text="前レール", font=("", 14))
            self.prevRailLb.grid(row=i, column=3, sticky=W+E, padx=10, pady=5)
            self.v_prevRailNo = IntVar()
            self.varRailList.append(self.v_prevRailNo)
            self.prevRailNoEt = ttk.Entry(self.railFrame, textvariable=self.v_prevRailNo, font=("", 14), width=7, justify="center", state="readonly")
            self.prevRailNoEt.grid(row=i, column=4, sticky=W+E, pady=5)
            self.v_prevRailPos = IntVar()
            self.varRailList.append(self.v_prevRailPos)
            self.prevRailPosEt = ttk.Entry(self.railFrame, textvariable=self.v_prevRailPos, font=("", 14), width=7, justify="center", state="readonly")
            self.prevRailPosEt.grid(row=i, column=5, sticky=W+E, pady=5)

    def searchRail(self, railNo):
        if railNo < 0 or railNo >= len(self.railList):
            mb.showerror(title="エラー", message="存在しないレールです")
            return
        railInfo = self.railList[railNo]

        self.v_prevRail.set(railInfo[1])
        self.v_block.set(railInfo[2])
        self.v_x.set(round(railInfo[3], 4))
        self.v_y.set(round(railInfo[4], 4))
        self.v_z.set(round(railInfo[5], 4))
        self.mdlNoCb.current(railInfo[6])
        self.v_mdlKasen.set(railInfo[7])
        kasenchuNo = railInfo[8]
        if kasenchuNo == -1 or kasenchuNo == -2:
            kasenchuNo = len(self.smfList) + kasenchuNo
        self.mdlKasenchuCb.current(kasenchuNo)
        self.v_per.set(round(railInfo[9], 4))

        for i in range(4):
            for j in range(8):
                if railInfo[10+i] & (2**(7-j)) == 0:
                    self.v_flagInfoList[i][j].set(0)
                else:
                    self.v_flagInfoList[i][j].set(1)

        self.v_railDataCnt.set(railInfo[14])
        self.setRailInfo(railInfo[14])
        for i in range(len(self.varRailList)):
            self.varRailList[i].set(railInfo[15+i])
