import os
import struct
import traceback

class RailDecrypt:
    def __init__(self, filePath):
        self.filePath = filePath
        self.filename = os.path.splitext(os.path.basename(self.filePath))[0]
        self.byteArr = bytearray()
        self.musicCnt = 0
        self.trainCnt = 0
        self.trainList = []
        self.trainList2 = []
        self.trainList3 = []
        self.else1List = []
        self.lightList = []
        self.pngList = []
        self.stationList = []
        self.baseBinList = []
        self.binAnimeList = []
        self.smfList = []
        self.stationNameList = []
        self.cpuList = []
        self.elseList2 = []
        self.comicScriptList = []
        self.dosansenList = []
        self.error = ""

    def open(self):
        try:
            f = open(self.filePath, "rb")
            line = f.read()
            f.close()
            self.byteArr = bytearray(line)
            self.decrypt()
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False
    def printError(self):
        f = open("error_log.txt", "w")
        f.write(self.error)
        f.close()
    def decrypt(self):
        self.musicCnt = 0
        self.trainCnt = 0
        self.trainList = []
        self.trainList2 = []
        self.trainList3 = []
        self.else1List = []
        self.lightList = []
        self.pngList = []
        self.stationList = []
        self.baseBinList = []
        self.binAnimeList = []
        self.smfList = []
        self.stationNameList = []
        self.cpuList = []
        self.elseList2 = []
        self.comicScriptList = []
        self.dosansenList = []
        
        index = 16
        readFlag = False
        
        header = self.byteArr[0:index]
        if header != b'DEND_MAP_VER0300' and header != b'DEND_MAP_VER0400':
            raise Exception

        if header == b'DEND_MAP_VER0400':
            readFlag = True

        #使う音楽(ダミーデータ?)
        self.musicIdx = index
        self.musicCnt = self.byteArr[index]
        index += 1
        for i in range(self.musicCnt):
            index += 1

        #配置する車両カウント
        self.trainCntIdx = index
        self.trainCnt = self.byteArr[index]
        index += 1
        
        #3車両の初期レール位置
        for i in range(self.trainCnt):
            trainInfo = []
            railNo = struct.unpack("<h", self.byteArr[index:index+2])[0]
            trainInfo.append(railNo)
            index += 2
            boneNo = struct.unpack("<h", self.byteArr[index:index+2])[0]
            trainInfo.append(boneNo)
            index += 2

            ########## rail pos unknown
            tempH = struct.unpack("<h", self.byteArr[index:index+2])[0]
            trainInfo.append(tempH)
            index += 2
            tempH = struct.unpack("<h", self.byteArr[index:index+2])[0]
            trainInfo.append(tempH)
            index += 2

            trainInfo.append(self.byteArr[index])
            index += 1
            ########## rail pos unknown
            self.trainList.append(trainInfo)

        self.trainCntIdx2 = index
        trainInfo2 = []
        #ダミー位置？
        railNo = struct.unpack("<h", self.byteArr[index:index+2])[0]
        trainInfo2.append(railNo)
        index += 2

        boneNo = struct.unpack("<h", self.byteArr[index:index+2])[0]
        trainInfo2.append(boneNo)
        index += 2

        tempH = struct.unpack("<h", self.byteArr[index:index+2])[0]
        trainInfo2.append(tempH)
        index += 2

        tempH = struct.unpack("<h", self.byteArr[index:index+2])[0]
        trainInfo2.append(tempH)
        index += 2

        trainInfo2.append(self.byteArr[index])
        index += 1
        self.trainList2.append(trainInfo2)

        #試運転、二人バトルの初期レール位置
        self.trainCntIdx3 = index
        for i in range(2):
            trainInfo3 = []
            railNo = struct.unpack("<h", self.byteArr[index:index+2])[0]
            trainInfo3.append(railNo)
            index += 2
            boneNo = struct.unpack("<h", self.byteArr[index:index+2])[0]
            trainInfo3.append(boneNo)
            index += 2

            ##########unknown
            tempH = struct.unpack("<h", self.byteArr[index:index+2])[0]
            trainInfo3.append(tempH)
            index += 2
            
            tempH = struct.unpack("<h", self.byteArr[index:index+2])[0]
            trainInfo3.append(tempH)
            index += 2

            trainInfo3.append(self.byteArr[index])
            index += 1
            self.trainList3.append(trainInfo3)
            ##########unknown

        index += 1
        ##########unknown
        self.elseIdx = index
        tempF = struct.unpack("<f", self.byteArr[index:index+4])[0]
        self.else1List.append(tempF)
        index += 4

        cnt = self.byteArr[index]
        index += 1
        for i in range(cnt):
            else1Info = []
            for j in range(2):
                tempF = struct.unpack("<f", self.byteArr[index:index+4])[0]
                else1Info.append(tempF)
                index += 4
            for j in range(3):
                else1Info.append(self.byteArr[index])
                index += 1
            self.else1List.append(else1Info)
        ##########unknown

        self.lightIdx = index
        #Light情報
        lightCnt = self.byteArr[index]
        index += 1
        for i in range(lightCnt):
            b = self.byteArr[index]
            index += 1
            text = self.byteArr[index:index+b].decode()
            self.lightList.append(text)
            index += b
        
        #駅名標画像情報
        self.pngIdx = index
        pngCnt = struct.unpack("<h", self.byteArr[index:index+2])[0]
        index += 2
        for i in range(pngCnt):
            b = self.byteArr[index]
            index += 1
            text = self.byteArr[index:index+b].decode()
            self.pngList.append(text)
            index += b

        #駅名標AMB情報
        self.stationIdx = index
        cnt = struct.unpack("<h", self.byteArr[index:index+2])[0]
        index += 2
        for i in range(cnt):
            stationInfo = []
            stationInfo.append(self.byteArr[index])
            index += 1
            for j in range(4):
                tempH = struct.unpack("<h", self.byteArr[index:index+2])[0]
                stationInfo.append(tempH)
                index += 2
            self.stationList.append(stationInfo)

        #base bin
        self.binIdx = index
        binCnt = self.byteArr[index]
        index += 1
        for i in range(binCnt):
            b = self.byteArr[index]
            index += 1
            text = self.byteArr[index:index+b].decode()
            self.baseBinList.append(text)
            index += b

        #bin ANIME
        self.binAnimeIdx = index
        cnt = self.byteArr[index]
        index += 1
        for i in range(cnt):
            binAnimeInfo = []
            binAnimeInfo.append(self.byteArr[index])
            index += 1
            tempH = struct.unpack("<h", self.byteArr[index:index+2])[0]
            binAnimeInfo.append(tempH)
            index += 2
            tempH = struct.unpack("<h", self.byteArr[index:index+2])[0]
            binAnimeInfo.append(tempH)
            index += 2
            self.binAnimeList.append(binAnimeInfo)
        #bin ANIME

        #smf
        self.smfIdx = index
        smfCnt = self.byteArr[index]
        index += 1
        for i in range(smfCnt):
            smfInfo = []
            b = self.byteArr[index]
            index += 1
            text = self.byteArr[index:index+b].decode()
            smfInfo.append(text)
            index += b
            for j in range(5):
                res = self.byteArr[index]
                if j != 2:
                    res = hex(res)
                smfInfo.append(res)
                index += 1
            kasenchu = self.byteArr[index]
            smfInfo.append(kasenchu)
            index += 1
            kasenNo = struct.unpack("<h", self.byteArr[index:index+2])[0]
            smfInfo.append(kasenNo)
            index += 2
            self.smfList.append(smfInfo)

        #stationName
        self.stationNameIdx = index    
        snameCnt = self.byteArr[index]
        index += 1
        for i in range(snameCnt):
            stationNameInfo = []
            b = self.byteArr[index]
            index += 1
            text = self.byteArr[index:index+b].decode("shift-jis")
            stationNameInfo.append(text)
            index += b

            stFlag = self.byteArr[index]
            stationNameInfo.append(stFlag)
            index += 1
            railNo = struct.unpack("<h", self.byteArr[index:index+2])[0]
            stationNameInfo.append(railNo)
            index += 2
            for i in range(3):
                tempF = struct.unpack("<f", self.byteArr[index:index+4])[0]
                stationNameInfo.append(tempF)
                index += 4
            for i in range(3):
                tempI = struct.unpack("<i", self.byteArr[index:index+4])[0]
                stationNameInfo.append(tempI)
                index += 4
            tempH = struct.unpack("<h", self.byteArr[index:index+2])[0]
            stationNameInfo.append(tempH)
            index += 2
            self.stationNameList.append(stationNameInfo)
            
        ##########unknown
        self.else2Idx = index
        cnt = self.byteArr[index]
        index += 1
        for c in range(cnt):
            elseInfo2 = []
            for i in range(2):
                tempH = struct.unpack("<h", self.byteArr[index:index+2])[0]
                elseInfo2.append(tempH)
                index += 2
            for i in range(2):
                tempF = struct.unpack("<f", self.byteArr[index:index+4])[0]
                elseInfo2.append(tempF)
                index += 4
            for i in range(2):
                tempH = struct.unpack("<h", self.byteArr[index:index+2])[0]
                elseInfo2.append(tempH)
                index += 2
            elseInfo2.append(self.byteArr[index])
            index += 1
            self.elseList2.append(elseInfo2)
        ##########unknown
        
        #cpu
        self.cpuIdx = index
        cpuCnt = self.byteArr[index]
        index += 1
        for i in range(cpuCnt):
            cpuInfo = []
            railNo = struct.unpack("<h", self.byteArr[index:index+2])[0]
            cpuInfo.append(railNo)
            index += 2
            
            org = self.byteArr[index]
            index += 1
            cpuInfo.append(org)
            mode = self.byteArr[index]
            index += 1
            cpuInfo.append(mode)

            for j in range(4):
                tempF = struct.unpack("<f", self.byteArr[index:index+4])[0]
                index += 4
                cpuInfo.append(tempF)
            self.cpuList.append(cpuInfo)

        #comic bin data
        self.comicScriptIdx = index
        comicbinCnt = self.byteArr[index]
        index += 1
        
        for i in range(comicbinCnt):
            comicScriptInfo = []
            comicNum = struct.unpack("<h", self.byteArr[index:index+2])[0]
            comicScriptInfo.append(comicNum)
            index += 2
            comicType = self.byteArr[index]
            comicScriptInfo.append(comicType)
            index += 1
            railNo = struct.unpack("<h", self.byteArr[index:index+2])[0]
            comicScriptInfo.append(railNo)
            index += 2
            self.comicScriptList.append(comicScriptInfo)

        #Dosan data
        self.dosansenIdx = index
        dosanCnt = self.byteArr[index]
        index += 1

        for i in range(dosanCnt):
            dosanInfo = []

            sRailNo = struct.unpack("<h", self.byteArr[index:index+2])[0]
            dosanInfo.append(sRailNo)
            index += 2
            sRailFrom = struct.unpack("<h", self.byteArr[index:index+2])[0]
            dosanInfo.append(sRailFrom)
            index += 2
            sRailTo = struct.unpack("<h", self.byteArr[index:index+2])[0]
            dosanInfo.append(sRailTo)
            index += 2
            
            eRailNo = struct.unpack("<h", self.byteArr[index:index+2])[0]
            dosanInfo.append(eRailNo)
            index += 2
            eRailFrom = struct.unpack("<h", self.byteArr[index:index+2])[0]
            dosanInfo.append(eRailFrom)
            index += 2
            eRailTo = struct.unpack("<h", self.byteArr[index:index+2])[0]
            dosanInfo.append(eRailTo)
            index += 2

            tempH = struct.unpack("<h", self.byteArr[index:index+2])[0]
            dosanInfo.append(tempH)
            index += 2

            for j in range(4):
                tempF = struct.unpack("<f", self.byteArr[index:index+4])[0]
                dosanInfo.append(tempF)
                index += 4

            tempH = struct.unpack("<h", self.byteArr[index:index+2])[0]
            dosanInfo.append(tempH)
            index += 2

            tempF = struct.unpack("<f", self.byteArr[index:index+4])[0]
            dosanInfo.append(tempF)
            index += 4
                
            self.dosansenList.append(dosanInfo)

        self.railIdx = index
        #Map
        print("Read Map Data...")
        w = open(self.filename + ".csv", "w")
        w.write("index,prev_rail,block,")
        w.write("dir_x,dir_y,dir_z,")
        w.write("mdl_no,mdl_flg,mdl_kasenchu,per,")
        w.write("flg,flg,flg,flg,")
        w.write("rail_data,")
        w.write("next_rail,next_no,prev_rail,prev_no,\n")
        mapCnt = struct.unpack("<h", self.byteArr[index:index+2])[0]
        index += 2

        for i in range(mapCnt):
            prev_rail = struct.unpack("<h", self.byteArr[index:index+2])[0]
            index += 2
            block = struct.unpack("<b", self.byteArr[index].to_bytes(1, "little"))[0]
            index += 1

            w.write("{0},{1},{2},".format(i, prev_rail, block))

            #vector
            xyz = []
            for j in range(3):
                f = struct.unpack("<f", self.byteArr[index:index+4])[0]
                xyz.append(f)
                index += 4
                w.write("{0},".format(f))

            mdl_no = struct.unpack("<b", self.byteArr[index].to_bytes(1, "little"))[0]
            index += 1
            w.write("{0},".format(mdl_no))

            mdl_flg = struct.unpack("<b", self.byteArr[index].to_bytes(1, "little"))[0]
            index += 1
            w.write("{0},".format(mdl_flg))

            mdl_kasenchu = struct.unpack("<b", self.byteArr[index].to_bytes(1, "little"))[0]
            index += 1
            w.write("{0},".format(mdl_kasenchu))

            per = struct.unpack("<f", self.byteArr[index:index+4])[0]
            index += 4
            w.write("{0},".format(per))
            
            #flg
            flg = []
            for j in range(4):
                flag = self.byteArr[index]
                flg.append(flag)
                index += 1
                w.write("0x{:02x},".format(flag))

            #rail_data
            rail_data = self.byteArr[index]
            w.write("{0},".format(rail_data))
            index += 1

            for j in range(rail_data):
                if readFlag:
                    next_rail = struct.unpack("<h", self.byteArr[index:index+2])[0]
                    index += 2
                    next_no = struct.unpack("<h", self.byteArr[index:index+2])[0]
                    index += 2
                    prev_rail = struct.unpack("<h", self.byteArr[index:index+2])[0]
                    index += 2
                    prev_no = struct.unpack("<h", self.byteArr[index:index+2])[0]
                    index += 2
                    w.write("{0},{1},{2},{3},".format(next_rail, next_no, prev_rail, prev_no))
                    
                next_rail = struct.unpack("<h", self.byteArr[index:index+2])[0]
                index += 2
                next_no = struct.unpack("<h", self.byteArr[index:index+2])[0]
                index += 2
                prev_rail = struct.unpack("<h", self.byteArr[index:index+2])[0]
                index += 2
                prev_no = struct.unpack("<h", self.byteArr[index:index+2])[0]
                index += 2
                w.write("{0},{1},{2},{3},".format(next_rail, next_no, prev_rail, prev_no))
            w.write("\n")
        w.close()

        print("Map End!")
        print(hex(index))
        ##########unknown
        cnt = struct.unpack("<h", self.byteArr[index:index+2])[0]
        index += 2
        for i in range(cnt):
            railNo = struct.unpack("<h", self.byteArr[index:index+2])[0]
            index += 2
            print(railNo, end=", ")
            endcnt = self.byteArr[index]
            index += 1
            print(endcnt, end=", ")
            for j in range(endcnt):
                for k in range(8):
                    temp = self.byteArr[index]
                    index += 1
                    print(temp, end=", ")
            print()

        index += 2
        ##########unknown

        print("amb data...")
        ambcnt = struct.unpack("<h", self.byteArr[index:index+2])[0]
        index += 2
        w = open(self.filename + "_amb.csv", "w")
        for i in range(ambcnt):
            w.write("{0},".format(i))
            temp = self.byteArr[index]
            index += 1
            w.write("{0},".format(temp))
            temp = struct.unpack("<f", self.byteArr[index:index+4])[0]
            index += 4
            w.write("{0},".format(temp))
            for j in range(2):
                temp = struct.unpack("<h", self.byteArr[index:index+2])[0]
                index += 2
                w.write("{0},".format(temp))

            for j in range(6):
                temp = struct.unpack("<f", self.byteArr[index:index+4])[0]
                index += 4
                w.write("{0},".format(temp))

            temp = self.byteArr[index]
            index += 1
            w.write("{0},".format(temp))
            temp = self.byteArr[index]
            index += 1
            w.write("{0},".format(temp))

            temp = struct.unpack("<h", self.byteArr[index:index+2])[0]
            index += 2
            w.write("{0},".format(temp))

            for j in range(10):
                temp = struct.unpack("<f", self.byteArr[index:index+4])[0]
                index += 4
                w.write("{0},".format(temp))
                
            w.write("\n")
            w.write(","*12)
            
            cnta = self.byteArr[index]
            index += 1
            w.write("{0},".format(cnta))
            for j in range(cnta):
                temp = struct.unpack("<h", self.byteArr[index:index+2])[0]
                index += 2
                w.write("{0},".format(temp))

                for k in range(10):
                    temp = struct.unpack("<f", self.byteArr[index:index+4])[0]
                    index += 4
                    w.write("{0},".format(temp))
                w.write("\n")
                w.write(","*13)
            w.write("\n")
        w.close()

        return True
    def saveMusic(self, cnt):
        try:
            index = self.musicIdx
            newByteArr = self.byteArr[0:index]
            
            newByteArr.append(cnt)
            for i in range(cnt):
                newByteArr.append(i)

            index = self.trainCntIdx
            newByteArr.extend(self.byteArr[index:])
            self.save(newByteArr)
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False

    def saveTrainCnt(self, cnt):
        try:
            index = self.trainCntIdx
            index += 1
            newByteArr = bytearray()

            if cnt > self.trainCnt:
                index = self.trainCntIdx2
                newByteArr = self.byteArr[0:index]

                for i in range(cnt - self.trainCnt):
                    tempH0 = struct.pack("<h", 0)
                    tempH1 = struct.pack("<h", 1)
                    newByteArr.extend(tempH0)
                    newByteArr.extend(tempH0)
                    newByteArr.extend(tempH1)
                    newByteArr.extend(tempH0)
                    newByteArr.append(0)
            else:
                for i in range(cnt):
                    index += 2
                    index += 2
                    index += 2
                    index += 2
                    index += 1
                newByteArr = self.byteArr[0:index]
            
            index = self.trainCntIdx2
            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.trainCntIdx] = cnt
            self.save(newByteArr)
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False

    def saveRailPos(self, num, trainList):
        try:
            if num == 0:
                index = self.trainCntIdx
                index += 1
            elif num == 1:
                index = self.trainCntIdx2
            elif num == 2:
                index = self.trainCntIdx3
                
            newByteArr = self.byteArr[0:index]

            for i in range(len(trainList)):
                trainInfo = trainList[i]
                for j in range(len(trainInfo)):
                    if j == 4:
                        newByteArr.append(trainInfo[j])
                        index += 1
                    else:
                        tempH = struct.pack("<h", trainInfo[j])
                        newByteArr.extend(tempH)
                        index += 2

            newByteArr.extend(self.byteArr[index:])
            self.save(newByteArr)
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False

    def saveEleList1(self, eleList1):
        try:
            index = self.elseIdx
            newByteArr = self.byteArr[0:index]

            for i in range(len(eleList1)):
                eleInfo = eleList1[i]
                if i == 0:
                    eleInfo
                    tempF = struct.pack("<f", eleInfo)
                    newByteArr.extend(tempF)
                    newByteArr.append(4)
                    continue

                for j in range(len(eleInfo)):
                    if j < 2:
                        tempF = struct.pack("<f", eleInfo[j])
                        newByteArr.extend(tempF)
                    else:
                        newByteArr.append(eleInfo[j])
                    
            index = self.lightIdx
            newByteArr.extend(self.byteArr[index:])
            self.save(newByteArr)
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False

    def saveSimpleList(self, index, listCntVer, simpleList):
        try:
            newByteArr = self.byteArr[0:index]
            if listCntVer == 1:
                newByteArr.append(len(simpleList))
            elif listCntVer == 2:
                tempH = struct.pack("<h", len(simpleList))
                newByteArr.extend(tempH)

            for i in range(len(simpleList)):
                name = simpleList[i]
                newByteArr.append(len(name))
                newByteArr.extend(name.encode("shift-jis"))

            cnt = 0
            if listCntVer == 1:
                cnt = self.byteArr[index]
                index += 1
            elif listCntVer == 2:
                cnt = struct.unpack("<h", self.byteArr[index:index+2])[0]
                index += 2

            for i in range(cnt):
                nameLen = self.byteArr[index]
                index += 1
                index += nameLen
    
            newByteArr.extend(self.byteArr[index:])
            self.save(newByteArr)
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False

    def saveStationCnt(self, cnt):
        try:
            index = self.stationIdx
            stationCnt = self.byteArr[index]
            index += 2

            if cnt > stationCnt:
                index = self.binIdx
                newByteArr = self.byteArr[0:index]

                for i in range(cnt - stationCnt):
                    tempH0 = struct.pack("<h", 0)
                    tempHM1 = struct.pack("<h", -1)
                    tempH100 = struct.pack("<h", 100)
                    newByteArr.append(0)
                    newByteArr.extend(tempH0)
                    newByteArr.extend(tempHM1)
                    newByteArr.extend(tempH100)
                    newByteArr.extend(tempH0)
            else:
                for i in range(cnt):
                    index += 1
                    index += 2
                    index += 2
                    index += 2
                    index += 2
                newByteArr = self.byteArr[0:index]

            index = self.binIdx
            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.stationIdx] = cnt
            
            self.save(newByteArr)
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False

    def saveStation(self, valList):
        try:
            index = self.stationIdx
            stationCnt = self.byteArr[index]
            index += 2

            newByteArr = self.byteArr[0:index]
            for i in range(len(valList)):
                valInfo = valList[i]
                for j in range(len(valInfo)):
                    if j == 0:
                        newByteArr.append(valInfo[j])
                    else:
                        tempH = struct.pack("<h", valInfo[j])
                        newByteArr.extend(tempH)

            index = self.binIdx
            newByteArr.extend(self.byteArr[index:])
            
            self.save(newByteArr)
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False

    def saveBinAnimeCnt(self, cnt):
        try:
            index = self.binAnimeIdx
            binAnimeCnt = self.byteArr[index]
            index += 1

            if cnt > binAnimeCnt:
                index = self.smfIdx
                newByteArr = self.byteArr[0:index]

                for i in range(cnt - binAnimeCnt):
                    tempH0 = struct.pack("<h", 0)
                    newByteArr.append(1)
                    newByteArr.extend(tempH0)
                    newByteArr.extend(tempH0)
            else:
                for i in range(cnt):
                    index += 1
                    index += 2
                    index += 2
                newByteArr = self.byteArr[0:index]

            index = self.smfIdx
            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.binAnimeIdx] = cnt
            
            self.save(newByteArr)
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False

    def saveBinAnime(self, valList):
        try:
            index = self.binAnimeIdx
            binAnimeCnt = self.byteArr[index]
            index += 1

            newByteArr = self.byteArr[0:index]
            print(valList)
            for i in range(len(valList)):
                valInfo = valList[i]
                for j in range(len(valInfo)):
                    if j == 0:
                        newByteArr.append(valInfo[j])
                    else:
                        tempH = struct.pack("<h", valInfo[j])
                        newByteArr.extend(tempH)

            index = self.smfIdx
            newByteArr.extend(self.byteArr[index:])
            
            self.save(newByteArr)
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False

    def saveSmfInfo(self, num, mode, smfInfo):
        try:
            index = self.smfIdx
            cnt = self.byteArr[index]
            index += 1
            for i in range(num):
                b = self.byteArr[index]
                index += 1
                index += b
                for j in range(5):
                    index += 1
                index += 1
                index += 2

            newByteArr = self.byteArr[0:index]
            
            if mode == "modify" or mode == "insert":
                newByteArr.append(len(smfInfo[0]))
                newByteArr.extend(smfInfo[0].encode("shift-jis"))
                for i in range(5):
                    newByteArr.append(smfInfo[1+i])
                newByteArr.append(smfInfo[6])
                tempH = struct.pack("<h", smfInfo[7])
                newByteArr.extend(tempH)

                if mode == "modify":
                    b = self.byteArr[index]
                    index += 1
                    index += b
                    for j in range(5):
                        index += 1
                    index += 1
                    index += 2
                else:
                    cnt += 1
            elif mode == "delete":
                b = self.byteArr[index]
                index += 1
                index += b
                for j in range(5):
                    index += 1
                index += 1
                index += 2
                cnt -= 1
            
            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.smfIdx] = cnt
            
            self.save(newByteArr)
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False

    def saveStationNameInfo(self, num, mode, smfInfo):
        try:
            index = self.stationNameIdx
            cnt = self.byteArr[index]
            index += 1
            for i in range(num):
                b = self.byteArr[index]
                index += 1
                index += b
                index += 1
                index += 2
                for j in range(6):
                    index += 4
                index += 2

            newByteArr = self.byteArr[0:index]
            
            if mode == "modify" or mode == "insert":
                encodeName = smfInfo[0].encode("shift-jis")
                newByteArr.append(len(encodeName))
                newByteArr.extend(encodeName)
                newByteArr.append(smfInfo[1])
                tempH = struct.pack("<h", smfInfo[2])
                newByteArr.extend(tempH) 
                for i in range(3):
                    tempF = struct.pack("<f", smfInfo[3+i])
                    newByteArr.extend(tempF)
                for i in range(3):
                    tempI = struct.pack("<i", smfInfo[6+i])
                    newByteArr.extend(tempI)
                tempH = struct.pack("<h", smfInfo[9])
                newByteArr.extend(tempH)

                if mode == "modify":
                    b = self.byteArr[index]
                    index += 1
                    index += b
                    index += 1
                    index += 2
                    for j in range(6):
                        index += 4
                    index += 2
                else:
                    cnt += 1
            elif mode == "delete":
                b = self.byteArr[index]
                index += 1
                index += b
                index += 1
                index += 2
                for j in range(6):
                    index += 4
                index += 2
                cnt -= 1
            
            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.stationNameIdx] = cnt
            
            self.save(newByteArr)
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False

    def saveElse2Cnt(self, cnt):
        try:
            index = self.else2Idx
            else2Cnt = self.byteArr[index]
            index += 1

            if cnt > else2Cnt:
                index = self.cpuIdx
                newByteArr = self.byteArr[0:index]

                for i in range(cnt - else2Cnt):
                    tempH0 = struct.pack("<h", 0)
                    tempF0 = struct.pack("<f", 0)
                    newByteArr.extend(tempH0)
                    newByteArr.extend(tempH0)
                    newByteArr.extend(tempF0)
                    newByteArr.extend(tempF0)
                    newByteArr.extend(tempH0)
                    newByteArr.extend(tempH0)
                    newByteArr.append(0)
            else:
                for i in range(cnt):
                    index += 2
                    index += 2
                    index += 4
                    index += 4
                    index += 2
                    index += 2
                    index += 1
                newByteArr = self.byteArr[0:index]

            index = self.cpuIdx
            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.else2Idx] = cnt
            
            self.save(newByteArr)
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False

    def saveEles2List(self, valList):
        try:
            index = self.else2Idx
            else2Cnt = self.byteArr[index]
            index += 1

            newByteArr = self.byteArr[0:index]
            for i in range(len(valList)):
                valInfo = valList[i]
                for j in range(len(valInfo)):
                    if j in [2, 3]:
                        tempF = struct.pack("<f", valInfo[j])
                        newByteArr.extend(tempF)
                    elif j == 6:
                        newByteArr.append(valInfo[j])
                    else:
                        tempH = struct.pack("<h", valInfo[j])
                        newByteArr.extend(tempH)

            index = self.cpuIdx
            newByteArr.extend(self.byteArr[index:])
            
            self.save(newByteArr)
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False
        
    def saveCpuInfo(self, num, mode, smfInfo):
        try:
            index = self.cpuIdx
            cnt = self.byteArr[index]
            index += 1
            for i in range(num):
                index += 2
                index += 1
                index += 1
                for j in range(4):
                    index += 4

            newByteArr = self.byteArr[0:index]
            
            if mode == "modify" or mode == "insert":
                tempH = struct.pack("<h", smfInfo[0])
                newByteArr.extend(tempH)
                newByteArr.append(smfInfo[1])
                newByteArr.append(smfInfo[2])
                for i in range(4):
                    tempF = struct.pack("<f", smfInfo[3+i])
                    newByteArr.extend(tempF)

                if mode == "modify":
                    index += 2
                    index += 1
                    index += 1
                    for j in range(4):
                        index += 4
                else:
                    cnt += 1
            elif mode == "delete":
                index += 2
                index += 1
                index += 1
                for j in range(4):
                    index += 4
                cnt -= 1
            
            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.cpuIdx] = cnt
            
            self.save(newByteArr)
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False

    def saveComicScriptList(self, comicScriptList):
        try:
            index = self.comicScriptIdx
            newByteArr = self.byteArr[0:index]

            newByteArr.append(len(comicScriptList))
            for i in range(len(comicScriptList)):
                comicScriptInfo = comicScriptList[i]
                for j in range(len(comicScriptInfo)):
                    if j == 1:
                        newByteArr.append(comicScriptInfo[j])
                    else:
                        tempH = struct.pack("<h", comicScriptInfo[j])
                        newByteArr.extend(tempH)

            index = self.dosanIdx
            newByteArr.extend(self.byteArr[index:])
            self.save(newByteArr)
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False

    def saveDosansenCnt(self, cnt):
        try:
            index = self.dosansenIdx
            dosansenCnt = self.byteArr[index]
            index += 1

            if cnt > dosansenCnt:
                index = self.railIdx
                newByteArr = self.byteArr[0:index]

                for i in range(cnt - dosansenCnt):
                    tempH0 = struct.pack("<h", 0)
                    tempF0 = struct.pack("<f", 0)
                    for j in range(7):
                        newByteArr.extend(tempH0)
                    for j in range(4):
                        newByteArr.extend(tempF0)
                    newByteArr.extend(tempH0)
                    newByteArr.extend(tempF0)
            else:
                for i in range(cnt):
                    for j in range(7):
                        index += 2
                    for j in range(4):
                        index += 4
                    index += 2
                    index += 4
                newByteArr = self.byteArr[0:index]

            index = self.railIdx
            newByteArr.extend(self.byteArr[index:])
            newByteArr[self.dosansenIdx] = cnt
            
            self.save(newByteArr)
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False

    def saveDosansenList(self, valList):
        try:
            index = self.dosansenIdx
            dosansenCnt = self.byteArr[index]
            index += 1

            newByteArr = self.byteArr[0:index]
            for i in range(len(valList)):
                valInfo = valList[i]
                for j in range(len(valInfo)):
                    if j in [7, 8, 9, 10, 12]:
                        tempF = struct.pack("<f", valInfo[j])
                        newByteArr.extend(tempF)
                    else:
                        tempH = struct.pack("<h", valInfo[j])
                        newByteArr.extend(tempH)

            index = self.railIdx
            newByteArr.extend(self.byteArr[index:])
            
            self.save(newByteArr)
            return True
        except Exception as e:
            self.error = traceback.format_exc()
            return False
        
    def reload(self):
        self.open()
        return self
    
    def save(self, newByteArr):
        self.byteArr = newByteArr
        w = open(self.filePath, "wb")
        w.write(newByteArr)
        w.close()
        
