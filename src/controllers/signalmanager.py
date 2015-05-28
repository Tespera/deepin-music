#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys
from PyQt5.QtCore import (QObject, pyqtSignal, pyqtSlot, 
    pyqtProperty, QUrl)
from .utils import registerContext, contexts


class SignalManager(QObject):

    __contextName__ = 'SignalManager'

    #添加我的收藏
    addtoFavorite = pyqtSignal('QString')

    #移出我的收藏
    removeFromFavorite = pyqtSignal('QString')

    # 在线音乐添加到下载列表
    addtoDownloadlist = pyqtSignal(int)
    addAlltoDownloadlist = pyqtSignal('QString')

    # 在线音乐对象切换本地音乐对象
    switchOnlinetoLocal = pyqtSignal('QString', 'QString')

    #
    addLocalSongToDataBase = pyqtSignal('QString')
    addLocalSongsToDataBase = pyqtSignal(list)

    # mediaplayer
    playingChanged = pyqtSignal(bool)
    lrcPositionChanged = pyqtSignal('qint64', int)

    #Dialog
    dialogClosed = pyqtSignal()

    #add playlist dialog
    newPlaylistDialogShowed = pyqtSignal()
    addNewPlaylist = pyqtSignal('QString')

    #add multi playlist dialog
    newMultiPlaylistDialogShowed = pyqtSignal('QString', 'QString')
    addMutiPlaylistFlags = pyqtSignal('QVariant')
    addSongsToMultiPlaylist = pyqtSignal('QString', 'QString', list)

    #global search
    globalSearched = pyqtSignal('QString')

    #lrc
    downloadLrc = pyqtSignal('QString', 'QString')
    noLrcFound = pyqtSignal()
    toggleShow = pyqtSignal()

    lineModeChanged = pyqtSignal(int)
    singleTextInfoChanged = pyqtSignal('QString', float, int)
    douleTextInfoChanged = pyqtSignal(list)

    previousSong = pyqtSignal()
    playToggle = pyqtSignal(bool)
    nextSong = pyqtSignal()
    fontIncreaseChanged = pyqtSignal()
    fontDecreaseChanged = pyqtSignal()
    lrcBackHalfSecond = pyqtSignal()
    lrcForwardHarfSecond = pyqtSignal()
    lrcThemeChanged = pyqtSignal()
    showLrcSingleLine = pyqtSignal()
    showLrcDoubleLine = pyqtSignal()
    kalaokChanged = pyqtSignal()
    locked = pyqtSignal()
    unlocked = pyqtSignal()
    lrcSetting = pyqtSignal()
    lrcSearch = pyqtSignal()
    lrcClosed = pyqtSignal()

    @registerContext
    def __init__(self, parent=None):
        super(SignalManager, self).__init__(parent)



signalManager = SignalManager()