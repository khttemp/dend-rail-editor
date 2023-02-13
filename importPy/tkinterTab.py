import tkinter
from tkinter import ttk

from importPy.tkinterScrollbarFrameClass import ScrollbarFrame

from importPy.tab1.musicWidget import MusicWidget
from importPy.tab1.trainCountWidget import TrainCountWidget
from importPy.tab1.railPosWidget import RailPosWidget

from importPy.tab2.else1ListWidget import Else1ListWidget
from importPy.tab2.simpleListWidget import SimpleListWidget
from importPy.tab2.stationWidget import StationWidget
from importPy.tab2.binAnimeListWidget import BinAnimeListWidget

from importPy.tab3.smfListWidget import SmfListWidget

from importPy.tab4.stationNameWidget import StationNameWidget

from importPy.tab5.else2ListWidget import Else2ListWidget

from importPy.tab6.cpuWidget import CpuWidget

from importPy.tab7.comicScriptWidget import ComicScriptWidget
from importPy.tab7.dosansenListWidget import DosansenListWidget

from importPy.tab8.railListWidget import RailListWidget

from importPy.tab9.else3ListWidget import Else3ListWidget

from importPy.tab10.else4ListWidget import Else4ListWidget

from importPy.tab11.ambListWidget import AmbListWidget


def tab1AllWidget(tabFrame, decryptFile, reloadFunc):
    tab_one_frame = ttk.Frame(tabFrame)
    tab_one_frame.pack(expand=True, fill=tkinter.BOTH)
    frame = ScrollbarFrame(tab_one_frame)

    MusicWidget(frame.frame, decryptFile, reloadFunc)
    TrainCountWidget(frame.frame, decryptFile, reloadFunc)

    railPosFrame = ttk.Frame(frame.frame)
    railPosFrame.pack(anchor=tkinter.NW, padx=10, pady=5)

    railPos1Frame = ttk.Frame(railPosFrame)
    railPos1Frame.grid(sticky=tkinter.NW, row=0, column=0, pady=3)

    RailPosWidget(railPos1Frame, "初期配置", 0, decryptFile, decryptFile.trainList, reloadFunc)

    railPos2Frame = ttk.Frame(railPosFrame)
    railPos2Frame.grid(sticky=tkinter.NW, row=1, column=0, pady=3)
    RailPosWidget(railPos2Frame, "ダミー配置？", 1, decryptFile, decryptFile.trainList2, reloadFunc)

    railPos3Frame = ttk.Frame(railPosFrame)
    railPos3Frame.grid(sticky=tkinter.NW, row=2, column=0, pady=3)
    RailPosWidget(railPos3Frame, "試運転、二人バトル配置", 2, decryptFile, decryptFile.trainList3, reloadFunc)


def tab2AllWidget(tabFrame, decryptFile, reloadFunc):
    tab_two_frame = ttk.Frame(tabFrame)
    tab_two_frame.pack(expand=True, fill=tkinter.BOTH)
    frame = ScrollbarFrame(tab_two_frame)

    Else1ListWidget(frame.frame, decryptFile, decryptFile.else1List, reloadFunc)

    simpleListFrame = ttk.Frame(frame.frame)
    simpleListFrame.pack(anchor=tkinter.NW)
    SimpleListWidget(simpleListFrame, "light情報", decryptFile, decryptFile.lightList, decryptFile.lightIdx, 1, reloadFunc)
    if decryptFile.game in ["CS", "RS"]:
        SimpleListWidget(simpleListFrame, "駅名標画像情報", decryptFile, decryptFile.pngList, decryptFile.pngIdx, 2, reloadFunc)
        StationWidget(frame.frame, decryptFile, decryptFile.stationList, reloadFunc)

    simpleListFrame2 = ttk.Frame(frame.frame)
    simpleListFrame2.pack(anchor=tkinter.NW)
    SimpleListWidget(simpleListFrame2, "ベースbin情報", decryptFile, decryptFile.baseBinList, decryptFile.binIdx, 1, reloadFunc)
    BinAnimeListWidget(simpleListFrame2, decryptFile, decryptFile.binAnimeList, reloadFunc)


def tab3AllWidget(tabFrame, decryptFile, reloadFunc):
    SmfListWidget(tabFrame, decryptFile, decryptFile.smfList, 20, reloadFunc)


def tab4AllWidget(tabFrame, decryptFile, reloadFunc):
    StationNameWidget(tabFrame, decryptFile, decryptFile.stationNameList, 20, reloadFunc)


def tab5AllWidget(tabFrame, decryptFile, reloadFunc):
    Else2ListWidget(tabFrame, decryptFile, decryptFile.else2List, reloadFunc)


def tab6AllWidget(tabFrame, decryptFile, reloadFunc):
    CpuWidget(tabFrame, decryptFile, decryptFile.cpuList, 20, reloadFunc)


def tab7AllWidget(tabFrame, decryptFile, reloadFunc):
    ComicScriptWidget(tabFrame, decryptFile, decryptFile.comicScriptList, reloadFunc)
    if decryptFile.game in ["CS", "RS"]:
        DosansenListWidget(tabFrame, decryptFile, decryptFile.dosansenList, reloadFunc)


def tab8AllWidget(tabFrame, decryptFile, reloadFunc):
    frame = ScrollbarFrame(tabFrame)
    RailListWidget(frame.frame, decryptFile, decryptFile.railList, reloadFunc)


def tab9AllWidget(tabFrame, decryptFile, reloadFunc):
    Else3ListWidget(tabFrame, decryptFile, decryptFile.else3List, reloadFunc)


def tab10AllWidget(tabFrame, decryptFile, reloadFunc):
    Else4ListWidget(tabFrame, decryptFile, decryptFile.else4List, reloadFunc)


def tab11AllWidget(tabFrame, decryptFile, reloadFunc):
    frame = ScrollbarFrame(tabFrame)
    AmbListWidget(frame.frame, decryptFile, decryptFile.ambList, reloadFunc)
