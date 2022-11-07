from importPy.tkinterScrollbarFrameClass import *

from importPy.tab1.musicWidget import *
from importPy.tab1.trainCountWidget import *
from importPy.tab1.railPosWidget import *

from importPy.tab2.else1ListWidget import *
from importPy.tab2.simpleListWidget import *
from importPy.tab2.stationWidget import *
from importPy.tab2.binAnimeListWidget import *

from importPy.tab3.smfListWidget import *

from importPy.tab4.stationNameWidget import *

from importPy.tab5.elseList2Widget import *

from importPy.tab6.cpuWidget import *

from importPy.tab7.comicScriptWidget import *
from importPy.tab7.dosansenListWidget import *

from importPy.tab8.railListWidget import *

from importPy.tab9.elseList3Widget import *

from importPy.tab10.ambListWidget import *

def tab1AllWidget(tab_one, decryptFile, reloadFunc):
    tab_one_frame = ttk.Frame(tab_one)
    tab_one_frame.pack(expand=True, fill=BOTH)
    frame = ScrollbarFrame(tab_one_frame)

    MusicWidget(frame.frame, decryptFile, reloadFunc)
    TrainCountWidget(frame.frame, decryptFile, reloadFunc)

    railPosFrame = ttk.Frame(frame.frame)
    railPosFrame.pack(anchor=NW, padx=10, pady=5)
    
    railPos1Frame = ttk.Frame(railPosFrame)
    railPos1Frame.grid(row=0, column=0, pady=3)
    RailPosWidget(railPos1Frame, "初期配置", 0, decryptFile, decryptFile.trainList, reloadFunc)

    railPos2Frame = ttk.Frame(railPosFrame)
    railPos2Frame.grid(row=1, column=0, pady=3)
    RailPosWidget(railPos2Frame, "ダミー配置？", 1, decryptFile, decryptFile.trainList2, reloadFunc)

    railPos3Frame = ttk.Frame(railPosFrame)
    railPos3Frame.grid(row=2, column=0, pady=3)
    RailPosWidget(railPos3Frame, "試運転、二人バトル配置", 2, decryptFile, decryptFile.trainList3, reloadFunc)

def tab2AllWidget(tab_two, decryptFile, reloadFunc):
    tab_two_frame = ttk.Frame(tab_two)
    tab_two_frame.pack(expand=True, fill=BOTH)
    frame = ScrollbarFrame(tab_two_frame)

    Else1ListWidget(frame.frame, decryptFile, decryptFile.else1List, reloadFunc)

    simpleListFrame = ttk.Frame(frame.frame)
    simpleListFrame.pack(anchor=NW)
    SimpleListWidget(simpleListFrame, "light情報", decryptFile, decryptFile.lightList, decryptFile.lightIdx, 1, reloadFunc)
    SimpleListWidget(simpleListFrame, "駅名標画像情報", decryptFile, decryptFile.pngList, decryptFile.pngIdx, 2, reloadFunc)

    StationWidget(frame.frame, decryptFile, decryptFile.stationList, reloadFunc)

    simpleListFrame2 = ttk.Frame(frame.frame)
    simpleListFrame2.pack(anchor=NW)
    SimpleListWidget(simpleListFrame2, "ベースbin情報", decryptFile, decryptFile.baseBinList, decryptFile.binIdx, 1, reloadFunc)
    BinAnimeListWidget(simpleListFrame2, decryptFile, decryptFile.binAnimeList, reloadFunc)

def tab3AllWidget(tab_3, decryptFile, reloadFunc):
    SmfListWidget(tab_3, decryptFile, decryptFile.smfList, 20, reloadFunc)

def tab4AllWidget(tab_4, decryptFile, reloadFunc):
    StationNameWidget(tab_4, decryptFile, decryptFile.stationNameList, 20, reloadFunc)

def tab5AllWidget(tab_5, decryptFile, reloadFunc):
    EleList2Widget(tab_5, decryptFile, decryptFile.elseList2, reloadFunc)

def tab6AllWidget(tab_6, decryptFile, reloadFunc):
    CpuWidget(tab_6, decryptFile, decryptFile.cpuList, 20, reloadFunc)

def tab7AllWidget(tab_7, decryptFile, reloadFunc):
    ComicScriptWidget(tab_7, decryptFile, decryptFile.comicScriptList, reloadFunc)
    DosansenListWidget(tab_7, decryptFile, decryptFile.dosansenList, reloadFunc)

def tab8AllWidget(tab_8, decryptFile, reloadFunc):
    frame = ScrollbarFrame(tab_8)
    RailListWidget(frame.frame, decryptFile, decryptFile.railList, reloadFunc)

def tab9AllWidget(tab_9, decryptFile, reloadFunc):
    ElseList3Widget(tab_9, decryptFile, decryptFile.elseList3, reloadFunc)

def tab10AllWidget(tab_10, decryptFile, reloadFunc):
    frame = ScrollbarFrame(tab_10)
    AmbListWidget(frame.frame, decryptFile, decryptFile.ambList, reloadFunc)
