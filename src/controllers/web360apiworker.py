#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from .utils import registerContext
from dwidgets import dthread
import threading
import copy
from log import logger


class Web360ApiWorker(QObject):

    addMediaContent = pyqtSignal('QVariant')

    requestSuccessed = pyqtSignal(int, dict)

    __contextName__ = 'Web360ApiWorker'

    @registerContext
    def __init__(self, parent=None):
        super(Web360ApiWorker, self).__init__(parent)
        self.playedMusics = {}
        self._musicIds = []
        self._results = {}
        self.initConnect()

    def initConnect(self):
        self.requestSuccessed.connect(self.collectResults)

    @classmethod
    def md5(cls, musicId):
        import hashlib
        s = 'id=%d_projectName=linuxdeepin' % (musicId)
        md5Value = hashlib.md5(s)
        return md5Value.hexdigest()

    @classmethod
    def getUrlByID(cls, musicId):
        sign = cls.md5(musicId)
        params = {
            'id': musicId,
            'src': 'linuxdeepin',
            'sign': sign
        }

        url = 'http://s.music.haosou.com/player/songForPartner?id=%s&src=%s&sign=%s'\
            %(params['id'], params['src'], params['sign'])
        return url

    def getResult(self, musicId):
        import requests
        sign = self.md5(musicId)
        params = {
            'id': musicId,
            'src': 'linuxdeepin',
            'sign': sign
        }

        url = self.getUrlByID(musicId)
        try:
            # ret = requests.get("http://s.music.haosou.com/player/songForPartner", params=params)
            ret = requests.get(url)
            result = {
                'url': ret.url,
                'ret': ret.json()
            }
        except:
            result = None        

        self.playedMusics.update({musicId: result})

        return result

    @pyqtSlot(int)
    def getMusicUrlById(self, musicId):
        if musicId in self.playedMusics:
            result = self.playedMusics[musicId]
            if result:
                self.addMediaContent.emit(result)
        else:
            self.getNetMusicUrlById(musicId)

    @dthread
    @pyqtSlot(int)
    def getNetMusicUrlById(self, musicId):
        result = self.getResult(musicId)
        if result:
            self.addMediaContent.emit(result)

    @dthread
    def getQueueResults(self, musicId):
        result = self.getResult(musicId)
        if result:
            self.requestSuccessed.emit(musicId, result)

    @pyqtSlot('QString')
    def getMusicUrlByIds(self, musicIds):
        self._musicIds = [int(k) for k in musicIds.split('_')]
        for musicId in self._musicIds:
            if musicId in self.playedMusics:
                result = self.playedMusics[musicId]
                if result:
                    self.requestSuccessed.emit(musicId, result)
            else:
                self.getQueueResults(musicId)

    @pyqtSlot(int, dict)
    def collectResults(self, musicId, result):
        self._results.update({musicId: result})
        if len(self._results) == len(self._musicIds):
            results = copy.deepcopy(self._results)
            musicIds =copy.deepcopy(self._musicIds)
            for musicId in  musicIds:
                result = results[musicId]
                self.addMediaContent.emit(result)
                self._musicIds.remove(musicId) 
                self._results.pop(musicId)
            self.addMediaContent.emit(results[musicIds[0]])
