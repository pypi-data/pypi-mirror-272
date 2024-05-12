# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QMainWindow, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(502, 370)
        MainWindow.setMinimumSize(QSize(502, 370))
        MainWindow.setMaximumSize(QSize(502, 372))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralVerticalLayout = QVBoxLayout(self.centralwidget)
        self.centralVerticalLayout.setObjectName(u"centralVerticalLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_1_welcome = QWidget()
        self.page_1_welcome.setObjectName(u"page_1_welcome")
        self.verticalLayout_2 = QVBoxLayout(self.page_1_welcome)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.page_1_welcome)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_2.addWidget(self.label)

        self.line_2 = QFrame(self.page_1_welcome)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_2)

        self.label_3 = QLabel(self.page_1_welcome)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.line_3 = QFrame(self.page_1_welcome)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_3)

        self.label_4 = QLabel(self.page_1_welcome)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.stackedWidget.addWidget(self.page_1_welcome)
        self.page_2_programs = QWidget()
        self.page_2_programs.setObjectName(u"page_2_programs")
        self.verticalLayout = QVBoxLayout(self.page_2_programs)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.programsTitle = QLabel(self.page_2_programs)
        self.programsTitle.setObjectName(u"programsTitle")

        self.verticalLayout.addWidget(self.programsTitle)

        self.installBrave = QCheckBox(self.page_2_programs)
        self.installBrave.setObjectName(u"installBrave")
        self.installBrave.setChecked(False)

        self.verticalLayout.addWidget(self.installBrave)

        self.installChrome = QCheckBox(self.page_2_programs)
        self.installChrome.setObjectName(u"installChrome")

        self.verticalLayout.addWidget(self.installChrome)

        self.installVsCode = QCheckBox(self.page_2_programs)
        self.installVsCode.setObjectName(u"installVsCode")
        self.installVsCode.setChecked(False)

        self.verticalLayout.addWidget(self.installVsCode)

        self.installAudacity = QCheckBox(self.page_2_programs)
        self.installAudacity.setObjectName(u"installAudacity")
        self.installAudacity.setChecked(False)

        self.verticalLayout.addWidget(self.installAudacity)

        self.installDiscord = QCheckBox(self.page_2_programs)
        self.installDiscord.setObjectName(u"installDiscord")
        self.installDiscord.setChecked(False)

        self.verticalLayout.addWidget(self.installDiscord)

        self.installVlc = QCheckBox(self.page_2_programs)
        self.installVlc.setObjectName(u"installVlc")
        self.installVlc.setChecked(False)

        self.verticalLayout.addWidget(self.installVlc)

        self.installSteam = QCheckBox(self.page_2_programs)
        self.installSteam.setObjectName(u"installSteam")
        self.installSteam.setChecked(False)

        self.verticalLayout.addWidget(self.installSteam)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_6)

        self.stackedWidget.addWidget(self.page_2_programs)
        self.page_3_more = QWidget()
        self.page_3_more.setObjectName(u"page_3_more")
        self.verticalLayout_3 = QVBoxLayout(self.page_3_more)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.toolsTitle = QLabel(self.page_3_more)
        self.toolsTitle.setObjectName(u"toolsTitle")

        self.verticalLayout_3.addWidget(self.toolsTitle)

        self.installGnomeConsole = QCheckBox(self.page_3_more)
        self.installGnomeConsole.setObjectName(u"installGnomeConsole")

        self.verticalLayout_3.addWidget(self.installGnomeConsole)

        self.installGnomeTweaks = QCheckBox(self.page_3_more)
        self.installGnomeTweaks.setObjectName(u"installGnomeTweaks")

        self.verticalLayout_3.addWidget(self.installGnomeTweaks)

        self.installDconfEditor = QCheckBox(self.page_3_more)
        self.installDconfEditor.setObjectName(u"installDconfEditor")

        self.verticalLayout_3.addWidget(self.installDconfEditor)

        self.installExtensionManager = QCheckBox(self.page_3_more)
        self.installExtensionManager.setObjectName(u"installExtensionManager")

        self.verticalLayout_3.addWidget(self.installExtensionManager)

        self.installVirtualBox = QCheckBox(self.page_3_more)
        self.installVirtualBox.setObjectName(u"installVirtualBox")

        self.verticalLayout_3.addWidget(self.installVirtualBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.stackedWidget.addWidget(self.page_3_more)
        self.page_4_extensions = QWidget()
        self.page_4_extensions.setObjectName(u"page_4_extensions")
        self.verticalLayout_4 = QVBoxLayout(self.page_4_extensions)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.extensionsTitle = QLabel(self.page_4_extensions)
        self.extensionsTitle.setObjectName(u"extensionsTitle")

        self.verticalLayout_4.addWidget(self.extensionsTitle)

        self.setupDock = QCheckBox(self.page_4_extensions)
        self.setupDock.setObjectName(u"setupDock")

        self.verticalLayout_4.addWidget(self.setupDock)

        self.infoDock = QLabel(self.page_4_extensions)
        self.infoDock.setObjectName(u"infoDock")

        self.verticalLayout_4.addWidget(self.infoDock)

        self.setupOverview = QCheckBox(self.page_4_extensions)
        self.setupOverview.setObjectName(u"setupOverview")

        self.verticalLayout_4.addWidget(self.setupOverview)

        self.infoOverview = QLabel(self.page_4_extensions)
        self.infoOverview.setObjectName(u"infoOverview")

        self.verticalLayout_4.addWidget(self.infoOverview)

        self.setupSmallTweaks = QCheckBox(self.page_4_extensions)
        self.setupSmallTweaks.setObjectName(u"setupSmallTweaks")

        self.verticalLayout_4.addWidget(self.setupSmallTweaks)

        self.infoJustPerfection = QLabel(self.page_4_extensions)
        self.infoJustPerfection.setObjectName(u"infoJustPerfection")

        self.verticalLayout_4.addWidget(self.infoJustPerfection)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.stackedWidget.addWidget(self.page_4_extensions)
        self.page_5_config = QWidget()
        self.page_5_config.setObjectName(u"page_5_config")
        self.verticalLayout_5 = QVBoxLayout(self.page_5_config)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.configTitle = QLabel(self.page_5_config)
        self.configTitle.setObjectName(u"configTitle")

        self.verticalLayout_5.addWidget(self.configTitle)

        self.dynamicTouchpad = QCheckBox(self.page_5_config)
        self.dynamicTouchpad.setObjectName(u"dynamicTouchpad")

        self.verticalLayout_5.addWidget(self.dynamicTouchpad)

        self.detachModals = QCheckBox(self.page_5_config)
        self.detachModals.setObjectName(u"detachModals")

        self.verticalLayout_5.addWidget(self.detachModals)

        self.flatMouseProfile = QCheckBox(self.page_5_config)
        self.flatMouseProfile.setObjectName(u"flatMouseProfile")

        self.verticalLayout_5.addWidget(self.flatMouseProfile)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)

        self.stackedWidget.addWidget(self.page_5_config)
        self.page_6_key_shorts = QWidget()
        self.page_6_key_shorts.setObjectName(u"page_6_key_shorts")
        self.verticalLayout_6 = QVBoxLayout(self.page_6_key_shorts)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.shortsTitle = QLabel(self.page_6_key_shorts)
        self.shortsTitle.setObjectName(u"shortsTitle")

        self.verticalLayout_6.addWidget(self.shortsTitle)

        self.shortcutNautilus = QCheckBox(self.page_6_key_shorts)
        self.shortcutNautilus.setObjectName(u"shortcutNautilus")

        self.verticalLayout_6.addWidget(self.shortcutNautilus)

        self.shortcutSysMon = QCheckBox(self.page_6_key_shorts)
        self.shortcutSysMon.setObjectName(u"shortcutSysMon")

        self.verticalLayout_6.addWidget(self.shortcutSysMon)

        self.shortcutMinimize = QCheckBox(self.page_6_key_shorts)
        self.shortcutMinimize.setObjectName(u"shortcutMinimize")

        self.verticalLayout_6.addWidget(self.shortcutMinimize)

        self.shortcutWorkspaceSwitch = QCheckBox(self.page_6_key_shorts)
        self.shortcutWorkspaceSwitch.setObjectName(u"shortcutWorkspaceSwitch")

        self.verticalLayout_6.addWidget(self.shortcutWorkspaceSwitch)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_5)

        self.stackedWidget.addWidget(self.page_6_key_shorts)
        self.page_7_ext_install = QWidget()
        self.page_7_ext_install.setObjectName(u"page_7_ext_install")
        self.verticalLayout_8 = QVBoxLayout(self.page_7_ext_install)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_6 = QLabel(self.page_7_ext_install)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_8.addWidget(self.label_6)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gnome4xButton = QPushButton(self.page_7_ext_install)
        self.gnome4xButton.setObjectName(u"gnome4xButton")

        self.horizontalLayout_2.addWidget(self.gnome4xButton)

        self.gnome4xLabel = QLabel(self.page_7_ext_install)
        self.gnome4xLabel.setObjectName(u"gnome4xLabel")

        self.horizontalLayout_2.addWidget(self.gnome4xLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_8.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.justPerfectionButton = QPushButton(self.page_7_ext_install)
        self.justPerfectionButton.setObjectName(u"justPerfectionButton")

        self.horizontalLayout_3.addWidget(self.justPerfectionButton)

        self.justPerfectionLabel = QLabel(self.page_7_ext_install)
        self.justPerfectionLabel.setObjectName(u"justPerfectionLabel")

        self.horizontalLayout_3.addWidget(self.justPerfectionLabel)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout_8.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_8 = QSpacerItem(20, 71, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_8)

        self.stackedWidget.addWidget(self.page_7_ext_install)
        self.page_8_finishing = QWidget()
        self.page_8_finishing.setObjectName(u"page_8_finishing")
        self.verticalLayout_7 = QVBoxLayout(self.page_8_finishing)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.applyTitle = QLabel(self.page_8_finishing)
        self.applyTitle.setObjectName(u"applyTitle")

        self.verticalLayout_7.addWidget(self.applyTitle)

        self.line_4 = QFrame(self.page_8_finishing)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_7.addWidget(self.line_4)

        self.progressBar = QProgressBar(self.page_8_finishing)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMaximum(0)
        self.progressBar.setValue(-1)
        self.progressBar.setTextVisible(False)

        self.verticalLayout_7.addWidget(self.progressBar)

        self.progressBarLabel = QLabel(self.page_8_finishing)
        self.progressBarLabel.setObjectName(u"progressBarLabel")

        self.verticalLayout_7.addWidget(self.progressBarLabel)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_7)

        self.stackedWidget.addWidget(self.page_8_finishing)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_9 = QVBoxLayout(self.page)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.finishLabel = QLabel(self.page)
        self.finishLabel.setObjectName(u"finishLabel")

        self.verticalLayout_9.addWidget(self.finishLabel)

        self.stackedWidget.addWidget(self.page)

        self.centralVerticalLayout.addWidget(self.stackedWidget)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.centralVerticalLayout.addWidget(self.line)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.exitButton = QPushButton(self.centralwidget)
        self.exitButton.setObjectName(u"exitButton")

        self.horizontalLayout.addWidget(self.exitButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.backButton = QPushButton(self.centralwidget)
        self.backButton.setObjectName(u"backButton")

        self.horizontalLayout.addWidget(self.backButton)

        self.nextButton = QPushButton(self.centralwidget)
        self.nextButton.setObjectName(u"nextButton")

        self.horizontalLayout.addWidget(self.nextButton)


        self.centralVerticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(False)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(7)
        self.nextButton.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Ubuntu Post Install Setup", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">Welcome to Ubuntu Post Install Setup</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Requirements:</span></p><p>- Fresh Ubuntu 23.10 Default (not full) install<br/>(it might not work as expected on other versions)</p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Disclaimer:</span></p><p>- I'm not responsible for bricked devices, dead SD cards,<br/>thermonuclear war, or you getting fired because<br/>the alarm app failed.</p><p>- YOU are choosing to make these modifications, and if you point your<br/>finger at me for messing up your device, I will laugh at you.</p></body></html>", None))
        self.programsTitle.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">General programs<br/></span>Choose what programs to install</p></body></html>", None))
        self.installBrave.setText(QCoreApplication.translate("MainWindow", u"Brave Browser", None))
        self.installChrome.setText(QCoreApplication.translate("MainWindow", u"Google Chrome", None))
        self.installVsCode.setText(QCoreApplication.translate("MainWindow", u"Visual Studio Code", None))
        self.installAudacity.setText(QCoreApplication.translate("MainWindow", u"Audacity", None))
        self.installDiscord.setText(QCoreApplication.translate("MainWindow", u"Discord", None))
        self.installVlc.setText(QCoreApplication.translate("MainWindow", u"VLC", None))
        self.installSteam.setText(QCoreApplication.translate("MainWindow", u"Steam", None))
        self.toolsTitle.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Tools<br/></span>Choose what tools to install</p></body></html>", None))
        self.installGnomeConsole.setText(QCoreApplication.translate("MainWindow", u"GNOME Console (remove GNOME Terminal)", None))
        self.installGnomeTweaks.setText(QCoreApplication.translate("MainWindow", u"GNOME Tweaks", None))
        self.installDconfEditor.setText(QCoreApplication.translate("MainWindow", u"dconf Editor", None))
        self.installExtensionManager.setText(QCoreApplication.translate("MainWindow", u"GNOME Extension Manager", None))
        self.installVirtualBox.setText(QCoreApplication.translate("MainWindow", u"VirtualBox", None))
        self.extensionsTitle.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">UI modifications<br/></span>Choose which UI modifications to apply</p></body></html>", None))
        self.setupDock.setText(QCoreApplication.translate("MainWindow", u"Dock instead of side panel", None))
        self.infoDock.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>INFO: Removes the side panel on the left side, instead shows<br/>an autohiding macOS-like Dock at the bottom.</p></body></html>", None))
        self.setupOverview.setText(QCoreApplication.translate("MainWindow", u"Improve Overview", None))
        self.infoOverview.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>INFO: Makes workspace thumbnails bigger, shows wallpaper<br/>on them and makes them visible even when only one<br/>workspace is used.</p></body></html>", None))
        self.setupSmallTweaks.setText(QCoreApplication.translate("MainWindow", u"Smaller tweaks", None))
        self.infoJustPerfection.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>INFO: Moves volume OSD to the top, disables buggy<br/>workspace indicator when switching, removes Alt+Tab delay.</p></body></html>", None))
        self.configTitle.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Various tweaks<br/></span>Choose which settings to apply</p></body></html>", None))
        self.dynamicTouchpad.setText(QCoreApplication.translate("MainWindow", u"Disable touchpad on external mouse", None))
        self.detachModals.setText(QCoreApplication.translate("MainWindow", u"Let modal dialogs be moved freely", None))
        self.flatMouseProfile.setText(QCoreApplication.translate("MainWindow", u"Flat mouse profile", None))
        self.shortsTitle.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Keyboard shortcuts<br/></span>Choose which Windows keyboard shortcuts you want to enable</p></body></html>", None))
        self.shortcutNautilus.setText(QCoreApplication.translate("MainWindow", u"Win+E - file explorer", None))
        self.shortcutSysMon.setText(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+Esc - System Monitor", None))
        self.shortcutMinimize.setText(QCoreApplication.translate("MainWindow", u"Win+D - Minimize window", None))
        self.shortcutWorkspaceSwitch.setText(QCoreApplication.translate("MainWindow", u"Ctrl+Win+Left/Right - Switch workspaces", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Installing Extensions<br/></span>The following extensions need to be installed for<br/>the selected modifications to work.<br/><br/>All you have to do is click install,<br/>and in the popup click install againt<br/><br/>NOTE: If you don't see anything below, you can click next.</p></body></html>", None))
        self.gnome4xButton.setText(QCoreApplication.translate("MainWindow", u"Install", None))
        self.gnome4xLabel.setText(QCoreApplication.translate("MainWindow", u"GNOME 4x UI Improvements", None))
        self.justPerfectionButton.setText(QCoreApplication.translate("MainWindow", u"Install", None))
        self.justPerfectionLabel.setText(QCoreApplication.translate("MainWindow", u"Just Perfection", None))
        self.applyTitle.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">Applying selected changes<br/><br/></span>Performing modifications in the background...<br/>Please be patient!</p></body></html>", None))
        self.progressBarLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><br/></p></body></html>", None))
        self.finishLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">We are all done<br/><br/></span>Click Finish to exit the program</p></body></html>", None))
        self.exitButton.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.backButton.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.nextButton.setText(QCoreApplication.translate("MainWindow", u"Next", None))
    # retranslateUi
