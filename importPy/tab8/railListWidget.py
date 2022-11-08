import traceback

from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
from tkinter import filedialog as fd

class RailListWidget:
    def __init__(self, frame, decryptFile, railList, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.smfList = [smfInfo[0] for smfInfo in decryptFile.smfList]
        self.railList = railList
        self.varRailList = []
        self.varRevRailList = []
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

        self.csvSaveBtn = ttk.Button(self.railNoFrame, text="CSVで上書きする", command=self.saveCsv)
        self.csvSaveBtn.grid(row=0, column=3, sticky=W+E, padx=30)

        ###
        self.sidePackFrame = ttk.Frame(self.frame)
        self.sidePackFrame.pack(anchor=NW, padx=20)

        #
        self.blockFrameLf = ttk.LabelFrame(self.sidePackFrame, text="ブロック情報")
        self.blockFrameLf.pack(anchor=NW, side=LEFT, padx=5, pady=15)
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
        self.xyzFrame.pack(anchor=NW, side=LEFT, padx=5, pady=15)
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
        self.kasenFrame.pack(anchor=NW, side=LEFT, padx=5, pady=15)
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
            [
                "踏み切り\n通過中の音",
                "複線ドリフトで\n飛ぶ",
                "手前位置に\n180度回転",
                "LAST_POS",
                "LAST01",
                "LAST02",
                "橋\n通過中の音",
                "Noドリフト"
            ],
            [
                "クラッシュ時\nカメラ位置を高く",
                "他のレールも\nドリフト対象",
                "フラグ3",
                "フラグ4",
                "CPU振り子車両\n振り子のみ",
                "CPU\n片輪ドリフト\n戻し",
                "CPU\n右片輪ドリフト",
                "CPU\n左片輪ドリフト"
            ],
            [
                "片輪ドリフト時\n飛ぶ",
                "右側線路\n片輪ドリフト時\n飛ぶ",
                "左側線路\n片輪ドリフト時\n飛ぶ",
                "レール非表示",
                "左入力で\n土讃線",
                "右入力で\n土讃線",
                "右側に\nレールガード",
                "左側に\nレールガード"
            ],
            [
                "Disabled\nレール",
                "CPU\n転線",
                "L_RUN",
                "R_RUN",
                "フラグ5",
                "CPU\nドリフト\n戻し",
                "CPU\n右ドリフト",
                "CPU\n左ドリフト"
            ]
        ]

        self.v_flagHexList = []
        self.v_flagInfoList = []
        self.chkInfoList = []
        
        for i in range(len(flagInfoList)):
            v_flagInfo = []
            chkInfo = []
            self.flagFrame = ttk.Frame(self.flagFrameLf)
            self.flagFrame.pack(anchor=NW, pady=3)

            self.v_flagHex = StringVar()
            self.v_flagHex.set("0x00")
            self.v_flagHexList.append(self.v_flagHex)
            self.flagHexLb = ttk.Label(self.flagFrame, textvariable=self.v_flagHex, font=("", 14))
            self.flagHexLb.grid(row=0, column=0, sticky=W+E, padx=3, pady=3)
            for j in range(len(flagInfoList[i])):
                self.v_flag = IntVar()
                self.v_flag.set(0)
                v_flagInfo.append(self.v_flag)
                self.flagChk = Checkbutton(self.flagFrame, text=flagInfoList[i][j], width=10, variable=self.v_flag, command=self.changeFlag)
                self.flagChk.grid(row=1, column=j, sticky=W+E, padx=3, pady=3)
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

        if self.decryptFile.ver == "DEND_MAP_VER0300":
            self.csvRevRailSaveBtn = ttk.Button(self.railFrameCntFrame, text="往復レール作成", command=self.saveRevRailCsv)
            self.csvRevRailSaveBtn.grid(row=0, column=2, sticky=W+E, padx=30)
    
        self.railFrame = ttk.Frame(self.railFrameLf)
        self.railFrame.pack(anchor=NW, padx=10, pady=10)

        self.revRailFrame = ttk.Frame(self.railFrameLf)
        self.revRailFrame.pack(anchor=NW, padx=10, pady=10)

        self.searchRail(self.v_railNo.get())

    def changeFlag(self):
        for i in range(len(self.v_flagInfoList)):
            res = 0
            v_flagInfo = self.v_flagInfoList[i]
            for j in range(len(v_flagInfo)):
                if v_flagInfo[j].get() == 1:
                    res += 2**(7-j)
            strFlagHex = "0x{0:02x}".format(res)
            self.v_flagHexList[i].set(strFlagHex)
        
    def setRailInfo(self, cnt):
        self.varRailList = []
        children = self.railFrame.winfo_children()
        for child in children:
            child.destroy()
            
        for i in range(cnt):
            self.nextRailLb = ttk.Label(self.railFrame, text="次レール", width=11, font=("", 14))
            self.nextRailLb.grid(row=i, column=0, sticky=W+E, padx=10, pady=5)
            self.v_nextRailNo = IntVar()
            self.varRailList.append(self.v_nextRailNo)
            self.nextRailNoEt = ttk.Entry(self.railFrame, textvariable=self.v_nextRailNo, font=("", 14), width=7, justify="center", state="readonly")
            self.nextRailNoEt.grid(row=i, column=1, sticky=W+E, pady=5)
            self.v_nextRailPos = IntVar()
            self.varRailList.append(self.v_nextRailPos)
            self.nextRailPosEt = ttk.Entry(self.railFrame, textvariable=self.v_nextRailPos, font=("", 14), width=7, justify="center", state="readonly")
            self.nextRailPosEt.grid(row=i, column=2, sticky=W+E, pady=5)

            self.prevRailLb = ttk.Label(self.railFrame, text="前レール", width=11, font=("", 14))
            self.prevRailLb.grid(row=i, column=3, sticky=W+E, padx=10, pady=5)
            self.v_prevRailNo = IntVar()
            self.varRailList.append(self.v_prevRailNo)
            self.prevRailNoEt = ttk.Entry(self.railFrame, textvariable=self.v_prevRailNo, font=("", 14), width=7, justify="center", state="readonly")
            self.prevRailNoEt.grid(row=i, column=4, sticky=W+E, pady=5)
            self.v_prevRailPos = IntVar()
            self.varRailList.append(self.v_prevRailPos)
            self.prevRailPosEt = ttk.Entry(self.railFrame, textvariable=self.v_prevRailPos, font=("", 14), width=7, justify="center", state="readonly")
            self.prevRailPosEt.grid(row=i, column=5, sticky=W+E, pady=5)

    def setRevRailInfo(self, cnt):
        self.varRevRailList = []
        children = self.revRailFrame.winfo_children()
        for child in children:
            child.destroy()
            
        for i in range(cnt):
            self.revNextRailLb = ttk.Label(self.revRailFrame, text="次レール(rev)", font=("", 14))
            self.revNextRailLb.grid(row=i, column=0, sticky=W+E, padx=10, pady=5)
            self.v_revNextRailNo = IntVar()
            self.varRevRailList.append(self.v_revNextRailNo)
            self.revNextRailNoEt = ttk.Entry(self.revRailFrame, textvariable=self.v_revNextRailNo, font=("", 14), width=7, justify="center", state="readonly")
            self.revNextRailNoEt.grid(row=i, column=1, sticky=W+E, pady=5)
            self.v_revNextRailPos = IntVar()
            self.varRevRailList.append(self.v_revNextRailPos)
            self.revNextRailPosEt = ttk.Entry(self.revRailFrame, textvariable=self.v_revNextRailPos, font=("", 14), width=7, justify="center", state="readonly")
            self.revNextRailPosEt.grid(row=i, column=2, sticky=W+E, pady=5)

            self.revPrevRailLb = ttk.Label(self.revRailFrame, text="前レール(rev)", font=("", 14))
            self.revPrevRailLb.grid(row=i, column=3, sticky=W+E, padx=10, pady=5)
            self.v_revPrevRailNo = IntVar()
            self.varRevRailList.append(self.v_revPrevRailNo)
            self.revPrevRailNoEt = ttk.Entry(self.revRailFrame, textvariable=self.v_revPrevRailNo, font=("", 14), width=7, justify="center", state="readonly")
            self.revPrevRailNoEt.grid(row=i, column=4, sticky=W+E, pady=5)
            self.v_revPrevRailPos = IntVar()
            self.varRevRailList.append(self.v_revPrevRailPos)
            self.revPrevRailPosEt = ttk.Entry(self.revRailFrame, textvariable=self.v_revPrevRailPos, font=("", 14), width=7, justify="center", state="readonly")
            self.revPrevRailPosEt.grid(row=i, column=5, sticky=W+E, pady=5)

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
            strFlagHex = "0x{0:02x}".format(railInfo[10+i])
            self.v_flagHexList[i].set(strFlagHex)
            for j in range(8):
                if railInfo[10+i] & (2**(7-j)) == 0:
                    self.v_flagInfoList[i][j].set(0)
                else:
                    self.v_flagInfoList[i][j].set(1)

        self.v_railDataCnt.set(railInfo[14])
        self.setRailInfo(railInfo[14])
        for i in range(len(self.varRailList)):
            self.varRailList[i].set(railInfo[15+i])

        if self.decryptFile.ver == "DEND_MAP_VER0400":
            railCount = railInfo[14]
            self.setRevRailInfo(railCount)
            for i in range(len(self.varRevRailList)):
                self.varRevRailList[i].set(railInfo[15+railCount*4+i])

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
            railList = []
            count = 2
            for csv in csvLines:
                railInfo = []
                csv = csv.strip()
                arr = csv.split(",")
                if len(arr) < 15:
                    raise Exception

                prev_rail = int(arr[1])
                railInfo.append(prev_rail)

                block = int(arr[2])
                railInfo.append(block)

                for i in range(3):
                    dirF = float(arr[3+i])
                    railInfo.append(dirF)

                mdl_no = int(arr[6])
                railInfo.append(mdl_no)

                kasen = int(arr[7])
                railInfo.append(kasen)

                kasenchu = int(arr[8])
                railInfo.append(kasenchu)

                per = float(arr[9])
                railInfo.append(per)

                for i in range(4):
                    flag = int(arr[10+i], 16)
                    railInfo.append(flag)

                rail_data = int(arr[14])
                railInfo.append(rail_data)

                readCount = 4
                if self.decryptFile.ver == "DEND_MAP_VER0400":
                    readCount = 8
                    
                for i in range(rail_data * readCount):
                    rail = int(arr[15+i])
                    railInfo.append(rail)

                railList.append(railInfo)
                count += 1

            count -= 3
            msg = "{0}行のデータを読み込みしました。\n上書きしますか？".format(count)
            result = mb.askokcancel(title="警告", message=msg, icon="warning")

            if result:
                if not self.decryptFile.saveRailCsv(railList):
                    self.decryptFile.printError()
                    mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                    return
                mb.showinfo(title="成功", message="レール情報を修正しました")
                self.reloadFunc()
            
        except:
            errorMsg = "{0}行のデータを読み込み失敗しました。".format(count)
            mb.showerror(title="読み込みエラー", message=errorMsg)
            return

    def saveRevRailCsv(self):
        allModelRailCount = {railInfo[0] : railInfo[14] for railInfo in self.railList}
        allModelRailLen = {i : self.decryptFile.smfList[i][3] for i in range(len(self.decryptFile.smfList))}
        
        filename = self.decryptFile.filename + "_rev.csv"
        file_path = fd.asksaveasfilename(initialfile=filename, defaultextension='csv', filetypes=[('レールcsv', '*.csv')])
        newRailList = []
        errorMsg = "CSVで取り出す機能が失敗しました。\n権限問題の可能性があります。"
        if file_path:
            try:
                w = open(file_path, "w")
                w.write("index,prev_rail,block,")
                w.write("dir_x,dir_y,dir_z,")
                w.write("mdl_no,mdl_flg,mdl_kasenchu,per,")
                w.write("flg,flg,flg,flg,")
                w.write("rail_data,")
                w.write("next_rail,next_no,prev_rail,prev_no,\n")
                for railInfo in self.railList:
                    newRailInfo = railInfo[1:]
                    w.write("{0},{1},{2},".format(railInfo[0], railInfo[1], railInfo[2]))
                    for i in range(3):
                        w.write("{0},".format(railInfo[3+i]))
                    w.write("{0},".format(railInfo[6]))
                    w.write("{0},".format(railInfo[7]))
                    w.write("{0},".format(railInfo[8]))
                    w.write("{0},".format(railInfo[9]))
                    for i in range(4):
                        w.write("0x{:02x},".format(railInfo[10+i]))
                    rail_data = railInfo[14]
                    w.write("{0},".format(rail_data))
                    preNextList = []
                    for i in range(rail_data):
                        preNextInfo = []
                        for j in range(4):
                            if j % 2 == 0:
                                preNextInfo.append(railInfo[15+4*i+j])
                            w.write("{0},".format(railInfo[15+4*i+j]))
                        preNextList.append(preNextInfo)

                    preNextList.reverse()
                    railCount = 0
                    for preNextInfo in preNextList:
                        preNextInfo.reverse()
                        for i in range(len(preNextInfo)):                                
                            w.write("{0},".format(preNextInfo[i]))
                            newRailInfo.append(preNextInfo[i])
                            
                            if i == 0:
                                if preNextInfo[i] == -1:
                                    w.write("{0},".format(-1))
                                    newRailInfo.append(-1)
                                    continue
                                    
                                if allModelRailCount[preNextInfo[i]] > 1:
                                    w.write("{0},".format(railCount*100))
                                    newRailInfo.append(railCount*100)
                                else:
                                    w.write("{0},".format(0))
                                    newRailInfo.append(0)
                            else:
                                if preNextInfo[i] == -1:
                                    w.write("{0},".format(-1))
                                    newRailInfo.append(-1)
                                    continue

                                mdlNo = self.railList[preNextInfo[i]][6]
                                railLen = allModelRailLen[mdlNo]
                                if allModelRailCount[preNextInfo[i]] > 1:
                                    w.write("{0},".format(railCount*100 + railLen - 1))
                                    newRailInfo.append(railCount*100 + railLen - 1)
                                else:
                                    w.write("{0},".format(railLen - 1))
                                    newRailInfo.append(railLen - 1)
                    newRailList.append(newRailInfo)
                    w.write("\n")
                w.close()

                self.decryptFile.ver = "DEND_MAP_VER0400"
                self.decryptFile.byteArr[13] = 0x34
                if not self.decryptFile.saveRailCsv(newRailList):
                    self.decryptFile.printError()
                    mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                    return
                mb.showinfo(title="成功", message="CSVで自動作成しました。")
                self.reloadFunc()
                
            except:
                print(traceback.format_exc())
                mb.showerror(title="エラー", message=errorMsg)
        
            
