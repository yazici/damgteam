#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# http://13.55.214.163/check
# http://13.55.214.163/auth
"""

Script Name: plt.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script is master file of Pipeline Tool

"""

# -------------------------------------------------------------------------------------------------------------
""" Import modules """

# Python
import logging
import os
import subprocess
import sys
import webbrowser
import requests

import sqlite3 as lite
from functools import partial

# PyQt5
from PyQt5.QtCore import Qt, QSize, QCoreApplication, QSettings, pyqtSignal, QByteArray
from PyQt5.QtGui import QIcon, QPixmap, QImage, QIntValidator
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFrame, QDialog, QWidget, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QLineEdit, QLabel, QPushButton, QMessageBox, QGroupBox,
                             QCheckBox, QTabWidget, QSystemTrayIcon, QAction, QMenu, QFileDialog, QComboBox,
                             QDockWidget, QSlider, QSizePolicy, QStackedWidget, QStackedLayout)

import qdarkgraystyle

from __init__ import (__root__, __appname__, __version__, __organization__, __website__)

# -------------------------------------------------------------------------------------------------------------
""" Set up env variable path """
# Main path
os.environ[__root__] = os.getcwd()

# Preset
import plt_presets as pltp

pltp.preset3_maya_intergrate()

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain log """

logPth = os.path.join(os.getenv(__root__), 'appData', 'logs', 'plt.log')
logger = logging.getLogger('plt')
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------
""" Plt tools """
from ui import ui_acc_setting
from ui import ui_preference

from utilities import utils as func
from utilities import sql_local as usql
from utilities import message as mess
from utilities import variables as var

# -------------------------------------------------------------------------------------------------------------
""" Variables """

# PyQt5 ui elements
__center__ = Qt.AlignCenter
__right__ = Qt.AlignRight
__left__ = Qt.AlignLeft
frameStyle = QFrame.Sunken | QFrame.Panel

UNIT = 60
MARG = 5
BUFF = 10
SCAL = 1
STEP = 1
VAL = 1
MIN = 0
MAX = 1000

# Get apps info config
APPINFO = pltp.preset4_gather_configure_info()

# -------------------------------------------------------------------------------------------------------------
""" A label with center align """

class Clabel(QLabel):

    def __init__(self, text = "", align = __center__, lbW = 50, parent=None):
        super(Clabel, self).__init__(parent)

        self.text = text
        self.align = align
        self.lbW = lbW

        self.layout = QHBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        label = QLabel(self.text)
        label.setAlignment(self.align)
        label.setMinimumWidth(self.lbW)
        self.layout.addWidget(label)

# -------------------------------------------------------------------------------------------------------------
""" A spacer line to be able to add between layouts """

class QSpacer(QWidget):

    def __init__(self, lineW=MARG, parent=None):
        super(QSpacer, self).__init__(parent)

        self.lineW = lineW

        self.layout = QVBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        Separador = QFrame()
        Separador.setFrameShape(QFrame.HLine)
        Separador.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        Separador.setLineWidth(self.lineW)

        self.layout.addWidget(Separador)

# -------------------------------------------------------------------------------------------------------------
""" Sign up layout """

class Plt_sign_up(QDialog):

    showLoginSig1 = pyqtSignal(bool)

    def __init__(self, parent=None):

        super(Plt_sign_up, self).__init__(parent)

        self.setWindowTitle("Sign Up")
        self.setWindowIcon(QIcon(func.get_icon('Logo')))
        self.setContentsMargins(0,0,0,0)
        self.setFixedSize(450, 900)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        avatar_section = self.avatar_section()
        account_section = self.account_section()
        profile_section = self.profile_section()
        contact_section = self.location_section()
        security_section = self.security_section()
        buttons_section = self.buttons_section()

        self.layout.addWidget(Clabel("ALL FIELD ARE REQUIRED."), 0, 0, 1, 6)
        self.layout.addWidget(avatar_section, 1, 0, 1, 2)
        self.layout.addWidget(account_section, 1, 2, 1, 4)
        self.layout.addWidget(profile_section, 2, 0, 1, 6)
        self.layout.addWidget(contact_section, 3, 0, 1, 6)
        self.layout.addWidget(security_section, 4, 0, 1, 6)
        self.layout.addWidget(buttons_section, 5, 0, 1, 6)

    def avatar_section(self):
        avatar_groupBox = QGroupBox("Avatar")
        avatar_grid = QGridLayout()
        avatar_groupBox.setLayout(avatar_grid)

        defaultImg = QPixmap.fromImage(QImage(func.get_avatar('default')))
        self.userAvatar = QLabel()
        self.userAvatar.setPixmap(defaultImg)
        self.userAvatar.setScaledContents(True)
        self.userAvatar.setFixedSize(100, 100)

        set_avatarBtn = QPushButton("Set Avatar")
        set_avatarBtn.clicked.connect(self.on_set_avatar_btn_clicked)

        avatar_grid.addWidget(self.userAvatar, 0, 0, 2, 2)
        avatar_grid.addWidget(set_avatarBtn, 2, 0, 1, 2)

        return avatar_groupBox

    def account_section(self):

        account_groupBox = QGroupBox("Account")
        account_grid = QGridLayout()
        account_groupBox.setLayout(account_grid)

        account_grid.addWidget(Clabel('User Name'), 0, 0, 1, 2)
        account_grid.addWidget(Clabel('Password'), 1, 0, 1, 2)
        account_grid.addWidget(Clabel('Confirm Password'), 2, 0, 1, 2)

        self.usernameField = QLineEdit()
        self.passwordField = QLineEdit()
        self.confirmPassField = QLineEdit()

        self.passwordField.setEchoMode(QLineEdit.Password)
        self.confirmPassField.setEchoMode(QLineEdit.Password)

        account_grid.addWidget(self.usernameField, 0, 3, 1, 4)
        account_grid.addWidget(self.passwordField, 1, 3, 1, 4)
        account_grid.addWidget(self.confirmPassField, 2, 3, 1, 4)

        return account_groupBox

    def profile_section(self):

        profile_groupBox = QGroupBox("Profile")
        profile_grid = QGridLayout()
        profile_groupBox.setLayout(profile_grid)

        profile_grid.addWidget(Clabel('First Name'), 0, 0, 1, 2)
        profile_grid.addWidget(Clabel('Last Name'), 1, 0, 1, 2)
        profile_grid.addWidget(Clabel('Your Title'), 2, 0, 1, 2)
        profile_grid.addWidget(Clabel('Email'), 3, 0, 1, 2)
        profile_grid.addWidget(Clabel('Phone Number'), 4, 0, 1, 2)

        self.titleField = QLineEdit()
        self.firstnameField = QLineEdit()
        self.lastnameField = QLineEdit()
        self.emailField = QLineEdit()
        self.phoneField = QLineEdit()

        profile_grid.addWidget(self.firstnameField, 0, 2, 1, 4)
        profile_grid.addWidget(self.lastnameField, 1, 2, 1, 4)
        profile_grid.addWidget(self.titleField, 2, 2, 1, 4)
        profile_grid.addWidget(self.emailField, 3, 2, 1, 4)
        profile_grid.addWidget(self.phoneField, 4, 2, 1, 4)

        return profile_groupBox

    def location_section(self):

        contact_groupBox = QGroupBox("Location")
        contact_grid = QGridLayout()
        contact_groupBox.setLayout(contact_grid)

        contact_grid.addWidget(Clabel("Address Line 1"), 0, 0, 1, 2)
        contact_grid.addWidget(Clabel("Address Line 2"), 1, 0, 1, 2)
        contact_grid.addWidget(Clabel("Postal"), 2, 0, 1, 2)
        contact_grid.addWidget(Clabel("City"), 3, 0, 1, 2)
        contact_grid.addWidget(Clabel("Country"), 4, 0, 1, 2)

        self.addressLine1 = QLineEdit()
        self.addressLine2 = QLineEdit()
        self.postalCode = QLineEdit()
        self.city = QLineEdit()
        self.country = QLineEdit()

        contact_grid.addWidget(self.addressLine1, 0, 2, 1, 4)
        contact_grid.addWidget(self.addressLine2, 1, 2, 1, 4)
        contact_grid.addWidget(self.city, 2, 2, 1, 4)
        contact_grid.addWidget(self.postalCode, 3, 2, 1, 4)
        contact_grid.addWidget(self.country, 4, 2, 1, 4)

        return contact_groupBox

    def security_section(self):

        questions_groupBox = QGroupBox("Security Question")
        questions_grid = QGridLayout()
        questions_groupBox.setLayout(questions_grid)

        self.question1 = QComboBox()
        self.question1.setMaximumWidth(300)
        self.answer2 = QLineEdit()
        self.question2 = QComboBox()
        self.question2.setMaximumWidth(300)
        self.answer1 = QLineEdit()

        questions = usql.query_all_questions()
        for i in questions:
            self.question1.addItem(str(i[0]))
            self.question2.addItem(str(i[0]))

        questions_grid.addWidget(Clabel('Question 1'), 0, 0, 1, 3)
        questions_grid.addWidget(Clabel('Answer 1'), 1, 0, 1, 3)
        questions_grid.addWidget(Clabel('Question 2'), 2, 0, 1, 3)
        questions_grid.addWidget(Clabel('Answer 2'), 3, 0, 1, 3)

        questions_grid.addWidget(self.question1, 0, 3, 1, 6)
        questions_grid.addWidget(self.answer1, 1, 3, 1, 6)
        questions_grid.addWidget(self.question2, 2, 3, 1, 6)
        questions_grid.addWidget(self.answer2, 3, 3, 1, 6)

        return questions_groupBox

    def buttons_section(self):
        btn_groupBox = QGroupBox()
        btn_grid = QGridLayout()
        btn_groupBox.setLayout(btn_grid)

        self.user_agree_checkBox = QCheckBox(mess.USER_CHECK_REQUIRED)
        btn_grid.addWidget(self.user_agree_checkBox, 0, 0, 1, 6)

        okBtn = QPushButton('Create Account')
        okBtn.clicked.connect(self.on_create_btn_clicked)
        btn_grid.addWidget(okBtn, 1, 0, 1, 2)

        cancelBtn = QPushButton('Cancel')
        cancelBtn.clicked.connect(self.on_cancel_btn_clicked)
        btn_grid.addWidget(cancelBtn, 1, 2, 1, 2)

        quitBtn = QPushButton('Quit')
        quitBtn.clicked.connect(QApplication.quit)
        btn_grid.addWidget(quitBtn, 1,4,1,2)

        return btn_groupBox

    def on_set_avatar_btn_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        imgsDir = os.path.join(os.getenv(__root__), 'avatar')
        self.rawAvatarPth, _ = QFileDialog.getOpenFileName(self, "Your Avatar", imgsDir, "All Files (*);;Img Files (*.jpg)",
                                                           options=options)
        if self.rawAvatarPth:
            self.userAvatar.setPixmap(QPixmap.fromImage(QImage(self.rawAvatarPth)))
            self.userAvatar.update()

    def on_create_btn_clicked(self):

        username = str(self.usernameField.text())
        password = str(self.passwordField.text())
        confirm = str(self.confirmPassField.text())
        firstname = str(self.firstnameField.text())
        lastname = str(self.lastnameField.text())
        email = str(self.emailField.text())
        phone = str(self.phoneField.text())
        address1 = str(self.addressLine1.text())
        address2 = str(self.addressLine2.text())
        postal = str(self.postalCode.text())
        city = str(self.city.text())
        country = str(self.country.text())
        answer1 = str(self.answer1.text())
        answer2 = str(self.answer2.text())

        reg = [username, password, confirm, firstname, lastname, email, phone, address1, address2, postal, city, country,
               answer1, answer2]

        if self.check_all_conditions(confirm, password, reg):

            data = self.create_user_data()

            usql.create_new_user_data(data)

    def create_user_data(self):

        username = str(self.usernameField.text())
        password = str(self.passwordField.text())
        firstname = str(self.firstnameField.text())
        lastname = str(self.lastnameField.text())
        email = str(self.emailField.text())
        phone = str(self.phoneField.text())
        address1 = str(self.addressLine1.text())
        address2 = str(self.addressLine2.text())
        postal = str(self.postalCode.text())
        city = str(self.city.text())
        country = str(self.country.text())
        question1 = str(self.question1.currentText())
        answer1 = str(self.answer1.text())
        question2 = str(self.question2.currentText())
        answer2 = str(self.answer2.text())
        title = str(self.titleField.text())
        token = func.get_token()
        timelog = func.get_time()
        sysInfo = func.get_local_pc()
        productID = sysInfo['Product ID']
        ip, cityIP, countryIP = func.get_pc_location()
        unix = func.get_unix()
        datelog = func.get_date()
        pcOS = sysInfo['os']
        pcUser = sysInfo['pcUser']
        pcPython = sysInfo['python']

        if not os.path.exists(self.rawAvatarPth):
            rawAvatarPth = func.get_avatar('default')
        else:
            rawAvatarPth = self.rawAvatarPth

        data = [username, password, firstname, lastname, title, email, phone, address1, address2, postal, city,
                    country, token, timelog, productID, ip, cityIP, countryIP, unix, question1, answer1, question2,
                    answer2, datelog, pcOS, pcUser, pcPython, rawAvatarPth]

        return data

    def on_cancel_btn_clicked(self):
        self.close()
        self.settings.setValue("showLogin", True)
        self.showLoginSig1.emit(True)

    def check_all_conditions(self, confirm, password, reg):

        if self.check_all_field_blank(reg):
            if self.check_pw_matching(confirm, password):
                if self.check_user_agreement():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def check_user_agreement(self):
        state = self.user_agree_checkBox.checkState()
        if not state:
            QMessageBox.critical(self, "Warning", mess.USER_NOT_CHECK, QMessageBox.Retry)
            return False
        else:
            return True

    def check_pw_matching(self, confirm, password):
        check_pass = func.check_match(password, confirm)
        if not check_pass:
            QMessageBox.critical(self, "Warning", mess.PW_UNMATCH, QMessageBox.Retry)
            return False
        else:
            return True

    def check_all_field_blank(self, reg):
        secName = ['Username', 'Password', 'Confirm Password', 'Firstname', 'Lastname', 'Email', 'Phone', 'Address line 1',
                   'Address line 2', 'Postal', 'City', 'Country', 'Answer 1', 'Answer 2']

        check = []

        for i in reg:
            if not func.check_blank(i):
                index = reg.index(i)
                QMessageBox.critical(self, "Warning", secName[index] + mess.SEC_BLANK, QMessageBox.Retry)
                check.append(secName[index])
                break
            else:
                continue

        if len(check) == 0:
            return True
        else:
            return False

    def check_password_matching(self, password, passretype):

        if not password == passretype:
            QMessageBox.critical(self, "Warning", mess.PW_UNMATCH, QMessageBox.Retry)
            return False
        else:
            return True

    def closeEvent(self, event):
        self.on_cancel_btn_clicked()

# -------------------------------------------------------------------------------------------------------------
""" Login Layout """

class Plt_sign_in(QDialog):

    def __init__(self, parent=None):

        super(Plt_sign_in, self).__init__(parent)

        # Sign in layout preset
        self.setWindowTitle('Sign in')
        self.setWindowIcon(QIcon(func.get_icon('Logo')))
        self.setFixedSize(400, 300)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
        self.signup = Plt_sign_up()
        showLoginSig1 = self.signup.showLoginSig1
        showLoginSig1.connect(self.show_hide_login)

        # Main layout
        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        login_groupBox = QGroupBox('Sign in')
        login_grid = QGridLayout()
        login_groupBox.setLayout(login_grid)

        self.usernameField = QLineEdit()
        self.passwordField = QLineEdit()
        self.rememberCheckBox = QCheckBox('Remember me.')
        self.passwordField.setEchoMode(QLineEdit.Password)

        forgot_pw_btn = QPushButton('Forgot your password?')
        forgot_pw_btn.clicked.connect(self.on_forgot_pw_btn_clicked)
        login_btn = QPushButton('Login')
        cancel_btn = QPushButton('Cancel')
        login_btn.clicked.connect(self.on_sign_in_btn_clicked)
        cancel_btn.clicked.connect(QApplication.quit)

        login_grid.addWidget(Clabel(text='Username'), 0, 0, 1, 2)
        login_grid.addWidget(Clabel(text='Password'), 1, 0, 1, 2)
        login_grid.addWidget(self.usernameField, 0, 2, 1, 4)
        login_grid.addWidget(self.passwordField, 1, 2, 1, 4)
        login_grid.addWidget(self.rememberCheckBox, 2, 1, 1, 2)
        login_grid.addWidget(login_btn, 2, 3, 1, 3)
        login_grid.addWidget(forgot_pw_btn, 3, 0, 1, 3)
        login_grid.addWidget(cancel_btn, 3, 3, 1, 3)

        signup_groupBox = QGroupBox('Sign up')
        signup_grid = QGridLayout()
        signup_groupBox.setLayout(signup_grid)

        sign_up_btn = QPushButton('Sign up')
        sign_up_btn.clicked.connect(self.on_sign_up_btn_clicked)

        signup_grid.addWidget(Clabel(text=mess.SIGN_UP), 0, 0, 1, 6)
        signup_grid.addWidget(sign_up_btn, 1, 0, 1, 6)

        self.layout.addWidget(login_groupBox, 0, 0, 1, 1)
        self.layout.addWidget(signup_groupBox, 1, 0, 1, 1)

    def show_hide_login(self, param):
        param = func.str2bool(param)
        if param:
            self.show()
        else:
            self.hide()

    def on_forgot_pw_btn_clicked(self):
        from ui import ui_pw_reset_form
        reset_pw_form = ui_pw_reset_form.Reset_password_form()
        reset_pw_form.show()
        reset_pw_form.exec_()

    def on_sign_up_btn_clicked(self):
        self.hide()
        self.signup.show()
        self.signup.exec_()

    def on_sign_in_btn_clicked(self):

        username = str(self.usernameField.text())
        pass_word = str(self.passwordField.text())

        if username == "" or username is None:
            QMessageBox.critical(self, 'Login Failed', mess.USER_BLANK)
            return
        elif pass_word == "" or pass_word is None:
            QMessageBox.critical(self, 'Login Failed', mess.PW_BLANK)
            return

        password = str(pass_word)

        r = requests.post("https://pipeline.damgteam.com/auth", verify=False,
                          data={'user': username, 'pwd': password})

        if r.status_code == 200:
            for i in r.headers['set-cookie'].split(";"):
                if 'connect.sid=' in i:
                    cookie = i.split('connect.sid=')[-1]

            token = r.json()['token']
            if func.str2bool(self.rememberCheckBox.checkState()):
                usql.update_user_token(username, token, cookie)
            else:
                usql.remove_data_table('userTokenLogin')

            self.hide()
            self.settings.setValue("showMain", True)

            window = Plt_application()
            showLoginSig2 = window.showLoginSig2
            showLoginSig2.connect(self.show_hide_login)
            window.show()
            if not QSystemTrayIcon.isSystemTrayAvailable():
                QMessageBox.critical(None, mess.SYSTRAY_UNAVAI)
                sys.exit(1)
        else:
            QMessageBox.critical(self, 'Login Failed', mess.PW_WRONG)
            return

    def closeEvent(self, event):
        QApplication.quit()

# -------------------------------------------------------------------------------------------------------------
""" Menu bar Layout """

class MenuBarLayout(QMainWindow):

    showTDSig2 = pyqtSignal(bool)
    showCompSig2 = pyqtSignal(bool)
    showArtSig2 = pyqtSignal(bool)

    def __init__(self, parent=None):

        super(MenuBarLayout, self).__init__(parent)

        self.appInfo = APPINFO
        self.mainID = var.PLT_ID
        self.message = var.PLT_MESS
        self.url = var.PLT_URL

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
        self.setFixedHeight(30)

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        self.createAction()

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.prefAct)
        self.fileMenu.addAction(self.separator1)
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = self.menuBar().addMenu("&View")
        self.viewMenu.addAction(self.viewTDAct)
        self.viewMenu.addAction(self.viewCompAct)
        self.viewMenu.addAction(self.viewArtAct)
        self.viewMenu.addAction(self.viewAllAct)

        self.toolMenu = self.menuBar().addMenu("&Tools")
        self.toolMenu.addAction(self.cleanAct)
        self.toolMenu.addAction(self.reconfigAct)

        self.aboutMenu = self.menuBar().addMenu("&About")
        self.aboutMenu.addAction(self.aboutAct)

        self.creditMenu = self.menuBar().addMenu("&Credit")
        self.creditMenu.addAction(self.creditAct)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.helpAct)

    def createAction(self):
        # Preferences
        self.prefAct = QAction(QIcon(func.get_icon('Preferences')), 'Preferences', self)
        self.prefAct.setStatusTip('Preferences')
        self.prefAct.triggered.connect(self.preferences_action_triggered)

        # Exit
        self.exitAct = QAction(QIcon(self.appInfo['Exit'][1]), self.appInfo['Exit'][0], self)
        self.exitAct.setStatusTip(self.appInfo['Exit'][0])
        self.exitAct.triggered.connect(self.exit_action_trigger)

        # View TD toolbar
        self.viewTDAct = QAction(QIcon(func.get_icon("")), "hide/view TD tool bar", self)
        viewTDToolBar = func.str2bool(self.settings.value("showTDToolbar", True))
        self.viewTDAct.setChecked(viewTDToolBar)
        self.viewTDAct.triggered.connect(self.show_hide_TDtoolBar)

        # View comp toolbar
        self.viewCompAct = QAction(QIcon(func.get_icon("")), "hide/view Comp tool bar", self)
        viewCompToolBar = func.str2bool(self.settings.value("showCompToolbar", True))

        # self.viewCompAct.setCheckable(True)
        self.viewCompAct.setChecked(viewCompToolBar)
        self.viewCompAct.triggered.connect(self.show_hide_ComptoolBar)

        # View art toolbar
        self.viewArtAct = QAction(QIcon(func.get_icon("")), "hide/view Art tool bar", self)
        viewArtToolBar = func.str2bool(self.settings.value("showArtToolbar", True))

        # self.viewArtAct.setCheckable(True)
        self.viewArtAct.setChecked(viewArtToolBar)
        self.viewArtAct.triggered.connect(self.show_hide_ArttoolBar)

        # View all toolbar
        self.viewAllAct = QAction(QIcon(func.get_icon("Alltoolbar")), "hide/view All tool bar", self)
        viewAllToolbar = func.str2bool(self.settings.value("showAllToolbar", True))

        # self.viewAllAct.setCheckable(True)
        self.viewAllAct.setChecked(viewAllToolbar)
        self.viewAllAct.triggered.connect(self.show_hide_AlltoolBar)

        # Clean trash file
        self.cleanAct = QAction(QIcon(self.appInfo['CleanPyc'][1]), self.appInfo['CleanPyc'][0], self)
        self.cleanAct.setStatusTip(self.appInfo['CleanPyc'][0])
        self.cleanAct.triggered.connect(partial(func.clean_unnecessary_file, '.pyc'))

        # Re-configuration
        self.reconfigAct = QAction(QIcon(self.appInfo['ReConfig'][1]), self.appInfo['ReConfig'][0], self)
        self.reconfigAct.setStatusTip(self.appInfo['ReConfig'][0])
        self.reconfigAct.triggered.connect(func.Collect_info)

        # About action
        self.aboutAct = QAction(QIcon(self.appInfo['About'][1]), self.appInfo['About'][0], self)
        self.aboutAct.setStatusTip(self.appInfo['About'][0])
        self.aboutAct.triggered.connect(partial(self.info_layout, self.mainID['About'], self.message['About'], self.appInfo['About'][1]))

        # Credit action
        self.creditAct = QAction(QIcon(self.appInfo['Credit'][1]), self.appInfo['Credit'][0], self)
        self.creditAct.setStatusTip(self.appInfo['Credit'][0])
        self.creditAct.triggered.connect(partial(self.info_layout, self.mainID['Credit'], self.message['Credit'], self.appInfo['Credit'][1]))

        # Help action
        self.helpAct = QAction(QIcon(self.appInfo['Help'][1]), self.appInfo['Help'][0], self)
        self.helpAct.setStatusTip((self.appInfo['Help'][0]))
        self.helpAct.triggered.connect(partial(webbrowser.open, self.url['Help']))

        # Seperator action
        self.separator1 = QAction(QIcon(self.appInfo['Sep'][0]), self.appInfo['Sep'][1], self)
        self.separator1.setSeparator(True)

    def preferences_action_triggered(self):
        dlg = ui_preference.Pref_layout()
        dlg.show()
        sigTD = dlg.checkboxTDSig
        sigComp = dlg.checkboxCompSig
        sigArt = dlg.checkboxArtSig
        sigTD.connect(self.show_hide_TDtoolBar)
        sigComp.connect(self.show_hide_ComptoolBar)
        sigArt.connect(self.show_hide_ArttoolBar)
        dlg.exec_()

    def exit_action_trigger(self):
        usql.insert_timeLog("Log out")
        logger.debug("LOG OUT")
        QApplication.instance().quit()

    def show_hide_TDtoolBar(self, param):
        self.showTDSig2.emit(param)

    def show_hide_ComptoolBar(self, param):
        self.showCompSig2.emit(param)

    def show_hide_ArttoolBar(self, param):
        self.showArtSig2.emit(param)

    def show_hide_AlltoolBar(self, param):
        self.show_hide_TDtoolBar(param)
        self.show_hide_ComptoolBar(param)
        self.show_hide_ArttoolBar(param)

    def info_layout(self, id='Note', message="", icon=func.get_icon('Logo')):
        from ui import ui_info_template
        dlg = ui_info_template.About_plt_layout(id=id, message=message, icon=icon)
        dlg.exec_()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        # menu.addAction(self.cutAct)
        # menu.addAction(self.copyAct)
        # menu.addAction(self.pasteAct)
        menu.exec_(event.globalPos())

# -------------------------------------------------------------------------------------------------------------
""" Slider Layout """

class SliderWidget(QWidget):

    valueChangeSig = pyqtSignal(float)

    def __init__(self, lab="slider", min=MIN, max=MAX, step=STEP, val=VAL, parent=None):
        super(SliderWidget, self).__init__(parent)

        self.min = min
        self.max = max
        self.step = step
        self.lab = lab
        self.val = val

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.label = Clabel(text=self.lab + ": ")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(int(self.min))
        self.slider.setMaximum(int(self.max))
        self.slider.setSingleStep(int(self.step))
        self.slider.setValue(int(self.val))

        self.numField = QLineEdit()
        self.numField.setValidator(QIntValidator(0, 999, self))
        self.numField.setText("0")
        self.numField.setFixedSize(30,20)
        self.numField.setText(str(self.val))

        self.slider.valueChanged.connect(self.set_value)
        self.numField.textChanged.connect(self.set_slider)

        self.layout.addWidget(self.label, 0, 0, 1, 1)
        self.layout.addWidget(self.numField, 0, 1, 1, 1)
        self.layout.addWidget(self.slider, 0, 2, 1, 1)

    def set_value(self):
        val = self.slider.value()
        self.numField.setText(str(val))

    def set_slider(self):
        val = self.numField.text()
        # Debug empty value making crash
        if val == "" or val == None:
            val = "0"
        self.slider.setValue(float(val))

    def changeEvent(self, event):
        self.settings.setValue("{name}Value".format(name=self.lab), float)
        self.valueChangeSig.emit(self.slider.value())

# -------------------------------------------------------------------------------------------------------------
""" Unit setting Layout """

class UnitSettingLayout(QWidget):

    stepChangeSig = pyqtSignal(float)
    valueChangeSig = pyqtSignal(float)
    minChangeSig = pyqtSignal(float)
    maxChangeSig = pyqtSignal(float)

    def __init__(self, parent=None):
        super(UnitSettingLayout, self).__init__(parent)

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.layout = QGridLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        self.stepVal = QLineEdit("1")
        self.valueVal = QLineEdit("1")
        self.minVal = QLineEdit("0")
        self.maxVal = QLineEdit("1000")

        self.stepVal.setValidator(QIntValidator(0, 999, self))
        self.valueVal.setValidator(QIntValidator(0, 999, self))
        self.minVal.setValidator(QIntValidator(0, 999, self))
        self.maxVal.setValidator(QIntValidator(0, 999, self))

        self.stepVal.textChanged.connect(self.set_step)
        self.valueVal.textChanged.connect(self.set_value)
        self.minVal.textChanged.connect(self.set_min)
        self.maxVal.textChanged.connect(self.set_max)

        self.layout.addWidget(Clabel("STEP: "), 0,0,1,1)
        self.layout.addWidget(Clabel("VALUE: "), 1,0,1,1)
        self.layout.addWidget(Clabel("MIN: "), 2,0,1,1)
        self.layout.addWidget(Clabel("MAX: "), 3,0,1,1)

        self.layout.addWidget(self.stepVal, 0, 1, 1, 1)
        self.layout.addWidget(self.valueVal, 1, 1, 1, 1)
        self.layout.addWidget(self.minVal, 2, 1, 1, 1)
        self.layout.addWidget(self.maxVal, 3, 1, 1, 1)

    def set_step(self):
        val = float(self.stepVal.text())
        self.stepChangeSig.emit(val)
        self.settings.setValue("stepSetting", float)

    def set_value(self):
        val = float(self.valueVal.text())
        self.valueChangeSig.emit(float(val))
        self.settings.setValue("valueSetting", float)

    def set_min(self):
        val = float(self.minVal.text())
        self.minChangeSig.emit(float(val))
        self.settings.setValue("minSetting", float)

    def set_max(self):
        val = float(self.maxVal.text())
        self.maxChangeSig.emit(float(val))
        self.settings.setValue("maxSetting", float)

    def changeEvent(self, event):
        pass

# -------------------------------------------------------------------------------------------------------------
""" Tab Layout """

class TabWidget(QWidget):

    dbConn = lite.connect(var.DB_PATH)
    showMainSig = pyqtSignal(bool)
    showLoginSig = pyqtSignal(bool)
    tabSizeSig = pyqtSignal(int, int)

    def __init__(self, username, package, parent=None):

        super(TabWidget, self).__init__(parent)

        self.username = username
        self.package = package

        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)

        self.layout = QVBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):
        # Create tab layout
        # ------------------------------------------------------
        self.tabs = QTabWidget()

        self.tab1Layout()
        self.tab2Layout()
        self.tab3Layout()
        self.tab4Layout()

        self.tabs.addTab(self.tab1, 'Tool')
        self.tabs.addTab(self.tab2, 'Prj')
        self.tabs.addTab(self.tab3, 'User')
        self.tabs.addTab(self.tab4, 'Lib')

        userClass = usql.query_userClass(self.username)

        if userClass == 'Administrator Privilege':
            self.tab5 = QGroupBox()
            self.tab5Layout()
            self.tabs.addTab(self.tab5, 'DB')

        self.layout.addWidget(self.tabs)

    def tab1Layout(self):

        self.tab1 = QWidget()
        tab1layout = QGridLayout()
        self.tab1.setLayout(tab1layout)

        tab1Sec1GrpBox = QGroupBox('Dev')
        tab1Sec1Grid = QGridLayout()
        tab1Sec1GrpBox.setLayout(tab1Sec1Grid)

        for key in APPINFO:
            if key == 'PyCharm':
                pycharmBtn = self.make_icon_btn2('PyCharm')
                tab1Sec1Grid.addWidget(pycharmBtn, 0, 0, 1, 1)
            if key == 'SublimeText 3':
                sublimeBtn = self.make_icon_btn2('SublimeText 3')
                tab1Sec1Grid.addWidget(sublimeBtn, 0, 1, 1, 1)
            if key == 'QtDesigner':
                qtdesignerBtn = self.make_icon_btn2('QtDesigner')
                tab1Sec1Grid.addWidget(qtdesignerBtn, 0, 2, 1, 1)

        tab1Sec2GrpBox = QGroupBox('CMD')
        tab1Sec2Grid = QGridLayout()
        tab1Sec2GrpBox.setLayout(tab1Sec2Grid)

        tab1Sec2Grid.addWidget(Clabel("Just for fun"), 0, 0, 1, 1)

        tab1Sec3GrpBox = QGroupBox('Custom')
        tab1Sec3Grid = QGridLayout()
        tab1Sec3GrpBox.setLayout(tab1Sec3Grid)

        arIconBtn = self.make_icon_btn2('Advance Renamer')
        noteReminderBtn = self.make_icon_btn1('QtNote', 'Note Reminder', self.note_reminder)
        textEditorBtn = self.make_icon_btn1('Text Editor', 'Text Editor', self.text_editor)
        dictBtn = self.make_icon_btn1('English Dictionary', 'English Dictionary', self.english_dictionary)
        screenshotBtn = self.make_icon_btn1('Screenshot', 'Screenshot', self.make_screen_shot)
        calendarBtn = self.make_icon_btn1('Calendar', 'Calendar', self.calendar)
        calculatorBtn = self.make_icon_btn1('Calculator', 'Calculator', self.calculator)
        fileFinderBtn = self.make_icon_btn1('Finder', 'Find files', self.findFiles)

        tab1Sec3Grid.addWidget(arIconBtn, 0, 0, 1, 1)
        tab1Sec3Grid.addWidget(noteReminderBtn, 0, 1, 1, 1)
        tab1Sec3Grid.addWidget(textEditorBtn, 0, 2, 1, 1)
        tab1Sec3Grid.addWidget(dictBtn, 1, 0, 1, 1)
        tab1Sec3Grid.addWidget(screenshotBtn, 1, 1, 1, 1)
        tab1Sec3Grid.addWidget(calendarBtn, 1, 2, 1, 1)
        tab1Sec3Grid.addWidget(calculatorBtn, 2, 0, 1, 1)
        tab1Sec3Grid.addWidget(fileFinderBtn, 2, 1, 1, 1)

        tab1Sec4GrpBox = QGroupBox('CGI')
        tab1Sec4Grid = QGridLayout()
        tab1Sec4GrpBox.setLayout(tab1Sec4Grid)

        for key in APPINFO:
            if key == 'Mudbox 2018':
                mudbox18Btn = self.make_icon_btn2(key)
                tab1Sec4Grid.addWidget(mudbox18Btn, 2, 0, 1, 1)
            if key == 'Mudbox 2017':
                mudbox17Btn = self.make_icon_btn2(key)
                tab1Sec4Grid.addWidget(mudbox17Btn, 2, 1, 1, 1)
            if key == '3ds Max 2018':
                max18Btn = self.make_icon_btn2(key)
                tab1Sec4Grid.addWidget(max18Btn, 2, 2, 1, 1)
            if key == '3ds Max 2017':
                max17Btn = self.make_icon_btn2(key)
                tab1Sec4Grid.addWidget(max17Btn, 3, 0, 1, 1)

        tab1layout.addWidget(tab1Sec1GrpBox, 0,0,1,3)
        tab1layout.addWidget(tab1Sec2GrpBox, 1,0,2,3)
        tab1layout.addWidget(tab1Sec3GrpBox, 0,3,3,3)
        tab1layout.addWidget(tab1Sec4GrpBox, 0,6,3,2)

    def tab2Layout(self):
        # Create Layout for Tab 2.
        self.tab2 = QWidget()
        tab2layout = QHBoxLayout()
        self.tab2.setLayout(tab2layout)

        tab2Section1GrpBox = QGroupBox('Proj')
        tab2Section1Grid = QGridLayout()
        tab2Section1GrpBox.setLayout(tab2Section1Grid)

        newProjBtn = QPushButton('New Project')
        newProjBtn.clicked.connect(self.on_newProjBtbn_clicked)
        newGrpBtn = QPushButton('New Group')
        newGrpBtn.clicked.connect(self.on_newGrpBtn_clicked)
        prjLstBtn = QPushButton('Your Projects')
        prjLstBtn.clicked.connect(self.on_prjLstBtn_clicked)

        tab2Section1Grid.addWidget(newProjBtn, 0, 0, 1, 2)
        tab2Section1Grid.addWidget(newGrpBtn, 1, 0, 1, 2)
        tab2Section1Grid.addWidget(prjLstBtn, 2, 0, 1, 2)

        tab2Section2GrpBox = QGroupBox('Crew')
        tab2Section2Grid = QGridLayout()
        tab2Section2GrpBox.setLayout(tab2Section2Grid)

        recruitBtn = QPushButton('Find crew')
        recruitBtn.clicked.connect(self.on_recruitBtn_clicked)
        getCrewBtn = QPushButton('Get crew')
        getCrewBtn.clicked.connect(self.on_getCrewBtn_clicked)
        crewLstBtn = QPushButton('Your crew')
        crewLstBtn.clicked.connect(self.on_crewLstBtn_clicked)
        tab2Section2Grid.addWidget(recruitBtn, 0, 0, 1, 2)
        tab2Section2Grid.addWidget(getCrewBtn, 1, 0, 1, 2)
        tab2Section2Grid.addWidget(crewLstBtn, 2, 0, 1, 2)

        tab2Section3GrpBox = QGroupBox('Com')
        tab2Section3Grid = QGridLayout()
        tab2Section3GrpBox.setLayout(tab2Section3Grid)

        tab2Section3Grid.addWidget(QLabel(""), 0, 0, 1, 2)

        tab2layout.addWidget(tab2Section1GrpBox)
        tab2layout.addWidget(tab2Section2GrpBox)
        tab2layout.addWidget(tab2Section3GrpBox)

    def tab3Layout(self):
        # Create Layout for Tab 3.
        self.tab3 = QWidget()
        tab3layout = QGridLayout()
        self.tab3.setLayout(tab3layout)

        tab3Sec1GrpBox = QGroupBox(self.username)
        tab3Sec1Grid = QGridLayout()
        tab3Sec1GrpBox.setLayout(tab3Sec1Grid)

        self.userAvatar = QLabel()
        self.userAvatar.setPixmap(QPixmap.fromImage(QImage(func.get_avatar(self.username))))
        self.userAvatar.setScaledContents(True)
        self.userAvatar.setFixedSize(100, 100)

        tab3Sec2GrpBox = QGroupBox("Account Setting")
        tab3Sec2Grid = QGridLayout()
        tab3Sec2GrpBox.setLayout(tab3Sec2Grid)

        userSettingBtn = QPushButton('Account Setting')
        userSettingBtn.clicked.connect(self.on_userSettingBtn_clicked)

        signOutBtn = QPushButton('Log Out')
        signOutBtn.clicked.connect(self.on_signOutBtn_clicked)

        tab3Sec1Grid.addWidget(self.userAvatar, 0, 0, 2, 3)
        tab3Sec2Grid.addWidget(userSettingBtn, 0, 2, 1, 5)
        tab3Sec2Grid.addWidget(signOutBtn, 1, 2, 1, 5)

        tab3layout.addWidget(tab3Sec1GrpBox)
        tab3layout.addWidget(tab3Sec2GrpBox)

    def tab4Layout(self):
        # Create Layout for Tab 4.
        self.tab4 = QWidget()
        tab4layout = QGridLayout()
        self.tab4.setLayout(tab4layout)

        tab4Section1GrpBox = QGroupBox('Library')
        tab4Section1Grid = QGridLayout()
        tab4Section1GrpBox.setLayout(tab4Section1Grid)

        tab4Section1Grid.addWidget(Clabel("Update later"), 0, 0, 1, 8)

        tab4layout.addWidget(tab4Section1GrpBox, 0, 0, 1, 8)

    def tab5Layout(self):
        # Create Layout for Tab 4
        tab5Widget = QWidget()
        tab5layout = QHBoxLayout()
        tab5Widget.setLayout(tab5layout)

        tab5Section1GrpBox = QGroupBox('Library')
        tab5Section1Grid = QGridLayout()
        tab5Section1GrpBox.setLayout(tab5Section1Grid)

        dataBrowserIconBtn = self.make_icon_btn2('Database Browser')
        tab5Section1Grid.addWidget(dataBrowserIconBtn, 0, 0, 1, 1)

        tab5layout.addWidget(tab5Section1GrpBox)
        return tab5Widget

    def update_avatar(self, param):
        self.userAvatar.setPixmap(QPixmap.fromImage(QImage(param)))
        self.userAvatar.update()

    def make_icon_btn1(self, iconName, tooltip, func_tool):
        icon = QIcon(func.get_icon(iconName))
        iconBtn = QPushButton()
        iconBtn.setToolTip(tooltip)
        iconBtn.setIcon(icon)
        iconBtn.setFixedSize(30, 30)
        iconBtn.setIconSize(QSize(30 - 3, 30 - 3))
        iconBtn.clicked.connect(func_tool)
        return iconBtn

    def make_icon_btn2(self, name):
        icon = QIcon(APPINFO[name][1])
        iconBtn = QPushButton()
        iconBtn.setToolTip(APPINFO[name][0])
        iconBtn.setIcon(icon)
        iconBtn.setFixedSize(30, 30)
        iconBtn.setIconSize(QSize(30 - 3, 30 - 3))
        iconBtn.clicked.connect(partial(subprocess.Popen, APPINFO[name][2]))
        return iconBtn

    def english_dictionary(self):
        from ui import ui_english_dict
        EngDict = ui_english_dict.EnglishDict()
        EngDict.exec_()

    def make_screen_shot(self):
        from ui import ui_screenshot
        dlg = ui_screenshot.Screenshot()
        dlg.exec_()

    def calendar(self):
        from ui import ui_calendar
        dlg = ui_calendar.Calendar()
        dlg.exec_()

    def calculator(self):
        from ui import ui_calculator
        dlg = ui_calculator.Calculator()
        dlg.exec_()

    def findFiles(self):
        from ui import ui_find_files
        dlg = ui_find_files.Findfiles()
        dlg.exec_()

    def note_reminder(self):
        from ui import ui_note_reminder
        window = ui_note_reminder.WindowDialog()
        window.exec_()

    def text_editor(self):
        from ui.textedit import textedit
        window = textedit.WindowDialog()
        window.exec_()

    def on_newProjBtbn_clicked(self):
        from ui import ui_new_project
        window = ui_new_project.NewProject()
        window.exec_()

    def on_newGrpBtn_clicked(self):
        pass

    def on_prjLstBtn_clicked(self):
        pass

    def on_recruitBtn_clicked(self):
        pass

    def on_getCrewBtn_clicked(self):
        pass

    def on_crewLstBtn_clicked(self):
        pass

    def on_userSettingBtn_clicked(self):
        user_setting_layout = ui_acc_setting.Account_setting()
        user_setting_layout.show()
        sig = user_setting_layout.changeAvatarSignal
        sig.connect(self.update_avatar)
        user_setting_layout.exec_()

    def on_signOutBtn_clicked(self):
        self.settings.setValue("showMain", False)
        self.showMainSig.emit(False)
        self.showLoginSig.emit(True)

# -------------------------------------------------------------------------------------------------------------
""" Pipeline Tool main layout """

class Plt_application(QMainWindow):

    showLoginSig2 = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(Plt_application, self).__init__(parent)

        self.username, rememberLogin = usql.query_curUser()
        self.mainID = var.PLT_ID
        self.appInfo = APPINFO
        self.package = var.PLT_PKG
        self.message = var.PLT_MESS
        self.url = var.PLT_URL

        self.setWindowTitle(self.mainID['Main'])
        self.setWindowIcon(QIcon(func.get_icon('Logo')))
        self.settings = QSettings(var.UI_SETTING, QSettings.IniFormat)
        self.setFixedWidth(400)

        self.trayIcon = self.sys_tray_icon_menu()
        self.trayIcon.setToolTip(__appname__)
        self.trayIcon.show()
        self.trayIcon.activated.connect(self.sys_tray_icon_activated)
        icon = QSystemTrayIcon.Information
        self.trayIcon.showMessage('Welcome', "Log in as %s" % self.username, icon, 500)

        self.mainWidget = QWidget()
        self.buildUI()
        self.setCentralWidget(self.mainWidget)

        # self.showMainUI = func.str2bool(self.settings.value("showMain", True))
        # self.show_hide_main(self.showMainUI)

        # self.layout_magrin_ratio()
        # self.layout_height_ratio()
        # self.layout_width_ratio()

        # self.restoreState(self.settings.value("layoutState", QBitArray()))

        # Log record
        # usql.insert_timeLog('Log in')

    def buildUI(self):

        sizeW, sizeH = self.get_layout_dimention()
        posX, posY, sizeW, sizeH = func.set_app_stick_to_bot_right(sizeW, sizeH)
        self.setGeometry(posX, posY, sizeW, sizeH)
        self.layout = QGridLayout()
        self.mainWidget.setLayout(self.layout)

        # Menubar build
        self.menuGrpBox = QGroupBox("Menu Layout")
        menuLayout = QHBoxLayout()
        self.menuGrpBox.setLayout(menuLayout)

        menuBar = MenuBarLayout()
        menuLayout.addWidget(menuBar)

        # ----------------------------------------------
        self.tdToolBar = self.toolBarTD()
        self.compToolBar = self.toolBarComp()
        self.artToolBar = self.toolBarArt()

        # Load Setting
        self.showTDToolBar = func.str2bool(self.settings.value("showTDToolbar", True))
        self.showCompToolBar = func.str2bool(self.settings.value("showCompToolbar", True))
        self.showArtToolBar = func.str2bool(self.settings.value("showArtToolbar", True))

        self.tdToolBar.setVisible(self.showTDToolBar)
        self.compToolBar.setVisible(self.showCompToolBar)
        self.artToolBar.setVisible(self.showArtToolBar)

        showTDSig = menuBar.showTDSig2
        showCompSig = menuBar.showCompSig2
        showArtSig = menuBar.showArtSig2
        showTDSig.connect(self.show_hide_TDtoolBar)
        showCompSig.connect(self.show_hide_ComptoolBar)
        showArtSig.connect(self.show_hide_ArttoolBar)

        # Status bar viewing message
        self.statusBar().showMessage(self.message['status'])

        # Top build
        self.topGrpBox = QGroupBox("Top Layout")
        topLayout = QHBoxLayout()
        self.topGrpBox.setLayout(topLayout)
        topLayout.addWidget(Clabel("This Layout is for drag and drop"))

        # Mid build
        self.midGrpBox = QGroupBox("plt Tool Box")
        midLayout = QHBoxLayout()
        self.midGrpBox.setLayout(midLayout)

        self.tabWidget = TabWidget(self.username, self.package)

        showMainSig = self.tabWidget.showMainSig
        showLoginSig = self.tabWidget.showLoginSig
        tabSizeSig = self.tabWidget.tabSizeSig
        showMainSig.connect(self.show_hide_main)
        showLoginSig.connect(self.send_to_login)
        tabSizeSig.connect(self.autoResize)
        midLayout.addWidget(self.tabWidget)

        # Bot build
        self.sizeGrpBox = QGroupBox("Size Setting")
        sizeGridLayout = QGridLayout()
        self.sizeGrpBox.setLayout(sizeGridLayout)

        unitSlider = SliderWidget(lab="UNIT", min=0, max=1000, step=1, val=UNIT)
        margSlider = SliderWidget(lab="MARG", min=0, max=1000, step=1, val=MARG)
        buffSlider = SliderWidget(lab="BUFF", min=0, max=1000, step=1, val=BUFF)
        scalSlider = SliderWidget(lab="SCAL", min=0, max=1000, step=1, val=SCAL)

        unitSig = unitSlider.valueChangeSig
        margSig = margSlider.valueChangeSig
        buffSig = buffSlider.valueChangeSig
        scalSig = scalSlider.valueChangeSig

        sizeGridLayout.addWidget(unitSlider, 0, 0, 1, 5)
        sizeGridLayout.addWidget(margSlider, 1, 0, 1, 5)
        sizeGridLayout.addWidget(buffSlider, 2, 0, 1, 5)
        sizeGridLayout.addWidget(scalSlider, 3, 0, 1, 5)

        # Bot build
        self.unitGrpBox = QGroupBox("Unit Setting")
        unitGridLayout = QGridLayout()
        self.unitGrpBox.setLayout(unitGridLayout)

        unitSetting = UnitSettingLayout()
        unitGridLayout.addWidget(unitSetting)

        # Add layout to main
        self.layout.addWidget(self.menuGrpBox, 1, 0, 1, 6)
        self.layout.addWidget(self.topGrpBox, 2, 0, 2, 6)
        self.layout.addWidget(self.midGrpBox, 4, 0, 4, 6)
        self.layout.addWidget(self.sizeGrpBox, 8, 0, 4, 3)
        self.layout.addWidget(self.unitGrpBox, 8, 3, 4, 3)

        # Restore last setting layout from user
        stateLayout = self.settings.value("layoutState", QByteArray().toBase64())
        try:
            self.restoreState(QByteArray(stateLayout))
        except IOError or TypeError:
            pass

    def sys_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()

    def sys_tray_icon_menu(self):
        trayIconMenu = QMenu(self)

        snippingAction = self.createAction(self.appInfo, 'Snipping Tool')
        trayIconMenu.addAction(snippingAction)

        screenshoticon = QIcon(func.get_icon('Screenshot'))
        screenshotAction = QAction(screenshoticon, "Screenshot", self)
        screenshotAction.triggered.connect(func.screenshot)
        trayIconMenu.addAction(screenshotAction)

        maximizeIcon = QIcon(func.get_icon("Maximize"))
        maximizeAction = QAction(maximizeIcon, "Maximize", self)
        maximizeAction.triggered.connect(self.showMaximized)
        trayIconMenu.addSeparator()
        trayIconMenu.addAction(maximizeAction)

        minimizeIcon = QIcon(func.get_icon('Minimize'))
        minimizeAction = QAction(minimizeIcon, "Minimize", self)
        minimizeAction.triggered.connect(self.hide)
        trayIconMenu.addAction(minimizeAction)

        restoreIcon = QIcon(func.get_icon('Restore'))
        restoreAction = QAction(restoreIcon, "Restore", self)
        restoreAction.triggered.connect(self.showNormal)
        trayIconMenu.addAction(restoreAction)

        quitIcon = QIcon(func.get_icon('Close'))
        quitAction = QAction(quitIcon, "Quit", self)
        quitAction.triggered.connect(self.exit_action_trigger)
        trayIconMenu.addSeparator()
        trayIconMenu.addAction(quitAction)

        trayIcon = QSystemTrayIcon(self)
        trayIcon.setIcon(QIcon(func.get_icon('Logo')))
        trayIcon.setContextMenu(trayIconMenu)

        return trayIcon

    def toolBarTD(self):
        # TD Tool Bar
        toolBarTD = self.addToolBar('TD')

        # Maya_tk 2017
        if 'Maya 2018' in self.appInfo:
            maya2017 = self.createAction(self.appInfo, 'Maya 2017')
            toolBarTD.addAction(maya2017)

        # Maya_tk 2017
        if 'Maya 2017' in self.appInfo:
            maya2017 = self.createAction(self.appInfo, 'Maya 2017')
            toolBarTD.addAction(maya2017)

        # ZBrush 4R8
        if 'ZBrush 4R8' in self.appInfo:
            zbrush4R8 = self.createAction(self.appInfo, 'ZBrush 4R8')
            toolBarTD.addAction(zbrush4R8)

        # ZBrush 4R7
        if 'ZBrush 4R7' in self.appInfo:
            zbrush4R7 = self.createAction(self.appInfo, 'ZBrush 4R7')
            toolBarTD.addAction(zbrush4R7)

        # Houdini FX
        if 'Houdini FX' in self.appInfo:
            houdiniFX = self.createAction(self.appInfo, 'Houdini FX')
            toolBarTD.addAction(houdiniFX)

        # Mari
        if 'Mari' in self.appInfo:
            mari = self.createAction(self.appInfo, 'Mari')
            toolBarTD.addAction(mari)

        # return Tool Bar
        return toolBarTD

    def toolBarComp(self):
        # VFX toolBar
        toolBarComp = self.addToolBar('VFX')
        # Davinci
        if 'Resolve' in self.appInfo:
            davinci = self.createAction(self.appInfo, 'Resolve')
            toolBarComp.addAction(davinci)
        # NukeX
        if 'NukeX' in self.appInfo:
            nukeX = self.createAction(self.appInfo, 'NukeX')
            toolBarComp.addAction(nukeX)
        # Hiero
        if 'Hiero' in self.appInfo:
            hiero = self.createAction(self.appInfo, 'Hiero')
            toolBarComp.addAction(hiero)
        # After Effect CC
        if 'After Effects CC' in self.appInfo:
            aeCC = self.createAction(self.appInfo, 'After Effects CC')
            toolBarComp.addAction(aeCC)
        # After Effect CS6
        if 'After Effects CS6' in self.appInfo:
            aeCS6 = self.createAction(self.appInfo, 'After Effects CS6')
            toolBarComp.addAction(aeCS6)
        # Premiere CC
        if 'Premiere Pro CC' in self.appInfo:
            prCC = self.createAction(self.appInfo, 'Premiere Pro CC')
            toolBarComp.addAction(prCC)
        # Premiere CS6
        if 'Premiere Pro CS6' in self.appInfo:
            prCS6 = self.createAction(self.appInfo, 'Premiere Pro CS6')
            toolBarComp.addAction(prCS6)
        # Return Tool Bar
        return toolBarComp

    def toolBarArt(self):
        toolbarArt = self.addToolBar('Art')
        if 'Photoshop CC' in self.appInfo:
            ptsCS6 = self.createAction(self.appInfo, 'Photoshop CC')
            toolbarArt.addAction(ptsCS6)
        # Photoshop CS6
        if 'Photoshop CS6' in self.appInfo:
            ptsCC = self.createAction(self.appInfo, 'Photoshop CS6')
            toolbarArt.addAction(ptsCC)
        # Illustrator CC
        if 'Illustrator CC' in self.appInfo:
            illusCC = self.createAction(self.appInfo, 'Illustrator CC')
            toolbarArt.addAction(illusCC)
        # Illustrator CS6
        if 'Illustrator CS6' in self.appInfo:
            illusCS6 = self.createActioin(self.appInfo, 'Illustrator CS6')
            toolbarArt.addAction(illusCS6)
        return toolbarArt

    def createAction(self, appInfo, key):
        action = QAction(QIcon(appInfo[key][1]), appInfo[key][0], self)
        action.setStatusTip(appInfo[key][0])
        action.triggered.connect (partial(subprocess.Popen, appInfo[key][2]))
        return action

    def createSeparatorAction(self):
        separator = QAction(QIcon(self.appInfo['Sep'][0]), self.appInfo['Sep'][1], self)
        separator.setSeparator(True)
        return separator

    def show_hide_TDtoolBar(self, param):
        self.settings.setValue("showTDToolbar", func.bool2str(param))
        self.tdToolBar.setVisible(func.str2bool(param))

    def show_hide_ComptoolBar(self, param):
        self.settings.setValue("showCompToolbar", func.bool2str(param))
        self.compToolBar.setVisible(func.str2bool(param))

    def show_hide_ArttoolBar(self, param):
        self.settings.setValue("showArtToolbar", func.bool2str(param))
        self.artToolBar.setVisible(func.str2bool(param))

    def show_hide_AlltoolBar(self, param):
        self.show_hide_TDtoolBar(param)
        self.show_hide_ComptoolBar(param)
        self.show_hide_ArttoolBar(param)

    def show_hide_main(self, param):
        param = func.str2bool(param)
        if not param:
            self.trayIcon.hide()
            self.close()
        else:
            self.trayIcon.show()
            self.show()

    def send_to_login(self, param):
        self.settings.setValue("showLogin", param)
        self.showLoginSig2.emit(param)

    def exit_action_trigger(self):
        usql.insert_timeLog("Log out")
        logger.debug("LOG OUT")
        QApplication.instance().quit()

    def set_app_position(self):
        pass

    def get_layout_dimention(self):
        sizeW = self.frameGeometry().width()
        sizeH = self.frameGeometry().height()
        return sizeW, sizeH

    def layout_magrin_ratio(self, margin = MARG):
        self.menuGrpBox.setContentsMargins(margin, margin, margin, margin)
        self.topGrpBox.setContentsMargins(margin, margin, margin, margin)
        self.midGrpBox.setContentsMargins(margin, margin, margin, margin)
        self.sizeGrpBox.setContentsMargins(margin, margin, margin, margin)
        return True

    def layout_height_ratio(self, baseH = UNIT):
        self.menuGrpBox.setFixedHeight(baseH)
        self.topGrpBox.setFixedHeight(baseH*2)
        self.midGrpBox.setFixedHeight(baseH*4)
        self.sizeGrpBox.setFixedHeight(baseH * 2)
        return True

    def layout_width_ratio(self, baseW = UNIT):
        self.menuGrpBox.setFixedWidth(baseW)
        self.topGrpBox.setFixedWidth(baseW)
        self.midGrpBox.setFixedWidth(baseW)
        self.sizeGrpBox.setFixedWidth(baseW)
        return True

    def autoResize(self, param):

        # print(param)
        pass

    def resizeEvent(self, event):
        sizeW, sizeH = self.get_layout_dimention()
        self.settings.setValue("appW", sizeW)
        self.settings.setValue("appH", sizeH)

    def windowState(self):
        self.settings.setValue("layoutState", self.saveState().data())

    def closeEvent(self, event):
        self.settings.setValue("layoutState", QByteArray(self.saveState().data()).toBase64())
        icon = QSystemTrayIcon.Information
        self.trayIcon.showMessage('Notice', "Pipeline Tool will keep running in the system tray.", icon, 1000)
        self.hide()
        event.ignore()

# -------------------------------------------------------------------------------------------------------------
""" Operation """

def main():

    usql.query_userData()

    QCoreApplication.setApplicationName(__appname__)
    QCoreApplication.setApplicationVersion(__version__)
    QCoreApplication.setOrganizationName(__organization__)
    QCoreApplication.setOrganizationDomain(__website__)

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(func.get_icon('Logo')))
    app.setStyleSheet(qdarkgraystyle.load_stylesheet_pyqt5())

    username, token, cookie = usql.query_user_session()

    if username is None or token is None or cookie is None:
        login = Plt_sign_in()
        login.show()
    else:
        r = requests.get("https://pipeline.damgteam.com/check", verify = False,
                     headers={'Authorization': 'Bearer {token}'.format(token=token)},
                     cookies={'connect.sid': cookie})

        if r.status_code == 200:
            window = Plt_application()
            window.show()
            if not QSystemTrayIcon.isSystemTrayAvailable():
                QMessageBox.critical(None, mess.SYSTRAY_UNAVAI)
                sys.exit(1)
        else:
            login = Plt_sign_in()
            login.show()

    QApplication.setQuitOnLastWindowClosed(False)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

# ----------------------------------------------------------------------------