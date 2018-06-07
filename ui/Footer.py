#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: Footer.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys, os

# PyQt5
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QGridLayout, QPushButton

# Plt
import appData as app
from ui import uirc as rc

# -------------------------------------------------------------------------------------------------------------
""" Footer """

class Footer(QWidget):
    FooterSig = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(Footer, self).__init__(parent)

        self.settings = app.appSetting
        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        # self.logo = QPixmap(os.path.join(os.getenv(app.__envKey__), 'imgs', 'logo','DAMGteam', 'icons', '24x24.png'))
        # self.damgLogo = rc.Label(txt="")
        # self.damgLogo.setPixmap(self.logo)
        # self.damgLogo.resize(self.logo.width(), self.logo.height())
        # self.damgLogo.setToolTip(app.COPYRIGHT)

        self.logoBtn = QPushButton()
        self.logoBtn.setToolTip(app.COPYRIGHT)
        self.logoBtn.setIcon(QIcon(os.path.join(os.getenv(app.__envKey__), 'imgs', 'logo','DAMGteam', 'icons', '24x24.png')))
        self.layout.addWidget(self.logoBtn, 0, 8, 1, 1)

        self.applySetting()

    def applySetting(self):
        self.layout.setSpacing(0)
        self.logoBtn.setFixedSize(QSize(25, 25))
        self.logoBtn.setIconSize(QSize(24, 24))
        self.logoBtn.setMouseTracking(True)

def main():
    app = QApplication(sys.argv)
    layout = Footer()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 1/06/2018 - 4:24 AM