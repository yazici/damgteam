#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Name: EnglishDictionary.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    It is a very fun english dictionary.
"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import json
import os
import sys
from difflib import get_close_matches

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QDialog, QGridLayout, QHBoxLayout, QLineEdit, QTextEdit, QApplication, QWidget)

from utilities.utils import getAppIcon
from ui.uirc import Label, Button
from core.Specs import Specs

class EnglishDictionary(QDialog):

    key = 'engDict'

    def __init__(self, parent=None):

        super(EnglishDictionary, self).__init__(parent)

        self.specs = Specs(self.key, self)
        self.setWindowIcon(QIcon(getAppIcon(32, "EnglishDictionary")))

        central_widget = QWidget(self)
        self.layout = QGridLayout(self)
        central_widget.setLayout(self.layout)

        self.buildUI()

    def buildUI(self):

        hbox = QHBoxLayout()
        grid = QGridLayout()

        self.lineInput = QLineEdit()
        self.suggessLabel = Label()

        searchBtn = Button(['Translate', ' '])
        searchBtn.clicked.connect(self.translate)

        yesBtn = Button(['Yes', ' '])
        yesBtn.clicked.connect(self.translate)

        noBtn = Button(['No', ' '])
        noBtn.clicked.connect(self.translate)

        self.answer = QTextEdit()

        grid.addWidget(self.lineInput, 0, 0, 1, 3)
        grid.addWidget(self.suggessLabel, 1, 0, 1, 3)
        grid.addWidget(searchBtn, 2, 0, 1, 1)
        grid.addWidget(yesBtn, 2, 1, 1, 1)
        grid.addWidget(noBtn, 2, 2, 1, 1)
        grid.addWidget(self.answer, 3, 0, 4, 3)

        hbox.addLayout(grid)

        self.setLayout(hbox)

    def translate(self, *args):
        from appData import __envKey__
        filePth = os.path.join(os.getenv(__envKey__), 'appData', 'ED.json')
        data = json.load(open(filePth))
        w = self.lineInput.text().lower()
        if w in data:
            answer = str(data[w])
        elif len(get_close_matches(w, data.keys())) > 0:
            answer = "Did you mean %s instead?" % str(get_close_matches(w, data.keys())[0])
            if 'Yes':
                answer = str(data[get_close_matches(w, data.keys())[0]])
            elif 'No':
                answer = "The word doesn't exist. Please double check it."
            else:
                answer = "We did not understand your entry."
        else:
            answer = "The word doesn't exist. Please double check it."
        self.populateAnswer(answer)

    def populateAnswer(self, answer, *args):
        blocks = ["[u'", "']", "', u'", "', u", ", u'", "['"]
        for block in blocks:
            if block in answer:
                stringToList = answer.split(block)
                answer = self.listToString(stringToList)
        self.answer.setPlainText("%s" % answer)

    def listToString(self, stringToList, *args):
        listToString = ""
        for i in stringToList:
            listToString += i
        return listToString


def initialize():
    app = QApplication(sys.argv)
    dictUI = EnglishDictionary()
    dictUI.show()
    app.exec_()

if __name__ == "__main__":
    initialize()