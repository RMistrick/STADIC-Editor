"""
This is a stadic script by Ling
 """


from PyQt4 import QtCore, QtGui
import sys, os
import json
import shutil
import time
from extractimg import *
import copy
import subprocess

##PyQt initialization

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)



##Main Window Gui Layout and Design
class Ui_FormSTADIC(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.imported=False
        self.created=False
        self.simchecked=False
        self.warning=True
        # self.lumlayout=False
        self.fimport=False
        self.owd=os.getcwd()
        self.jfimported=False

    def setupUi(self, FormSTADIC):

        ##Base Frame and Tab Widget
        FormSTADIC.resize(1400, 800)
        FormSTADIC.setWindowTitle(_translate("FormSTADIC", "STADIC1.1", None))
        FormSTADIC.setWindowIcon(QtGui.QIcon("PennState.png"))
        self.FormHLayout = QtGui.QHBoxLayout()
        self.setLayout(self.FormHLayout)
        VLayout = QtGui.QVBoxLayout()
        self.FormHLayout.addLayout(VLayout)
        self.STADICMark = QtGui.QLabel(FormSTADIC)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Impact"))
        font.setPointSize(24)
        self.STADICMark.setFont(font)
        self.STADICMark.setAutoFillBackground(False)
        self.STADICMark.setTextFormat(QtCore.Qt.LogText)
        self.STADICMark.setText(_translate("FormSTADIC", "STADIC", None))
        self.FormHLayout.addWidget(self.STADICMark)
        VLayout.addWidget(self.STADICMark)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        VLayout.addItem(spacerItem)
        self.SaveBtn = QtGui.QPushButton("Save")
        VLayout.addWidget(self.SaveBtn)
        self.SaveBtn.clicked.connect(self.SaveAll)
        self.SaveAsBtn = QtGui.QPushButton("Save As")
        VLayout.addWidget(self.SaveAsBtn)
        self.SaveAsBtn.clicked.connect(self.SaveAs)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        VLayout.addItem(spacerItem)
        self.StadicTab = QtGui.QTabWidget(FormSTADIC)
        self.FormHLayout.addWidget(self.StadicTab)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.StadicTab.setFont(font)
        self.StadicTab.setMovable(False)



        ## Tab1: File
        self.TabFile = QtGui.QWidget(self.StadicTab)
        self.StadicTab.addTab(self.TabFile, _fromUtf8("FILE"))
        self.StadicTab.setTabToolTip(self.StadicTab.indexOf(self.TabFile),"Project File Information")
        HLayout = QtGui.QHBoxLayout(self.TabFile)
        Scroll=QtGui.QScrollArea()
        Scroll.setWidgetResizable(1)
        HLayout.addWidget(Scroll)
        AreaContents=QtGui.QWidget()
        AreaContents.setGeometry(QtCore.QRect(0,0,1400,600))
        Grid2= QtGui.QGridLayout(AreaContents)
        Scroll.setWidget(AreaContents)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 1, 0, 1, 1)
        FLbl = QtGui.QLabel(self.TabFile)
        Grid2.addWidget(FLbl, 1, 1, 1, 1)
        FLbl.setText(_translate("FormSTADIC", "JSON File:", None))
        self.TabFileJFLineEd = QtGui.QLineEdit(self.TabFile)
        Grid2.addWidget(self.TabFileJFLineEd, 1, 2, 1, 1)
        self.TabFileJFLineEd.setReadOnly(1)
        self.TabFileJFBtn = QtGui.QPushButton("Browse")
        Grid2.addWidget(self.TabFileJFBtn, 1, 3, 1, 1)
        self.TabFileJFBtn.clicked.connect(self.JFBtn)
        self.TabFileJFCrtBtn = QtGui.QPushButton("Create")
        Grid2.addWidget(self.TabFileJFCrtBtn, 1, 4, 1, 1)
        self.TabFileJFCrtBtn.clicked.connect(self.JFCrtBtn)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 1, 5, 1, 1)
        FLbl = QtGui.QLabel(self.TabFile)
        Grid2.addWidget(FLbl, 2, 1, 1, 1)
        FLbl.setText(_translate("FormSTADIC", "Import Dimensions:", None))
        self.TabFileDUnitComBox = QtGui.QComboBox(self.TabFile)
        Units=["Inches", "Feet", "Meters", "Millimeters"]
        self.TabFileDUnitComBox.addItems(Units)
        Grid2.addWidget(self.TabFileDUnitComBox, 2, 2, 1, 1)
        self.TabFileDUnitComBox.setCurrentIndex(-1)
        FLbl = QtGui.QLabel(self.TabFile)
        Grid2.addWidget(FLbl, 3, 1, 1, 1)
        FLbl.setText(_translate("FormSTADIC", "Display Dimensions:", None))
        self.TabFileDDUnitComBox = QtGui.QComboBox(self.TabFile)
        self.TabFileDDUnitComBox.addItems(Units)
        self.TabFileDDUnitComBox.setCurrentIndex(-1)
        Grid2.addWidget(self.TabFileDDUnitComBox, 3, 2, 1, 1)
        FLbl = QtGui.QLabel(self.TabFile)
        Grid2.addWidget(FLbl, 4, 1, 1, 1)
        FLbl.setText(_translate("FormSTADIC", "Lighting Units:", None))
        self.TabFileLUnitsComBox = QtGui.QComboBox(self.TabFile)
        self.TabFileLUnitsComBox.addItems(["lux", "fc"])
        Grid2.addWidget(self.TabFileLUnitsComBox, 4, 2, 1, 1)
        self.TabFileLUnitsComBox.setCurrentIndex(-1)
        FLbl=QtGui.QLabel(self.TabFile)
        Grid2.addWidget(FLbl, 5, 1, 1, 1)
        FLbl.setText("Directory:")
        self.TabFileDirLineEd=QtGui.QLineEdit(self.TabFile)
        Grid2.addWidget(self.TabFileDirLineEd, 5, 2, 1, 1)
        self.TabFileDirLineEd.setReadOnly(1)
        self.TabFileDirBtn=QtGui.QPushButton("Set")
        Grid2.addWidget(self.TabFileDirBtn, 5, 3, 1, 1)
        self.TabFileDirBtn.clicked.connect(self.FileDir)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        Grid2.addItem(spacerItem, 6, 2, 1, 1)


        ## Tab2: Site
        self.TabSite = QtGui.QWidget(self.StadicTab)
        self.StadicTab.addTab(self.TabSite, _fromUtf8("SITE"))
        self.StadicTab.setTabToolTip(self.StadicTab.indexOf(self.TabSite),"Weather File Information")
        HLayout = QtGui.QHBoxLayout(self.TabSite)
        Scroll=QtGui.QScrollArea()
        Scroll.setWidgetResizable(1)
        HLayout.addWidget(Scroll)
        AreaContents=QtGui.QWidget()
        AreaContents.setGeometry(QtCore.QRect(0,0,1400,600))
        Grid2= QtGui.QGridLayout(AreaContents)
        Scroll.setWidget(AreaContents)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 1, 0, 1, 1)
        SLbl = QtGui.QLabel(self.TabSite)
        Grid2.addWidget(SLbl, 1, 1, 1, 1)
        SLbl.setText(_translate("FormSTADIC", "Weather File:", None))
        SLbl.setFixedWidth(180)
        self.TabSiteWeaLineEd = QtGui.QLineEdit(self.TabSite)
        Grid2.addWidget(self.TabSiteWeaLineEd, 1, 2, 1, 1)
        self.TabSiteWeaLineEd.setReadOnly(1)
        spacerItem = QtGui.QSpacerItem(5, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 1, 3, 1, 1)
        self.TabSiteWeaBtn = QtGui.QPushButton(self.TabSite)
        Grid2.addWidget(self.TabSiteWeaBtn, 1, 4, 1, 1)
        self.TabSiteWeaBtn.setText("Import")
        self.TabSiteWeaBtn.clicked.connect(self.WeaFile)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 1, 5, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 2, 1, 1, 1)
        SLbl=QtGui.QLabel(self.TabSite)
        Grid2.addWidget(SLbl, 3, 1, 1, 1)
        SLbl.setText(_translate("FormSTADIC","Daylight Savings:", None))
        self.TabSiteDaySChk=QtGui.QCheckBox(self.TabSite)
        Grid2.addWidget(self.TabSiteDaySChk, 3, 2, 1, 1)
        self.TabSiteDaySChk.stateChanged.connect(self.DayS)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 4, 1, 1, 1)
        SLbl=QtGui.QLabel(self.TabSite)
        Grid2.addWidget(SLbl, 5, 1, 1, 1)
        SLbl.setText(_translate("FormSTADIC", "Ground Reflectance:", None))
        self.TabSiteGrdReflLineEd=QtGui.QLineEdit(self.TabSite)
        Grid2.addWidget(self.TabSiteGrdReflLineEd, 5, 2, 1, 1)
        self.TabSiteGrdReflLineEd.setFixedWidth(100)
        site=lambda: self.SiteData(self.TabSiteGrdReflLineEd,"ground_reflectance")
        self.TabSiteGrdReflLineEd.editingFinished.connect(site)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 6, 1, 1, 1)
        SLbl = QtGui.QLabel(self.TabSite)
        Grid2.addWidget(SLbl, 7, 1, 1, 1)
        SLbl.setText(_translate("FormSTADIC", "Building Rotation:", None))
        self.TabSiteBldgRotLineEd = QtGui.QLineEdit(self.TabSite)
        self.TabSiteBldgRotLineEd.setFixedWidth(100)
        Grid2.addWidget(self.TabSiteBldgRotLineEd, 7, 2, 1, 1)
        site=lambda: self.SiteData(self.TabSiteBldgRotLineEd,"building_rotation")
        self.TabSiteBldgRotLineEd.editingFinished.connect(site)
        self.TabSiteBldgRotLineEd.setValidator(QtGui.QIntValidator(0,359))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        Grid2.addItem(spacerItem, 8, 0, 1, 1)


        ## Tab3: Space Data
        self.TabSData = QtGui.QWidget(self.StadicTab)
        self.StadicTab.addTab(self.TabSData, _fromUtf8("SPACE"))
        self.StadicTab.setTabToolTip(self.StadicTab.indexOf(self.TabSData),"Editing the space information")
        HLayout = QtGui.QHBoxLayout(self.TabSData)
        Scroll=QtGui.QScrollArea()
        Scroll.setWidgetResizable(1)
        HLayout.addWidget(Scroll)
        AreaContents=QtGui.QWidget()
        AreaContents.setGeometry(QtCore.QRect(0,0,1400,600))
        V1Layout= QtGui.QVBoxLayout(AreaContents)
        Scroll.setWidget(AreaContents)
        Grid2=QtGui.QGridLayout()
        V1Layout.addLayout(Grid2)
        spacerItem= QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 1, 0, 1, 1)
        SPLbl = QtGui.QLabel(self.TabSData)
        Grid2.addWidget(SPLbl, 1, 1, 1, 1)
        SPLbl.setFixedWidth(180)
        SPLbl.setText(_translate("FormSTADIC", "Space Name:", None))
        self.TabSDataSPComBox = QtGui.QComboBox(self.TabSData)
        Grid2.addWidget(self.TabSDataSPComBox, 1, 2, 1, 1)
        self.TabSDataSPComBox.setFixedWidth(500)
        self.TabSDataSPAddBtn= QtGui.QPushButton(self.TabSData)
        Grid2.addWidget(self.TabSDataSPAddBtn, 1, 3, 1, 1)
        self.TabSDataSPAddBtn.setText(_translate("FormSTADIC", "Add", None))
        self.TabSDataSPAddBtn.clicked.connect(self.SPAdd)

        self.TabSDataSPCopyBtn= QtGui.QPushButton(self.TabSData)
        Grid2.addWidget(self.TabSDataSPCopyBtn, 1, 4, 1, 1)
        self.TabSDataSPCopyBtn.setText(_translate("FormSTADIC", "Copy", None))
        self.TabSDataSPCopyBtn.clicked.connect(self.SPCopy)
        self.TabSDataSPCopyBtn.setDisabled(1)
        self.TabSDataSPDelBtn= QtGui.QPushButton(self.TabSData)
        Grid2.addWidget(self.TabSDataSPDelBtn, 1, 5, 1, 1)
        self.TabSDataSPDelBtn.setText(_translate("FormSTADIC", "Delete", None))
        self.TabSDataSPDelBtn.clicked.connect(self.SPDel)
        self.TabSDataSPDelBtn.setDisabled(1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 1, 6, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 2, 0, 1, 1)
        self.TabSData2HLayout = QtGui.QHBoxLayout()
        V1Layout.addLayout(self.TabSData2HLayout)
        spacerItem14 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.TabSData2HLayout.addItem(spacerItem14)
        SPLbl = QtGui.QLabel(self.TabSData)
        self.TabSData2HLayout.addWidget(SPLbl)
        SPLbl.setText(_translate("FormSTADIC", "FOLDER PATHS:", None))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.TabSData2HLayout.addItem(spacerItem)
        Grid2 = QtGui.QGridLayout()
        V1Layout.addLayout(Grid2)
        spacerItem = QtGui.QSpacerItem(100, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 0, 0, 1, 1)
        SPLbl = QtGui.QLabel(self.TabSData)
        SPLbl.setFixedWidth(120)
        Grid2.addWidget(SPLbl, 0, 1, 1, 1)
        SPLbl.setText(_translate("FormSTADIC", "Geometry:", None))
        self.TabSDataGeoBrwLineEd = QtGui.QLineEdit(self.TabSData)
        self.TabSDataGeoBrwLineEd.setFixedWidth(500)
        self.TabSDataGeoBrwLineEd.setReadOnly(1)
        Grid2.addWidget(self.TabSDataGeoBrwLineEd, 0, 2, 1, 1)
        self.TabSDataGeoBrwBtn=QtGui.QPushButton(self.TabSData)
        Grid2.addWidget(self.TabSDataGeoBrwBtn, 0, 3, 1, 1)
        self.TabSDataGeoBrwBtn.setText("Set")
        brw=lambda: self.sppath(self.TabSDataGeoBrwLineEd,"geometry_directory")
        self.TabSDataGeoBrwBtn.clicked.connect(brw)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 0, 4, 1, 1)
        SPLbl = QtGui.QLabel(self.TabSData)
        Grid2.addWidget(SPLbl, 1, 1, 1, 1)
        SPLbl.setText(_translate("FormSTADIC", "IES Files:", None))
        self.TabSDataIESBrwLineEd = QtGui.QLineEdit(self.TabSData)
        self.TabSDataIESBrwLineEd.setFixedWidth(500)
        self.TabSDataIESBrwLineEd.setReadOnly(1)
        Grid2.addWidget(self.TabSDataIESBrwLineEd, 1, 2, 1, 1)
        self.TabSDataIESBrwBtn=QtGui.QPushButton(self.TabSData)
        Grid2.addWidget(self.TabSDataIESBrwBtn, 1 , 3, 1, 1)
        self.TabSDataIESBrwBtn.setText("Set")
        brw=lambda: self.sppath(self.TabSDataIESBrwLineEd,"ies_directory")
        self.TabSDataIESBrwBtn.clicked.connect(brw)
        SPLbl = QtGui.QLabel(self.TabSData)
        Grid2.addWidget(SPLbl, 2, 1, 1, 1)
        SPLbl.setText(_translate("FormSTADIC", "Input:", None))
        self.TabSDataInputLineEd = QtGui.QLineEdit(self.TabSData)
        self.TabSDataInputLineEd.setFixedWidth(500)
        self.TabSDataInputLineEd.setReadOnly(1)
        Grid2.addWidget(self.TabSDataInputLineEd, 2, 2, 1, 1)
        self.TabSDataInputBrwBtn=QtGui.QPushButton(self.TabSData)
        Grid2.addWidget(self.TabSDataInputBrwBtn, 2 , 3, 1, 1)
        self.TabSDataInputBrwBtn.setText("Set")
        brw=lambda: self.sppath(self.TabSDataInputLineEd,"input_directory")
        self.TabSDataInputBrwBtn.clicked.connect(brw)
        SPLbl = QtGui.QLabel(self.TabSData)
        SPLbl.setText(_translate("FormSTADIC", "Results:", None))
        Grid2.addWidget(SPLbl, 3, 1, 1, 1)
        self.TabSDataResLineEd = QtGui.QLineEdit(self.TabSData)
        self.TabSDataResLineEd.setFixedWidth(500)
        self.TabSDataResLineEd.setReadOnly(1)
        Grid2.addWidget(self.TabSDataResLineEd, 3, 2, 1, 1)
        self.TabSDataResBrwBtn=QtGui.QPushButton(self.TabSData)
        Grid2.addWidget(self.TabSDataResBrwBtn, 3, 3, 1, 1)
        self.TabSDataResBrwBtn.setText("Set")
        brw=lambda: self.sppath(self.TabSDataResLineEd, "results_directory")
        self.TabSDataResBrwBtn.clicked.connect(brw)
        Grid2=QtGui.QGridLayout()
        V1Layout.addLayout(Grid2)
        spacerItem10 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem10, 0, 0, 1, 1)
        spacerItem11 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem11, 1, 0, 1, 1)
        SPLbl = QtGui.QLabel(self.TabSData)
        Grid2.addWidget(SPLbl, 1, 1, 1, 1)
        SPLbl.setText(_translate("FormSTADIC", "Material RAD File:", None))
        SPLbl.setFixedWidth(180)
        self.TabSDataMatLineEd = QtGui.QLineEdit(self.TabSData)
        self.TabSDataMatLineEd.setFixedWidth(500)
        Grid2.addWidget(self.TabSDataMatLineEd, 1, 2, 1, 1)
        self.TabSDataMatLineEd.setReadOnly(1)
        self.TabSDataMatBtn = QtGui.QPushButton(self.TabSData)
        Grid2.addWidget(self.TabSDataMatBtn, 1, 3, 1, 1)
        self.TabSDataMatBtn.setText(_translate("FormSTADIC", "View/Edit", None))
        viewedit=lambda: self.view_edit(self.TabSDataMatLineEd)
        self.TabSDataMatBtn.clicked.connect(viewedit)
        self.TabSDataMatImportBtn = QtGui.QPushButton(self.TabSData)
        Grid2.addWidget(self.TabSDataMatImportBtn, 1, 4, 1, 1)
        self.TabSDataMatImportBtn.setText(_translate("FormSTADIC", "Import", None))
        self.TabSDataMatImportBtn.clicked.connect(self.MatImport)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 1, 5, 1, 1)
        SPLbl = QtGui.QLabel(self.TabSData)
        Grid2.addWidget(SPLbl, 2, 1, 1, 1)
        SPLbl.setText(_translate("FormSTADIC", "Geometry RAD File:", None))
        self.TabSDataGeoLineEd = QtGui.QLineEdit(self.TabSData)
        self.TabSDataGeoLineEd.setFixedWidth(500)
        Grid2.addWidget(self.TabSDataGeoLineEd, 2, 2, 1, 1)
        self.TabSDataGeoLineEd.setReadOnly(1)
        self.TabSDataGeoBtn = QtGui.QPushButton(self.TabSData)
        Grid2.addWidget(self.TabSDataGeoBtn, 2, 3, 1, 1)
        self.TabSDataGeoBtn.setText(_translate("FormSTADIC", "View/Edit", None))
        viewedit=lambda: self.view_edit(self.TabSDataGeoLineEd)
        self.TabSDataGeoBtn.clicked.connect(viewedit)
        self.TabSDataGeoImportBtn = QtGui.QPushButton(self.TabSData)
        Grid2.addWidget(self.TabSDataGeoImportBtn, 2, 4, 1, 1)
        self.TabSDataGeoImportBtn.setText(_translate("FormSTADIC", "Import", None))
        self.TabSDataGeoImportBtn.clicked.connect(self.GeoImport)
        # SPLbl = QtGui.QLabel(self.TabFile)
        # Grid2.addWidget(SPLbl, 3, 1, 1, 1)
        # SPLbl.setText(_translate("FormSTADIC", "Occupancy Schedule:", None))
        # self.TabSDataOccLineEd = QtGui.QLineEdit(self.TabFile)
        # self.TabSDataOccLineEd.setFixedWidth(500)
        # Grid2.addWidget(self.TabSDataOccLineEd, 3, 2, 1, 1)
        # self.TabSDataOccLineEd.setReadOnly(1)
        # self.TabSDataOccBtn = QtGui.QPushButton(self.TabFile)
        # Grid2.addWidget(self.TabSDataOccBtn, 3, 3, 1, 1)
        # self.TabSDataOccBtn.setText(_translate("FormSTADIC", "Browse", None))
        # self.TabSDataOccBtn.clicked.connect(self.OccImport)
        SPLbl = QtGui.QLabel(self.TabFile)
        Grid2.addWidget(SPLbl, 4, 1, 1, 1)
        SPLbl.setText(_translate("FormSTADIC", "Lighting Schedule", None))
        self.TabSDataLSLineEd = QtGui.QLineEdit(self.TabFile)
        self.TabSDataLSLineEd.setFixedWidth(500)
        Grid2.addWidget(self.TabSDataLSLineEd, 4, 2, 1, 1)
        self.TabSDataLSLineEd.setReadOnly(1)
        self.TabSDataLSBtn = QtGui.QPushButton(self.TabFile)
        Grid2.addWidget(self.TabSDataLSBtn, 4, 3, 1, 1)
        self.TabSDataLSBtn.setText(_translate("FormSTADIC", "Browse", None))
        self.TabSDataLSBtn.clicked.connect(self.LSImport)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        V1Layout.addItem(spacerItem)



        ## Tab4: Analysis Grids
        self.TabAna = QtGui.QWidget(self.StadicTab)
        self.StadicTab.addTab(self.TabAna, _fromUtf8("ANALYSIS GRID"))
        self.StadicTab.setTabToolTip(self.StadicTab.indexOf(self.TabAna),"")
        VVLayout = QtGui.QVBoxLayout(self.TabAna)
        Scroll=QtGui.QScrollArea()
        Scroll.setWidgetResizable(1)
        VVLayout.addWidget(Scroll)
        AreaContents=QtGui.QWidget()
        AreaContents.setGeometry(QtCore.QRect(0,0,1400,600))
        VLayout= QtGui.QVBoxLayout(AreaContents)
        Scroll.setWidget(AreaContents)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        VLayout.addItem(spacerItem)
        H1Layout=QtGui.QHBoxLayout()
        VLayout.addLayout(H1Layout)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        H1Layout.addItem(spacerItem)
        ALbl=QtGui.QLabel(self.TabAna)
        H1Layout.addWidget(ALbl)
        ALbl.setText(_translate("FormSTADIC", "Space Name:", None))
        ALbl.setFixedWidth(130)
        self.TabAnaSPNComBox=QtGui.QComboBox(self.TabAna)
        H1Layout.addWidget(self.TabAnaSPNComBox)
        self.TabAnaSPNComBox.setFixedWidth(300)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        H1Layout.addItem(spacerItem)
        H1Layout= QtGui.QHBoxLayout()
        VLayout.addLayout(H1Layout)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        H1Layout.addItem(spacerItem)
        ALbl = QtGui.QLabel(self.TabAna)
        H1Layout.addWidget(ALbl)
        ALbl.setFixedWidth(130)
        ALbl.setText(_translate("FormSTADIC", "Grid Points File:", None))
        self.TabAnaGPFLineEd=QtGui.QLineEdit(self.TabAna)
        H1Layout.addWidget(self.TabAnaGPFLineEd)
        self.TabAnaGPFLineEd.setFixedWidth(300)
        self.TabAnaGPFLineEd.setReadOnly(1)
        self.TabAnaGPWBtn = QtGui.QPushButton(self.TabAna)
        H1Layout.addWidget(self.TabAnaGPWBtn)
        self.TabAnaGPWBtn.setText(_translate("FormSTADIC", "Import", None))
        self.TabAnaGPWBtn.setFixedWidth((100))
        self.TabAnaGPWBtn.clicked.connect(self.AddPts)
        self.TabAnaGPRstBtn = QtGui.QPushButton(self.TabAna)
        H1Layout.addWidget(self.TabAnaGPRstBtn)
        self.TabAnaGPRstBtn.setText(_translate("FormSTADIC", "Reset", None))
        self.TabAnaGPRstBtn.setFixedWidth((100))
        self.TabAnaGPRstBtn.clicked.connect(self.PtsRst)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        H1Layout.addItem(spacerItem)
        Grid2 = QtGui.QGridLayout()
        VLayout.addLayout(Grid2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 0, 0, 1, 1)
        ALbl = QtGui.QLabel(self.TabAna)
        Grid2.addWidget(ALbl, 0, 1, 1, 1)
        ALbl.setFixedWidth(130)
        ALbl.setText(_translate("FormSTADIC", "Material Name:", None))
        self.TabAnaMatNComBox = QtGui.QComboBox(self.TabAna)
        Grid2.addWidget(self.TabAnaMatNComBox, 0, 2, 1, 1)
        self.TabAnaMatNComBox.setFixedWidth(300)
        self.TabAnaMatAddBtn=QtGui.QPushButton(self.TabAna)
        Grid2.addWidget(self.TabAnaMatAddBtn, 0, 3, 1, 1)
        self.TabAnaMatAddBtn.setText(_translate("FormSTADIC","Add", None))
        self.TabAnaMatAddBtn.clicked.connect(self.PtsMatAdd)
        self.TabAnaMatAddBtn.setFixedWidth(100)
        self.TabAnaMatDelBtn=QtGui.QPushButton(self.TabAna)
        Grid2.addWidget(self.TabAnaMatDelBtn, 0, 4, 1, 1)
        self.TabAnaMatDelBtn.setText(_translate("FormSTADIC","Delete", None))
        self.TabAnaMatDelBtn.clicked.connect(self.PtsMatDel)
        self.TabAnaMatDelBtn.setFixedWidth(100)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 0, 5, 1, 1)
        Grid2 = QtGui.QGridLayout()
        VLayout.addLayout(Grid2)
        spacerItem26 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem26, 0, 0, 1, 1)
        self.AnaSPLbl = QtGui.QLabel(self.TabAna)
        Grid2.addWidget(self.AnaSPLbl, 0, 1, 1, 1)
        self.AnaSPLbl.setText(_translate("FormSTADIC", "Spacing:", None))
        self.AnaSPLbl.setFixedWidth(134)
        ALbl = QtGui.QLabel(self.TabAna)
        Grid2.addWidget(ALbl, 0, 2, 1, 1)
        ALbl.setFixedWidth(22)
        ALbl.setText(_translate("FormSTADIC", "X:", None))
        self.TabAnaSPXLineEd = QtGui.QLineEdit(self.TabAna)
        Grid2.addWidget(self.TabAnaSPXLineEd, 0, 3, 1, 1)
        self.TabAnaSPXLineEd.setValidator(QtGui.QDoubleValidator())
        self.TabAnaSPXLineEd.setFixedWidth(65)
        anadata=lambda: self.Ptsdata(self.TabAnaSPXLineEd,"x_spacing")
        self.TabAnaSPXLineEd.editingFinished.connect(anadata)
        ALbl = QtGui.QLabel(self.TabAna)
        Grid2.addWidget(ALbl, 0, 4, 1, 1)
        ALbl.setFixedWidth(22)
        ALbl.setText(_translate("FormSTADIC", "Y:", None))
        self.TabAnaSPYLineEd = QtGui.QLineEdit(self.TabAna)
        Grid2.addWidget(self.TabAnaSPYLineEd, 0, 5, 1, 1)
        self.TabAnaSPYLineEd.setFixedWidth(65)
        self.TabAnaSPYLineEd.setValidator(QtGui.QDoubleValidator())
        anadata=lambda: self.Ptsdata(self.TabAnaSPYLineEd,"y_spacing")
        self.TabAnaSPYLineEd.editingFinished.connect(anadata)
        spacerItem= QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 0, 8, 1, 1)
        self.AnaOSLbl= QtGui.QLabel(self.TabAna)
        Grid2.addWidget(self.AnaOSLbl, 1, 1, 1, 1)
        self.AnaOSLbl.setFixedWidth(134)
        self.AnaOSLbl.setText(_translate("FormSTADIC", "Offset:", None))
        ALbl = QtGui.QLabel(self.TabAna)
        Grid2.addWidget(ALbl, 1, 2, 1, 1)
        ALbl.setFixedWidth(22)
        ALbl.setText(_translate("FormSTADIC", "X:", None))
        self.TabAnaOffXLineEd = QtGui.QLineEdit(self.TabAna)
        Grid2.addWidget(self.TabAnaOffXLineEd, 1, 3, 1, 1)
        self.TabAnaOffXLineEd.setFixedWidth(65)
        self.TabAnaOffXLineEd.setValidator(QtGui.QDoubleValidator())
        anadata=lambda: self.Ptsdata(self.TabAnaOffXLineEd,"offset")
        self.TabAnaOffXLineEd.editingFinished.connect(anadata)
        ALbl = QtGui.QLabel(self.TabAna)
        Grid2.addWidget(ALbl, 1, 4, 1, 1)
        ALbl.setFixedWidth(22)
        ALbl.setText(_translate("FormSTADIC", "Y:", None))
        self.TabAnaOffYLineEd = QtGui.QLineEdit(self.TabAna)
        anadata=lambda: self.Ptsdata(self.TabAnaOffYLineEd,"offset")
        self.TabAnaOffYLineEd.editingFinished.connect(anadata)
        Grid2.addWidget(self.TabAnaOffYLineEd, 1, 5, 1, 1)
        self.TabAnaOffYLineEd.setFixedWidth(65)
        self.TabAnaOffYLineEd.setValidator(QtGui.QDoubleValidator())
        ALbl = QtGui.QLabel(self.TabAna)
        Grid2.addWidget(ALbl, 1, 6, 1, 1)
        ALbl.setFixedWidth(22)
        self.TabAnaOffZLineEd = QtGui.QLineEdit(self.TabAna)
        Grid2.addWidget(self.TabAnaOffZLineEd, 1, 7, 1, 1)
        self.TabAnaOffZLineEd.setFixedWidth(65)
        self.TabAnaOffZLineEd.setValidator(QtGui.QDoubleValidator())
        anadata=lambda: self.Ptsdata(self.TabAnaOffZLineEd,"z_offset")
        self.TabAnaOffZLineEd.editingFinished.connect(anadata)
        ALbl.setText(_translate("FormSTADIC", "Z:", None))
        spacerItem27 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        VLayout.addItem(spacerItem27)


        ##Tab5: Window Groups
        self.TabWin = QtGui.QWidget()
        self.StadicTab.addTab(self.TabWin, _fromUtf8("WINDOW GROUPS"))
        self.StadicTab.setTabToolTip(self.StadicTab.indexOf(self.TabWin),"")
        Grid= QtGui.QGridLayout()
        self.TabWin.setLayout(Grid)

        #self.TabWinGridLayout = QtGui.QGridLayout(self.TabWin)
        Scroll=QtGui.QScrollArea()
        Scroll.setWidgetResizable(1)
        Grid.addWidget(Scroll, 0, 0, 1 ,1)
        AreaContents=QtGui.QWidget()
        AreaContents.setGeometry(QtCore.QRect(0,0,1400,1000))
        self.WGrid1 = QtGui.QGridLayout(AreaContents)
        Scroll.setWidget(AreaContents)

        #self.TabWinGridLayout.addLayout(self.TabWin1Grid, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.WGrid1.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.WGrid1.addItem(spacerItem, 0, 1, 1, 1)
        Grid1 = QtGui.QGridLayout()
        self.WGrid1.addLayout(Grid1, 1, 1, 1, 1)
        WLbl=QtGui.QLabel(self.TabWin)
        Grid1.addWidget(WLbl, 0, 0, 1, 1)
        WLbl.setText(_translate("FormSTADIC","Space Name:", None))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 0, 1, 1, 1)
        self.TabWinSPNComBox=QtGui.QComboBox(self.TabWin)
        Grid1.addWidget(self.TabWinSPNComBox, 0, 2, 1, 1)
        self.TabWinSPNComBox.setFixedWidth(150)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 0, 3, 1, 1)
        WLbl = QtGui.QLabel(self.TabWin)
        Grid1.addWidget(WLbl, 1, 0, 1, 1)
        WLbl.setText(_translate("FormSTADIC", "Window Groups:", None))

        Grid2 = QtGui.QGridLayout()
        self.WGrid1.addLayout(Grid2, 2, 1, 1, 1)
        WLbl = QtGui.QLabel(self.TabWin)
        Grid2.addWidget(WLbl, 0, 1, 1, 1)
        WLbl.setText(_translate("FormSTADIC", "Group Name:", None))
        self.TabWinWGComBox = QtGui.QComboBox(self.TabWin)
        Grid2.addWidget(self.TabWinWGComBox, 0, 2, 1, 1)
        self.TabWinWGAddBtn = QtGui.QPushButton(self.TabWin)
        Grid2.addWidget(self.TabWinWGAddBtn, 0, 3, 1, 1)
        self.TabWinWGAddBtn.setText(_translate("FormSTADIC", "Add", None))
        self.TabWinWGAddBtn.clicked.connect(self.WGAdd)
        self.TabWinWGDelBtn = QtGui.QPushButton(self.TabWin)
        Grid2.addWidget(self.TabWinWGDelBtn, 0, 4, 1, 1)
        self.TabWinWGDelBtn.setText(_translate("FormSTADIC", "Delete", None))
        self.TabWinWGDelBtn.clicked.connect(self.WGDel)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 0, 5, 1, 1)
        WLbl=QtGui.QLabel()
        WLbl.setText("Calculate:")
        Grid2.addWidget(WLbl, 1, 1, 1, 1)
        self.WGCalCbx=QtGui.QCheckBox()
        self.WGCalCbx.setChecked(1)
        self.WGCalCbx.setDisabled(1)
        self.WGCalCbx.clicked.connect(self.WCalc)
        Grid2.addWidget(self.WGCalCbx, 1, 2, 1, 1)
        WLbl=QtGui.QLabel(self.TabWin)
        Grid2.addWidget(WLbl, 2, 1, 1, 1)
        WLbl.setText(_translate("FormSTADIC","Base Geometry:", None))
        self.TabWinBGeoLineEd = QtGui.QLineEdit(self.TabWin)
        Grid2.addWidget(self.TabWinBGeoLineEd, 2, 2, 1, 1)
        self.TabWinBGeoLineEd.setReadOnly(1)
        self.TabWinBGeoBtn = QtGui.QPushButton(self.TabWin)
        Grid2.addWidget(self.TabWinBGeoBtn, 2, 3, 1, 1)
        self.TabWinBGeoBtn.setText(_translate("FormSTADIC","Browse", None))
        self.TabWinBGeoBtn.clicked.connect(self.WinG)
        WLbl = QtGui.QLabel(self.TabWin)
        Grid2.addWidget(WLbl, 3, 1, 1, 1)
        WLbl.setText(_translate("FormSTADIC", "Material:", None))
        self.TabWinWGMatComBox = QtGui.QComboBox(self.TabWin)
        Grid2.addWidget(self.TabWinWGMatComBox, 3, 2, 1, 1)
        self.TabWinWGMatAddBtn=QtGui.QPushButton(self.TabWin)
        Grid2.addWidget(self.TabWinWGMatAddBtn, 3, 3, 1, 1)
        self.TabWinWGMatAddBtn.setText(_translate("FormSTADIC","Add", None))
        self.TabWinWGMatAddBtn.clicked.connect(self.WGMatAdd)
        self.TabWinWGMatDelBtn=QtGui.QPushButton(self.TabWin)
        Grid2.addWidget(self.TabWinWGMatDelBtn, 3, 4, 1, 1)
        self.TabWinWGMatDelBtn.setText(_translate("FormSTADIC","Delete", None))
        self.TabWinWGMatDelBtn.clicked.connect(self.WGMatDel)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 4, 1, 1, 1)
        WLbl = QtGui.QLabel(self.TabWin)
        Grid2.addWidget(WLbl, 5, 0, 1, 1)
        WLbl.setText(_translate("FormSTADIC", "Shading Devices:", None))
        WLbl.setFixedWidth(150)
        WLbl = QtGui.QLabel(self.TabWin)
        Grid2.addWidget(WLbl, 6, 1, 1, 1)
        WLbl.setText(_translate("FormSTADIC", "Shade File:", None))
        WLbl.setAlignment(QtCore.Qt.AlignTop)
        WLbl.setFixedHeight(100)
        self.TabWinShadeTbl=QtGui.QTableWidget(self.TabWin)
        Grid2.addWidget(self.TabWinShadeTbl, 6, 2, 1, 1)
        self.TabWinShadeTbl.setFixedHeight(200)
        self.TabWinShadeTbl.setColumnCount(4)
        item = QtGui.QTableWidgetItem()
        self.TabWinShadeTbl.setHorizontalHeaderItem(0,item)
        item = self.TabWinShadeTbl.horizontalHeaderItem(0)
        item.setText(_translate("FormSTADIC", "File Name", None))
        item = QtGui.QTableWidgetItem()
        self.TabWinShadeTbl.setHorizontalHeaderItem(1,item)
        item = self.TabWinShadeTbl.horizontalHeaderItem(1)
        item.setText(_translate("FormSTADIC", "sDA Shade", None))
        item = QtGui.QTableWidgetItem()
        self.TabWinShadeTbl.setHorizontalHeaderItem(2,item)
        item = self.TabWinShadeTbl.horizontalHeaderItem(2)
        item.setText(_translate("FormSTADIC", "Calculate", None))
        item = QtGui.QTableWidgetItem()
        self.TabWinShadeTbl.setHorizontalHeaderItem(3,item)
        item = self.TabWinShadeTbl.horizontalHeaderItem(3)
        item.setText(_translate("FormSTADIC", "Delete", None))
        self.TabWinShadeTbl.setColumnWidth(0,200)
        self.TabWinShadeTbl.setColumnWidth(1,100)
        self.TabWinShadeTbl.setColumnWidth(2,100)
        self.TabWinShadeTbl.setColumnWidth(3,100)
        self.TabWinShadeAddBtn = QtGui.QPushButton(self.TabWin)
        Grid2.addWidget(self.TabWinShadeAddBtn, 6, 3, 1, 1)
        self.TabWinShadeAddBtn.setText(_translate("FormSTADIC", "Add", None))
        self.TabWinShadeAddBtn.clicked.connect(self.WShadeAdd)
        WLbl = QtGui.QLabel(self.TabWin)
        Grid2.addWidget(WLbl, 7, 1, 1, 1)
        WLbl.setText(_translate("FormSTADIC", "Control:", None))
        self.TabWinMtdComBox = QtGui.QComboBox(self.TabWin)
        self.TabWinMtdComBox.addItem(_fromUtf8("Signal"))
        self.TabWinMtdComBox.addItem(_fromUtf8("Profile Angle"))
        self.TabWinMtdComBox.addItem(_fromUtf8("Signal and Profile Angle"))
        self.TabWinMtdComBox.addItem(_fromUtf8("None"))
        self.TabWinMtdComBox.currentIndexChanged.connect(self.ShadeCtrlMtd)
        Grid2.addWidget(self.TabWinMtdComBox, 7, 2, 1, 1)
        self.TabWinMtdComBox.setCurrentIndex(3)
        # WLbl=QtGui.QLabel(self.TabWin)
        # Grid2.addWidget(WLbl, 7, 1, 1, 1)
        # WLbl.setText(_translate("FormSTADIC","BSDF", None))
        # self.TabWinBSDFChkB = QtGui.QCheckBox(self.TabWin)
        # self.TabWinBSDFChkB.setText(_fromUtf8(""))
        # Grid2.addWidget(self.TabWinBSDFChkB, 7, 2, 1, 1)
        # cboxsta=lambda: self.CheckState(self.TabWinBSDFChkB,"BSDF")
        # self.TabWinBSDFChkB.stateChanged.connect(cboxsta)
        # WLbl = QtGui.QLabel(self.TabWin)
        # Grid2.addWidget(WLbl, 8, 1, 1, 1)
        # WLbl.setText(_translate("FormSTADIC", "Base Material:", None))
        # self.TabWinBSDFBMatComBox = QtGui.QComboBox(self.TabWin)
        # Grid2.addWidget(self.TabWinBSDFBMatComBox, 8, 2, 1, 1)
        # WLbl = QtGui.QLabel(self.TabWin)
        # Grid2.addWidget(WLbl, 9, 1, 1, 1)
        # WLbl.setText(_translate("FormSTADIC", "Setting Material:", None))
        # self.TabWinBSDFSetList = QtGui.QListWidget(self.TabWin)
        # Grid2.addWidget(self.TabWinBSDFSetList, 9, 2, 1, 1)
        # self.TabWinBSDFSetList.setFixedHeight(60)
        # self.TabWinBSDFSetAddBtn = QtGui.QPushButton(self.TabWin)
        # Grid2.addWidget(self.TabWinBSDFSetAddBtn, 9, 3, 1, 1)
        # self.TabWinBSDFSetAddBtn.setText(_translate("FormSTADIC", "Add", None))
        # #self.TabWinBSDFSetAddBtn.clicked.connect()
        # self.TabWinBSDFSetDelBtn = QtGui.QPushButton(self.TabWin)
        # Grid2.addWidget(self.TabWinBSDFSetDelBtn, 9, 4, 1, 1)
        # self.TabWinBSDFSetDelBtn.setText(_translate("FormSTADIC", "Delete", None))
        # #self.TabWinBSDFSetDelBtn.clicked.connect()
        # WLbl.hide()
        # self.TabWinBSDFChkB.hide()
        # self.TabWinBSDFBMatComBox.hide()
        # self.TabWinBSDFSetList.hide()
        # WLbl.hide()
        # self.TabWinBSDFSetAddBtn.hide()
        # self.TabWinBSDFSetDelBtn.hide()
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.WGrid1.addItem(spacerItem, 7, 0, 1, 1)
        #self.TabWinGridLayout.addItem(spacerItem, 3, 0, 1, 1)


        ##Tab6: Electric Lighting
        self.TabElec = QtGui.QWidget()
        self.StadicTab.addTab(self.TabElec, _fromUtf8("ELECTRIC LIGHTING"))
        self.StadicTab.setTabToolTip(self.StadicTab.indexOf(self.TabElec),"")
        Grid= QtGui.QGridLayout()
        self.TabElec.setLayout(Grid)
        Scroll=QtGui.QScrollArea()
        Scroll.setWidgetResizable(1)
        Grid.addWidget(Scroll, 0, 0, 1 ,1)
        AreaContents=QtGui.QWidget()
        AreaContents.setGeometry(QtCore.QRect(0,0,1500,1000))
        Grid1 = QtGui.QGridLayout(AreaContents)
        Scroll.setWidget(AreaContents)

        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 1, 0, 1, 1)
        H1Layout=QtGui.QHBoxLayout()
        Grid1.addLayout(H1Layout, 1, 1, 1, 1)
        ELbl=QtGui.QLabel(self.TabElec)
        H1Layout.addWidget(ELbl)
        ELbl.setText(_translate("FormSTADIC", "Space Name:", None))
        ELbl.setFixedWidth(120)
        self.TabElecSPComBox=QtGui.QComboBox(self.TabElec)
        H1Layout.addWidget(self.TabElecSPComBox)
        self.TabElecSPComBox.setFixedWidth(180)

        ELbl=QtGui.QLabel(self.TabElec)
        H1Layout.addWidget(ELbl)
        ELbl.setFixedWidth(120)
        ELbl.setText("Floor Layer:")
        self.TabElecLayerCbx=QtGui.QComboBox(self.TabElec)
        H1Layout.addWidget(self.TabElecLayerCbx)
        self.TabElecLayerCbx.setFixedWidth(180)
        self.TabElecLayerAddBtn=QtGui.QPushButton(self.TabElec)
        self.TabElecLayerAddBtn.setText("Add")
        H1Layout.addWidget(self.TabElecLayerAddBtn)
        self.TabElecLayerAddBtn.clicked.connect(self.PtsMatAdd)
        self.TabElecLayerDelBtn=QtGui.QPushButton(self.TabElec)
        self.TabElecLayerDelBtn.setText("Delete")
        H1Layout.addWidget(self.TabElecLayerDelBtn)
        self.TabElecLayerDelBtn.clicked.connect(self.PtsMatDel)
        self.TabElecLayoutDipBtn = QtGui.QPushButton(self.TabElec)
        H1Layout.addWidget(self.TabElecLayoutDipBtn)
        self.TabElecLayoutDipBtn.setText(_translate("FormSTADIC", "View Layout", None))
        self.TabElecLayoutDipBtn.setFixedWidth(150)
        self.TabElecLayoutDipBtn.clicked.connect(self.LumLayoutDisplay)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        H1Layout.addItem(spacerItem)
        ELbl = QtGui.QLabel(self.TabElec)
        Grid1.addWidget(ELbl, 2, 1, 1, 1)
        ELbl.setText(_translate("FormSTADIC", "Luminaire and Ballast Info:", None))
        self.TabElecInfoTable=QtGui.QTableWidget(self.TabElec)
        self.TabElecInfoTable.setFixedHeight(200)
        Grid1.addWidget(self.TabElecInfoTable, 3, 1, 1, 1)
        self.TabElecInfoTable.setColumnCount(10)
        item = QtGui.QTableWidgetItem()
        self.TabElecInfoTable.setHorizontalHeaderItem(0,item)
        item = self.TabElecInfoTable.horizontalHeaderItem(0)
        item.setText(_translate("FormSTADIC", "Zone", None))
        item = QtGui.QTableWidgetItem()
        self.TabElecInfoTable.setHorizontalHeaderItem(1,item)
        item = self.TabElecInfoTable.horizontalHeaderItem(1)
        item.setText(_translate("FormSTADIC", "IES File", None))
        item = QtGui.QTableWidgetItem()
        self.TabElecInfoTable.setHorizontalHeaderItem(2,item)
        item = self.TabElecInfoTable.horizontalHeaderItem(2)
        item.setText(_translate("FormSTADIC", "Lumens/Lamp", None))
        item = QtGui.QTableWidgetItem()
        self.TabElecInfoTable.setHorizontalHeaderItem(3,item)
        item = self.TabElecInfoTable.horizontalHeaderItem(3)
        item.setText(_translate("FormSTADIC", "LLF", None))
        item = QtGui.QTableWidgetItem()
        self.TabElecInfoTable.setHorizontalHeaderItem(4,item)
        item = self.TabElecInfoTable.horizontalHeaderItem(4)
        item.setText(_translate("FormSTADIC", "BF Min", None))
        item = QtGui.QTableWidgetItem()
        self.TabElecInfoTable.setHorizontalHeaderItem(5,item)
        item = self.TabElecInfoTable.horizontalHeaderItem(5)
        item.setText(_translate("FormSTADIC", "BF Max", None))
        item = QtGui.QTableWidgetItem()
        self.TabElecInfoTable.setHorizontalHeaderItem(6,item)
        item = self.TabElecInfoTable.horizontalHeaderItem(6)
        item.setText(_translate("FormSTADIC", "Power Min", None))
        item = QtGui.QTableWidgetItem()
        self.TabElecInfoTable.setHorizontalHeaderItem(7,item)
        item = self.TabElecInfoTable.horizontalHeaderItem(7)
        item.setText(_translate("FormSTADIC", "Power Max", None))
        item = QtGui.QTableWidgetItem()
        self.TabElecInfoTable.setHorizontalHeaderItem(8,item)
        item = self.TabElecInfoTable.horizontalHeaderItem(8)
        item.setText(_translate("FormSTADIC", "Control Type", None))
        item = QtGui.QTableWidgetItem()
        self.TabElecInfoTable.setHorizontalHeaderItem(9,item)
        item = self.TabElecInfoTable.horizontalHeaderItem(9)
        item.setText(_translate("FormSTADIC", "Delete", None))
        item = QtGui.QTableWidgetItem()
        self.TabElecInfoTable.horizontalHeader().setCascadingSectionResizes(False)
        self.TabElecInfoTable.setColumnWidth(0,100)
        self.TabElecInfoTable.setColumnWidth(1,200)
        self.TabElecInfoTable.setColumnWidth(2,150)
        self.TabElecInfoTable.setColumnWidth(3,100)
        self.TabElecInfoTable.setColumnWidth(4,100)
        self.TabElecInfoTable.setColumnWidth(5,100)
        self.TabElecInfoTable.setColumnWidth(6,100)
        self.TabElecInfoTable.setColumnWidth(7,100)
        self.TabElecInfoTable.setColumnWidth(8,150)
        self.TabElecInfoTable.setColumnWidth(9,100)
        self.TabElecInfoTable.cellChanged.connect(self.InfoChange)
        H1Layout = QtGui.QHBoxLayout()
        Grid1.addLayout(H1Layout, 4, 1, 1, 1)
        self.TabElecInfoAddBtn = QtGui.QPushButton(self.TabElec)
        H1Layout.addWidget(self.TabElecInfoAddBtn)
        self.TabElecInfoAddBtn.setText(_translate("FormSTADIC", "Add A Zone", None))
        self.TabElecInfoAddBtn.setFixedWidth(150)
        self.TabElecInfoAddBtn.clicked.connect(self.ElecInfoAdd)
        self.TabElecZoneCopyBtn=QtGui.QPushButton(self.TabElec)
        H1Layout.addWidget(self.TabElecZoneCopyBtn)
        self.TabElecZoneCopyBtn.setText(_translate("FormSTADIC", "Duplicate A Zone", None))
        self.TabElecZoneCopyBtn.clicked.connect(self.ElecZoneCopy)
        self.TabElecZoneCopyBtn.setFixedWidth(150)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        H1Layout.addItem(spacerItem)
        H1Layout=QtGui.QHBoxLayout()
        Grid1.addLayout(H1Layout, 5, 1, 1, 1)
        ELbl=QtGui.QLabel(self.TabElec)
        H1Layout.addWidget(ELbl)
        ELbl.setText("Zone:")
        ELbl.setFixedWidth(120)
        self.TabElecZoneCombox=QtGui.QComboBox(self.TabElec)
        H1Layout.addWidget(self.TabElecZoneCombox)
        self.TabElecZoneCombox.setCurrentIndex(0)
        self.TabElecZoneCombox.setFixedWidth(180)
        self.TabElecZoneCombox.currentIndexChanged.connect(self.ElecLOLoad)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        H1Layout.addItem(spacerItem)
        self.TabElecLumLayoutLbl = QtGui.QLabel(self.TabElec)
        Grid1.addWidget(self.TabElecLumLayoutLbl, 6, 1, 1, 1)
        self.TabElecLumLayoutLbl.setText(_translate("FormSTADIC", "Luminaire Layout:", None))
        self.TabElecLayoutTable = QtGui.QTableWidget(self.TabElec)
        self.TabElecLayoutTable.setFixedHeight(300)
        Grid1.addWidget(self.TabElecLayoutTable, 7, 1, 1, 1)
        self.TabElecLayoutTable.setColumnCount(8)
        item = QtGui.QTableWidgetItem()
        self.TabElecLayoutTable.setHorizontalHeaderItem(0, item)
        item = self.TabElecLayoutTable.horizontalHeaderItem(0)
        item.setText(_translate("FormSTADIC", "Zone", None))
        item = QtGui.QTableWidgetItem()
        self.TabElecLayoutTable.setHorizontalHeaderItem(1, item)
        item = self.TabElecLayoutTable.horizontalHeaderItem(1)
        item.setText(_translate("FormSTADIC", "X", None))
        item = QtGui.QTableWidgetItem()
        self.TabElecLayoutTable.setHorizontalHeaderItem(2, item)
        item = self.TabElecLayoutTable.horizontalHeaderItem(2)
        item.setText(_translate("FormSTADIC", "Y", None))
        item = QtGui.QTableWidgetItem()
        self.TabElecLayoutTable.setHorizontalHeaderItem(3, item)
        item = self.TabElecLayoutTable.horizontalHeaderItem(3)
        item.setText(_translate("FormSTADIC", "Z", None))
        item = QtGui.QTableWidgetItem()
        self.TabElecLayoutTable.setHorizontalHeaderItem(4, item)
        item = self.TabElecLayoutTable.horizontalHeaderItem(4)
        item.setText(_translate("FormSTADIC", "ROT", None))
        item = QtGui.QTableWidgetItem()
        self.TabElecLayoutTable.setHorizontalHeaderItem(5, item)
        item = self.TabElecLayoutTable.horizontalHeaderItem(5)
        item.setText(_translate("FormSTADIC", "TILT", None))
        item = QtGui.QTableWidgetItem()
        self.TabElecLayoutTable.setHorizontalHeaderItem(6, item)
        item = self.TabElecLayoutTable.horizontalHeaderItem(6)
        item.setText(_translate("FormSTADIC", "SPIN", None))
        item = QtGui.QTableWidgetItem()
        self.TabElecLayoutTable.setHorizontalHeaderItem(7, item)
        item = self.TabElecLayoutTable.horizontalHeaderItem(7)
        item.setText(_translate("FormSTADIC", "Delete", None))
        self.TabElecLayoutTable.setColumnWidth(0,100)
        self.TabElecLayoutTable.setColumnWidth(1,100)
        self.TabElecLayoutTable.setColumnWidth(2,100)
        self.TabElecLayoutTable.setColumnWidth(3,100)
        self.TabElecLayoutTable.setColumnWidth(4,100)
        self.TabElecLayoutTable.setColumnWidth(5,100)
        self.TabElecLayoutTable.setColumnWidth(6,100)
        self.TabElecLayoutTable.setColumnWidth(7,100)
        self.TabElecLayoutTable.cellChanged.connect(self.LOChange)
        H1Layout = QtGui.QHBoxLayout()
        Grid1.addLayout(H1Layout, 8, 1, 1, 1)
        self.TabElecLayoutAddBtn = QtGui.QPushButton(self.TabElec)
        H1Layout.addWidget(self.TabElecLayoutAddBtn)
        self.TabElecLayoutAddBtn.setText(_translate("FormSTADIC", "Add A Luminaire", None))
        self.TabElecLayoutAddBtn.setFixedWidth(150)
        self.TabElecLayoutAddBtn.clicked.connect(self.ElecLOAdd)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        H1Layout.addItem(spacerItem)
        self.scene=QtGui.QGraphicsScene()
        self.view = QtGui.QGraphicsView(self.scene)
        self.view.setFixedHeight(500)
        Grid1.addWidget(self.view, 9,1,1,1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        Grid1.addItem(spacerItem, 10, 1, 1, 1)


        ##Tab7: Ctrl Group
        self.TabCtrl = QtGui.QWidget()
        self.StadicTab.addTab(self.TabCtrl, _fromUtf8("CONTROL"))
        self.StadicTab.setTabToolTip(self.StadicTab.indexOf(self.TabCtrl),"Electric Lighting Photocontrol Setup")
        VLayout = QtGui.QVBoxLayout(self.TabCtrl)
        Scroll=QtGui.QScrollArea()
        Scroll.setWidgetResizable(1)
        VLayout.addWidget(Scroll)
        AreaContents=QtGui.QWidget()
        AreaContents.setGeometry(QtCore.QRect(0,0,1400,600))
        HLayout= QtGui.QVBoxLayout(AreaContents)
        Scroll.setWidget(AreaContents)
        self.CGrid1 = QtGui.QGridLayout()
        HLayout.addLayout(self.CGrid1)
        spacerItem = QtGui.QSpacerItem(40, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.CGrid1.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.CGrid1.addItem(spacerItem, 1, 0, 1, 1)
        CLbl=QtGui.QLabel(self.TabCtrl)
        self.CGrid1.addWidget(CLbl, 1, 1, 1, 1)
        CLbl.setText(_translate("FormSTADIC","Space Name:", None))
        H1Layout=QtGui.QHBoxLayout()
        self.CGrid1.addLayout(H1Layout, 1, 2, 1, 1)
        self.TabCtrlSPNComBox=QtGui.QComboBox(self.TabCtrl)
        H1Layout.addWidget(self.TabCtrlSPNComBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        H1Layout.addItem(spacerItem)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.CGrid1.addItem(spacerItem, 2, 0, 1, 1)
        CLbl = QtGui.QLabel(self.TabCtrl)
        self.CGrid1.addWidget(CLbl, 3, 1, 1, 1)
        CLbl.setText(_translate("FormSTADIC", "Control Zone:", None))
        H1Layout=QtGui.QHBoxLayout()
        self.CGrid1.addLayout(H1Layout, 3, 2, 1, 1)
        self.TabCtrlCtrlZComBox = QtGui.QComboBox(self.TabCtrl)
        H1Layout.addWidget(self.TabCtrlCtrlZComBox)
        self.TabCtrlCtrlZComBox.setFixedWidth(200)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        H1Layout.addItem(spacerItem)

        CLbl = QtGui.QLabel(self.TabCtrl)
        self.CGrid1.addWidget(CLbl, 4, 1, 1, 1)
        CLbl.setText(_translate("FormSTADIC", "Control Algorithm:", None))
        H1Layout=QtGui.QHBoxLayout()
        self.CGrid1.addLayout(H1Layout, 4, 2, 1, 1)
        self.TabCtrlOptCComBox = QtGui.QComboBox(self.TabCtrl)
        H1Layout.addWidget(self.TabCtrlOptCComBox)
        self.TabCtrlOptCComBox.addItem("Dimming")
        self.TabCtrlOptCComBox.addItem("On")
        self.TabCtrlOptCComBox.addItem("Switched")
        self.TabCtrlOptCComBox.addItem("EPlus Dimming")
        self.TabCtrlOptCComBox.setCurrentIndex(-1)
        self.TabCtrlOptCComBox.setFixedWidth(200)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        H1Layout.addItem(spacerItem)
        CLbl = QtGui.QLabel(self.TabCtrl)
        self.CGrid1.addWidget(CLbl, 5, 1, 1, 1)
        CLbl.setText(_translate("FormSTADIC", "Critical Points:", None))
        Grid2 = QtGui.QGridLayout()
        self.CGrid1.addLayout(Grid2, 6, 2, 1, 1)
        CLbl = QtGui.QLabel(self.TabCtrl)
        Grid2.addWidget(CLbl, 0, 0, 1, 1)
        CLbl.setText(_translate("FormSTADIC", "Target Illuminance: ", None))
        self.TabCtrlTgtIllLineEd = QtGui.QLineEdit(self.TabCtrl)
        Grid2.addWidget(self.TabCtrlTgtIllLineEd, 0, 1, 1, 1)
        self.TabCtrlTgtIllLineEd.editingFinished.connect(self.Tgt)
        self.TabCtrlTgtIllLineEd.setFixedWidth(300)
        self.TabCtrlTgtIllLineEd.setValidator(QtGui.QIntValidator(0, 10000000))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 0, 3, 1, 1)
        CLbl = QtGui.QLabel(self.TabCtrl)
        Grid2.addWidget(CLbl, 1, 0, 1, 1)
        CLbl.setText(_translate("FormSTADIC", "Method:", None))
        self.TabCtrlCPMtdComBox = QtGui.QComboBox(self.TabCtrl)
        Grid2.addWidget(self.TabCtrlCPMtdComBox, 1, 1, 1, 1)
        self.TabCtrlCPMtdComBox.setFixedWidth(300)
        # self.TabCtrlCPMtdComBox.addItem("Auto")
        # self.TabCtrlCPMtdComBox.addItem("Manual")
        CLbl = QtGui.QLabel(self.TabCtrl)
        Grid2.addWidget(CLbl, 2, 0, 1, 1)
        CLbl.setText(_translate("FormSTADIC", "CP Quantity:", None))
        self.TabCtrlQtyComBox = QtGui.QComboBox(self.TabCtrl)
        Grid2.addWidget(self.TabCtrlQtyComBox, 2, 1, 1, 1)
        self.TabCtrlQtyComBox.setFixedWidth(300)
        for i in range(5):
            self.TabCtrlQtyComBox.addItem(str(i+1))
        self.TabCtrlQtyComBox.addItem("All")
        self.TabCtrlQtyComBox.setCurrentIndex(-1)
        self.TabCtrlQtyComBox.currentIndexChanged.connect(self.CPQty)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 3, 0, 1, 1)
        CLbl = QtGui.QLabel("Critical Points Exclusion:")
        Grid2.addWidget(CLbl, 4, 0, 1, 1)
        CLbl = QtGui.QLabel(self.TabCtrl)
        Grid2.addWidget(CLbl, 5, 0, 1, 1)
        CLbl.setText(_translate("FormSTADIC", "     Min Dimmed Zone Fraction:", None))
        self.TabCtrlTgtPctgLineEd = QtGui.QLineEdit(self.TabCtrl)
        Grid2.addWidget(self.TabCtrlTgtPctgLineEd, 5, 1, 1, 1)
        self.TabCtrlTgtPctgLineEd.editingFinished.connect(self.TgtPctg)
        self.TabCtrlTgtPctgLineEd.setFixedWidth(300)
        CLbl = QtGui.QLabel(self.TabCtrl)
        Grid2.addWidget(CLbl, 6, 0, 1, 1)
        CLbl.setText(_translate("FormSTADIC", "     Excluded Points File:", None))
        self.TabCtrlEPtsLineEd = QtGui.QLineEdit(self.TabCtrl)
        Grid2.addWidget(self.TabCtrlEPtsLineEd, 6, 1, 1, 1)
        self.TabCtrlEPtsLineEd.setFixedWidth(300)
        self.TabCtrlEPtsLineEd.setReadOnly(1)
        self.TabCtrlEPtsBtn = QtGui.QPushButton(self.TabCtrl)
        Grid2.addWidget(self.TabCtrlEPtsBtn, 6, 2, 1, 1)
        self.TabCtrlEPtsBtn.setText(_translate("FormSTADIC", "Browse", None))
        self.TabCtrlEPtsBtn.clicked.connect(self.CPExclude)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.CGrid1.addItem(spacerItem, 7, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.CGrid1.addItem(spacerItem, 10, 0, 1, 1)


        ##Tab8: Metrics
        self.TabDMtr = QtGui.QWidget()
        self.StadicTab.addTab(self.TabDMtr, _fromUtf8("METRICS"))
        self.StadicTab.setTabToolTip(self.StadicTab.indexOf(self.TabDMtr),"Daylight Metric Settings")
        HLayout = QtGui.QHBoxLayout(self.TabDMtr)
        Scroll=QtGui.QScrollArea()
        Scroll.setWidgetResizable(1)
        HLayout.addWidget(Scroll)
        AreaContents=QtGui.QWidget()
        AreaContents.setGeometry(QtCore.QRect(0,0,1400,600))
        Grid1= QtGui.QGridLayout(AreaContents)
        Scroll.setWidget(AreaContents)

        spacerItem= QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem= QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 0, 1, 1, 1)
        MLbl=QtGui.QLabel(self.TabDMtr)
        Grid1.addWidget(MLbl, 1, 1, 1, 1)
        MLbl.setText(_translate("FormSTADIC", "General Setting", None))
        self.TabDMtrGCbx=QtGui.QCheckBox(self.TabDMtr)
        Grid1.addWidget(self.TabDMtrGCbx, 1, 3, 1, 1)
        self.TabDMtrGCbx.stateChanged.connect(self.mtrGeneral)
        MLbl=QtGui.QLabel(self.TabDMtr)
        Grid1.addWidget(MLbl, 2, 1, 1, 1)
        MLbl.setText(_translate("FormSTADIC", "Space Name:", None))
        self.TabDMtrSPNComBox=QtGui.QComboBox(self.TabDMtr)
        Grid1.addWidget(self.TabDMtrSPNComBox, 2, 3, 1, 1)
        spacerItem= QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 3, 1, 1, 1)

        MLbl = QtGui.QLabel(self.TabDMtr)
        Grid1.addWidget(MLbl, 4, 1, 1, 1)
        MLbl.setText(_translate("FormSTADIC", "Lighting Energy:", None))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 4, 2, 1, 1)
        self.TabDMtrEgyChkB = QtGui.QCheckBox(self.TabDMtr)
        self.TabDMtrEgyChkB.setText(_fromUtf8(""))
        Grid1.addWidget(self.TabDMtrEgyChkB, 4, 3, 1, 1)
        cboxsta=lambda: self.CheckState(self.TabDMtrDAChkB,"Energy")
        self.TabDMtrEgyChkB.stateChanged.connect(cboxsta)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 4, 7, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 6, 2, 1, 1)

        MLbl = QtGui.QLabel(self.TabDMtr)
        Grid1.addWidget(MLbl, 7, 1, 1, 1)
        MLbl.setText(_translate("FormSTADIC", "DA", None))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 7, 2, 1, 1)
        self.TabDMtrDAChkB = QtGui.QCheckBox(self.TabDMtr)
        self.TabDMtrDAChkB.setText(_fromUtf8(""))
        Grid1.addWidget(self.TabDMtrDAChkB, 7, 3, 1, 1)
        cboxsta=lambda: self.CheckState(self.TabDMtrDAChkB,"DA")
        self.TabDMtrDAChkB.stateChanged.connect(cboxsta)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 7, 7, 1, 1)
        MLbl = QtGui.QLabel(self.TabDMtr)
        Grid1.addWidget(MLbl, 8, 1, 1, 1)
        MLbl.setText(_translate("FormSTADIC", "Target Illuminance:", None))
        self.TabDMtrDATgtLineEd = QtGui.QLineEdit(self.TabDMtr)
        Grid1.addWidget(self.TabDMtrDATgtLineEd, 8, 3, 1, 1)
        self.TabDMtrDATgtLineEd.setValidator(QtGui.QIntValidator(0,10000))
        MtrV=lambda: self.MtrValue(self.TabDMtrDATgtLineEd,"DA", "illuminance")
        self.TabDMtrDATgtLineEd.editingFinished.connect(MtrV)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 9, 1, 1, 1)
        MLbl = QtGui.QLabel(self.TabDMtr)
        Grid1.addWidget(MLbl, 10, 1, 1, 1)
        MLbl.setText(_translate("FormSTADIC", "cDA", None))
        self.TabDMtrcDAChkB = QtGui.QCheckBox(self.TabDMtr)
        self.TabDMtrcDAChkB.setText(_fromUtf8(""))
        Grid1.addWidget(self.TabDMtrcDAChkB, 10, 3, 1, 1)
        cboxsta=lambda: self.CheckState(self.TabDMtrcDAChkB,"cDA")
        self.TabDMtrcDAChkB.stateChanged.connect(cboxsta)
        MLbl = QtGui.QLabel(self.TabDMtr)
        Grid1.addWidget(MLbl, 11, 1, 1, 1)
        MLbl.setText(_translate("FormSTADIC", "Target Illuminance:", None))
        self.TabDMtrcDATgtLineEd = QtGui.QLineEdit(self.TabDMtr)
        self.TabDMtrcDATgtLineEd.setValidator(QtGui.QIntValidator(0,10000))
        Grid1.addWidget(self.TabDMtrcDATgtLineEd, 11, 3, 1, 1)
        MtrV=lambda: self.MtrValue(self.TabDMtrcDATgtLineEd,"cDA", "illuminance")
        self.TabDMtrcDATgtLineEd.editingFinished.connect(MtrV)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 12, 1, 1, 1)
        MLbl = QtGui.QLabel(self.TabDMtr)
        Grid1.addWidget(MLbl, 13, 1, 1, 1)
        MLbl.setText(_translate("FormSTADIC", "sDA", None))
        self.TabDMtrsDAChkB = QtGui.QCheckBox(self.TabDMtr)
        self.TabDMtrsDAChkB.setText(_fromUtf8(""))
        Grid1.addWidget(self.TabDMtrsDAChkB, 13, 3, 1, 1)
        cboxsta=lambda: self.CheckState(self.TabDMtrsDAChkB,"sDA")
        self.TabDMtrsDAChkB.stateChanged.connect(cboxsta)
        MLbl = QtGui.QLabel(self.TabDMtr)
        Grid1.addWidget(MLbl, 14, 1, 1, 1)
        MLbl.setText(_translate("FormSTADIC", "Target Illuminance:", None))
        self.TabDMtrsDATgtLineEd = QtGui.QLineEdit(self.TabDMtr)
        Grid1.addWidget(self.TabDMtrsDATgtLineEd, 14, 3, 1, 1)
        self.TabDMtrsDATgtLineEd.setValidator(QtGui.QIntValidator(0,10000))
        MtrV=lambda: self.MtrValue(self.TabDMtrsDATgtLineEd,"sDA", "illuminance")
        self.TabDMtrsDATgtLineEd.editingFinished.connect(MtrV)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 14, 4, 1, 1)
        MLbl = QtGui.QLabel(self.TabDMtr)
        Grid1.addWidget(MLbl, 14, 5, 1, 1)
        MLbl.setText(_translate("FormSTADIC", "DA Fraction:", None))
        self.TabDMtrsDAFrcLineEd = QtGui.QLineEdit(self.TabDMtr)
        Grid1.addWidget(self.TabDMtrsDAFrcLineEd, 14, 6, 1, 1)
        MtrV=lambda: self.MtrValue(self.TabDMtrsDAFrcLineEd,"sDA", "DA_fraction")
        self.TabDMtrsDAFrcLineEd.editingFinished.connect(MtrV)
        MLbl = QtGui.QLabel(self.TabDMtr)
        Grid1.addWidget(MLbl, 15, 1, 1, 1)
        MLbl.setText(_translate("FormSTADIC", "Start Time:", None))
        self.TabDMtrsDASTmLineEd = QtGui.QLineEdit(self.TabDMtr)
        Grid1.addWidget(self.TabDMtrsDASTmLineEd, 15, 3, 1, 1)
        self.TabDMtrsDASTmLineEd.setValidator(QtGui.QIntValidator(0,24))
        MtrV=lambda: self.MtrValue(self.TabDMtrsDASTmLineEd,"sDA", "start_time")
        self.TabDMtrsDASTmLineEd.editingFinished.connect(MtrV)
        MLbl = QtGui.QLabel(self.TabDMtr)
        Grid1.addWidget(MLbl, 15, 5, 1, 1)
        MLbl.setText(_translate("FormSTADIC", "End Time:", None))
        self.TabDMtrsDAETmLineEd = QtGui.QLineEdit(self.TabDMtr)
        self.TabDMtrsDAETmLineEd.setValidator(QtGui.QIntValidator(0,24))
        Grid1.addWidget(self.TabDMtrsDAETmLineEd, 15, 6, 1, 1)
        MtrV=lambda: self.MtrValue(self.TabDMtrsDAETmLineEd,"sDA", "end_time")
        self.TabDMtrsDAETmLineEd.editingFinished.connect(MtrV)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 16, 1, 1, 1)
        MLbl = QtGui.QLabel(self.TabDMtr)
        Grid1.addWidget(MLbl, 17, 1, 1, 1)
        MLbl.setText(_translate("FormSTADIC", "Occupied sDA", None))
        self.TabDMtrOsDAChkB = QtGui.QCheckBox(self.TabDMtr)
        self.TabDMtrOsDAChkB.setText(_fromUtf8(""))
        Grid1.addWidget(self.TabDMtrOsDAChkB, 17, 3, 1, 1)
        cboxsta=lambda: self.CheckState(self.TabDMtrOsDAChkB,"occupied_sDA")
        self.TabDMtrOsDAChkB.stateChanged.connect(cboxsta)
        MLbl = QtGui.QLabel(self.TabDMtr)
        Grid1.addWidget(MLbl, 18, 1, 1, 1)
        MLbl.setText(_translate("FormSTADIC", "Target Illuminance:", None))
        self.TabDMtrOsDATgtLineEd = QtGui.QLineEdit(self.TabDMtr)
        Grid1.addWidget(self.TabDMtrOsDATgtLineEd, 18, 3, 1, 1)
        self.TabDMtrOsDATgtLineEd.setValidator(QtGui.QIntValidator(0,10000))
        MtrV=lambda: self.MtrValue(self.TabDMtrOsDATgtLineEd,"occupied_sDA", "illuminance")
        self.TabDMtrOsDATgtLineEd.editingFinished.connect(MtrV)
        MLbl = QtGui.QLabel(self.TabDMtr)
        Grid1.addWidget(MLbl, 18, 5, 1, 1)
        MLbl.setText(_translate("FormSTADIC", "DA Fraction:", None))
        self.TabDMtrOsDAFrcLineEd = QtGui.QLineEdit(self.TabDMtr)
        Grid1.addWidget(self.TabDMtrOsDAFrcLineEd, 18, 6, 1, 1)
        MtrV=lambda: self.MtrValue(self.TabDMtrOsDAFrcLineEd,"occupied_sDA", "DA_fraction")
        self.TabDMtrOsDAFrcLineEd.editingFinished.connect(MtrV)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 19, 1, 1, 1)
        MLbl = QtGui.QLabel(self.TabDMtr)
        Grid1.addWidget(MLbl, 20, 1, 1, 1)
        MLbl.setText(_translate("FormSTADIC", "DF", None))
        self.TabDMtrDFChkB = QtGui.QCheckBox(self.TabDMtr)
        self.TabDMtrDFChkB.setText(_fromUtf8(""))
        Grid1.addWidget(self.TabDMtrDFChkB, 20, 3, 1, 1)
        cboxsta=lambda: self.CheckState(self.TabDMtrDFChkB,"DF")
        self.TabDMtrDFChkB.stateChanged.connect(cboxsta)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 21, 1, 1, 1)
        MLbl= QtGui.QLabel(self.TabDMtr)
        Grid1.addWidget(MLbl, 22, 1, 1, 1)
        MLbl.setText(_translate("FormSTADIC", "UDI", None))
        self.TabDMtrUDIChkB = QtGui.QCheckBox(self.TabDMtr)
        self.TabDMtrUDIChkB.setText(_fromUtf8(""))
        Grid1.addWidget(self.TabDMtrUDIChkB, 22, 3, 1, 1)
        cboxsta=lambda: self.CheckState(self.TabDMtrUDIChkB,"UDI")
        self.TabDMtrUDIChkB.stateChanged.connect(cboxsta)
        MLbl = QtGui.QLabel(self.TabDMtr)
        MLbl.setText(_translate("FormSTADIC", "Minimum:", None))
        Grid1.addWidget(MLbl, 23, 1, 1, 1)
        self.TabDMtrUDIMinLineEd = QtGui.QLineEdit(self.TabDMtr)
        self.TabDMtrUDIMinLineEd.setValidator(QtGui.QIntValidator(0,10000))
        Grid1.addWidget(self.TabDMtrUDIMinLineEd, 23, 3, 1, 1)
        MtrV=lambda: self.MtrValue(self.TabDMtrUDIMinLineEd,"UDI", "minimum")
        self.TabDMtrUDIMinLineEd.editingFinished.connect(MtrV)
        MLbl = QtGui.QLabel(self.TabDMtr)
        Grid1.addWidget(MLbl, 23, 5, 1, 1)
        MLbl.setText(_translate("FormSTADIC", "Maximum:", None))
        self.TabDMtrUDIMaxLineEd = QtGui.QLineEdit(self.TabDMtr)
        self.TabDMtrUDIMaxLineEd.setValidator(QtGui.QIntValidator(0,10000))
        Grid1.addWidget(self.TabDMtrUDIMaxLineEd, 23, 6, 1, 1)
        MtrV=lambda: self.MtrValue(self.TabDMtrUDIMaxLineEd,"UDI", "maximum")
        self.TabDMtrUDIMaxLineEd.editingFinished.connect(MtrV)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        Grid1.addItem(spacerItem, 24, 1, 1, 1)


        ##Tab9: Simulation
        self.TabSimu = QtGui.QWidget()
        self.StadicTab.addTab(self.TabSimu, _fromUtf8("SIMULATION"))
        self.StadicTab.setTabToolTip(self.StadicTab.indexOf(self.TabSimu),"Simulation Parameters")
        HLayout = QtGui.QHBoxLayout(self.TabSimu)
        Scroll=QtGui.QScrollArea()
        Scroll.setWidgetResizable(1)
        HLayout.addWidget(Scroll)
        AreaContents=QtGui.QWidget()
        AreaContents.setGeometry(QtCore.QRect(0,0,1400,600))
        HHLayout= QtGui.QHBoxLayout(AreaContents)
        Scroll.setWidget(AreaContents)

        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        HHLayout.addItem(spacerItem)
        V1Layout=QtGui.QVBoxLayout()
        HHLayout.addLayout(V1Layout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        V1Layout.addItem(spacerItem)
        SMLbl = QtGui.QLabel()
        V1Layout.addWidget(SMLbl)
        SMLbl.setText(_translate("FormSTADIC", "Radiance Parameters:", None))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        V1Layout.addItem(spacerItem)
        Grid2 = QtGui.QGridLayout()
        V1Layout.addLayout(Grid2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem,0,0,1,1)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,0,4,1,1)
        SMLbl.setText(_translate("FormSTADIC", "Sky Division:", None))
        SMLbl.setFixedWidth(120)
        self.TabSimuSkyDivLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuSkyDivLineEd,0,6,1,1)
        self.TabSimuSkyDivLineEd.setFixedWidth(100)
        self.TabSimuSkyDivLineEd.setValidator(QtGui.QIntValidator(0,1000000))
        self.TabSimuSkyDivLineEd.setToolTip("No more than 20 divisions")
        simupara=lambda: self.simuWrite(self.TabSimuSkyDivLineEd,0,"","sky_divisions","int")
        self.TabSimuSkyDivLineEd.editingFinished.connect(simupara)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem,0,7,1,1)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,0,8,1,1)
        SMLbl.setText(_translate("FormSTADIC", "Sun Division:", None))
        SMLbl.setFixedWidth(120)
        self.TabSimuSunDivLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuSunDivLineEd,0,10,1,1)
        self.TabSimuSunDivLineEd.setFixedWidth(100)
        self.TabSimuSunDivLineEd.setValidator(QtGui.QIntValidator(0,1000000))
        self.TabSimuSunDivLineEd.setToolTip("No more than 20 divisions")
        simupara=lambda: self.simuWrite(self.TabSimuSunDivLineEd,0,"","sun_divisions","int")
        self.TabSimuSunDivLineEd.editingFinished.connect(simupara)
        spacerItem = QtGui.QSpacerItem(120, 40, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 0, 11, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 0, 14, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 1, 0, 1, 1)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,2,1,1,1)
        SMLbl.setText(_translate("FormSTADIC", "VMX:", None))
        SMLbl.setFixedWidth(100)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,2,2,1,1)
        SMLbl.setText(_translate("FormSTADIC", "ab:", None))
        self.TabSimuVabLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuVabLineEd,2,3,1,1)
        self.TabSimuVabLineEd.setFixedWidth(100)
        self.TabSimuVabLineEd.setValidator(QtGui.QIntValidator(0,1000000))
        SMLbl.setToolTip("No more than 20 bounces")
        simupara=lambda: self.simuWrite(self.TabSimuVabLineEd,1,"vmx","ab","int")
        self.TabSimuVabLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,2,5,1,1)
        SMLbl.setText(_translate("FormSTADIC", "ad:", None))
        self.TabSimuVadLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuVadLineEd,2,6,1,1)
        self.TabSimuVadLineEd.setFixedWidth(100)
        self.TabSimuVadLineEd.setValidator(QtGui.QIntValidator(0,1000000000))
        SMLbl.setToolTip("No more than 1000000")
        simupara=lambda: self.simuWrite(self.TabSimuVadLineEd,1,"vmx","ad","int")
        self.TabSimuVadLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl, 2, 8, 1, 1)
        SMLbl.setText("Default:")
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl, 2, 9, 1, 1)
        SMLbl.setText("ab:")
        SMLbl.setToolTip("No more than 20 bounces")
        self.TabSimuDefabLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDefabLineEd,2,10,1,1)
        self.TabSimuDefabLineEd.setFixedWidth(100)
        self.TabSimuDefabLineEd.setValidator(QtGui.QIntValidator(0,100000))
        simupara=lambda: self.simuWrite(self.TabSimuDefabLineEd,1,"default","ab","int")
        self.TabSimuDefabLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl, 2, 12, 1, 1)
        SMLbl.setText("ad:")
        self.TabSimuDefadLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDefadLineEd,2,13,1,1)
        self.TabSimuDefadLineEd.setFixedWidth(100)
        self.TabSimuDefadLineEd.setValidator(QtGui.QIntValidator(0,100000000))
        simupara=lambda: self.simuWrite(self.TabSimuDefadLineEd,1,"default","ad","int")
        self.TabSimuDefadLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,3,2,1,1)
        SMLbl.setText(_translate("FormSTADIC", "as:", None))
        self.TabSimuVasLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuVasLineEd,3,3,1,1)
        self.TabSimuVasLineEd.setFixedWidth(100)
        self.TabSimuVasLineEd.setValidator(QtGui.QIntValidator(0,1000000))
        SMLbl.setToolTip("No more than 1000000")
        simupara=lambda: self.simuWrite(self.TabSimuVasLineEd,1,"vmx","as","int")
        self.TabSimuVasLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,3,5,1,1)
        SMLbl.setText(_translate("FormSTADIC", "ar:", None))
        self.TabSimuVarLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuVarLineEd,3,6,1,1)
        self.TabSimuVarLineEd.setFixedWidth(100)
        self.TabSimuVarLineEd.setValidator(QtGui.QIntValidator(0,1000000))
        SMLbl.setToolTip("No more than 1000000")
        simupara=lambda: self.simuWrite(self.TabSimuVarLineEd,1,"vmx","ar","int")
        self.TabSimuVarLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl, 3, 9, 1, 1)
        SMLbl.setText("as:")
        self.TabSimuDefasLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDefasLineEd,3,10,1,1)
        self.TabSimuDefasLineEd.setFixedWidth(100)
        self.TabSimuDefasLineEd.setValidator(QtGui.QIntValidator(0,1000000))
        simupara=lambda: self.simuWrite(self.TabSimuDefasLineEd,1,"default","as","int")
        self.TabSimuDefasLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl, 3, 12, 1, 1)
        SMLbl.setText("ar:")
        self.TabSimuDefarLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDefarLineEd,3,13,1,1)
        self.TabSimuDefarLineEd.setFixedWidth(100)
        self.TabSimuDefarLineEd.setValidator(QtGui.QIntValidator(0,1000000))
        simupara=lambda: self.simuWrite(self.TabSimuDefarLineEd,1,"default","ar","int")
        self.TabSimuDefarLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,4,2,1,1)
        SMLbl.setText(_translate("FormSTADIC", "aa:", None))
        self.TabSimuVaaLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuVaaLineEd,4,3,1,1)
        self.TabSimuVaaLineEd.setFixedWidth(100)
        self.TabSimuVaaLineEd.setValidator(QtGui.QDoubleValidator(0,1,15))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuVaaLineEd,1,"vmx","aa","float")
        self.TabSimuVaaLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,4,5,1,1)
        SMLbl.setText(_translate("FormSTADIC", "lr:", None))
        self.TabSimuVlrLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuVlrLineEd,4,6,1,1)
        self.TabSimuVlrLineEd.setFixedWidth(100)
        self.TabSimuVlrLineEd.setValidator(QtGui.QIntValidator(0,100000))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuVlrLineEd,1,"vmx","lr","int")
        self.TabSimuVlrLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl, 4, 9, 1, 1)
        SMLbl.setText("aa:")
        self.TabSimuDefaaLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDefaaLineEd,4,10,1,1)
        self.TabSimuDefaaLineEd.setFixedWidth(100)
        self.TabSimuDefaaLineEd.setValidator(QtGui.QDoubleValidator(0,1,15))
        simupara=lambda: self.simuWrite(self.TabSimuDefaaLineEd,1,"default","aa","float")
        self.TabSimuDefaaLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl, 4, 12, 1, 1)
        SMLbl.setText("lr:")
        self.TabSimuDeflrLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDeflrLineEd,4,13,1,1)
        self.TabSimuDeflrLineEd.setFixedWidth(100)
        self.TabSimuDeflrLineEd.setValidator(QtGui.QIntValidator(0,1000000))
        simupara=lambda: self.simuWrite(self.TabSimuDeflrLineEd,1,"default","lr","int")
        self.TabSimuDeflrLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,5,2,1,1)
        SMLbl.setText(_translate("FormSTADIC", "st:", None))
        self.TabSimuVstLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuVstLineEd,5,3,1,1)
        self.TabSimuVstLineEd.setFixedWidth(100)
        self.TabSimuVstLineEd.setValidator(QtGui.QDoubleValidator(0,1,15))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuVstLineEd,1,"vmx","st","float")
        self.TabSimuVstLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,5,5,1,1)
        SMLbl.setText(_translate("FormSTADIC", "sj:", None))
        self.TabSimuVsjLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuVsjLineEd,5,6,1,1)
        self.TabSimuVsjLineEd.setFixedWidth(100)
        self.TabSimuVsjLineEd.setValidator(QtGui.QDoubleValidator(0,5,15))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuVsjLineEd,1,"vmx","sj","float")
        self.TabSimuVsjLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl, 5, 9, 1, 1)
        SMLbl.setText("st:")
        self.TabSimuDefstLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDefstLineEd,5,10,1,1)
        self.TabSimuDefstLineEd.setFixedWidth(100)
        self.TabSimuDefstLineEd.setValidator(QtGui.QDoubleValidator(0,1,15))
        simupara=lambda: self.simuWrite(self.TabSimuDefstLineEd,1,"default","st","float")
        self.TabSimuDefstLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl, 5, 12, 1, 1)
        SMLbl.setText("sj:")
        self.TabSimuDefsjLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDefsjLineEd,5,13,1,1)
        self.TabSimuDefsjLineEd.setFixedWidth(100)
        self.TabSimuDefsjLineEd.setValidator(QtGui.QDoubleValidator(0,5,15))
        simupara=lambda: self.simuWrite(self.TabSimuDefsjLineEd,1,"default","sj","float")
        self.TabSimuDefsjLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,6,2,1,1)
        SMLbl.setText(_translate("FormSTADIC", "lw:", None))
        self.TabSimuVlwLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuVlwLineEd,6,3,1,1)
        self.TabSimuVlwLineEd.setFixedWidth(100)
        self.TabSimuVlwLineEd.setValidator(QtGui.QDoubleValidator(0,1,15))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuVlwLineEd,1,"vmx","lw","float")
        self.TabSimuVlwLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,6,5,1,1)
        SMLbl.setText(_translate("FormSTADIC", "dj:", None))
        self.TabSimuVdjLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuVdjLineEd,6,6,1,1)
        self.TabSimuVdjLineEd.setFixedWidth(100)
        self.TabSimuVdjLineEd.setValidator(QtGui.QDoubleValidator(0,5,15))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuVdjLineEd,1,"vmx","dj","float")
        self.TabSimuVdjLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl, 6, 9, 1, 1)
        SMLbl.setText("lw:")
        self.TabSimuDeflwLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDeflwLineEd, 6,10,1,1)
        self.TabSimuDeflwLineEd.setFixedWidth(100)
        self.TabSimuDeflwLineEd.setValidator(QtGui.QDoubleValidator(0,1,15))
        simupara=lambda: self.simuWrite(self.TabSimuDeflwLineEd,1,"default","lw","float")
        self.TabSimuDeflwLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl, 6, 12, 1, 1)
        SMLbl.setText("dj:")
        self.TabSimuDefdjLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDefdjLineEd,6,13,1,1)
        self.TabSimuDefdjLineEd.setFixedWidth(100)
        self.TabSimuDefdjLineEd.setValidator(QtGui.QDoubleValidator(0,5,15))
        simupara=lambda: self.simuWrite(self.TabSimuDefdjLineEd,1,"default","dj","float")
        self.TabSimuDefdjLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,7,2,1,1)
        SMLbl.setText(_translate("FormSTADIC", "ds:", None))
        self.TabSimuVdsLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuVdsLineEd,7,3,1,1)
        self.TabSimuVdsLineEd.setFixedWidth(100)
        self.TabSimuVdsLineEd.setValidator(QtGui.QDoubleValidator(0,1,15))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuVdsLineEd,1,"vmx","ds","float")
        self.TabSimuVdsLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,7,5,1,1)
        SMLbl.setText(_translate("FormSTADIC", "dr:", None))
        self.TabSimuVdrLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuVdrLineEd,7,6,1,1)
        self.TabSimuVdrLineEd.setFixedWidth(100)
        self.TabSimuVdrLineEd.setValidator(QtGui.QIntValidator(0,1000000))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuVdrLineEd,1,"vmx","dr","int")
        self.TabSimuVdrLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl, 7, 9, 1, 1)
        SMLbl.setText("ds:")
        self.TabSimuDefdsLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDefdsLineEd,7,10,1,1)
        self.TabSimuDefdsLineEd.setFixedWidth(100)
        self.TabSimuDefdsLineEd.setValidator(QtGui.QDoubleValidator(0,1,15))
        simupara=lambda: self.simuWrite(self.TabSimuDefdsLineEd,1,"default","ds","float")
        self.TabSimuDefdsLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl, 7, 12, 1, 1)
        SMLbl.setText("dr:")
        self.TabSimuDefdrLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDefdrLineEd,7,13,1,1)
        self.TabSimuDefdrLineEd.setFixedWidth(100)
        self.TabSimuDefdrLineEd.setValidator(QtGui.QIntValidator(0,100000))
        simupara=lambda: self.simuWrite(self.TabSimuDefdrLineEd,1,"default","dr","int")
        self.TabSimuDefdrLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,8,2,1,1)
        SMLbl.setText(_translate("FormSTADIC", "dp:", None))
        self.TabSimuVdpLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuVdpLineEd,8,3,1,1)
        self.TabSimuVdpLineEd.setFixedWidth(100)
        self.TabSimuVdpLineEd.setValidator(QtGui.QDoubleValidator(0,5,15))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuVdpLineEd,1,"vmx","dp","float")
        self.TabSimuVdpLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,8,5,1,1)
        SMLbl.setText(_translate("FormSTADIC", "dc:", None))
        self.TabSimuVdcLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuVdcLineEd,8,6,1,1)
        self.TabSimuVdcLineEd.setFixedWidth(100)
        self.TabSimuVdcLineEd.setValidator(QtGui.QDoubleValidator(0,5,15))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuVdcLineEd,1,"vmx","dc","float")
        self.TabSimuVdcLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl, 8, 9, 1, 1)
        SMLbl.setText("dp:")
        self.TabSimuDefdpLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDefdpLineEd,8,10,1,1)
        self.TabSimuDefdpLineEd.setFixedWidth(100)
        self.TabSimuDefdpLineEd.setValidator(QtGui.QDoubleValidator(0,5,15))
        simupara=lambda: self.simuWrite(self.TabSimuDefdpLineEd,1,"default","dp","float")
        self.TabSimuDefdpLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl, 8, 12, 1, 1)
        SMLbl.setText("dc:")
        self.TabSimuDefdcLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDefdcLineEd,8,13,1,1)
        self.TabSimuDefdcLineEd.setFixedWidth(100)
        self.TabSimuDefdcLineEd.setValidator(QtGui.QDoubleValidator(0,5,15))
        simupara=lambda: self.simuWrite(self.TabSimuDefdcLineEd,1,"default","dc","float")
        self.TabSimuDefdcLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,9,2,1,1)
        SMLbl.setText(_translate("FormSTADIC", "dt:", None))
        self.TabSimuVdtLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuVdtLineEd,9,3,1,1)
        self.TabSimuVdtLineEd.setFixedWidth(100)
        self.TabSimuVdtLineEd.setValidator(QtGui.QDoubleValidator(0,1,15))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuVdtLineEd,1,"vmx","dt","float")
        self.TabSimuVdtLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl, 9, 9, 1, 1)
        SMLbl.setText("dt:")
        self.TabSimuDefdtLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDefdtLineEd,9,10,1,1)
        self.TabSimuDefdtLineEd.setFixedWidth(100)
        self.TabSimuDefdtLineEd.setValidator(QtGui.QDoubleValidator(0,1,15))
        simupara=lambda: self.simuWrite(self.TabSimuDefdtLineEd,1,"default","dt","float")
        self.TabSimuDefdtLineEd.editingFinished.connect(simupara)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem, 10, 0, 1, 1)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,11,1,1,1)
        SMLbl.setText(_translate("FormSTADIC", "DMX:", None))
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,11,2,1,1)
        SMLbl.setText(_translate("FormSTADIC", "ab:", None))
        self.TabSimuDabLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDabLineEd,11,3,1,1)
        self.TabSimuDabLineEd.setFixedWidth(100)
        self.TabSimuDabLineEd.setValidator(QtGui.QIntValidator(0,1000000))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuDabLineEd,1,"dmx","ab","int")
        self.TabSimuDabLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,11,5,1,1)
        SMLbl.setText(_translate("FormSTADIC", "ad:", None))
        self.TabSimuDadLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDadLineEd,11,6,1,1)
        self.TabSimuDadLineEd.setFixedWidth(100)
        self.TabSimuDadLineEd.setValidator(QtGui.QIntValidator(0,1000000000))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuDadLineEd,1,"dmx","ad","int")
        self.TabSimuDadLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,12,2,1,1)
        SMLbl.setText(_translate("FormSTADIC", "as:", None))
        self.TabSimuDasLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDasLineEd,12,3,1,1)
        self.TabSimuDasLineEd.setFixedWidth(100)
        self.TabSimuDasLineEd.setValidator(QtGui.QIntValidator(0,1000000))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuDasLineEd,1,"dmx","as","int")
        self.TabSimuDasLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,12,5,1,1)
        SMLbl.setText(_translate("FormSTADIC", "ar:", None))
        self.TabSimuDarLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDarLineEd,12,6,1,1)
        self.TabSimuDarLineEd.setFixedWidth(100)
        self.TabSimuDarLineEd.setValidator(QtGui.QIntValidator(0,1000000))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuDarLineEd,1,"dmx","ar","int")
        self.TabSimuDarLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,13,2,1,1)
        SMLbl.setText(_translate("FormSTADIC", "aa:", None))
        self.TabSimuDaaLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDaaLineEd,13,3,1,1)
        self.TabSimuDaaLineEd.setFixedWidth(100)
        self.TabSimuDaaLineEd.setValidator(QtGui.QDoubleValidator(0,1,15))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuDaaLineEd,1,"dmx","aa","float")
        self.TabSimuDaaLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,13,5,1,1)
        SMLbl.setText(_translate("FormSTADIC", "lr:", None))
        self.TabSimuDlrLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDlrLineEd,13,6,1,1)
        self.TabSimuDlrLineEd.setFixedWidth(100)
        self.TabSimuDlrLineEd.setValidator(QtGui.QIntValidator(0,1000000))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuDlrLineEd,1,"dmx","lr","int")
        self.TabSimuDlrLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,14,2,1,1)
        SMLbl.setText(_translate("FormSTADIC", "st:", None))
        self.TabSimuDstLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDstLineEd,14,3,1,1)
        self.TabSimuDstLineEd.setFixedWidth(100)
        self.TabSimuDstLineEd.setValidator(QtGui.QDoubleValidator(0,1,15))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuDstLineEd,1,"dmx","st","float")
        self.TabSimuDstLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,14,5,1,1)
        SMLbl.setText(_translate("FormSTADIC", "sj:", None))
        self.TabSimuDsjLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDsjLineEd,14,6,1,1)
        self.TabSimuDsjLineEd.setFixedWidth(100)
        self.TabSimuDsjLineEd.setValidator(QtGui.QDoubleValidator(0,5,15))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuDsjLineEd,1,"dmx","sj","float")
        self.TabSimuDsjLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,15,2,1,1)
        SMLbl.setText(_translate("FormSTADIC", "lw:", None))
        self.TabSimuDlwLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDlwLineEd,15,3,1,1)
        self.TabSimuDlwLineEd.setFixedWidth(100)
        v=QtGui.QDoubleValidator()
        v.setRange(0.0,1.0,15)
        v.setNotation(QtGui.QDoubleValidator.StandardNotation)
        self.TabSimuDlwLineEd.setValidator(v)
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuDlwLineEd,1,"dmx","lw","float")
        self.TabSimuDlwLineEd.editingFinished.connect(simupara)

        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,15,5,1,1)
        SMLbl.setText(_translate("FormSTADIC", "dj:", None))
        self.TabSimuDdjLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDdjLineEd,15,6,1,1)
        self.TabSimuDdjLineEd.setFixedWidth(100)
        self.TabSimuDdjLineEd.setValidator(QtGui.QDoubleValidator(0,5,15))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuDdjLineEd,1,"dmx","dj","float")
        self.TabSimuDdjLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,16,2,1,1)
        SMLbl.setText(_translate("FormSTADIC", "ds:", None))
        self.TabSimuDdsLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDdsLineEd,16,3,1,1)
        self.TabSimuDdsLineEd.setFixedWidth(100)
        self.TabSimuDdsLineEd.setValidator(QtGui.QDoubleValidator(0,1,15))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuDdsLineEd,1,"dmx","ds","float")
        self.TabSimuDdsLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,16,5,1,1)
        SMLbl.setText(_translate("FormSTADIC", "dr:", None))
        self.TabSimuDdrLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDdrLineEd,16,6,1,1)
        self.TabSimuDdrLineEd.setFixedWidth(100)
        self.TabSimuDdrLineEd.setValidator(QtGui.QIntValidator(0,100000))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuDdrLineEd,1,"dmx","dr","int")
        self.TabSimuDdrLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,17,2,1,1)
        SMLbl.setText(_translate("FormSTADIC", "dp:", None))
        self.TabSimuDdpLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDdpLineEd,17,3,1,1)
        self.TabSimuDdpLineEd.setFixedWidth(100)
        self.TabSimuDdpLineEd.setValidator(QtGui.QDoubleValidator(0,5,15))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuDdpLineEd,1,"dmx","dp","float")
        self.TabSimuDdpLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,17,5,1,1)
        SMLbl.setText(_translate("FormSTADIC", "dc:", None))
        self.TabSimuDdcLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDdcLineEd,17,6,1,1)
        self.TabSimuDdcLineEd.setFixedWidth(100)
        self.TabSimuDdcLineEd.setValidator(QtGui.QDoubleValidator(0,5,15))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuDdcLineEd,1,"dmx","dc","float")
        self.TabSimuDdcLineEd.editingFinished.connect(simupara)
        SMLbl=QtGui.QLabel(self.TabSimu)
        Grid2.addWidget(SMLbl,18,2,1,1)
        SMLbl.setText(_translate("FormSTADIC", "dt:", None))
        self.TabSimuDdtLineEd=QtGui.QLineEdit(self.TabSimu)
        Grid2.addWidget(self.TabSimuDdtLineEd,18,3,1,1)
        self.TabSimuDdtLineEd.setFixedWidth(100)
        self.TabSimuDdtLineEd.setValidator(QtGui.QDoubleValidator(0,1,15))
        SMLbl.setToolTip("")
        simupara=lambda: self.simuWrite(self.TabSimuDdtLineEd,1,"dmx","dt","float")
        self.TabSimuDdtLineEd.editingFinished.connect(simupara)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid2.addItem(spacerItem,19,0,1,1)
        H2Layout=QtGui.QHBoxLayout()
        V1Layout.addLayout(H2Layout)
        SMLbl=QtGui.QLabel("Automatic Reset Path and RayPath:")
        H2Layout.addWidget(SMLbl)
        self.TabSimuCbx = QtGui.QCheckBox()
        H2Layout.addWidget(self.TabSimuCbx)
        self.TabSimuCbx.setChecked(1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        H2Layout.addItem(spacerItem)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        V1Layout.addItem(spacerItem)
        H2Layout=QtGui.QHBoxLayout()
        V1Layout.addLayout(H2Layout)
        self.TabSimuStartBtn = QtGui.QPushButton(self.TabSimu)
        H2Layout.addWidget(self.TabSimuStartBtn)
        self.TabSimuStartBtn.setText(_translate("FormSTADIC", "Start Full Simulation", None))
        self.TabSimuPShadeBtn = QtGui.QPushButton(self.TabSimu)
        H2Layout.addWidget(self.TabSimuPShadeBtn)
        self.TabSimuPShadeBtn.setText(_translate("FormSTADIC", "Process Shade and Metrics", None))
        self.TabSimuPMtrBtn = QtGui.QPushButton(self.TabSimu)
        H2Layout.addWidget(self.TabSimuPMtrBtn)
        self.TabSimuPMtrBtn.setText(_translate("FormSTADIC", "Process Metrics", None))
        self.TabSimuElecBtn = QtGui.QPushButton(self.TabSimu)
        H2Layout.addWidget(self.TabSimuElecBtn)
        self.TabSimuElecBtn.setText(_translate("FormSTADIC", "Calc Electric Lighitng", None))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        V1Layout.addItem(spacerItem)
        self.TabSimuStartBtn.clicked.connect(self.simurun)
        self.TabSimuPShadeBtn.clicked.connect(self.PShade)
        self.TabSimuPMtrBtn.clicked.connect(self.PMtr)
        self.TabSimuElecBtn.clicked.connect(self.PElec)


        ##Tab10: Output
        self.TabOutput = QtGui.QWidget()
        self.StadicTab.addTab(self.TabOutput, _fromUtf8("OUTPUT"))
        self.StadicTab.setTabToolTip(self.StadicTab.indexOf(self.TabOutput),"Please find your output here!")
        HLayout = QtGui.QHBoxLayout(self.TabOutput)
        Scroll=QtGui.QScrollArea()
        Scroll.setWidgetResizable(1)
        HLayout.addWidget(Scroll)
        AreaContents=QtGui.QWidget()
        AreaContents.setGeometry(QtCore.QRect(0,0,1400,600))
        V1Layout= QtGui.QVBoxLayout(AreaContents)
        Scroll.setWidget(AreaContents)
        Grid1=QtGui.QGridLayout()
        V1Layout.addLayout(Grid1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 0, 1, 1, 1)
        Lbl=QtGui.QLabel("Numerical Summary:")
        Grid1.addWidget(Lbl, 1, 1, 1, 1)
        Lbl=QtGui.QLabel("Project:")
        Grid1.addWidget(Lbl, 2, 1, 1, 1)
        self.outputpjn=QtGui.QLabel("")
        Grid1.addWidget(self.outputpjn, 2, 2, 1, 1)
        self.PrjSmryBtn=QtGui.QPushButton("View Results")
        Grid1.addWidget(self.PrjSmryBtn, 2, 3, 1, 1)
        self.PrjSmryBtn.clicked.connect(self.PrjSmry)
        Lbl=QtGui.QLabel("Space Name:")
        Lbl.setFixedWidth(120)
        Grid1.addWidget(Lbl, 3, 1, 1, 1)
        self.OutputSPCbx=QtGui.QComboBox()
        self.OutputSPCbx.setFixedWidth(180)
        Grid1.addWidget(self.OutputSPCbx, 3, 2, 1, 1)
        self.MtrOptBtn=QtGui.QPushButton("View Results")
        Grid1.addWidget(self.MtrOptBtn, 3, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Grid1.addItem(spacerItem, 4, 1, 1, 1)
        Lbl=QtGui.QLabel("Graphical Results:")
        Grid1.addWidget(Lbl, 5, 1, 1, 1)
        Lbl=QtGui.QLabel("Space Name:")
        Lbl.setFixedWidth(120)
        Grid1.addWidget(Lbl, 6, 1, 1, 1)
        self.OutputSPCbx2=QtGui.QComboBox()
        self.OutputSPCbx2.setFixedWidth(180)
        Grid1.addWidget(self.OutputSPCbx2, 6, 2, 1, 1)
        self.OutputBtn=QtGui.QPushButton()
        self.OutputBtn.setText("Launch")
        Grid1.addWidget(self.OutputBtn, 6, 3, 1, 1)

        # spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        # Grid1.addItem(spacerItem, 2, 0, 1, 1)
        # divider=QtGui.QFrame()
        # divider.setFrameStyle(QtGui.QFrame.HLine)
        # divider.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        # Grid1.addWidget(divider, 3, 0, 1, 6)

        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        Grid1.addItem(spacerItem, 7, 4, 1, 1)
        self.OutputBtn.clicked.connect(self.LaunchOutput)
        self.MtrOptBtn.clicked.connect(self.MtrOutput)
        ##Tab Initialization
        self.StadicTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FormSTADIC)

    ##Json File Creation and Initialization with some default parameters
    def JFCrtBtn(self):
        dir=os.path.normpath("c:\\")
        self.JFileName=QtGui.QFileDialog.getSaveFileName(self,"Create JSON File",dir,"JSON File (*.json)")
        if self.JFileName:
            self.setWindowTitle(_translate("FormSTADIC", "STADIC1.1-"+self.JFileName, None))
            self.TabFileJFLineEd.setText(self.JFileName)
            self.JF=open(self.JFileName,"w")
            self.JFData={}
            self.JFData["general"]={}
            self.JFData["general"]["first_day"]=1
            self.JFData["general"]["radiance_parameters"]={}
            self.JFData["general"]["sun_divisions"]=4
            self.JFData["general"]["sky_divisions"]=1
            self.JFData["general"]["daylight_savings_time"]=False
            self.JFData["general"]["building_rotation"]=0
            self.JFData["general"]["project_directory"]=os.path.dirname(str(self.JFileName))+"/"
            self.TabFileDirLineEd.setText(self.JFData["general"]["project_directory"])
            self.dir=str(self.JFData["general"]["project_directory"])
            self.FPCheck(self.dir)
            fname=self.dir+"rad/empty.rad"
            n=os.path.basename(str(self.JFileName))
            n=n[:-5]
            self.outputpjn.setText(n)
            self.outputpjn.setStyleSheet("color: rgb(0, 0, 255);")
            try:
                if not os.path.exists(fname):
                    radf=open(fname,"w")
                    radf.close()
            except:
                pass
            para=["default","dmx","vmx"]
            for item in para:
                self.JFData["general"]["radiance_parameters"][item]={}
                self.JFData["general"]["radiance_parameters"][item]["aa"]=0.1
                self.JFData["general"]["radiance_parameters"][item]["ab"]=3
                self.JFData["general"]["radiance_parameters"][item]["dj"]=0.0
                self.JFData["general"]["radiance_parameters"][item]["ad"]=10000
                self.JFData["general"]["radiance_parameters"][item]["lw"]=1e-9
                self.JFData["general"]["radiance_parameters"][item]["dc"]=1.0
                self.JFData["general"]["radiance_parameters"][item]["st"]=0.15
                self.JFData["general"]["radiance_parameters"][item]["sj"]=1.0
                self.JFData["general"]["radiance_parameters"][item]["as"]=256
                self.JFData["general"]["radiance_parameters"][item]["ar"]=150
                self.JFData["general"]["radiance_parameters"][item]["lr"]=6
                self.JFData["general"]["radiance_parameters"][item]["dt"]=0.5
                self.JFData["general"]["radiance_parameters"][item]["dr"]=2
                self.JFData["general"]["radiance_parameters"][item]["ds"]=0.2
                self.JFData["general"]["radiance_parameters"][item]["dp"]=1.0
            self.JFData["spaces"]=[]
            self.Backup()
            self.TabFileJFLineEd.setDisabled(1)
            self.TabFileJFBtn.setDisabled(1)
            self.TabFileJFCrtBtn.setDisabled(1)
            QtGui.QMessageBox.information(self,"Successful","File is successfully created")
            self.TabSDataSPComBox.currentIndexChanged.connect(self.TabSDataLoad)
            self.TabAnaSPNComBox.currentIndexChanged.connect(self.TabAnaLoad)
            self.TabWinSPNComBox.currentIndexChanged.connect(self.TabWinGLoad)
            self.TabElecSPComBox.currentIndexChanged.connect(self.TabElecLoad)
            self.TabCtrlSPNComBox.currentIndexChanged.connect(self.TabCtrlLoad)
            self.TabDMtrSPNComBox.currentIndexChanged.connect(self.TabMtrLoad)
            self.TabWinWGComBox.currentIndexChanged.connect(self.TabWinGCombo)
            self.TabFileLUnitsComBox.currentIndexChanged.connect(self.LUnitChange)
            IU=lambda: self.DUnitChange(self.TabFileDUnitComBox, "import_units")
            self.TabFileDUnitComBox.currentIndexChanged.connect(IU)
            DU=lambda: self.DUnitChange(self.TabFileDDUnitComBox, "display_units")
            self.TabFileDDUnitComBox.currentIndexChanged.connect(DU)
            # self.TabCtrlOptCComBox.currentIndexChanged.connect(self.ElecCtrlAlg)
            self.created=True
            self.SimuLoad()
            self.SaveAll()

    ##Create Backup File
    def Backup(self):
        self.tempdata=self.JFData
        self.JF.close()
        self.tpfname=self.JFileName+".bak"
        i=0
        while os.path.exists(self.tpfname):
            self.tpfname=self.JFileName+str(i)+".bak"
            i+=1
            if i>=100:
                QtGui.QMessageBox.warning(self,"Warning","Too many backup files! Backup File Named as %s" %self.tpfname)
                break
        self.WriteToFile()

    ##Write to Backup File
    def WriteToFile(self):
        self.tpfile=open(self.tpfname,"w")
        self.tpjson=json.dumps(self.tempdata,indent=4)
        self.tpfile.write(self.tpjson)
        self.tpfile.close()

    ##Save to Json File
    def SaveAll(self):
        try:
            self.JFData=self.tempdata
            self.JF=open(self.JFileName,"w")
            tpall=json.dumps(self.JFData,indent=4)
            self.JF.write(tpall)
            self.JF.close()
        except:
            pass


    def SaveAs(self):
        if self.created or self.imported:
            try:
                ddir=self.dir
            except:
                ddir=os.path.dirname(str(self.JFileName))

            tempfname=QtGui.QFileDialog.getSaveFileName(self,"Save AS",ddir,"JSON File (*.json)",options=QtGui.QFileDialog.DontResolveSymlinks)
            if tempfname:
                self.JFileName=tempfname
                self.JFData=self.tempdata
                self.JF=open(self.JFileName,"w")
                tpall=json.dumps(self.tempdata,indent=4)
                self.JF.write(tpall)
                self.JF.close()
                self.setWindowTitle(_translate("FormSTADIC", "STADIC1.1-"+self.JFileName, None))


    def FileDir(self):
        if self.imported or self.created:
            dir2=QtGui.QFileDialog.getExistingDirectory(self, "Set Project Path Directory", "c:/" , options=QtGui.QFileDialog.DontResolveSymlinks)
            if dir2:
                try:
                    dir1=self.tempdata["general"]["project_directory"]
                    self.SaveAll()
                    self.CopyFile(str(self.JFileName),str(dir2))
                    self.JFileName=str(dir2)+"/"+os.path.basename(str(self.JFileName))
                    self.TabFileJFLineEd.setText(str(self.JFileName))
                    self.setWindowTitle(_translate("FormSTADIC", "STADIC1.1-"+self.JFileName, None))
                    dir1_folders = [dir for dir in os.listdir(dir1) if os.path.isdir(os.path.join(dir1, dir))]
                    for dir in dir1_folders:
                        shutil.copytree(os.path.join(dir1, dir), os.path.join(str(dir2), dir))
                except:
                   pass
                spd=os.path.normpath(str(dir2))
                spdlist=spd.split("\\")
                cleanspd=spdlist[0]
                try:
                    for item in spdlist[1:]:
                        cleanspd=cleanspd+"/"+item
                except:
                    pass
                self.tempdata["general"]["project_directory"]=cleanspd+"/"
                self.WriteToFile()
                self.SaveAll()
                self.TabSDataSPComBox.clear()
                self.TabAnaSPNComBox.clear()
                self.TabWinSPNComBox.clear()
                self.TabElecSPComBox.clear()
                self.TabCtrlSPNComBox.clear()
                self.TabDMtrSPNComBox.clear()
                self.OutputSPCbx.clear()
                self.OutputSPCbx2.clear()
                self.JFImport()


    def JFBtn(self):
        dir=os.path.normpath("c:\\")
        self.JFileName= QtGui.QFileDialog.getOpenFileName(self,"Open JSON File",dir,"JSON File (*.json)")
        if self.JFileName:
            self.TabFileJFLineEd.setText(self.JFileName)
            self.imported=True
            self.JFImport()


    def prjpathChk(self):
        pdir=str(os.path.normpath(os.path.normcase(os.path.dirname(str(self.JFileName)))))
        try:
            sdir=str(os.path.normpath(os.path.normcase(os.path.dirname(self.tempdata["general"]["project_directory"]))))
            pdir=pdir.split("\\")
            sdir=sdir.split("\\")
            mark=0
            for i in range(len(sdir)):
                if sdir[i]!=pdir[i]:
                    mark=1
            if mark==1:
                QtGui.QMessageBox.warning(self,"warning", "Your JSON file is not in the same directory of your project!")
        except:
            pass


    ##Loading Tab File
    def JFImport(self):
        self.JF=open(self.JFileName,"r+")
        self.JFData=json.load(self.JF)
        self.Backup()
        self.TabFileJFLineEd.setDisabled(1)
        self.TabFileJFBtn.setDisabled(1)
        self.TabFileJFCrtBtn.setDisabled(1)
        self.setWindowTitle(_translate("FormSTADIC", "STADIC1.1-"+self.JFileName, None))
        n=os.path.basename(str(self.JFileName))
        n=n[:-5]
        self.outputpjn.setText(n)
        self.outputpjn.setStyleSheet("color: rgb(0, 0, 255);")



        try:
            self.DUnits=self.tempdata["general"]["import_units"]
            self.TabFileDUnitComBox.setCurrentIndex(self.dunits(self.DUnits))
            self.DDUnits=self.tempdata["general"]["display_units"]
            self.TabFileDDUnitComBox.setCurrentIndex(self.dunits(self.DDUnits))
            self.LUnits=self.tempdata["general"]["illum_units"]
            self.TabFileLUnitsComBox.setCurrentIndex(self.lunits(self.LUnits))
        except:
            pass
        try:
            self.TabFileDirLineEd.setText(str(self.tempdata["general"]["project_directory"]))
        except:
            self.tempdata["general"]["project_directory"]=os.path.dirname(str(self.JFileName))+"/"
            self.TabFileDirLineEd.setText(str(self.tempdata["general"]["project_directory"]))
        self.prjpathChk()
        self.TabFileLUnitsComBox.currentIndexChanged.connect(self.LUnitChange)
        self.dir=str(self.tempdata["general"]["project_directory"])
        self.FPCheck(self.dir)
        fname=self.dir+"rad/empty.rad"
        try:
            if not os.path.exists(fname):
                radf=open(fname,"w")
                radf.close()
        except:
            pass
        try:
            basep=self.tempdata["general"]["project_directory"]
            self.TabSiteWeaLineEd.setText(os.path.normpath(os.path.join(basep,str(self.tempdata["general"]["epw_file"]))))
        except:
            pass
        try:
            if self.tempdata["general"]["daylight_savings_time"]==True:
                self.TabSiteDaySChk.setChecked(1)
            else:
                self.TabSiteDaySChk.setChecked(0)
        except:
            self.tempdata["general"]["daylight_savings_time"]=False
            self.TabSiteDaySChk.setChecked(0)
        try:
            self.TabSiteGrdReflLineEd.setText(self.tempdata["general"]["ground_reflectance"])
        except:
            self.tempdata["general"]["ground_reflectance"]=0.2
            self.TabSiteGrdReflLineEd.setText(str(self.tempdata["general"]["ground_reflectance"]))
        count=0
        for item in self.tempdata["spaces"]:
            self.TabSDataSPComBox.addItem(item["space_name"])
            self.TabAnaSPNComBox.addItem(item["space_name"])
            self.TabWinSPNComBox.addItem(item["space_name"])
            self.TabElecSPComBox.addItem(item["space_name"])
            self.TabCtrlSPNComBox.addItem(item["space_name"])
            self.TabDMtrSPNComBox.addItem(item["space_name"])
            self.OutputSPCbx.addItem(item["space_name"])
            self.OutputSPCbx2.addItem(item["space_name"])
            count += 1
        self.TabSDataSPComBox.setCurrentIndex(0)
        self.TabDMtrSPNComBox.setCurrentIndex(0)
        self.WriteToFile()


        self.SimuLoad()
        self.JFLoad(0)
        self.TabSDataSPComBox.currentIndexChanged.connect(self.TabSDataLoad)
        self.TabAnaSPNComBox.currentIndexChanged.connect(self.TabAnaLoad)
        self.TabWinSPNComBox.currentIndexChanged.connect(self.TabWinGLoad)
        self.TabElecSPComBox.currentIndexChanged.connect(self.TabElecLoad)
        self.TabCtrlSPNComBox.currentIndexChanged.connect(self.TabCtrlLoad)
        self.TabDMtrSPNComBox.currentIndexChanged.connect(self.TabMtrLoad)
        self.TabWinWGComBox.currentIndexChanged.connect(self.TabWinGCombo)
        IU=lambda: self.DUnitChange(self.TabFileDUnitComBox, "import_units")
        self.TabFileDUnitComBox.currentIndexChanged.connect(IU)
        DU=lambda: self.DUnitChange(self.TabFileDDUnitComBox, "display_units")
        self.TabFileDDUnitComBox.currentIndexChanged.connect(DU)
        self.jfimported=True
        # self.TabCtrlOptCComBox.currentIndexChanged.connect(self.ElecCtrlAlg)

    def JFLoad(self, spn):

        self.TabSDataLoad()
        if len(self.tempdata["spaces"])>1:
            self.TabSDataSPDelBtn.setEnabled(1)
        if len(self.tempdata["spaces"])>0:
            self.TabSDataSPCopyBtn.setEnabled(1)
        try:
            self.TabSiteBldgRotLineEd.setText(str(self.tempdata["general"]["building_rotation"]))
        except:
            self.TabSiteBldgRotLineEd.setText("0")
            self.tempdata["general"]["building_rotation"]=0
            self.WriteToFile()

        # self.fnames=[]
        # self.fnamesd=[]
        # self.fnamesb=[]
        # self.fnamesbd=[]
        self.wgcalc=[]
        self.sdcalc=[]
        # self.dxps=[]
        try:
            lenS=len(self.tempdata["spaces"])
            for i in range(lenS):
                lenWG=len(self.tempdata["spaces"][i]["window_groups"])
                temp=[]
                temp1=[]
                for j in range(lenWG):
                    # self.fnamesb.append(str(self.tempdata["spaces"][i]["space_name"])+"_"+str(self.tempdata["spaces"][i]["window_groups"][j]["name"])+ \
                    #         "_base.ill")
                    # self.fnamesbd.append(str(self.tempdata["spaces"][i]["space_name"])+"_"+str(self.tempdata["spaces"][i]["window_groups"][j]["name"])+ \
                    #         "_base_direct.ill")
                    p1=os.path.normpath(self.tempdata["general"]["project_directory"]+self.tempdata["spaces"][i]["results_directory"]+ \
                                        str(self.tempdata["spaces"][i]["space_name"])+"_"+str(self.tempdata["spaces"][i]["window_groups"][j]["name"])+ "_base.ill")
                    p2=os.path.normpath(self.tempdata["general"]["project_directory"]+self.tempdata["spaces"][i]["results_directory"]+ \
                                        str(self.tempdata["spaces"][i]["space_name"])+"_"+str(self.tempdata["spaces"][i]["window_groups"][j]["name"])+ "_base_direct.ill")
                    if os.path.exists(p1) and os.path.exists(p2):
                        temp.append(False)
                    else:
                        temp.append(True)
                    try:
                        lenSd=len(self.tempdata["spaces"][i]["window_groups"][j]["shade_settings"])
                        tp=[]
                        for k in range(lenSd):
                            # print i*lenWG*lenSd+j*(lenSd)+k
                            # self.fnames.append(str(self.tempdata["spaces"][i]["space_name"])+"_"+str(self.tempdata["spaces"][i]["window_groups"][j]["name"])+ \
                            #     "_set"+str(k+1)+".ill")
                            # self.fnamesd.append(str(self.tempdata["spaces"][i]["space_name"])+"_"+str(self.tempdata["spaces"][i]["window_groups"][j]["name"])+ \
                            #     "_set"+str(k+1)+"_direct.ill")
                            p1=os.path.normpath(self.tempdata["general"]["project_directory"]+self.tempdata["spaces"][i]["results_directory"]+str(self.tempdata["spaces"][i]["space_name"])+"_"+ \
                               str(self.tempdata["spaces"][i]["window_groups"][j]["name"])+"_set"+str(k+1)+".ill")
                            p2=os.path.normpath(self.tempdata["general"]["project_directory"]+self.tempdata["spaces"][i]["results_directory"]+str(self.tempdata["spaces"][i]["space_name"])+"_"+ \
                               str(self.tempdata["spaces"][i]["window_groups"][j]["name"])+"_set"+str(k+1)+"_direct.ill")
                            if os.path.exists(p1) and os.path.exists(p2):
                                tp.append(False)
                            else:
                                tp.append(True)
                        temp1.append(tp)
                    except:
                        p1=os.path.normpath(str(self.tempdata["spaces"][i]["space_name"])+"_"+str(self.tempdata["spaces"][i]["window_groups"][j]["name"])+ "_set0.ill")
                        p2=os.path.normpath(str(self.tempdata["spaces"][i]["space_name"])+"_"+str(self.tempdata["spaces"][i]["window_groups"][j]["name"])+ "_set0_direct.ill")
                        if os.path.exists(p1) and os.path.exists(p2):
                            temp1.append(False)
                        else:
                            temp1.append(True)
                        # self.fnames[i*lenWG+j]=str(self.tempdata["spaces"][i]["space_name"])+"_"+str(self.tempdata["spaces"][i]["window_groups"][j]["name"])+ \
                        #     "_set0.ill"
                        # self.fnamesd[i*lenWG+j]=str(self.tempdata["spaces"][i]["space_name"])+"_"+str(self.tempdata["spaces"][i]["window_groups"][j]["name"])+ \
                        #     "_set0_direct.ill"
                self.wgcalc.append(temp)
                self.sdcalc.append(temp1)
            # print self.sdcalc, self.wgcalc
            # print self.dxps
        except:
            pass
        self.TabAnaLoad()
        self.TabWinGLoad()
        # self.lumlayout=True
        self.TabElecLoad()
        self.TabCtrlLoad()
        self.TabMtrLoad()
        # self.lumlayout=False


    def dunits(self,unit):
        if unit=="in":
            return 0
        elif unit=="ft":
            return 1
        elif unit=="m":
            return 2
        elif unit=="mm":
            return 3


    def lunits(self,unit):
        if unit=="lux":
            return 0
        elif unit=="fc":
            return 1





    def DUnitChange(self, object, unittype):
        index=object.currentIndex()
        if index==0:
            Unit="in"
        elif index==1:
            Unit="ft"
        elif index==2:
            Unit="m"
        elif index==3:
            Unit="mm"
        try:
            if self.imported or self.created:
                self.tempdata["general"][unittype]=Unit
                self.tempdata["general"][unittype]=Unit
                self.WriteToFile()
                try:
                    del self.markunit
                except:
                    pass
                self.forceuchange=True
                self.forceuchange1=True
                self.TabAnaLoad()
                self.TabWinGLoad()
                # self.lumlayout=True
                self.TabElecLoad()
                # self.lumlayout=False
                self.TabCtrlLoad()
        except:
            pass


    def LUnitChange(self, index):
        test=True
        if self.imported:
            try:
                junk=self.tempdata["general"]["illum_units"]
                choice=QtGui.QMessageBox.question(self, "Warning","You may need to run the simulation again. Change?", \
                                                          QtGui.QMessageBox.Yes |QtGui.QMessageBox.No)
                if choice==QtGui.QMessageBox.Yes:
                    self.CalcCheck()
                    self.TabWinGLoad()
                else:
                    test=False
            except:
                pass
        if test==True:
            if index==0:
                LUnit="lux"
                try:
                    self.tempdata["general"]["target_illuminance"]=int(self.tempdata["general"]["target_illuminance"]*10)
                except:
                    self.tempdata["general"]["target_illuminance"]=300
                try:
                    for i in range(len(self.tempdata["spaces"])):
                        self.tempdata["spaces"][i]["target_illuminance"]=int(self.tempdata["spaces"][i]["target_illuminance"]*10)
                except:
                    for i in range(len(self.tempdata["spaces"])):
                        self.tempdata["spaces"][i]["target_illuminance"]=30
                items=["cDA", "DA", "occupied_sDA", "sDA"]
                for item in items:
                    try:
                        self.tempdata["general"][item]["illuminance"]=int(self.tempdata["general"][item]["illuminance"]*10)
                    except:
                        pass
                    for i in range(len(self.tempdata["spaces"])):
                        try:
                            self.tempdata["spaces"][i][item]["illuminance"]=int(self.tempdata["spaces"][i][item]["illuminance"]*10)
                        except:
                            pass
                items=["minimum","maximum"]
                for item in items:
                    try:
                        self.tempdata["general"]["UDI"][item]=int(self.tempdata["general"]["UDI"][item]*10)
                    except:
                        pass
                    for i in range(len(self.tempdata["spaces"])):
                        try:
                            self.tempdata["spaces"][i]["UDI"][item]=int(self.tempdata["spaces"][i]["UDI"][item]*10)
                        except:
                            pass
            else:
                LUnit="fc"
                try:
                    self.tempdata["general"]["target_illuminance"]=int(self.tempdata["general"]["target_illuminance"]/10)
                except:
                    self.tempdata["general"]["target_illuminance"]=30
                try:
                    for i in range(len(self.tempdata["spaces"])):
                        self.tempdata["spaces"][i]["target_illuminance"]=int(self.tempdata["spaces"][i]["target_illuminance"]/10)
                except:
                    for i in range(len(self.tempdata["spaces"])):
                        self.tempdata["spaces"][i]["target_illuminance"]=30
                items=["cDA", "DA", "occupied_sDA", "sDA"]
                for item in items:
                    try:
                        self.tempdata["general"][item]["illuminance"]=int(self.tempdata["general"]["cDA"]["illuminance"]/10)
                    except:
                        pass
                    for i in range(len(self.tempdata["spaces"])):
                        try:
                            self.tempdata["spaces"][i][item]["illuminance"]=int(self.tempdata["spaces"][i][item]["illuminance"]/10)
                        except:
                            pass
                items=["minimum","maximum"]
                for item in items:
                    try:
                        self.tempdata["general"]["UDI"][item]=int(self.tempdata["general"]["UDI"][item]/10)
                    except:
                        pass
                    for i in range(len(self.tempdata["spaces"])):
                        try:
                            self.tempdata["spaces"][i]["UDI"][item]=int(self.tempdata["spaces"][i]["UDI"][item]/10)
                        except:
                            pass
            try:
                if self.imported or self.created:
                    self.tempdata["general"]["illum_units"]=LUnit
                    self.WriteToFile()
                    # try:
                    #     print self.tempdata["general"]["target_illuminance"]
                    # except:
                    #     pass

                    self.TabCtrlLoad()
                    self.TabMtrLoad()
            except:
                pass
        elif test==False:
            self.TabFileLUnitsComBox.currentIndexChanged[int].disconnect()
            self.imported=False
            if index==0:
                self.TabFileLUnitsComBox.setCurrentIndex(1)
            else:
                self.TabFileLUnitsComBox.setCurrentIndex(0)
            self.imported=True
            self.LUnits=self.tempdata["general"]["illum_units"]
            self.TabFileLUnitsComBox.currentIndexChanged.connect(self.LUnitChange)
        del test
        self.WriteToFile()



    def WeaFile(self):
        if self.imported or self.created:
            WeaFile= QtGui.QFileDialog.getOpenFileName(self,"Import EPW Weather File",self.dir,"Weather File (*.epw)")
            if WeaFile:
                temp=open(WeaFile,"r").readlines()
                t1=temp[0].split(",")
                try:
                    for item in t1:
                        if item=="LOCATION":
                            id=t1.index(item)
                    if "/" in t1[id+1]:
                        t1[id+1]=t1[id+1].replace("/", "_")
                    t1=",".join(t1)
                    temp[0]=t1
                except:
                    pass
                WPath=self.tempdata["general"]["project_directory"]+"data/"+os.path.basename(str(WeaFile))
                dire=str(self.tempdata["general"]["project_directory"]+"data/")
                if not os.path.exists(dire):
                    os.mkdir(dire)
                WeaLine=open(WPath,"w")
                for item in temp:
                    WeaLine.write(item)
                WeaLine.close()
                self.TabSiteWeaLineEd.setText(WPath)
                self.JFData["general"]["epw_file"]="data/"+os.path.basename(str(WeaFile))
                self.CalcCheck()
                self.WriteToFile()


    def CalcCheck(self):
        #check calculation flags
        try:
            for i in range(len(self.tempdata["spaces"])):
                try:
                    for j in range(len(self.tempdata["spaces"][i]["window_groups"])):
                        self.wgcalc[i][j]=True
                        self.tempdata["spaces"][i]["window_groups"][j]["calculate_base"]=True
                        try:
                            for k in range(len(self.tempdata["spaces"][i]["window_groups"][j]["shade_settings"])):
                                self.sdcalc[i][j][k]=True
                                self.tempdata["spaces"][i]["window_groups"][j]["calculate_setting"][k]=True
                        except:
                            pass
                except:
                    pass
            self.WriteToFile()
            self.TabWinGLoad()
            # self.WGCalCbx.setDisabled(1)
        except:
            pass



    def DayS(self):
        if self.imported or self.created:
            if self.TabSiteDaySChk.isChecked():
                self.tempdata["general"]["daylight_savings_time"]=True
            else:
                self.tempdata["general"]["daylight_savings_time"]=False
            self.CalcCheck()
            self.WriteToFile()


    def SiteData(self, object, key):
        if self.imported or self.created:
            if key=="building_rotation":
                self.tempdata["general"][key]=int(object.text())
            else:
                mark=0
                mark=self.floatChk(object, 0, 1)
                if mark==0:
                    self.tempdata["general"][key]=float(object.text())
                else:
                    object.setText("0.2")
                    object.setFocus()
                    self.tempdata["general"][key]=0.2
            self.CalcCheck()
            self.WriteToFile()


    def CopyFile(self,fname,fnpath):
        if self.imported or self.created:
            try:
                os.stat(fnpath)
                mark=0
            except:
                try:
                    os.mkdir(fnpath)
                    mark=0
                except:
                    QtGui.QMessageBox.warning(self, "Error Creation of the File Path!")
                    mark=1
            if mark==0:
                base=os.path.basename(str(fname))
                fopath=os.path.dirname(str(fname))
                fnew=os.path.normpath(os.path.join(fnpath,base))
                if os.path.exists(fnew):
                    choice=QtGui.QMessageBox.question(self,"Overwrite","File already exists. Overwrite?", \
                                                      QtGui.QMessageBox.Yes |QtGui.QMessageBox.No)
                    if choice==QtGui.QMessageBox.Yes:
                        if os.stat(fname) == os.stat(fnew):
                            pass
                        else:
                            os.remove(fnew)
                            shutil.copy2(fname, fnew)
                else:
                    shutil.copy2(fname, fnew)
                return fnew


    def TabSDataLoad(self):
        try:
            index=self.TabSDataSPComBox.currentIndex()
            spname=self.tempdata["spaces"][index]

            try:
                self.TabSDataMatLineEd.setText(os.path.normpath(os.path.join(self.dir,spname["geometry_directory"],spname["material_file"])))
            except:
                self.TabSDataMatLineEd.setText(" ")
            try:
                self.TabSDataGeoLineEd.setText(os.path.normpath(os.path.join(self.dir,spname["geometry_directory"],spname["geometry_file"])))
            except:
                self.TabSDataGeoLineEd.setText(" ")
            # try:
            #     self.TabSDataOccLineEd.setText(os.path.normpath(os.path.join(self.dir,spname["input_directory"],spname["occupancy_schedule"])))
            # except:
            #     self.TabSDataOccLineEd.setText(" ")
            try:
                self.TabSDataLSLineEd.setText(os.path.normpath(os.path.join(self.dir,spname["input_directory"],spname["lighting_schedule"])))
            except:
                self.TabSDataLSLineEd.setText(" ")
            try:
                self.TabSDataGeoBrwLineEd.setText(os.path.normpath(os.path.join(self.dir,spname["geometry_directory"])))
                path=os.path.normpath(os.path.join(self.dir,spname["geometry_directory"]))
                self.FPCheck(path)
            except:
                spname["geometry_directory"]="rad/"
                self.TabSDataGeoBrwLineEd.setText(os.path.normpath(os.path.join(self.dir,spname["geometry_directory"])))
                path=os.path.normpath(os.path.join(self.dir,spname["geometry_directory"]))
                self.FPCheck(path)
            try:
                self.TabSDataIESBrwLineEd.setText(os.path.normpath(os.path.join(self.dir,spname["ies_directory"])))
                path=os.path.normpath(os.path.join(self.dir,spname["ies_directory"]))
                self.FPCheck(path)
            except:
                spname["ies_directory"]="ies/"
                self.TabSDataIESBrwLineEd.setText(os.path.normpath(os.path.join(self.dir,spname["ies_directory"])))
                path=os.path.normpath(os.path.join(self.dir,spname["ies_directory"]))
                self.FPCheck(path)
            try:
                self.TabSDataInputLineEd.setText(os.path.normpath(os.path.join(self.dir,spname["input_directory"])))
                path=os.path.normpath(os.path.join(self.dir,spname["input_directory"]))
                self.FPCheck(path)
            except:
                spname["input_directory"]="data/"
                self.TabSDataInputLineEd.setText(os.path.normpath(os.path.join(self.dir,spname["input_directory"])))
                path=os.path.normpath(os.path.join(self.dir,spname["input_directory"]))
                self.FPCheck(path)
            try:
                self.TabSDataResLineEd.setText(os.path.normpath(os.path.join(self.dir,spname["results_directory"])))
                path=os.path.normpath(os.path.join(self.dir,spname["results_directory"]))
                self.FPCheck(path)
            except:
                spname["results_directory"]="res/"
                self.TabSDataResLineEd.setText(os.path.normpath(os.path.join(self.dir,spname["results_directory"])))
                path=os.path.normpath(os.path.join(self.dir,spname["results_directory"]))
                self.FPCheck(path)
        except:
            pass


    def FPCheck(self,fpath):
        if not os.path.exists(str(fpath)):
            try:
                os.mkdir(str(fpath))
            except:
                pass


    def SPAdd(self):
        if self.imported or self.created:
            name, ok=QtGui.QInputDialog.getText(self,"Add Space", "Space Name:", QtGui.QLineEdit.Normal)
            stname=str(name)
            if len(stname.split())>1:
                QtGui.QMessageBox.warning(self, "Warning!", \
                                                  "No spaces (\" \") in the name!")
            else:
                if ok and name !=" ":
                    mark=0
                    for item in self.tempdata["spaces"]:
                        if item["space_name"]!= name:
                            mark=0
                            continue
                        else:
                            mark=1
                            QtGui.QMessageBox.warning(self, "Warning!", \
                                                      "The name is the same as one of the other space")
                            break
                    if mark==0:
                        self.tempdata["spaces"].append({})
                        self.tempdata["spaces"][len(self.tempdata["spaces"])-1]["space_name"]=str(name)
                        index=len(self.tempdata["spaces"])-1
                        self.tempdata["spaces"][index]["DA"]={}
                        self.tempdata["spaces"][index]["DA"]["calculate"]=False
                        self.tempdata["spaces"][index]["sDA"]={}
                        self.tempdata["spaces"][index]["sDA"]["calculate"]=False
                        self.tempdata["spaces"][index]["occupied_sDA"]={}
                        self.tempdata["spaces"][index]["occupied_sDA"]["calculate"]=False
                        self.tempdata["spaces"][index]["cDA"]={}
                        self.tempdata["spaces"][index]["cDA"]["calculate"]=False
                        self.tempdata["spaces"][index]["DF"]=False
                        self.tempdata["spaces"][index]["UDI"]={}
                        self.tempdata["spaces"][index]["UDI"]["calculate"]=False
                        try:
                            self.wgcalc.append([])
                            self.sdcalc.append([])
                            # print self.wgcalc, self.sdcalc
                        except:
                            pass
                        self.TabSDataSPComBox.addItem(str(name))
                        self.TabAnaSPNComBox.addItem(str(name))
                        self.TabWinSPNComBox.addItem(str(name))
                        self.TabElecSPComBox.addItem(str(name))
                        self.TabCtrlSPNComBox.addItem(str(name))
                        self.TabDMtrSPNComBox.addItem(str(name))
                        self.OutputSPCbx.addItem(str(name))
                        self.OutputSPCbx2.addItem(str(name))
                        self.TabSDataSPComBox.setCurrentIndex(len(self.tempdata["spaces"])-1)
                        self.TabAnaSPNComBox.setCurrentIndex(len(self.tempdata["spaces"])-1)
                        self.TabWinSPNComBox.setCurrentIndex(len(self.tempdata["spaces"])-1)
                        self.TabElecSPComBox.setCurrentIndex(len(self.tempdata["spaces"])-1)
                        self.TabCtrlSPNComBox.setCurrentIndex(len(self.tempdata["spaces"])-1)
                        self.TabDMtrSPNComBox.setCurrentIndex(len(self.tempdata["spaces"])-1)
                        self.OutputSPCbx.setCurrentIndex(len(self.tempdata["spaces"])-1)
                        self.OutputSPCbx2.setCurrentIndex(len(self.tempdata["spaces"])-1)
                        self.WriteToFile()
                        self.TabSDataSPDelBtn.setEnabled(1)
                        self.TabSDataSPCopyBtn.setEnabled(1)

    def SPCopy(self):
        if (self.imported or self.created):
            try:
                if len(self.tempdata["spaces"])>0:
                    Dupcombo=DupSPUi_Combo()
                    for item in self.tempdata["spaces"]:
                        Dupcombo.cboxsp.addItem(item["space_name"])
                    Dupcombo.show()
                    Dupcombo.exec_()
                    try:
                        newname=Dupcombo.newname
                        cindex=Dupcombo.id
                        self.tempdata["spaces"].append({})
                        lenc=len(self.tempdata["spaces"])
                        self.tempdata["spaces"][lenc-1]=copy.deepcopy(self.tempdata["spaces"][cindex])
                        self.tempdata["spaces"][lenc-1]["space_name"]=str(newname)
                        self.tempdata["spaces"][lenc-1]["analysis_points"]["files"][0]=str(newname)+"_AutoGen.pts"
                        QtGui.QMessageBox.information(self,"Successful", "Space information is copied successfully")
                        self.WriteToFile()
                        self.TabSDataSPComBox.addItem(self.tempdata["spaces"][lenc-1]["space_name"])
                        self.TabAnaSPNComBox.addItem(self.tempdata["spaces"][lenc-1]["space_name"])
                        self.TabWinSPNComBox.addItem(self.tempdata["spaces"][lenc-1]["space_name"])
                        self.TabElecSPComBox.addItem(self.tempdata["spaces"][lenc-1]["space_name"])
                        self.TabCtrlSPNComBox.addItem(self.tempdata["spaces"][lenc-1]["space_name"])
                        self.TabDMtrSPNComBox.addItem(self.tempdata["spaces"][lenc-1]["space_name"])
                        self.OutputSPCbx.addItem(self.tempdata["spaces"][lenc-1]["space_name"])
                        self.OutputSPCbx2.addItem(self.tempdata["spaces"][lenc-1]["space_name"])
                        self.TabSDataSPComBox.setCurrentIndex(lenc-1)
                        try:
                            temp=copy.deepcopy(self.wgcalc[cindex])
                            self.wgcalc.append(temp)
                            temp=copy.deepcopy(self.sdcalc[cindex])
                            self.sdcalc.append(temp)
                            for j in range(len(self.tempdata["spaces"][lenc-1]["window_groups"])):
                                self.wgcalc[lenc-1][j]=True
                                self.tempdata["spaces"][lenc-1]["window_groups"][j]["calculate_base"]=True
                                try:
                                    for k in range(len(self.tempdata["spaces"][lenc-1]["window_groups"][j]["shade_settings"])):
                                        self.tempdata["spaces"][lenc-1]["window_groups"][j]["calculate_setting"][k]=True
                                        self.sdcalc[lenc-1][j][k]=True
                                except:
                                    pass
                            self.TabWinGLoad()
                            self.TabSDataSPDelBtn.setEnabled(1)
                        except:
                            pass
                    except:
                        pass
            except:
                pass

    def SPDel(self):
        if len(self.tempdata["spaces"]) > 1:
            choice=QtGui.QMessageBox.question(self, "Warning", "Are you sure to delete the space?", \
                                              QtGui.QMessageBox.Yes |QtGui.QMessageBox.No)
            if choice==QtGui.QMessageBox.Yes:
                index=self.TabSDataSPComBox.currentIndex()
                del self.tempdata["spaces"][index]
                self.TabSDataSPComBox.removeItem(index)
                self.TabAnaSPNComBox.removeItem(index)
                self.TabWinSPNComBox.removeItem(index)
                self.TabElecSPComBox.removeItem(index)
                self.TabCtrlSPNComBox.removeItem(index)
                self.TabDMtrSPNComBox.removeItem(index)
                self.OutputSPCbx.removeItem(index)
                self.OutputSPCbx2.removeItem(index)
                self.WriteToFile()
                self.JFLoad(0)
                try:
                    self.wgcalc.remove(index)
                    self.sdcalc.remove(index)
                    # print self.wgcalc, self.sdcalc
                except:
                    pass
        else:
            QtGui.QMessageBox.warning(self,"No more spaces","Cannot delete the only space!")


    def view_edit(self, object):
        if self.imported or self.created:
            fpath=str(object.text())
            if os.path.exists(fpath):
                QtGui.QMessageBox.warning(self,"Warning!!!","Please click on \"Import\" if you did save as!")
                subprocess.Popen("notepad.exe "+fpath, shell=False)

                # os.system(fpath)
                self.WISPWGCalc(self.TabSDataSPComBox.currentIndex())
            else:
                QtGui.QMessageBox.warning(self,"Warning!!!","No such file in directory!!!")


    def MatImport(self):
        if self.imported or self.created:
            try:
                if len(self.tempdata["spaces"])>0:
                    MatFile= QtGui.QFileDialog.getOpenFileName(self,"Import Material File",self.dir,"Material Rad File (*.rad)")
                    if MatFile:
                        index=self.TabSDataSPComBox.currentIndex()
                        MPath=os.path.join(self.dir,self.tempdata["spaces"][index]["geometry_directory"])
                        MatLine=self.CopyFile(MatFile,MPath)
                        self.TabSDataMatLineEd.setText(MatLine)
                        self.tempdata["spaces"][index]["material_file"]=os.path.basename(str(MatLine))
                        self.WriteToFile()
                        self.WISPWGCalc(index)
            except:
                pass

    def GeoImport(self):
        if self.imported or self.created:
            try:
                if len(self.tempdata["spaces"])>0:
                    GeoFile= QtGui.QFileDialog.getOpenFileName(self,"Import Geometry File",self.dir,"Geometry Rad File (*.rad)")
                    if GeoFile:
                        index=self.TabSDataSPComBox.currentIndex()
                        GPath=os.path.join(self.dir,self.tempdata["spaces"][index]["geometry_directory"])
                        GeoLine=self.CopyFile(GeoFile,GPath)
                        self.TabSDataGeoLineEd.setText(GeoLine)
                        self.tempdata["spaces"][index]["geometry_file"]=os.path.basename(str(GeoLine))
                        self.WriteToFile()
                        self.WISPWGCalc(index)
            except:
                pass

    # def OccImport(self):
    #     if self.imported or self.created:
    #         OccFile= QtGui.QFileDialog.getOpenFileName(self,"Import Occupancy Schedule","C:/","Occupancy File (*.csv)")
    #         if OccFile:
    #             index=self.TabSDataSPComBox.currentIndex()
    #             OPath=os.path.join(self.dir,self.tempdata["spaces"][index]["input_directory"])
    #             OLine=self.CopyFile(OccFile,OPath)
    #             self.TabSDataOccLineEd.setText(OLine)
    #             self.tempdata["spaces"][index]["occupancy_schedule"]=os.path.basename(str(OLine))
    #             self.WriteToFile()

    def LSImport(self):
        if self.imported or self.created:
            try:
                if len(self.tempdata["spaces"])>0:
                    LSFile= QtGui.QFileDialog.getOpenFileName(self,"Import Lighting Schedule",self.dir,"Lighting Schedule File (*.csv)")
                    if LSFile:
                        index=self.TabSDataSPComBox.currentIndex()
                        LPath=os.path.join(self.dir,self.tempdata["spaces"][index]["input_directory"])
                        LLine=self.CopyFile(LSFile,LPath)
                        self.TabSDataLSLineEd.setText(LLine)
                        self.TabSDataLSLineEd.setText(LLine)
                        self.tempdata["spaces"][index]["lighting_schedule"]=os.path.basename(str(LLine))
                        self.WriteToFile()
            except:
                pass


    def sppath(self, object,fuc):
        if self.imported or self.created:
            try:
                if len(self.tempdata["spaces"])>0:
                    index=self.TabSDataSPComBox.currentIndex()
                    if fuc=="geometry_directory":
                        fucs="Geometry"
                    elif fuc=="ies_directory":
                        fucs="IES"
                    elif fuc=="input_directory":
                        fucs="Input"
                    else:
                        fucs="Results"
                    dir2=QtGui.QFileDialog.getExistingDirectory(self, "Set %s Path Directory"%fucs, self.tempdata["general"]["project_directory"], options=QtGui.QFileDialog.DontResolveSymlinks)
                    if dir2:
                        if dir2.contains(self.tempdata["general"]["project_directory"]):
                            try:
                                dir1=os.path.join(self.tempdata["general"]["project_directory"],self.tempdata["spaces"][index][fuc])
                                dir3=dir2+"/"
                                # if fuc=="geometry_directory":
                                #     dir3=dir2+"/rad/"
                                # elif fuc=="ies_directory":
                                #     dir3=dir2+"/ies/"
                                # elif fuc=="input_directory":
                                #     dir3=dir2+"/data/"
                                # else:
                                #     dir3=dir2+"/res/"
                                shutil.copytree(os.path.normpath(dir1),os.path.normpath(str(dir3)))
                            except:
                                pass
                            spd=str(dir2)
                            spd=spd.strip()

                            spdlist=spd.split("/")
                            cleanspd=""
                            pjd=self.tempdata["general"]["project_directory"].strip().split("/")
                            k=0
                            try:
                                for item in spdlist:
                                    try:
                                        if item==pjd[k]:
                                            pass
                                        else:
                                            cleanspd=cleanspd+"/"+item
                                    except:
                                        cleanspd=cleanspd+"/"+item
                                    k=k+1
                            except:
                                pass
                            self.tempdata["spaces"][index][fuc]=cleanspd[1:]+"/"
                            # if fuc=="geometry_directory":
                            #     self.tempdata["spaces"][index][fuc]=cleanspd[1:]+"/rad/"
                            # elif fuc=="ies_directory":
                            #     self.tempdata["spaces"][index][fuc]=cleanspd[1:]+"/ies/"
                            # elif fuc=="input_directory":
                            #     self.tempdata["spaces"][index][fuc]=cleanspd[1:]+"/data/"
                            # else:
                            #     self.tempdata["spaces"][index][fuc]=cleanspd[1:]+"/res/"
                            object.setText(str(self.tempdata["spaces"][index][fuc]))
                            self.JFLoad(index)
                            self.WriteToFile()
                        else:
                            index=self.TabSDataSPComBox.currentIndex()
                            if fuc=="geomtry_directory":
                                fucs="Geometry"
                            elif fuc=="ies_directory":
                                fucs="IES"
                            elif fuc=="input_directory":
                                fucs="Input"
                            else:
                                fucs="Results"
                            QtGui.QMessageBox.warning(self,"Error", "%s folder path should be the subfolder of your project folder!!" %fucs)
            except:
                pass



    def TabAnaLoad(self):
        if self.created or self.imported:
            try:
                index=self.TabAnaSPNComBox.currentIndex()
                spname=self.tempdata["spaces"][index]
                self.TabAnaMatNComBox.clear()
                self.TabAnaGPFLineEd.setStyleSheet("color: rgb(0, 0, 0);")
                try:
                    self.TabAnaGPFLineEd.setText(spname["analysis_points"]["files"][0])
                    pth=os.path.join(self.dir,spname["input_directory"],spname["analysis_points"]["files"][0])
                    if os.path.exists(pth):
                        self.TabAnaMatNComBox.setDisabled(1)
                        self.TabAnaMatAddBtn.setDisabled(1)
                        self.TabAnaMatDelBtn.setDisabled(1)
                        self.TabAnaOffXLineEd.setDisabled(1)
                        self.TabAnaOffYLineEd.setDisabled(1)
                        self.TabAnaOffZLineEd.setDisabled(1)
                        self.TabAnaSPXLineEd.setDisabled(1)
                        self.TabAnaSPYLineEd.setDisabled(1)
                    else:
                        self.TabAnaGPFLineEd.setStyleSheet("color: rgb(255, 0, 0);")
                        self.TabAnaMatNComBox.setEnabled(1)
                        self.TabAnaMatAddBtn.setEnabled(1)
                        self.TabAnaMatDelBtn.setEnabled(1)
                        self.TabAnaOffXLineEd.setEnabled(1)
                        self.TabAnaOffYLineEd.setEnabled(1)
                        self.TabAnaOffZLineEd.setEnabled(1)
                        self.TabAnaSPXLineEd.setEnabled(1)
                        self.TabAnaSPYLineEd.setEnabled(1)
                except:
                    self.TabAnaMatNComBox.setEnabled(1)
                    self.TabAnaMatAddBtn.setEnabled(1)
                    self.TabAnaMatDelBtn.setEnabled(1)
                    self.TabAnaOffXLineEd.setEnabled(1)
                    self.TabAnaOffYLineEd.setEnabled(1)
                    self.TabAnaOffZLineEd.setEnabled(1)
                    self.TabAnaSPXLineEd.setEnabled(1)
                    self.TabAnaSPYLineEd.setEnabled(1)
                    try:
                        spname["analysis_points"]["files"][0]=spname["space_name"]+"_AutoGen.pts"
                        self.TabAnaGPFLineEd.setText(spname["analysis_points"]["files"][0])
                    except:
                        try:
                            spname["analysis_points"]["files"]=[]
                            spname["analysis_points"]["files"].append(spname["space_name"]+"_AutoGen.pts")
                            self.TabAnaGPFLineEd.setText(spname["analysis_points"]["files"][0])
                        except:
                            spname["analysis_points"]={}
                            spname["analysis_points"]["files"]=[]
                            spname["analysis_points"]["files"].append(spname["space_name"]+"_AutoGen.pts")
                            self.TabAnaGPFLineEd.setText(spname["analysis_points"]["files"][0])
                    self.TabAnaGPFLineEd.setStyleSheet("color: rgb(255, 0, 0);")
                try:
                    dunit= self.tempdata["general"]["display_units"]
                    iunit=self.tempdata["general"]["import_units"]
                    self.AnaSPLbl.setText("Spacing: (%s)"%dunit)
                    self.AnaOSLbl.setText("Offset: (%s)"%dunit)
                    try:
                        self.setUnitText(self.TabAnaSPXLineEd,dunit, iunit, spname["analysis_points"]["x_spacing"], True)
                    except:
                        self.TabAnaSPXLineEd.clear()
                    try:
                        self.setUnitText(self.TabAnaSPYLineEd,dunit, iunit, spname["analysis_points"]["y_spacing"], True)
                    except:
                        self.TabAnaSPYLineEd.clear()
                    try:
                        self.setUnitText(self.TabAnaOffXLineEd,dunit, iunit, spname["analysis_points"]["x_offset"], True)
                    except:
                        try:
                            self.setUnitText(self.TabAnaOffXLineEd,dunit, iunit, spname["analysis_points"]["offset"], True)
                        except:
                            self.TabAnaOffXLineEd.clear()
                    try:
                        self.setUnitText(self.TabAnaOffYineEd,dunit, iunit, spname["analysis_points"]["y_offset"], True)
                    except:
                        try:
                            self.setUnitText(self.TabAnaOffYLineEd,dunit, iunit, spname["analysis_points"]["offset"], True)
                        except:
                            self.TabAnaOffYLineEd.clear()
                    try:
                        self.setUnitText(self.TabAnaOffZLineEd,dunit, iunit, spname["analysis_points"]["z_offset"], True)
                    except:
                        self.TabAnaOffZLineEd.clear()
                except:
                    # if self.jfimported:
                    #     try:
                    #         if self.markunit>=1:
                    #             print "1.0"
                    #             QtGui.QMessageBox.warning(self,"Warning", "Please define units first!")
                    #     except:
                    #         self.markunit=1
                    # elif self.created:
                    try:
                        if self.forceuchange:
                            del self.forceuchange
                    except:
                        QtGui.QMessageBox.warning(self,"Warning", "Please define diemension units first!")

                try:
                    for item in spname["analysis_points"]["modifier"]:
                        self.TabAnaMatNComBox.addItem(str(item))
                    try:
                        len(spname["layout_base"])>=1
                    except:
                        try:
                            # print len(spname["analysis_points"]["modifier"]), spname["analysis_points"]["modifier"]
                            if len(spname["analysis_points"]["modifier"])>0:
                                try:
                                    spname["layout_base"]=copy.deepcopy(spname["analysis_points"]["modifier"])
                                except:
                                    pass
                                # self.TabElecLoad()
                        except:
                            pass
                except:
                    pass
                self.WriteToFile()
            except:
                pass

    def setUnitText(self, object,ud,ui, value, ForB):
        object.setText(str(self.uconvert(ud,ui,value,ForB)))

    def uconvert(self, ud, ui, value, ForB):
        if (ud=="ft" and ui=="ft") or (ud=="in" and ui=="in") or (ud=="m" and ui=="m") or (ud=="mm" and ui=="mm"):
            return round(value,2)
        else:
            if ForB==True:
                if ud=="ft" and ui=="in":
                    return round(float(value)/12,2)
                if ud=="ft" and ui=="m":
                    return round(value*3.28084,2)
                if ud=="ft" and ui=="mm":
                    return round(value*3.28084*1000,2)
                if ud=="in" and ui=="ft":
                    return round(value*12.0,2)
                if ud=="in" and ui=="m":
                    return round(value*39.37)
                if ud=="in" and ui=="mm":
                    return round(value*39.37*1000,2)
                if ud=="m" and ui=="ft":
                    return round(value*0.3048,2)
                if ud=="m" and ui=="in":
                    return round(value*0.0254, 2)
                if ud=="m" and ui=="mm":
                    return round(value*0.001,2)
                if ud=="mm" and ui=="ft":
                    return round(value*0.3048*1000,2)
                if ud=="mm" and ui=="in":
                    return round(value*25.4,2)
                if ud=="mm" and ui=="m":
                    return round(value*1000,2)
            else:
                if ud=="ft" and ui=="in":
                    return round(float(value)*12,2)
                if ud=="ft" and ui=="m":
                    return round(value/3.28084,2)
                if ud=="ft" and ui=="mm":
                    return round(value/3.28084/1000,2)
                if ud=="in" and ui=="ft":
                    return round(value/12.0,2)
                if ud=="in" and ui=="m":
                    return round(value/39.37)
                if ud=="in" and ui=="mm":
                    return round(value/39.37/1000,2)
                if ud=="m" and ui=="ft":
                    return round(value/0.3048,2)
                if ud=="m" and ui=="in":
                    return round(value/0.0254, 2)
                if ud=="m" and ui=="mm":
                    return round(value/0.001,2)
                if ud=="mm" and ui=="ft":
                    return round(value/0.3048/1000,2)
                if ud=="mm" and ui=="in":
                    return round(value/25.4,2)
                if ud=="mm" and ui=="m":
                    return round(value/1000,2)


    def AddPts(self):
        if self.imported or self.created:
            try:
                index=self.TabAnaSPNComBox.currentIndex()
                spname=self.tempdata["spaces"][index]
                try:
                    ptsFile=QtGui.QFileDialog.getOpenFileName(self,"Import Points File",self.dir,"Analysis Grid Points File (*.pts)")
                    if ptsFile:
                        self.TabAnaGPFLineEd.setStyleSheet("color: rgb(0, 0, 0);")
                        PPath=os.path.dirname(str(os.path.join(self.dir,spname["input_directory"])))
                        PLine=self.CopyFile(ptsFile,PPath)
                        self.TabAnaGPFLineEd.setText(os.path.basename(PLine))
                        try:
                            spname["analysis_points"]["files"][0]=str(os.path.basename(str(PLine)))
                        except:
                            spname["analysis_points"]={}
                            spname["analysis_points"]["files"]=[]
                            spname["analysis_points"]["files"].append(str(os.path.basename(str(PLine))))
                        self.WriteToFile()
                        self.TabAnaMatNComBox.clear()
                        self.TabAnaSPXLineEd.clear()
                        self.TabAnaSPYLineEd.clear()
                        self.TabAnaOffXLineEd.clear()
                        self.TabAnaOffYLineEd.clear()
                        self.TabAnaOffZLineEd.clear()
                        self.TabAnaMatAddBtn.setDisabled(1)
                        self.TabAnaMatNComBox.setDisabled(1)
                        self.TabAnaMatDelBtn.setDisabled(1)
                        self.TabAnaOffXLineEd.setDisabled(1)
                        self.TabAnaOffYLineEd.setDisabled(1)
                        self.TabAnaOffZLineEd.setDisabled(1)
                        self.TabAnaSPXLineEd.setDisabled(1)
                        self.TabAnaSPYLineEd.setDisabled(1)
                        self.WISPWGCalc(index)
                except:
                    QtGui.QMessageBox.warning(self,"Warning","Space directory not setup yet!")
            except:
                pass



    def PtsRst(self):
        if self.imported or self.created:
            try:
                if len(self.tempdata["spaces"])>0:
                    choice=QtGui.QMessageBox.question(self, "Warning", "Are you sure to RESET grid points?", \
                                                      QtGui.QMessageBox.Yes |QtGui.QMessageBox.No)
                    if choice==QtGui.QMessageBox.Yes:
                        index=self.TabAnaSPNComBox.currentIndex()
                        spname=self.tempdata["spaces"][index]
                        name=self.tempdata["general"]["project_directory"]+self.tempdata["spaces"][index]["input_directory"]+ \
                             self.TabAnaGPFLineEd.text()
                        try:
                            os.remove(str(name))
                        except:
                            pass
                        self.TabAnaGPFLineEd.clear()
                        self.TabAnaMatNComBox.clear()
                        self.TabAnaSPXLineEd.clear()
                        self.TabAnaSPYLineEd.clear()
                        self.TabAnaOffXLineEd.clear()
                        self.TabAnaOffYLineEd.clear()
                        self.TabAnaOffZLineEd.clear()
                        self.TabAnaMatAddBtn.setEnabled(1)
                        self.TabAnaMatNComBox.setEnabled(1)
                        self.TabAnaMatDelBtn.setEnabled(1)
                        self.TabAnaOffXLineEd.setEnabled(1)
                        self.TabAnaOffYLineEd.setEnabled(1)
                        self.TabAnaOffZLineEd.setEnabled(1)
                        self.TabAnaSPXLineEd.setEnabled(1)
                        self.TabAnaSPYLineEd.setEnabled(1)
                        self.TabAnaGPFLineEd.setStyleSheet("color: rgb(0, 0, 0);")
                        try:
                            spname["analysis_points"]["files"][0]=spname["space_name"]+"_AutoGen.pts"
                        except:
                            spname["analysis_points"]={}
                            spname["analysis_points"]["files"]=[]
                            spname["analysis_points"]["files"].append(spname["space_name"]+"_AutoGen.pts")
                        self.WriteToFile()
                        self.TabAnaLoad()
                        self.WISPWGCalc(index)
            except:
                pass

    def PtsMatAdd(self, object):
        if self.imported or self.created:
            try:
                if self.StadicTab.currentIndex()==3:
                    index=self.TabAnaSPNComBox.currentIndex()
                else:
                    index=self.TabElecSPComBox.currentIndex()
                spname=self.tempdata["spaces"][index]
                try:
                    modifier=[]
                    try:
                        WGMatPath=os.path.normpath(os.path.join(self.dir,spname["geometry_directory"],spname["material_file"]))
                        WGMatFile=open(WGMatPath,"r").read().split()
                        count=0
                        for item in WGMatFile:
                            if item=="void":
                                modifier.append(WGMatFile[count+2])
                            count += 1
                    except:
                        pass
                    try:
                        WGMatPath=os.path.normpath(os.path.join(self.dir,spname["geometry_directory"],spname["geometry_file"]))
                        WGMatFile=open(WGMatPath,"r").read().split()
                        count=0
                        for item in WGMatFile:
                            if item=="void":
                                modifier.append(WGMatFile[count+2])
                            count=count+1
                    except:
                        pass
                    try:
                        if len(modifier)>0:
                            self.combo=Ui_Combo()
                            for item in modifier:
                                self.combo.cbox.addItem(item)
                            self.combo.show()
                            self.combo.exec_()
                            mname=self.combo.mat
                            if self.StadicTab.currentIndex()==3:
                                mark1=0
                                try:
                                    if len(spname["layout_base"])<1:
                                        mark1=1
                                except:
                                    mark1=1
                                try:
                                    mark=0
                                    for item in spname["analysis_points"]["modifier"]:
                                        t1=str(mname)
                                        t2=str(item)
                                        if t1==t2:
                                            mark=1
                                    if mark==0:
                                        spname["analysis_points"]["modifier"].append(str(mname))
                                        self.WriteToFile()
                                        self.TabAnaLoad()
                                        self.WISPWGCalc(index)
                                    else:
                                        QtGui.QMessageBox.warning(self, "Warning", "Material already existed!")
                                except:
                                    spname["analysis_points"]={}
                                    spname["analysis_points"]["modifier"]=[]
                                    spname["analysis_points"]["modifier"].append(str(mname))
                                    self.WriteToFile()
                                    self.TabAnaLoad()
                                    self.WISPWGCalc(index)
                                try:
                                    if mark1==1:
                                        # self.lumlayout=True
                                        self.TabElecLoad()
                                        # self.lumlayout=False
                                except:
                                    pass
                            else:
                                try:
                                    mark=0
                                    for item in spname["layout_base"]:
                                        t1=str(mname)
                                        t2=str(item)
                                        if t1==t2:
                                            mark=1
                                    if mark==0:
                                        spname["layout_base"].append(str(mname))
                                        self.WriteToFile()
                                        # self.lumlayout=True
                                        self.TabElecLoad()
                                        # self.lumlayout=False
                                    else:
                                        QtGui.QMessageBox.warning(self, "Warning", "Material already existed!")
                                except:
                                    spname["layout_base"]=[]
                                    spname["layout_base"].append(str(mname))
                                    self.WriteToFile()
                                    # self.lumlayout=True
                                    self.TabElecLoad()
                                    # self.lumlayout=False
                        else:
                            QtGui.QMessageBox.warning(self, "warning", "Material file does not exist!")
                    except:
                        pass
                except:
                    try:
                        WGMatPath=os.path.normpath(os.path.join(self.dir,spname["geometry_directory"],spname["material_file"]))
                        if not os.path.exists(WGMatPath):
                            QtGui.QMessageBox.warning(self, "warning", "Material file does not exist!")
                    except:
                        pass
            except:
                pass

    def WISPWGCalc(self, index):
        try:
            for j in range(len(self.tempdata["spaces"][index]["window_groups"])):
                self.wgcalc[index][j]=True
                self.tempdata["spaces"][index]["window_groups"][j]["calculate_base"]=True
                try:
                    for k in range(len(self.tempdata["spaces"][index]["window_groups"][j]["shade_settings"])):
                        self.sdcalc[index][j][k]=True
                        self.tempdata["spaces"][index]["window_groups"][j]["calculate_setting"][k]=True
                except:
                    pass
            self.TabWinGCombo()
        except:
            pass


    def PtsMatDel(self):
        if self.imported or self.created:
            if self.StadicTab.currentIndex()==3:
                index=self.TabAnaSPNComBox.currentIndex()
                tgl=0
            else:
                tgl=1
                index=self.TabElecSPComBox.currentIndex()

            try:
                spname=self.tempdata["spaces"][index]
                if tgl==0 and len(spname["analysis_points"]["modifier"])>0:
                    choice=QtGui.QMessageBox.question(self,"Warning", "Are you sure to delete?", QtGui.QMessageBox.Yes |QtGui.QMessageBox.No)
            except:
                pass
            try:
                spname=self.tempdata["spaces"][index]
                if tgl==1 and len(spname["layout_base"])>0:
                    choice=QtGui.QMessageBox.question(self,"Warning", "Are you sure to delete?", QtGui.QMessageBox.Yes |QtGui.QMessageBox.No)
            except:
                pass
            try:
                if choice==QtGui.QMessageBox.Yes:
                    if tgl==0:
                        try:
                            try:
                                if len(spname["layout_base"])<1:
                                    mark1=1
                            except:
                                mark1=1
                            mindex=self.TabAnaMatNComBox.currentIndex()
                            self.TabAnaMatNComBox.removeItem(mindex)
                            del spname["analysis_points"]["modifier"][mindex]
                            self.WriteToFile()
                            self.TabAnaLoad()
                            self.WISPWGCalc(index)
                            try:
                                if mark1==1:
                                    # self.lumlayout=True
                                    self.TabElecLoad()
                                    # self.lumlayout=False
                            except:
                                pass
                        except:
                            pass
                    else:
                        try:
                            mindex=self.TabElecLayerCbx.currentIndex()
                            self.TabElecLayerCbx.removeItem(mindex)
                            del spname["layout_base"][mindex]
                            if len(spname["layout_base"])==0:
                                del spname["layout_base"]
                                self.scene.clear()
                            self.WriteToFile()
                            # self.lumlayout=True
                            self.TabElecLoad()
                            # self.lumlayout=False
                        except:
                            pass
            except:
                pass


    def Ptsdata(self,object, key):
        try:
            index=self.TabAnaSPNComBox.currentIndex()
            spname=self.tempdata["spaces"][index]["analysis_points"]
            try:
                ud=self.tempdata["general"]["display_units"]
                ui=self.tempdata["general"]["import_units"]
                value=self.uconvert(ud,ui,float(object.text()),False)
                spname[key]=float(value)
                self.WriteToFile()
                self.WISPWGCalc(index)
            except:
                # if self.jfimported:
                #     try:
                #         if self.markunit>=1:
                #             print "1.1"
                #             QtGui.QMessageBox.warning(self,"Warning", "Please define units first!")
                #     except:
                #         self.markunit=1
                # elif self.created:
                object.clear()
                QtGui.QMessageBox.warning(self,"Warning", "Please define dimension units first!")
                self.StadicTab.setCurrentIndex(0)

        except:
            pass

    def TabWinGLoad(self):
        if self.imported or self.created:
            self.TabWinWGComBox.clear()

            try:
                for cnt in reversed(range(self.TabWin2Grid3.count())):
                    widget = self.TabWin2Grid3.takeAt(cnt).widget()
                    if widget is not None:
                        widget.deleteLater()
            except:
                pass
            try:
                for cnt in reversed(range(self.TabWin2Grid4.count())):
                    widget = self.TabWin2Grid4.takeAt(cnt).widget()
                    if widget is not None:
                        widget.deleteLater()
            except:
                pass
            try:
                for cnt in reversed(range(self.TabWin2Grid5.count())):
                    widget = self.TabWin2Grid5.takeAt(cnt).widget()
                    if widget is not None:
                        widget.deleteLater()
            except:
                pass
            try:
                for cnt in reversed(range(self.TabWin2Grid6.count())):
                    widget = self.TabWin2Grid6.takeAt(cnt).widget()
                    if widget is not None:
                        widget.deleteLater()
            except:
                pass
            try:
                index=self.TabWinSPNComBox.currentIndex()
                spname=self.tempdata["spaces"][index]["window_groups"]
                try:
                    i=0
                    for item in spname:
                        try:
                            self.TabWinWGComBox.addItem(item["name"])
                        except:
                            QtGui.QMessageBox.warning(self, "Warning", "Empty Window Group! Deleted!")
                            del spname[i]
                        # try:
                        #     for j in range(len(spname[i]["calculate_setting"])):
                        #         spname[i]["calculate_setting"][j]=True
                        # except:
                        #     pass
                        i += 1

                    self.WriteToFile()
                except:
                    pass
                self.TabWinWGComBox.setCurrentIndex(0)
                self.TabWinGCombo()
            except:
                self.TabWinGCombo()

    def TabWinGCombo(self):
        if self.imported or self.created:
            index=self.TabWinSPNComBox.currentIndex()
            WGIndex=self.TabWinWGComBox.currentIndex()
            try:
                spname=self.tempdata["spaces"][index]["window_groups"][WGIndex]
            except:
                pass
            self.TabWinWGMatComBox.clear()
            # self.TabWinBSDFBMatComBox.clear()
            # self.TabWinBSDFSetList.clear()
            self.TabWinShadeTbl.setRowCount(0)
            try:
                for item in spname["glazing_materials"]:
                    self.TabWinWGMatComBox.addItem(item)
            except:
                pass
            try:
                # print WGIndex
                # print self.wgcalc[index][WGIndex]
                if self.wgcalc[index][WGIndex]==False:
                    # print "1"
                    self.WGCalCbx.setEnabled(1)
                else:
                    self.WGCalCbx.setChecked(1)
                    self.WGCalCbx.setDisabled(1)
            except:
                pass
            #BSDF disabled by now
            #try:
            #    bsdf=spname["BSDF"]
            #    self.TabWinBSDFChkB.setChecked(1)
            #    self.TabWinBSDFBMatComBox.setEnabled(1)
            #    self.TabWinBSDFSetList.setEnabled(1)
            #    self.TabWinBSDFBMatComBox.clear()

            #    for item in spname["bsdf_base_materials"]:
            #        self.TabWinBSDFBMatComBox.addItem(item)
            #    try:
            #        for item in spname["bsdf_setting_materials"][0]:
            #            self.TabWinBSDFSetList.addItem(item)
            #    except:
            #        spname["bsdf_setting_materials"]=[]
            #except:
            #    self.TabWinBSDFChkB.setChecked(0)
            #    self.TabWinBSDFBMatComBox.setDisabled(1)
            #    self.TabWinBSDFSetList.setDisabled(1)
            try:
                self.TabWinBGeoLineEd.setText(spname["base_geometry"])
            except:
                self.TabWinBGeoLineEd.setText("empty.rad")
                try:
                    self.tempdata["spaces"][index]["window_groups"][WGIndex]["base_geometry"]="empty.rad"
                except:
                    pass
            try:
                self.qbgroup=QtGui.QButtonGroup(self.TabWinShadeTbl) # Number group
                for i in range(len(spname["shade_settings"])):
                    self.TabWinShadeTbl.insertRow(self.TabWinShadeTbl.rowCount())
                    self.TabWinShadeTbl.setRowHeight(i, 40)
                    ShadeNBtn=QtGui.QPushButton(self.TabWin)
                    ShadeNBtn.setText(spname["shade_settings"][i])
                    self.TabWinShadeTbl.setCellWidget(i,0,ShadeNBtn)
                    ShadeEnCkB=QtGui.QRadioButton()
                    self.qbgroup.addButton(ShadeEnCkB)
                    sWg=QtGui.QWidget()
                    sWgL=QtGui.QHBoxLayout()
                    sWgL.addWidget(ShadeEnCkB)
                    sWgL.setAlignment(QtCore.Qt.AlignCenter)
                    sWg.setLayout(sWgL)
                    self.TabWinShadeTbl.setCellWidget(i,1, sWg)
                    # print "s1"
                    ShadeCalcCkB=QtGui.QCheckBox(self.TabWinShadeTbl)
                    sWg=QtGui.QWidget()
                    sWgL=QtGui.QHBoxLayout()
                    sWgL.addWidget(ShadeCalcCkB)
                    sWgL.setAlignment(QtCore.Qt.AlignCenter)
                    sWg.setLayout(sWgL)
                    self.TabWinShadeTbl.setCellWidget(i,2, sWg)
                    # print "s2"
                    ShadeCalcCkB.setChecked(1)
                    ShadeDelBtn=QtGui.QPushButton(self.TabWin)
                    ShadeDelBtn.setText("Delete")
                    # print "s3"
                    self.TabWinShadeTbl.setCellWidget(i,3,ShadeDelBtn)
                    ShadeCalcCkB.clicked.connect(self.SCalc)
                    ShadeDelBtn.clicked.connect(self.WShadeDel)
                    ShadeEnCkB.clicked.connect(self.ShadeCkB)
                    ShadeNBtn.clicked.connect(self.WShadeVE)
                    # print "s4"
                try:
                    self.qbgroup.button(-self.tempdata["spaces"][index]["sDA"]["window_group_settings"][WGIndex]-1).setChecked(1)
                except:
                    pass

                try:
                    for i in range(len(spname["shade_settings"])):
                        self.TabWinShadeTbl.cellWidget(i,2).findChild(type(QtGui.QCheckBox())).setChecked(spname["calculate_setting"][i])
                        try:
                            if self.sdcalc[index][WGIndex][i]==False:
                                self.TabWinShadeTbl.cellWidget(i,2).findChild(type(QtGui.QCheckBox())).setEnabled(1)
                            else:
                                self.TabWinShadeTbl.cellWidget(i,2).findChild(type(QtGui.QCheckBox())).setDisabled(1)
                        except:
                            self.TabWinShadeTbl.cellWidget(i,2).findChild(type(QtGui.QCheckBox())).setDisabled(1)
                except:
                    pass
                try:
                    if spname["shade_control"]["method"]=="automated_signal":
                        self.TabWinMtdComBox.setCurrentIndex(0)
                        self.ShadeCtrlMtd()
                    elif spname["shade_control"]["method"]=="automated_profile_angle":
                        self.TabWinMtdComBox.setCurrentIndex(1)
                        self.ShadeCtrlMtd()
                    elif spname["shade_control"]["method"]=="automated_profile_angle_signal":
                        self.TabWinMtdComBox.setCurrentIndex(2)
                        self.ShadeCtrlMtd()
                    else:
                        self.TabWinMtdComBox.setCurrentIndex(3)
                        self.ShadeCtrlMtd()
                except:
                    self.TabWinMtdComBox.setCurrentIndex(3)
                    self.ShadeCtrlMtd()
            except:
                self.TabWinMtdComBox.setCurrentIndex(3)
                self.ShadeCtrlMtd()
        self.WriteToFile()

    def WGAdd(self):
        if (self.imported or self.created) and (self.TabWinSPNComBox.count()>0):
            index=self.TabWinSPNComBox.currentIndex()
            name, ok=QtGui.QInputDialog.getText(self,"Add Window Group", "Group Name:", QtGui.QLineEdit.Normal)

            if ok and name !=" ":
                mark=0
                if len(str(name).split())>1:
                    QtGui.QMessageBox.warning(self, "Warning!", \
                                                      "No spaces (\" \") in the name!")
                else:
                    try:
                        for item in self.tempdata["spaces"][index]["window_groups"]:
                            try:
                                if item["name"]!= name:
                                    mark=0
                                    continue
                                else:
                                    mark=1
                                    QtGui.QMessageBox.warning(self, "Warning!", \
                                                              "The name is the same as one of the other window group name!")
                                    break
                            except:
                                mark=0
                    except:
                        pass
                    if mark==0:
                        self.TabWinWGComBox.addItem(str(name))

                        try:
                            self.tempdata["spaces"][index]["window_groups"].append({})
                        except:
                            self.tempdata["spaces"][index]["window_groups"]=[]
                            self.tempdata["spaces"][index]["window_groups"].append({})
                        WGIndex=self.TabWinWGComBox.count()-1
                        self.tempdata["spaces"][index]["window_groups"][WGIndex]["name"]=str(name)
                        self.tempdata["spaces"][index]["window_groups"][WGIndex]["calculate_base"]=True
                        try:
                            self.tempdata["spaces"][index]["sDA"]["window_group_settings"].append(0)
                        except:
                            try:
                                self.tempdata["spaces"][index]["sDA"]["window_group_settings"]=[]
                                self.tempdata["spaces"][index]["sDA"]["window_group_settings"].append(0)
                            except:
                                self.tempdata["spaces"][index]["sDA"]={}
                                self.tempdata["spaces"][index]["sDA"]["window_group_settings"]={}
                                self.tempdata["spaces"][index]["sDA"]["window_group_settings"].append(0)
                        try:
                            self.wgcalc[index].append(True)
                            self.sdcalc[index].append([])
                            # print self.wgcalc, self.sdcalc
                        except:
                            pass
                        self.WriteToFile()
                        self.TabWinWGComBox.setCurrentIndex(WGIndex)
                        self.TabWinMtdComBox.setCurrentIndex(3)



    def WGDel(self):
        if (self.imported or self.created) and (self.TabWinWGComBox.count()>1):
            index=self.TabWinSPNComBox.currentIndex()
            WGIndex=self.TabWinWGComBox.currentIndex()
            choice=QtGui.QMessageBox.question(self, "Warning", "Are you sure to DELETE the window group?", \
                                              QtGui.QMessageBox.Yes |QtGui.QMessageBox.No)
            if choice==QtGui.QMessageBox.Yes:
                del self.tempdata["spaces"][index]["window_groups"][WGIndex]
                try:
                    del self.tempdata["spaces"][index]["sDA"]["window_group_settings"][WGIndex]
                except:
                    pass
                self.TabWinWGComBox.removeItem(WGIndex)
                try:
                    del self.wgcalc[index][WGIndex]
                    del self.sdcalc[index][WGIndex]
                    # print self.wgcalc, self.sdcalc
                except:
                    pass
                self.WriteToFile()
                self.TabWinGCombo()
        else:
            QtGui.QMessageBox.warning(self,"No more window groups","Not deleted!")

    def WCalc(self):
        index=self.TabWinSPNComBox.currentIndex()
        WGIndex=self.TabWinWGComBox.currentIndex()
        if not self.WGCalCbx.isChecked():
            self.tempdata["spaces"][index]["window_groups"][WGIndex]["calculate_base"]=False
        else:
            self.tempdata["spaces"][index]["window_groups"][WGIndex]["calculate_base"]=True
        self.WriteToFile()

    def SCalc(self):
        button=self.sender()
        index=self.TabWinSPNComBox.currentIndex()
        bindex = self.TabWinShadeTbl.indexAt(button.pos())
        WGIndex=self.TabWinWGComBox.currentIndex()
        sindex=bindex.row()
        if not self.TabWinShadeTbl.cellWidget(sindex,2).findChild(type(QtGui.QCheckBox())).isChecked():
            self.tempdata["spaces"][index]["window_groups"][WGIndex]["calculate_setting"][sindex]=False
        else:
            self.tempdata["spaces"][index]["window_groups"][WGIndex]["calculate_setting"][sindex]=True
        self.WriteToFile()



    def WGMatAdd(self):
        if (self.imported or self.created) and (self.TabWinWGComBox.count()>0):
            index=self.TabWinSPNComBox.currentIndex()
            WGIndex=self.TabWinWGComBox.currentIndex()
            spname=self.tempdata["spaces"][index]
            self.combo=Ui_Combo()

            modifier=[]
            try:
                WGMatPath=os.path.normpath(os.path.join(self.dir,spname["geometry_directory"],spname["material_file"]))
                WGMatFile=open(WGMatPath,"r").read().split()
                count=0
                for item in WGMatFile:
                    if item=="void":
                        if WGMatFile[count+1]=="glass" or WGMatFile[count+1]=="trans":
                            modifier.append(WGMatFile[count+2])
                    count=count+1
            except:
                try:
                    WGMatPath=os.path.normpath(os.path.join(self.dir,spname["geometry_directory"],spname["material_file"]))
                    if os.path.exists(WGMatPath):
                        pass
                    else:
                        QtGui.QMessageBox.warning(self, "warning", "Material file does not exist!")
                except:
                    QtGui.QMessageBox.warning(self, "warning", "Material file does not exist!")
            try:
                WGMatPath3=os.path.normpath(os.path.join(self.dir,spname["geometry_directory"],spname["geometry_file"]))
                count=0
                if os.path.exists(WGMatPath3):
                    WGMatFile3=open(WGMatPath3,"r").read().split()
                    for item in WGMatFile3:
                        if item=="void":
                            if WGMatFile3[count+1]=="glass" or WGMatFile3[count+1]=="trans":
                                modifier.append(WGMatFile3[count+2])
                        count=count+1
            except:
                pass
            try:
                WGMatPath2=os.path.normpath(os.path.join(self.dir,spname["geometry_directory"],spname["window_groups"][WGIndex]["base_geometry"]))
                count=0
                if os.path.exists(WGMatPath2):
                    WGMatFile2=open(WGMatPath2,"r").read().split()
                    for item in WGMatFile2:
                        if item=="void":
                            if WGMatFile2[count+1]=="glass" or WGMatFile2[count+1]=="trans":
                                modifier.append(WGMatFile2[count+2])
                        count=count+1
                else:
                    QtGui.QMessageBox.warning(self, "warning", "Window Group Base File does not exist!")
            except:
                pass
            try:
                if len(modifier)>0:
                    for item in modifier:
                        self.combo.cbox.addItem(item)

                    self.combo.show()
                    self.combo.exec_()
                    try:
                        mname=self.combo.mat
                        try:
                            mark=0
                            for item in spname["window_groups"][WGIndex]["glazing_materials"]:
                                t1=str(item)
                                t2=str(mname)
                                if t1==t2:
                                    mark=1
                            if mark==0:
                                spname["window_groups"][WGIndex]["glazing_materials"].append(str(mname))
                                # print "add"
                            else:
                                QtGui.QMessageBox.warning(self,"Warning", "Material already existed!")
                        except:
                            spname["window_groups"][WGIndex]["glazing_materials"]=[]
                            spname["window_groups"][WGIndex]["glazing_materials"].append(str(mname))
                        try:
                            self.wgcalc[index][WGIndex]==True
                            try:
                                for i in range(len(spname["window_groups"][WGIndex]["shade_settings"])):
                                    try:
                                        self.sdcalc[index][WGIndex][i]=True
                                        spname["window_groups"][WGIndex]["calculate_setting"][i]=True
                                    except:
                                        pass
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                    self.WriteToFile()
                    self.TabWinGCombo()
            except:
                pass


    def WGMatDel(self):
        if (self.imported or self.created) and (self.TabWinWGComBox.count()>0):
            index=self.TabWinSPNComBox.currentIndex()
            WGIndex=self.TabWinWGComBox.currentIndex()
            MIndex=self.TabWinWGMatComBox.currentIndex()
            try:
                if len(self.tempdata["spaces"][index]["window_groups"][WGIndex]["glazing_materials"])>0:
                    choice=QtGui.QMessageBox.question(self,"Warning", "Are you sure to delete?", \
                                                              QtGui.QMessageBox.Yes |QtGui.QMessageBox.No)
                    if choice==QtGui.QMessageBox.Yes:
                        try:
                            del self.tempdata["spaces"][index]["window_groups"][WGIndex]["glazing_materials"][MIndex]

                            try:
                                self.wgcalc[index][WGIndex]==True
                                try:
                                    for i in range(len(self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_settings"])):
                                        try:
                                            self.sdcalc[index][WGIndex][i]=True
                                            self.tempdata["spaces"][index]["window_groups"][WGIndex]["calculate_setting"][i]=True
                                        except:
                                            pass
                                except:
                                    pass
                            except:
                                pass
                            self.TabWinWGMatComBox.removeItem(MIndex)
                            self.WriteToFile()
                        except:
                            pass
            except:
                pass

    def WinG(self):
        if (self.imported or self.created) and (self.TabWinWGComBox.count()>0):
            GeoFile= QtGui.QFileDialog.getOpenFileName(self,"Import Geometry File",self.dir,"Geometry Rad File (*.rad)")
            if GeoFile:
                index=self.TabWinSPNComBox.currentIndex()
                WGIndex=self.TabWinWGComBox.currentIndex()
                GPath=os.path.join(self.dir,self.tempdata["spaces"][index]["geometry_directory"])
                GeoLine=self.CopyFile(GeoFile,GPath)
                self.TabWinBGeoLineEd.setText(os.path.basename(str(GeoLine)))
                self.tempdata["spaces"][index]["window_groups"][WGIndex]["base_geometry"]=os.path.basename(str(GeoLine))
                try:
                    self.wgcalc[index][WGIndex]==True
                    try:
                        for i in range(len(self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_settings"])):
                            try:
                                self.sdcalc[index][WGIndex][i]=True
                                self.tempdata["spaces"][index]["window_groups"][WGIndex]["calculate_setting"][i]=True
                            except:
                                pass
                    except:
                        pass
                except:
                    pass
                self.WriteToFile()
                self.TabWinGCombo()

    def WShadeVE(self):
        button = self.sender()
        index=self.TabWinSPNComBox.currentIndex()
        bindex = self.TabWinShadeTbl.indexAt(button.pos())
        WGIndex=self.TabWinWGComBox.currentIndex()
        sindex=bindex.row()
        widget=self.TabWinShadeTbl.cellWidget(bindex.row(),bindex.column())
        p1=os.path.join(self.dir, str(self.tempdata["spaces"][index]["geometry_directory"]))
        fpath=QtGui.QFileDialog.getOpenFileName(self,"Change Shade File",p1,"Rad File (*.rad)")
        # print fpath
        if fpath:
            base=os.path.basename(str(fpath))
            widget.setText(base)
            self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_settings"][sindex]=base
            # print self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_settings"][sindex]
            self.WriteToFile()
        # fpath=str(os.path.join(self.dir, self.tempdata["spaces"][index]["geometry_directory"], \
        #                            self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_settings"][sindex]))
        # if os.path.exists(fpath):
        #     QtGui.QMessageBox.warning(self,"Warning!!!","Please replace the file if you did save as!")
        #     os.system(fpath)
        #     try:
        #         try:
        #             self.sdcalc[index][WGIndex][sindex]=True
        #         except:
        #             pass
        #         self.tempdata["spaces"][index]["window_groups"][WGIndex]["calculate_setting"][sindex]=True
        #         # print self.sdcalc
        #         self.WriteToFile()
        #         self.TabWinGLoad()
        #     except:
        #         pass
        # else:
        #     QtGui.QMessageBox.warning(self,"Warning!!!","No such file in directory!!!")

    def WShadeAdd(self):
        if (self.imported or self.created) and (self.TabWinWGComBox.count()>0):
            SFile= QtGui.QFileDialog.getOpenFileName(self,"Import Shade File",self.dir,"Shade Rad File (*.rad)")
            if SFile:
                index=self.TabWinSPNComBox.currentIndex()
                WGIndex=self.TabWinWGComBox.currentIndex()
                SPath=os.path.join(self.dir,self.tempdata["spaces"][index]["geometry_directory"])
                SLine=self.CopyFile(SFile,SPath)
                self.TabWinShadeTbl.insertRow(self.TabWinShadeTbl.rowCount())
                i=self.TabWinShadeTbl.rowCount()-1
                self.TabWinShadeTbl.setRowHeight(i,40)
                ShadeNBtn=QtGui.QPushButton(self.TabWin)
                ShadeNBtn.setText(os.path.basename(str(SLine)))
                self.TabWinShadeTbl.setCellWidget(i,0,ShadeNBtn)
                ShadeNBtn.clicked.connect(self.WShadeVE)
                ShadeEnCkB=QtGui.QRadioButton()
                self.qbgroup.addButton(ShadeEnCkB)
                sWg=QtGui.QWidget()
                sWgL=QtGui.QHBoxLayout()
                sWgL.addWidget(ShadeEnCkB)
                sWgL.setAlignment(QtCore.Qt.AlignCenter)
                sWg.setLayout(sWgL)
                self.TabWinShadeTbl.setCellWidget(i,1, sWg)
                ShadeEnCkB.clicked.connect(self.ShadeCkB)
                ShadeDelBtn=QtGui.QPushButton(self.TabWin)
                ShadeDelBtn.setText("Delete")
                ShadeDelBtn.clicked.connect(self.WShadeDel)
                self.TabWinShadeTbl.setCellWidget(i,2,ShadeDelBtn)
                try:
                    self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_settings"].append(os.path.basename(str(SLine)))
                    self.tempdata["spaces"][index]["window_groups"][WGIndex]["calculate_setting"].append(True)
                    try:
                        self.sdcalc[index][WGIndex].append(True)
                    except:
                        pass
                except:
                    self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_settings"]=[]
                    self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_settings"].append(os.path.basename(str(SLine)))
                    self.tempdata["spaces"][index]["window_groups"][WGIndex]["calculate_setting"]=[]
                    self.tempdata["spaces"][index]["window_groups"][WGIndex]["calculate_setting"].append(True)
                    self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]={}
                    try:
                        self.sdcalc[index][WGIndex].append(True)
                    except:
                        pass
                # try:
                #
                #     self.tempdata["spaces"][index]["sDA"]["window_group_settings"].append(0)
                # except:
                #     self.tempdata["spaces"][index]["sDA"]["window_group_settings"]=[]
                #     self.tempdata["spaces"][index]["sDA"]["window_group_settings"].append(0)
                self.WriteToFile()
                self.TabWinGCombo()

    def WShadeDel(self):
        if (self.imported or self.created):
            btn=self.sender()
            bindex = self.TabWinShadeTbl.indexAt(btn.pos())
            index=self.TabWinSPNComBox.currentIndex()
            WGIndex=self.TabWinWGComBox.currentIndex()
            sname=self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_settings"][bindex.row()]
            choice=QtGui.QMessageBox.question(self,"Warning", "Are you sure to delete the shade: %s?" %sname, QtGui.QMessageBox.Yes |QtGui.QMessageBox.No)
            if choice==QtGui.QMessageBox.Yes:
                sname=self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_settings"][bindex.row()]
                del self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_settings"][bindex.row()]
                del self.tempdata["spaces"][index]["window_groups"][WGIndex]["calculate_setting"][bindex.row()]
                self.TabWinShadeTbl.removeRow(bindex.row())
                try:
                    spname=self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]
                    del spname["angle_settings"][bindex.row()]
                except:
                    pass
                try:
                    spname=self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]
                    del spname["signal_settings"][bindex.row()]

                except:
                    pass
                try:
                    del self.sdcalc[index][WGIndex][bindex.row()]
                except:
                    pass
                self.WriteToFile()
                try:
                    if self.tempdata["spaces"][index]["sDA"]["window_group_settings"][WGIndex]>len(self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_settings"]):
                        self.tempdata["spaces"][index]["sDA"]["window_group_settings"][WGIndex]=len(self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_settings"])
                except:
                    pass

                if len(self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_settings"])==0:
                    try:
                        del self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_settings"]
                    except:
                        pass
                    try:
                        del self.tempdata["spaces"][index]["window_groups"][WGIndex]["calculate_setting"]
                    except:
                        pass
                    try:
                        del self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]
                    except:
                        pass
                    self.tempdata["spaces"][index]["sDA"]["window_group_settings"][WGIndex]=0
                    self.TabWinMtdComBox.setCurrentIndex(3)

                self.WriteToFile()
                self.TabWinGLoad()
                # self.ShadeCtrlMtd()


    def ShadeCkB(self):
        cbx=self.sender()
        bindex = self.TabWinShadeTbl.indexAt(cbx.pos())
        index=self.TabWinSPNComBox.currentIndex()
        WGIndex=self.TabWinWGComBox.currentIndex()
        count=self.TabWinWGComBox.count()
        item=self.TabWinShadeTbl.cellWidget(bindex.row(),1)
        try:
            self.tempdata["spaces"][index]["sDA"]["window_group_settings"][WGIndex]=-1-self.qbgroup.checkedId()
        except:
            try:
                for i in range(count):
                    try:
                        self.tempdata["spaces"][index]["sDA"]["window_group_settings"][i]
                    except:
                        self.tempdata["spaces"][index]["sDA"]["window_group_settings"].append(0)
                self.tempdata["spaces"][index]["sDA"]["window_group_settings"][WGIndex]=-1-self.qbgroup.checkedId()
            except:
                self.tempdata["spaces"][index]["sDA"]["window_group_settings"]=[]
                for i in range(count):
                    self.tempdata["spaces"][index]["sDA"]["window_group_settings"].append(0)
                self.tempdata["spaces"][index]["sDA"]["window_group_settings"][WGIndex]=-1-self.qbgroup.checkedId()
        self.WriteToFile()


    def ShadeCtrlMtd(self):
        try:
            if (self.imported or self.created) and (self.TabWinWGComBox.count()>0):

                index=self.TabWinSPNComBox.currentIndex()
                WGIndex=self.TabWinWGComBox.currentIndex()
                try:
                    for cnt in reversed(range(self.TabWin2Grid3.count())):
                        widget = self.TabWin2Grid3.takeAt(cnt).widget()
                        if widget is not None:
                            widget.deleteLater()
                except:
                    pass
                try:
                    for cnt in reversed(range(self.TabWin2Grid4.count())):
                        widget = self.TabWin2Grid4.takeAt(cnt).widget()
                        if widget is not None:
                            widget.deleteLater()
                except:
                    pass
                try:
                    for cnt in reversed(range(self.TabWin2Grid5.count())):
                        widget = self.TabWin2Grid5.takeAt(cnt).widget()
                        if widget is not None:
                            widget.deleteLater()
                except:
                    pass
                try:
                    for cnt in reversed(range(self.TabWin2Grid6.count())):
                        widget = self.TabWin2Grid6.takeAt(cnt).widget()
                        if widget is not None:
                            widget.deleteLater()
                except:
                    pass
                try:
                    if len(self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_settings"])>0:
                        try:
                            spname=self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]
                        except:
                            self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]={}
                            spname=self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]
                        MIndex=self.TabWinMtdComBox.currentIndex()
                        if MIndex==0:
                            spname["method"]="automated_signal"
                            self.SCtrlSig()
                            try:
                                del spname["angle_settings"], spname["elevation_azimuth"]
                            except:
                                pass
                        elif MIndex==1:
                            self.SCtrlAng()
                            spname["method"]="automated_profile_angle"
                            try:
                                del spname["signal_settings"], spname["sensor"]
                            except:
                                pass
                        elif MIndex==2:
                            self.SCtrlBoth()
                            spname["method"]="automated_profile_angle_signal"
                        else:
                            # print "none"
                            self.SCtrlNone()
                        self.WriteToFile()
                except:
                    pass
        except:
            pass



    def SCtrlAng(self):
        if (self.imported or self.created) and (self.TabWinWGComBox.count()>0):
            self.TabWin2Grid3=QtGui.QGridLayout()
            self.WGrid1.addLayout(self.TabWin2Grid3, 3,1,1,1)
            spacerItem = QtGui.QSpacerItem(20, 60, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
            self.TabWin2Grid3.addItem(spacerItem, 0, 0, 1, 1)
            number=self.TabWinShadeTbl.rowCount()
            index=self.TabWinSPNComBox.currentIndex()
            WGIndex=self.TabWinWGComBox.currentIndex()
            spname=self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]
            spname["method"]="automated_profile_angle"
            try:
                if self.sdeleteang!=-1:
                    del spname["angle_settings"][self.sdeleteang]
                    self.sdeleteang=-1
                self.WriteToFile()
            except:
                pass
            self.TabWinAngCLbl=QtGui.QLabel(self.TabWin)
            self.TabWin2Grid3.addWidget(self.TabWinAngCLbl, 1,0,1,1)
            self.TabWinAngCLbl.setText("Angle Control:")
            self.TabWinSElvLbl=QtGui.QLabel(self.TabWin)
            self.TabWin2Grid3.addWidget(self.TabWinSElvLbl, 2,1,1,1)
            self.TabWinSElvLbl.setText("Elevation Az:")
            self.TabWinSElvLbl.setFixedWidth(125)
            self.TabWinSElvLineEd=QtGui.QLineEdit(self.TabWin)
            self.TabWinSElvLineEd.setFixedWidth(100)
            self.TabWin2Grid3.addWidget(self.TabWinSElvLineEd,2,2,1,1)
            self.TabWinSElvLineEd.editingFinished.connect(self.elev)
            try:
                self.TabWinSElvLineEd.setText(str(spname["elevation_azimuth"]))
            except:
                pass
            self.TabWinSSetLbl=QtGui.QLabel(self.TabWin)
            self.TabWin2Grid3.addWidget(self.TabWinSSetLbl, 3,1,1,1)
            self.TabWinSSetLbl.setText("Settings:")
            self.TabWinSSetLbl.setAlignment(QtCore.Qt.AlignTop)
            self.TabWinAngTbl=QtGui.QTableWidget(self.TabWin)
            self.TabWin2Grid3.addWidget(self.TabWinAngTbl, 3,2,1,1)
            self.TabWinAngTbl.setFixedHeight(80)
            self.TabWinAngTbl.setColumnCount(number)
            self.TabWinAngTbl.setRowCount(1)
            for i in range(number):
                item = QtGui.QTableWidgetItem()
                self.TabWinAngTbl.setHorizontalHeaderItem(i,item)
                text="Angle "+str(i+1)
                item.setText(text)
                try:
                    angle=str(spname["angle_settings"][i])
                    item=self.tableitem(angle)
                    self.TabWinAngTbl.setItem(0,i,item)
                except:
                    pass
            spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            self.TabWin2Grid3.addItem(spacerItem, 4 ,3, 1, 1)
            self.TabWinAngTbl.cellChanged.connect(self.CtrlAngTbl)
            try:
                if spname["sensor"]["location"]=={}:
                    del spname["sensor"]["location"]
                    if spname["sensor"]=={}:
                        del spname["sensor"]
            except:
                pass
            self.WriteToFile()

    def elev(self):
        index=self.TabWinSPNComBox.currentIndex()
        WGIndex=self.TabWinWGComBox.currentIndex()
        mark=0
        mark=self.intChk(self.TabWinSElvLineEd, -180, 180)
        if mark!=0:
            self.TabWinSElvLineEd.setText("0")
            self.TabWinSElvLineEd.setFocus()
        try:
            spname=self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]
            spname["elevation_azimuth"]=int(self.TabWinSElvLineEd.text())
        except:
            spname=self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]={}
            spname["elevation_azimuth"]=int(self.TabWinSElvLineEd.text())
        self.WriteToFile()

    def CtrlAngTbl(self):
        col = self.TabWinAngTbl.currentColumn()
        item=self.TabWinAngTbl.item(0,col)
        index=self.TabWinSPNComBox.currentIndex()
        WGIndex=self.TabWinWGComBox.currentIndex()
        try:
            spname=self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]["angle_settings"]
        except:
            self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]["angle_settings"]=[]
            spname=self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]["angle_settings"]
        if self.TabWinAngTbl.isItemSelected(item):
            mark=0
            mark=self.intChk(item, 0,90)
            if mark!=0:
                try:
                    self.TabWinAngTbl.item(0,col).setText(str(spname[col-2]))
                except:
                    self.TabWinAngTbl.item(0,col).setText("0")
            try:
                spname[col]=int(item.text())
            except:
                for i in range(len(spname), col+1):
                    spname.append(0)
                spname[col]=int(item.text())
            try:
                for i in range(0,len(spname)-1):
                    if int(spname[i+1])<int(spname[i]):
                        if i>col-1:
                            spname[i]=spname[i+1]-1
                            self.TabWinAngTbl.item(0,i).setText(str(spname[i]))
                        else:
                            spname[i+1]=spname[i]+1
                            self.TabWinAngTbl.item(0,i+1).setText(str(spname[i+1]))
                        QtGui.QMessageBox.warning(self, "Warning!","Wrong Entry! Only increments in angle can be accepted!")
                        break
            except:
                pass
            item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.WriteToFile()


    def SCtrlSig(self):
        if (self.imported or self.created) and (self.TabWinWGComBox.count()>0):
            self.TabWin2Grid4=QtGui.QGridLayout()
            self.WGrid1.addLayout(self.TabWin2Grid4, 4, 1,1,1)
            self.TabWinPSenLbl=QtGui.QLabel(self.TabWin)
            self.TabWin2Grid4.addWidget(self.TabWinPSenLbl, 0, 0, 1, 1)
            self.TabWinPSenLbl.setText("Photosensor:")
            self.TabWinUnitsLbl=QtGui.QLabel(self.TabWin)
            self.TabWin2Grid4.addWidget(self.TabWinUnitsLbl, 0, 1, 1, 1)
            try:
                self.TabWinUnitsLbl.setText("Units (%s)"%self.tempdata["general"]["display_units"])
            except:
                if self.jfimported:
                    try:
                        if self.markunit>=1:
                            # print "2.0"
                            QtGui.QMessageBox.warning(self,"Warning", "Please define dimension units first!")
                    except:
                        self.markunit=1
                elif self.created:
                    QtGui.QMessageBox.warning(self,"Warning", "Please define dimension units first!")
            self.TabWinSenTPLbl=QtGui.QLabel(self.TabWin)
            self.TabWin2Grid4.addWidget(self.TabWinSenTPLbl, 1, 1, 1, 1)
            self.TabWinSenTPLbl.setText("Sensor Type:")
            self.TabWinSenTPComBox=QtGui.QComboBox(self.TabWin)
            self.TabWin2Grid4.addWidget(self.TabWinSenTPComBox, 1, 2, 1, 1)
            self.TabWinSenTPComBox.addItem("Sensitivity File")
            self.TabWinSenTPComBox.addItem("Cosine")
            spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            self.TabWin2Grid4.addItem(spacerItem, 1, 4, 1, 1)
            self.TabWinSenFLbl=QtGui.QLabel(self.TabWin)
            self.TabWin2Grid4.addWidget(self.TabWinSenFLbl, 2, 1, 1, 1)
            self.TabWinSenFLbl.setText("Sensitivity File:")
            self.TabWinSenFLineEd=QtGui.QLineEdit(self.TabWin)
            self.TabWin2Grid4.addWidget(self.TabWinSenFLineEd, 2, 2, 1, 1)
            self.TabWinSenFBrwBtn=QtGui.QPushButton(self.TabWin)
            self.TabWin2Grid4.addWidget(self.TabWinSenFBrwBtn, 2, 3, 1, 1)
            self.TabWinSenFBrwBtn.setText("Browse")
            spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
            self.TabWin2Grid4.addItem(spacerItem, 3, 1, 1, 1)

            index=self.TabWinSPNComBox.currentIndex()
            WGIndex=self.TabWinWGComBox.currentIndex()
            spname=self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]
            try:
                spname["sensor"]["location"]
            except:
                spname["sensor"]={}
                spname["sensor"]["location"]={}
            self.SenType()
            self.TabWinSenFBrwBtn.clicked.connect(self.SFImport)
            self.TabWinSenTPComBox.currentIndexChanged.connect(self.SenType)

    def SenType(self):
        self.TabWin2Grid5=QtGui.QGridLayout()
        self.WGrid1.addLayout(self.TabWin2Grid5, 5, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(230, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.TabWin2Grid5.addItem(spacerItem, 0, 0, 1, 1)
        self.TabWinSenXLbl=QtGui.QLabel(self.TabWin)
        self.TabWin2Grid5.addWidget(self.TabWinSenXLbl, 0, 1, 1, 1)
        self.TabWinSenXLbl.setText("X:")
        self.TabWinSenXLineEd=QtGui.QLineEdit(self.TabWin)
        self.TabWin2Grid5.addWidget(self.TabWinSenXLineEd, 0, 2, 1, 1)
        self.TabWinSenXLineEd.setFixedWidth(80)
        self.TabWinSenYLbl=QtGui.QLabel(self.TabWin)
        self.TabWin2Grid5.addWidget(self.TabWinSenYLbl, 0, 3, 1, 1)
        self.TabWinSenYLbl.setText("Y:")
        self.TabWinSenYLineEd=QtGui.QLineEdit(self.TabWin)
        self.TabWin2Grid5.addWidget(self.TabWinSenYLineEd, 0, 4, 1, 1)
        self.TabWinSenYLineEd.setFixedWidth(80)
        self.TabWinSenZLbl=QtGui.QLabel(self.TabWin)
        self.TabWin2Grid5.addWidget(self.TabWinSenZLbl, 0, 5, 1, 1)
        self.TabWinSenZLbl.setText("Z:")
        self.TabWinSenZLineEd=QtGui.QLineEdit(self.TabWin)
        self.TabWin2Grid5.addWidget(self.TabWinSenZLineEd, 0, 6, 1, 1)
        self.TabWinSenZLineEd.setFixedWidth(80)
        spacerItem = QtGui.QSpacerItem(150, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.TabWin2Grid5.addItem(spacerItem, 0, 7, 1, 1)
        self.TabWinSenXDirLbl=QtGui.QLabel(self.TabWin)
        self.TabWin2Grid5.addWidget(self.TabWinSenXDirLbl, 1, 1, 1, 1)
        self.TabWinSenXDirLbl.setText("X Dir:")
        self.TabWinSenXDirLineEd=QtGui.QLineEdit(self.TabWin)
        self.TabWin2Grid5.addWidget(self.TabWinSenXDirLineEd, 1, 2, 1, 1)
        self.TabWinSenXDirLineEd.setFixedWidth(80)
        self.TabWinSenYDirLbl=QtGui.QLabel(self.TabWin)
        self.TabWin2Grid5.addWidget(self.TabWinSenYDirLbl, 1, 3, 1, 1)
        self.TabWinSenYDirLbl.setText("Y Dir:")
        self.TabWinSenYDirLineEd=QtGui.QLineEdit(self.TabWin)
        self.TabWin2Grid5.addWidget(self.TabWinSenYDirLineEd, 1, 4, 1, 1)
        self.TabWinSenYDirLineEd.setFixedWidth(80)
        self.TabWinSenZDirLbl=QtGui.QLabel(self.TabWin)
        self.TabWin2Grid5.addWidget(self.TabWinSenZDirLbl, 1, 5, 1, 1)
        self.TabWinSenZDirLbl.setText("Z Dir:")
        self.TabWinSenZDirLineEd=QtGui.QLineEdit(self.TabWin)
        self.TabWin2Grid5.addWidget(self.TabWinSenZDirLineEd, 1, 6, 1, 1)
        self.TabWinSenZDirLineEd.setFixedWidth(80)
        self.TabWinSenSpinLbl=QtGui.QLabel(self.TabWin)
        self.TabWin2Grid5.addWidget(self.TabWinSenSpinLbl, 2, 1, 1, 1)
        self.TabWinSenSpinLbl.setText("Spin:")
        self.TabWinSenSpinLineEd=QtGui.QLineEdit(self.TabWin)
        self.TabWinSenSpinLineEd.setFixedWidth(80)
        self.TabWin2Grid5.addWidget(self.TabWinSenSpinLineEd, 2, 2, 1, 1)
        number=self.TabWinShadeTbl.rowCount()
        index=self.TabWinSPNComBox.currentIndex()
        WGIndex=self.TabWinWGComBox.currentIndex()
        spname=self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]
        self.TabWin2Grid6=QtGui.QGridLayout()
        self.WGrid1.addLayout(self.TabWin2Grid6, 6, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(150, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.TabWin2Grid6.addItem(spacerItem, 0, 0, 1, 1)
        self.TabWinSigCLbl=QtGui.QLabel()
        self.TabWin2Grid6.addWidget(self.TabWinSigCLbl, 1,1,1,1)
        self.TabWinSigCLbl.setText("Settings:")
        self.TabWinSigTbl=QtGui.QTableWidget(self.TabWin)
        self.TabWin2Grid6.addWidget(self.TabWinSigTbl, 1,2,1,1)
        self.TabWinSigTbl.setFixedHeight(80)
        self.TabWinSigTbl.setColumnCount(number)
        self.TabWinSigTbl.setRowCount(1)
        for i in range(number):
            item = QtGui.QTableWidgetItem()
            self.TabWinSigTbl.setHorizontalHeaderItem(i,item)
            text="Signal "+str(i+1)
            item.setText(text)
            try:
                signal=str(spname["signal_settings"][i])
                item=self.tableitem(signal)
                self.TabWinSigTbl.setItem(0,i,item)
            except:
                pass
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.TabWin2Grid6.addItem(spacerItem, 1 ,3, 1, 1)
        self.TabWinSigCLbl.setAlignment(QtCore.Qt.AlignTop)
        SenL=lambda: self.sctrldata(self.TabWinSenXLineEd,"x")
        self.TabWinSenXLineEd.editingFinished.connect(SenL)
        SenL=lambda: self.sctrldata(self.TabWinSenYLineEd,"y")
        self.TabWinSenYLineEd.editingFinished.connect(SenL)
        SenL=lambda: self.sctrldata(self.TabWinSenZLineEd,"z")
        self.TabWinSenZLineEd.editingFinished.connect(SenL)
        SenL=lambda: self.sctrldata(self.TabWinSenXDirLineEd,"xd")
        self.TabWinSenXDirLineEd.editingFinished.connect(SenL)
        SenL=lambda: self.sctrldata(self.TabWinSenYDirLineEd,"yd")
        self.TabWinSenYDirLineEd.editingFinished.connect(SenL)
        SenL=lambda: self.sctrldata(self.TabWinSenZDirLineEd,"zd")
        self.TabWinSenZDirLineEd.editingFinished.connect(SenL)
        SenL=lambda: self.sctrldata(self.TabWinSenSpinLineEd,"spin_ccw")
        self.TabWinSenSpinLineEd.editingFinished.connect(SenL)
        try:
            ud=self.tempdata["general"]["display_units"]
            ui=self.tempdata["general"]["import_units"]
            try:
                self.setUnitText(self.TabWinSenXLineEd,ud,ui,spname["sensor"]["location"]["x"],True)
            except:
                pass
            try:
                self.setUnitText(self.TabWinSenYLineEd,ud,ui,spname["sensor"]["location"]["y"],True)
            except:
                pass
            try:
                self.setUnitText(self.TabWinSenZLineEd,ud,ui,spname["sensor"]["location"]["z"],True)
            except:
                pass
        except:
            pass
        try:
            self.TabWinSenXDirLineEd.setText(str(spname["sensor"]["location"]["xd"]))
        except:
            pass
        try:
            self.TabWinSenYDirLineEd.setText(str(spname["sensor"]["location"]["yd"]))
        except:
            pass
        try:
            self.TabWinSenZDirLineEd.setText(str(spname["sensor"]["location"]["zd"]))
        except:
            pass
        try:
            self.TabWinSenSpinLineEd.setText(str(spname["sensor"]["location"]["spin_ccw"]))
        except:
            pass


        if self.TabWinSenTPComBox.currentIndex()==0:
            self.TabWinSenFLineEd.setEnabled(1)
            self.TabWinSenFBrwBtn.setEnabled(1)
            self.TabWinSenFLineEd.setReadOnly(1)
            try:
                self.TabWinSenFLineEd.setText(str(spname["sensor"]["sensor_file"]))
            except:
                pass
        else:
            self.TabWinSenFLineEd.setDisabled(1)
            self.TabWinSenFLineEd.clear()
            self.TabWinSenFBrwBtn.setDisabled(1)
            index=self.TabWinSPNComBox.currentIndex()
            WGIndex=self.TabWinWGComBox.currentIndex()
            self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]["sensor"]["sensor_type"]="cosine"
            try:
                del self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]["sensor"]["sensor_file"]
            except:
                pass
        self.WriteToFile()
        self.TabWinSigTbl.cellChanged.connect(self.CtrlSigTbl)
        # self.TabWinSenTPComBox.currentIndexChanged.connect(self.SenType)

    def SFImport(self):
        if self.imported or self.created:
            try:
                SFile= QtGui.QFileDialog.getOpenFileName(self,"Import Sensor File",self.dir,"Sensor File (*.sen)")
                if SFile:
                    index=self.TabWinSPNComBox.currentIndex()
                    WGIndex=self.TabWinWGComBox.currentIndex()
                    try:
                        spname=self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]["sensor"]
                    except:
                        self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]["sensor"]={}
                        spname=self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]["sensor"]
                    spname["sensor_type"]="sensitivity_file"
                    SPath=os.path.join(self.dir,self.tempdata["spaces"][index]["input_directory"])
                    SLine=self.CopyFile(SFile,SPath)
                    SPath=os.path.join(self.dir)
                    SSLine=self.CopyFile(SFile,SPath)
                    self.TabWinSenFLineEd.setText(os.path.basename(SLine))
                    spname["sensor_file"]=os.path.basename(str(SLine))
                    self.WriteToFile()
            except:
                pass

    def CtrlSigTbl(self):
        col = self.TabWinSigTbl.currentColumn()
        item=self.TabWinSigTbl.item(0,col)
        index=self.TabWinSPNComBox.currentIndex()
        WGIndex=self.TabWinWGComBox.currentIndex()
        try:
            spname=self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]["signal_settings"]
        except:
            self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]["signal_settings"]=[]
            spname=self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]["signal_settings"]

        if self.TabWinSigTbl.isItemSelected(item):
            mark=0
            mark=self.intChk(item, 0,1000000)
            if mark!=0:
                try:
                    self.TabWinSigTbl.item(0,col).setText(str(spname[col-2]))
                except:
                    self.TabWinSigTbl.item(0,col).setText("0")
            try:
                spname[col]=int(item.text())
            except:
                for i in range(len(spname), col+1):
                    spname.append(0)
                spname[col]=int(item.text())

            # try:
            #     for i in range(0,len(spname)-1):
            #         if int(spname[i+1])>int(spname[i]):
            #             if i>col-1:
            #                 spname[i]=spname[i+1]
            #                 self.TabWinSigTbl.item(0,i).setText(str(spname[i]))
            #             else:
            #                 spname[i+1]=spname[i]
            #                 self.TabWinSigTbl.item(0,i+1).setText(str(spname[i+1]))
            #             QtGui.QMessageBox.warning(self, "Warning!","Wrong Entry! Only increments in angle can be accepted!")
            #             break
            # except:
            #     pass
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.WriteToFile()

    def SCtrlBoth(self):
        self.SCtrlAng()
        self.SCtrlSig()

    def SCtrlNone(self):
        if (self.imported or self.created) and (self.TabWinWGComBox.count()>0):
            index=self.TabWinSPNComBox.currentIndex()
            WGIndex=self.TabWinWGComBox.currentIndex()
            del self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]

    def sctrldata(self, object, key):
        mark=0
        index=self.TabWinSPNComBox.currentIndex()
        WGIndex=self.TabWinWGComBox.currentIndex()
        try:
            ud=self.tempdata["general"]["display_units"]
            ui=self.tempdata["general"]["import_units"]
            try:
                spname=self.tempdata["spaces"][index]["window_groups"][WGIndex]["shade_control"]["sensor"]
                mark=self.floatChk(object)
                if mark!=0:
                    object.setText("0")
                    object.setFocus()
                try:
                    if key=="x" or key=="y" or key=="z":
                        spname["location"][key]=self.uconvert(ud,ui,float(object.text()),False)
                    else:
                        spname["location"][key]=float(object.text())
                except:
                    spname["location"]={}
                    if key=="x" or key=="y" or key=="z":
                        spname["location"][key]=self.uconvert(ud,ui,float(object.text()),False)
                    else:
                        spname["location"][key]=float(object.text())
                self.WriteToFile()
            except:
                pass
        except:
            object.clear()
            QtGui.QMessageBox.warning(self,"Warning", "Please define dimension units first!")
            self.StadicTab.setCurrentIndex(0)

    def TabElecLoad(self):
        if self.imported or self.created:
            try:
                index=self.TabElecSPComBox.currentIndex()
                self.TabElecLayerCbx.clear()
                try:
                    spname=self.tempdata["spaces"][index]
                except:
                    pass
                try:
                    len(spname["layout_base"])>=1
                    for item in spname["layout_base"]:
                        self.TabElecLayerCbx.addItem(item)
                    # if self.lumlayout==True:
                    #     self.LumLayoutDisplay()
                except:
                    pass
                self.TabElecInfoTable.setRowCount(0)
                self.TabElecZoneCombox.clear()
                self.TabElecLayoutDipBtn.setEnabled(1)
                self.TabElecInfoAddBtn.setEnabled(1)
                self.TabElecLayoutAddBtn.setEnabled(1)
                try:
                    spname=self.tempdata["spaces"][index]["control_zones"]

                    for i in range(len(spname)):
                        self.TabElecInfoTable.insertRow(self.TabElecInfoTable.rowCount())
                        self.TabElecInfoTable.setRowHeight(i,40)

                        ctrlTP=QtGui.QComboBox()
                        ctrlTP.addItem("linear dimming")
                        ctrlTP.addItem("non dimming")
                        ctrlTP.addItem("Eplus Dimming")
                        self.TabElecInfoTable.setCellWidget(i,8,ctrlTP)

                        try:
                            self.TabElecZoneCombox.addItem(spname[i]["name"])
                            zoneName=spname[i]["name"]
                            item=self.tableitem(zoneName)
                            self.TabElecInfoTable.setItem(i,0,item)
                        except:
                            pass

                        try:
                            LLF=spname[i]["luminaire_information"]["LLF"]
                            item=self.tableitem(LLF)
                            self.TabElecInfoTable.setItem(i,3,item)
                        except:
                            pass
                        try:
                            junk=spname[i]["ballast_driver_information"]["ballast_type"]
                        except:
                            try:
                                spname[i]["ballast_driver_information"]["ballast_type"] ="linear_dimming"
                            except:
                                try:
                                    spname[i]["ballast_driver_information"]={}
                                    spname[i]["ballast_driver_information"]["ballast_type"]="linear_dimming"
                                except:
                                    pass

                        try:
                            controlType=spname[i]["ballast_driver_information"]["ballast_type"]
                            # print controlType
                            if controlType=="linear_dimming":
                                ctrlTP.setCurrentIndex(0)
                                self.TabElecLayoutDipBtn.setEnabled(1)
                                try:
                                    bfmin=spname[i]["ballast_driver_information"]["bf_min"]
                                    item=self.tableitem(bfmin)
                                    self.TabElecInfoTable.setItem(i,4,item)
                                except:
                                    pass
                                try:
                                    bfmax=spname[i]["ballast_driver_information"]["bf_max"]
                                    item=self.tableitem(bfmax)
                                    self.TabElecInfoTable.setItem(i,5,item)
                                except:
                                    pass
                                try:
                                    pwmin=spname[i]["ballast_driver_information"]["watts_min"]
                                    item=self.tableitem(pwmin)
                                    self.TabElecInfoTable.setItem(i,6,item)
                                except:
                                    pass
                                try:
                                    pwmax=spname[i]["ballast_driver_information"]["watts_max"]
                                    item=self.tableitem(pwmax)
                                    self.TabElecInfoTable.setItem(i,7,item)
                                except:
                                    pass

                                self.ies=QtGui.QPushButton()
                                try:
                                    iesFile=spname[i]["luminaire_information"]["ies_file"]
                                    self.ies.setText(str(iesFile))
                                except:
                                    pass
                                self.TabElecInfoTable.setCellWidget(i,1,self.ies)
                                try:
                                    lampLumens=spname[i]["luminaire_information"]["lamp_lumens"]
                                    item=self.tableitem(lampLumens)
                                    self.TabElecInfoTable.setItem(i,2,item)
                                except:
                                    pass
                                self.TabElecInfoAddBtn.setEnabled(1)
                                self.TabElecLayoutAddBtn.setEnabled(1)
                                self.TabElecZoneCopyBtn.setEnabled(1)
                            elif controlType=="non_dimming":
                                ctrlTP.setCurrentIndex(1)
                                self.TabElecLayoutDipBtn.setEnabled(1)
                                item=self.tableitem("")
                                item.setFlags(QtCore.Qt.ItemIsEnabled)
                                self.TabElecInfoTable.setItem(i,4,item)
                                item=self.tableitem("")
                                item.setFlags(QtCore.Qt.ItemIsEnabled)
                                self.TabElecInfoTable.setItem(i,6,item)
                                try:
                                    bf=spname[i]["ballast_driver_information"]["ballast_factor"]
                                    item=self.tableitem(bf)
                                    self.TabElecInfoTable.setItem(i,5,item)
                                except:
                                    pass
                                try:
                                    pw=spname[i]["ballast_driver_information"]["watts"]
                                    item=self.tableitem(pw)
                                    self.TabElecInfoTable.setItem(i,7,item)
                                except:
                                    pass
                                self.ies=QtGui.QPushButton()
                                try:
                                    iesFile=spname[i]["luminaire_information"]["ies_file"]
                                    self.ies.setText(str(iesFile))
                                except:
                                    pass
                                self.TabElecInfoTable.setCellWidget(i,1,self.ies)
                                try:
                                    lampLumens=spname[i]["luminaire_information"]["lamp_lumens"]
                                    item=self.tableitem(lampLumens)
                                    self.TabElecInfoTable.setItem(i,2,item)
                                except:
                                    pass
                                self.TabElecInfoAddBtn.setEnabled(1)
                                self.TabElecLayoutAddBtn.setEnabled(1)
                                self.TabElecZoneCopyBtn.setEnabled(1)
                            else:
                                ctrlTP.setCurrentIndex(2)
                                self.TabElecLayoutDipBtn.setDisabled(1)
                                self.ies=QtGui.QPushButton()
                                iesFile="null"
                                self.ies.setText(str(iesFile))
                                self.ies.setDisabled(1)
                                try:
                                    del spname[i]["luminaire_information"]["lamp_lumens"]
                                except:
                                    pass

                                try:
                                    spname[i]["name"]="EPlus"
                                    self.TabElecZoneCombox.clear()
                                    self.TabElecZoneCombox.addItem(spname[i]["name"])
                                    zoneName=spname[i]["name"]
                                    item=self.tableitem(zoneName)
                                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                                    self.TabElecInfoTable.setItem(i,0,item)
                                except:
                                    pass
                                try:
                                    spname[i]["luminaire_information"]["ies_file"]="null"
                                except:
                                    spname[i]["luminaire_information"]={}
                                    spname[i]["luminaire_information"]["ies_file"]="null"
                                self.TabElecInfoTable.setCellWidget(i,1,self.ies)
                                item=self.tableitem("")
                                item.setFlags(QtCore.Qt.ItemIsEnabled)
                                self.TabElecInfoTable.setItem(i,2,item)
                                item=self.tableitem("")
                                item.setFlags(QtCore.Qt.ItemIsEnabled)
                                self.TabElecInfoTable.setItem(i,3,item)
                                item=self.tableitem("")
                                item.setFlags(QtCore.Qt.ItemIsEnabled)
                                self.TabElecInfoTable.setItem(i,4,item)
                                item=self.tableitem("")
                                item.setFlags(QtCore.Qt.ItemIsEnabled)
                                self.TabElecInfoTable.setItem(i,5,item)
                                item=self.tableitem("")
                                item.setFlags(QtCore.Qt.ItemIsEnabled)
                                self.TabElecInfoTable.setItem(i,6,item)
                                item=self.tableitem("")
                                item.setFlags(QtCore.Qt.ItemIsEnabled)
                                self.TabElecInfoTable.setItem(i,7,item)
                                self.TabElecLayoutAddBtn.setDisabled(1)
                                try:
                                    del spname[i]["luminaire_layout"]
                                except:
                                    pass

                                zi=i
                                self.TabElecInfoAddBtn.setDisabled(1)
                                try:
                                    del spname[i]["ballast_driver_information"]["bf_min"]
                                except:
                                    pass
                                try:
                                    del spname[i]["ballast_driver_information"]["bf_max"]
                                except:
                                    pass
                                try:
                                    del spname[i]["ballast_driver_information"]["ballast_factor"]
                                except:
                                    pass
                                try:
                                    del spname[i]["ballast_driver_information"]["watts_min"]
                                except:
                                    pass
                                try:
                                    del spname[i]["ballast_driver_information"]["watts_max"]
                                except:
                                    pass
                                try:
                                    del spname[i]["ballast_driver_information"]["watts"]
                                except:
                                    pass
                                self.TabElecZoneCopyBtn.setDisabled(1)
                        except:
                            self.ies=QtGui.QPushButton()
                            self.TabElecInfoTable.setCellWidget(i,1,self.ies)
                            self.TabElecLayoutDipBtn.setEnabled(1)
                            self.TabElecInfoAddBtn.setEnabled(1)
                            self.TabElecLayoutAddBtn.setEnabled(1)


                        ZoneDeleteBtn = QtGui.QPushButton()
                        ZoneDeleteBtn.setText("Delete")
                        ZoneDeleteBtn.clicked.connect(self.ElecZDel)
                        self.TabElecInfoTable.setCellWidget(i,9,ZoneDeleteBtn)
                        self.ies.clicked.connect(self.elecies)
                        ctrlTP.currentIndexChanged.connect(self.ctrltype)

                    try:
                        if self.simchecked==False:
                            temp=copy.deepcopy(spname[zi])
                            del self.tempdata["spaces"][index]["control_zones"]
                            self.tempdata["spaces"][index]["control_zones"]=[]
                            self.tempdata["spaces"][index]["control_zones"].append(temp)
                            self.simchecked=True
                            self.TabElecLoad()
                    except:
                        pass
                    self.TabElecZoneCombox.setCurrentIndex(0)
                except:
                    self.TabElecInfoTable.setRowCount(0)
                    self.TabElecZoneCombox.clear()
            except:
                pass
            # print "elecloadtable"
            self.WriteToFile()

    def ElecLOLoad(self):
        if self.imported or self.created:
            index=self.TabElecSPComBox.currentIndex()
            zindex=self.TabElecZoneCombox.currentIndex()
            try:
                spname=self.tempdata["spaces"][index]["control_zones"][zindex]
                self.TabElecLayoutTable.setRowCount(0)
                try:
                    ud=self.tempdata["general"]["display_units"]
                    ui=self.tempdata["general"]["import_units"]
                    self.TabElecLumLayoutLbl.setText("Luminaire Layout: Units (%s)"%ud)
                    try:
                        for luminaire in spname["luminaire_layout"]:
                            self.TabElecLayoutTable.insertRow(self.TabElecLayoutTable.rowCount())
                            count=self.TabElecLayoutTable.rowCount()-1
                            self.TabElecLayoutTable.setRowHeight(count,40)
                            try:
                                ZN=QtGui.QComboBox()
                                for j in range(len(self.tempdata["spaces"][index]["control_zones"])):
                                    try:
                                        ZN.addItem(str(self.tempdata["spaces"][index]["control_zones"][j]["name"]))
                                    except:
                                        pass
                                self.TabElecLayoutTable.setCellWidget(count,0,ZN)
                                ZN.setCurrentIndex(zindex)
                                ZN.currentIndexChanged.connect(self.LOZNCombo)
                                lumx=self.uconvert(ud,ui,float(luminaire["x"]),True)
                                item=self.tableitem(lumx)
                                self.TabElecLayoutTable.setItem(count,1, item)
                                lumy=self.uconvert(ud,ui,float(luminaire["y"]),True)
                                item=self.tableitem(lumy)
                                self.TabElecLayoutTable.setItem(count,2, item)
                                lumz=self.uconvert(ud,ui,float(luminaire["z"]),True)
                                item=self.tableitem(lumz)
                                self.TabElecLayoutTable.setItem(count,3, item)
                            except:
                                pass
                            try:
                                lumrot=luminaire["rotation"]
                                item=self.tableitem(lumrot)
                                self.TabElecLayoutTable.setItem(count,4, item)
                            except:
                                pass
                            try:
                                lumspin=luminaire["spin_ccw"]
                                item=self.tableitem(lumspin)
                                self.TabElecLayoutTable.setItem(count,5, item)
                            except:
                                pass
                            try:
                                lumtilt=luminaire["tilt"]
                                item=self.tableitem(lumtilt)
                                self.TabElecLayoutTable.setItem(count,6, item)
                            except:
                                pass
                            LumDeleteBtn = QtGui.QPushButton()
                            LumDeleteBtn.setText("Delete")
                            LumDeleteBtn.clicked.connect(self.LumDel)
                            self.TabElecLayoutTable.setCellWidget(count,7,LumDeleteBtn)
                    except:
                        pass
                except:
                    try:
                        if self.forceuchange1:
                            del self.forceuchange1
                            # self.forceuchange=False
                            # del self.markunit
                        # else:
                        #     try:
                        #         if self.markunit>=2:
                        #             print "3.0y"
                        #             QtGui.QMessageBox.warning(self,"Warning", "Please define units first!")
                        #             self.StadicTab.setCurrentIndex(0)
                        #     except:
                        #         self.markunit=2
                    except:
                        if self.jfimported:
                            # print "j"
                            try:
                                # print self.markunit
                                if self.markunit>=2:
                                    # print "3.0"
                                    QtGui.QMessageBox.warning(self,"Warning", "Please define dimension units first!")
                                    self.StadicTab.setCurrentIndex(0)
                                    self.markunit=1
                                else:
                                    self.markunit=2
                            except:
                                self.markunit=2
                        elif self.created:
                            QtGui.QMessageBox.warning(self,"Warning", "Please define dimension units first!")
                            self.StadicTab.setCurrentIndex(0)
            except:
                self.TabElecLayoutTable.setRowCount(0)



    def InfoChange(self):
        try:
            col = self.TabElecInfoTable.currentColumn()
            row = self.TabElecInfoTable.currentRow()
            item=self.TabElecInfoTable.item(row,col)
            index=self.TabElecSPComBox.currentIndex()
            spname=self.tempdata["spaces"][index]["control_zones"]
            if self.TabElecInfoTable.isItemSelected(item):
                if col==0:
                    mark=0
                    if len(str(item.text()).split())>1:
                        QtGui.QMessageBox.warning(self, "Warning!", \
                                                          "No spaces (\" \") in the name!")
                        spname[row]["name"]=""
                        self.WriteToFile()
                        self.TabElecLoad()
                        self.TabCtrlLoad()
                    else:
                        for i in range(len(spname)):
                            if item.text()==spname[i]["name"]:
                                mark=1
                        if mark==1:
                            spname[row]["name"]=""
                            self.WriteToFile()
                            QtGui.QMessageBox.warning(self,"Warning!", "Zone name cannot be the same!")
                            self.TabElecLoad()
                            self.TabCtrlLoad()
                        else:
                            spname[row]["name"]=str(item.text())
                            self.WriteToFile()
                            self.TabElecLoad()
                            self.TabCtrlLoad()
                elif col==2:
                    mark=0
                    mark=self.floatChk(item, -1,10000000000000000)
                    if mark==0:
                        try:
                            spname[row]["luminaire_information"]["lamp_lumens"]=float(item.text())
                        except:
                            spname[row]["luminaire_information"]={}
                            spname[row]["luminaire_information"]["lamp_lumens"]=float(item.text())
                    else:
                        item.setText("0")
                        item.setFocus()
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                elif col==3:
                    mark=0
                    mark=self.floatChk(item, 0,1)
                    if mark==0:
                        try:
                            spname[row]["luminaire_information"]["LLF"]=float(item.text())
                        except:
                            spname[row]["luminaire_information"]={}
                            spname[row]["luminaire_information"]["LLF"]=float(item.text())
                    else:
                        item.setText("1")
                        item.setFocus()
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                elif col==4:
                    mark=0
                    try:
                        wdg=self.TabElecInfoTable.cellWidget(row,8)
                        if wdg.currentIndex()==0:
                            mark=self.floatChk(item, 0,1)
                            if mark==0:
                                spname[row]["ballast_driver_information"]["bf_min"]=float(item.text())
                                temp=float(spname[row]["ballast_driver_information"]["bf_min"])
                                try:
                                    if float(spname[row]["ballast_driver_information"]["bf_max"])<temp:
                                        QtGui.QMessageBox.warning(self, "Warning", "Wrong Entry! BFmin needs to be smaller than BFmax!")
                                        spname[row]["ballast_driver_information"]["bf_min"]=float(spname[row]["ballast_driver_information"]["bf_max"])
                                        item.setText(str(spname[row]["ballast_driver_information"]["bf_max"]))
                                except:
                                    pass
                            else:
                                item.setText("0")
                                item.setFocus()
                        else:
                            item.setText("")
                    except:
                        wdg=self.TabElecInfoTable.cellWidget(row,8)
                        if wdg.currentIndex()==0:
                            mark=self.floatChk(item, 0,1)
                            if mark==0:
                                spname[row]["ballast_driver_information"]={}
                                spname[row]["ballast_driver_information"]["bf_min"]=float(item.text())
                            else:
                                item.setText("0")
                                item.setFocus()
                        else:
                            item.setText(" ")
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                elif col==5:
                    mark=0
                    try:
                        wdg=self.TabElecInfoTable.cellWidget(row,8)
                        mark=0
                        if wdg.currentIndex()==0:
                            mark=self.floatChk(item, 0,1)
                            if mark==0:
                                spname[row]["ballast_driver_information"]["bf_max"]=float(item.text())
                                temp=float(spname[row]["ballast_driver_information"]["bf_max"])
                                try:
                                    if float(spname[row]["ballast_driver_information"]["bf_min"])>temp:
                                        QtGui.QMessageBox.warning(self, "Warning", "Wrong Entry! BFmax needs to be greater than BFmin!")
                                        spname[row]["ballast_driver_information"]["bf_max"]=float(spname[row]["ballast_driver_information"]["bf_min"])
                                        item.setText(str(spname[row]["ballast_driver_information"]["bf_min"]))
                                except:
                                    pass
                            else:
                                item.setText("1")
                                item.setFocus()
                        else:
                            mark=self.floatChk(item, 0,1)
                            if mark==0:
                                spname[row]["ballast_driver_information"]["ballast_factor"]=float(item.text())
                            else:
                                item.setText("1")
                                item.setFocus()
                    except:
                        if wdg.currentIndex()==0:
                            mark=self.floatChk(item, 0,1)
                            if mark==0:
                                spname[row]["ballast_driver_information"]={}
                                spname[row]["ballast_driver_information"]["bf_max"]=float(item.text())
                            else:
                                item.setText("0")
                                item.setFocus()
                        else:
                            mark=self.floatChk(item, 0,1)
                            if mark==0:
                                spname[row]["ballast_driver_information"]={}
                                spname[row]["ballast_driver_information"]["ballast_factor"]=float(item.text())
                            else:
                                item.setText("1")
                                item.setFocus()
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                elif col==6:
                    mark=0
                    try:
                        wdg=self.TabElecInfoTable.cellWidget(row,8)
                        if wdg.currentIndex()==0:
                            mark=self.intChk(item, 0,100000000000000)
                            if mark==0:
                                spname[row]["ballast_driver_information"]["watts_min"]=int(item.text())
                                temp=int(spname[row]["ballast_driver_information"]["watts_min"])
                                try:
                                    if int(spname[row]["ballast_driver_information"]["watts_max"])<temp:
                                        QtGui.QMessageBox.warning(self, "Warning", "Wrong Entry! WATTSmin needs to be smaller than WATTSmax!")
                                        spname[row]["ballast_driver_information"]["watts_min"]=int(spname[row]["ballast_driver_information"]["watts_max"])
                                        item.setText(str(spname[row]["ballast_driver_information"]["watts_max"]))
                                except:
                                    pass
                            else:
                                item.setText("0")
                                item.setFocus()
                        else:
                            item.setText("")
                    except:
                        wdg=self.TabElecInfoTable.cellWidget(row,8)
                        if wdg.currentIndex()==0:
                            mark=self.intChk(item, 0,100000000000000)
                            if mark==0:
                                spname[row]["ballast_driver_information"]={}
                                spname[row]["ballast_driver_information"]["watts_min"]=int(item.text())
                            else:
                                item.setText("0")
                                item.setFocus()
                        else:
                            item.setText(" ")
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                elif col==7:
                    mark=0
                    try:
                        wdg=self.TabElecInfoTable.cellWidget(row,8)
                        if wdg.currentIndex()==0:
                            mark=self.intChk(item, 0,100000000000000)
                            if mark==0:
                                spname[row]["ballast_driver_information"]["watts_max"]=int(item.text())
                                temp=int(spname[row]["ballast_driver_information"]["watts_max"])
                                try:
                                    if int(spname[row]["ballast_driver_information"]["watts_min"])>temp:
                                        QtGui.QMessageBox.warning(self, "Warning", "Wrong Entry! WATTSmax needs to be greater than WATTSmin!")
                                        spname[row]["ballast_driver_information"]["watts_max"]=int(spname[row]["ballast_driver_information"]["watts_min"])
                                        item.setText(str(spname[row]["ballast_driver_information"]["watts_max"]))
                                except:
                                    pass
                            else:
                                item.setText("0")
                        else:
                            mark=self.intChk(item, 0,100000000000000)
                            if mark==0:
                                spname[row]["ballast_driver_information"]["watts"]=int(item.text())
                            else:
                                item.setText("0")
                                item.setFocus()
                    except:
                        wdg=self.TabElecInfoTable.cellWidget(row,8)
                        if wdg.currentIndex()==0:
                            mark=self.intChk(item, 0,100000000000000)
                            if mark==0:
                                spname[row]["ballast_driver_information"]={}
                                spname[row]["ballast_driver_information"]["watts_max"]=int(item.text())
                            else:
                                item.setText("0")
                                item.setFocus()
                        else:
                            mark=self.intChk(item, 0,100000000000000)
                            if mark==0:
                                spname[row]["ballast_driver_information"]={}
                                spname[row]["ballast_driver_information"]["watts"]=int(item.text())
                            else:
                                item.setText("0")
                                item.setFocus()
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.WriteToFile()
        except:
            pass

    def elecies(self):
        button = self.sender()
        item = self.TabElecInfoTable.itemAt(button.pos())
        index=self.TabElecSPComBox.currentIndex()
        bindex = self.TabElecInfoTable.indexAt(button.pos())
        # widget=self.TabElecInfoTable.cellWidget(bindex.row(),bindex.column())
        iesFile=QtGui.QFileDialog.getOpenFileName(self,"Import IES File",self.dir,"IES File (*.ies)")
        if iesFile:
            IESPath=os.path.join(self.dir,self.tempdata["spaces"][index]["ies_directory"])
            IESLine=self.CopyFile(iesFile,IESPath)
            # widget.setText(str(os.path.basename(IESLine)))
            try:
                spname=self.tempdata["spaces"][index]["control_zones"][bindex.row()]
            except:
                self.tempdata["spaces"][index]["control_zones"]={}
                self.tempdata["spaces"][index]["control_zones"].append([])
                spname=self.tempdata["spaces"][index]["control_zones"][bindex.row()]
            try:
                spname["luminaire_information"]["ies_file"]=str(os.path.basename(IESLine))
            except:
                spname["luminaire_information"]={}
                spname["luminaire_information"]["ies_file"]=str(os.path.basename(IESLine))
            lampdata=open(iesFile).read().split()
            idx=lampdata.index("TILT=NONE")
            spname["luminaire_information"]["lamp_lumens"]=float(lampdata[idx+2])
            if float(lampdata[idx+2])==-1:
                QtGui.QMessageBox.warning(self, "Warning!", "Absolute photometry is used!")
                spname["luminaire_information"]["lamp_lumens"]=int(lampdata[idx+2])
            del lampdata

        self.WriteToFile()
        # self.lumlayout=True
        self.TabElecLoad()
        # self.lumlayout=False

    def ctrltype(self):
        button = self.sender()
        item = self.TabElecInfoTable.itemAt(button.pos())
        index=self.TabElecSPComBox.currentIndex()
        bindex = self.TabElecInfoTable.indexAt(button.pos())
        widget=self.TabElecInfoTable.cellWidget(bindex.row(),bindex.column())
        cindex=widget.currentIndex()
        spname=self.tempdata["spaces"][index]["control_zones"][bindex.row()]

        if cindex==0:
            spname["ballast_driver_information"]["ballast_type"]="linear_dimming"
            try:
                spname["ballast_driver_information"]["bf_max"]=spname["ballast_driver_information"]["ballast_factor"]
                del spname["ballast_driver_information"]["ballast_factor"]
            except:
                pass
            try:
                spname["ballast_driver_information"]["watts_max"]=spname["ballast_driver_information"]["watts"]
                del spname["ballast_driver_information"]["watts"]
            except:
                pass
            self.WriteToFile()
            self.TabElecLoad()
            self.TabCtrlLoad()
        elif cindex==1:
            spname["ballast_driver_information"]["ballast_type"]="non_dimming"
            spname["optimum_control"]="on"
            try:
                del spname["ballast_driver_information"]["bf_min"]
            except:
                pass
            try:
                spname["ballast_driver_information"]["ballast_factor"]=spname["ballast_driver_information"]["bf_max"]
                del spname["ballast_driver_information"]["bf_max"]
            except:
                pass
            try:
                del spname["ballast_driver_information"]["watts_min"]
            except:
                pass
            try:
                spname["ballast_driver_information"]["watts"]=spname["ballast_driver_information"]["watts_max"]
                del spname["ballast_driver_information"]["watts_max"]
            except:
                pass
            self.WriteToFile()
            self.TabElecLoad()
            self.TabCtrlLoad()
        else:
            choice=QtGui.QMessageBox.question(self, "Warning!", "All zonal information will be lost! Confirm to continue", QtGui.QMessageBox.Yes |QtGui.QMessageBox.No)
            if choice==QtGui.QMessageBox.Yes:
                self.StadicTab.setCurrentIndex(6)
                self.warning=False
                self.TabCtrlOptCComBox.setCurrentIndex(3)
            else:
                widget.setCurrentIndex(0)

    def ElecZDel(self):
        button = self.sender()
        item = self.TabElecInfoTable.itemAt(button.pos())
        index=self.TabElecSPComBox.currentIndex()
        bindex = self.TabElecInfoTable.indexAt(button.pos())
        widget=self.TabElecInfoTable.cellWidget(bindex.row(),bindex.column())
        choice=QtGui.QMessageBox.question(self,"Warning", "Are you sure to delete the whole zone? \n"
                                                             "You can move luminaires to other zones before deleting.", \
                                              QtGui.QMessageBox.Yes |QtGui.QMessageBox.No)
        if choice==QtGui.QMessageBox.Yes:
            del self.tempdata["spaces"][index]["control_zones"][bindex.row()]
            if len(self.tempdata["spaces"][index]["control_zones"])==0:
                del self.tempdata["spaces"][index]["control_zones"]
            self.WriteToFile()
            # self.lumlayout=True
            self.TabElecLoad()
            # self.lumlayout=False
            self.TabCtrlLoad()

    def ElecInfoAdd(self):
        if self.imported or self.created:
            try:
                index=self.TabElecSPComBox.currentIndex()
                junk=self.tempdata["spaces"][index]
                count=self.TabElecInfoTable.rowCount()
                self.TabElecInfoTable.setRowCount(count+1)
                self.TabElecInfoTable.setRowHeight(count,40)
                ZoneDeleteBtn = QtGui.QPushButton()
                ZoneDeleteBtn.setText("Delete")
                ZoneDeleteBtn.clicked.connect(self.ElecZDel)
                self.TabElecInfoTable.setCellWidget(count,9,ZoneDeleteBtn)
                try:
                    spname=self.tempdata["spaces"][index]["control_zones"]
                    spname.append({})
                except:
                    self.tempdata["spaces"][index]["control_zones"]=[]
                    spname=self.tempdata["spaces"][index]["control_zones"]
                    spname.append({})
                cindex=len(spname)-1
                spname[cindex]["name"]=""
                spname[cindex]["luminaire_information"]={}
                spname[cindex]["ballast_driver_information"]={}
                spname[cindex]["ballast_driver_information"]["ballast_type"]="non_dimming"
                spname[cindex]["luminaire_layout"]=[]
                self.WriteToFile()
                self.TabElecLoad()
                self.TabCtrlLoad()
                self.TabElecInfoTable.scrollToBottom()
            except:
                pass

    def ElecZoneCopy(self):
        if (self.imported or self.created):
            try:
                index=self.TabElecSPComBox.currentIndex()
                self.tempdata["spaces"][index]["control_zones"]
                if len(self.tempdata["spaces"][index]["control_zones"])>0:
                    Dupcombo=DupUi_Combo()
                    for item in self.tempdata["spaces"]:
                        Dupcombo.cboxsp.addItem(item["space_name"])
                    Dupcombo.show()
                    Dupcombo.exec_()
                    try:
                        newname=Dupcombo.newname
                        cindex, zindex=Dupcombo.id
                        try:
                            self.tempdata["spaces"][index]["control_zones"].append({})
                        except:
                            self.tempdata["spaces"][index]["control_zones"]=[]
                            self.tempdata["spaces"][index]["control_zones"].append({})
                        lenc=len(self.tempdata["spaces"][index]["control_zones"])
                        self.tempdata["spaces"][index]["control_zones"][lenc-1]["name"]=str(newname)
                        self.tempdata["spaces"][index]["control_zones"][lenc-1]["luminaire_information"]=copy.deepcopy(self.tempdata["spaces"][cindex]["control_zones"][zindex]["luminaire_information"])
                        self.tempdata["spaces"][index]["control_zones"][lenc-1]["ballast_driver_information"]=copy.deepcopy(self.tempdata["spaces"][cindex]["control_zones"][zindex]["ballast_driver_information"])
                        self.tempdata["spaces"][index]["control_zones"][lenc-1]["luminaire_layout"]=[]
                        # print self.tempdata["spaces"][index]["control_zones"][lenc-1]
                        QtGui.QMessageBox.information(self,"Successful", "Luminaire information is copied to %s successfully" %self.tempdata["spaces"][cindex]["space_name"])
                        self.WriteToFile()
                        # self.lumlayout=True
                        self.TabElecLoad()
                        # self.lumlayout=False
                        self.TabCtrlLoad()
                    except:
                        pass
            except:
                pass

    def LOChange(self):
        col = self.TabElecLayoutTable.currentColumn()
        row = self.TabElecLayoutTable.currentRow()
        item=self.TabElecLayoutTable.item(row,col)
        index=self.TabElecSPComBox.currentIndex()
        zindex=self.TabElecZoneCombox.currentIndex()
        if self.TabElecLayoutTable.isItemSelected(item):
            try:
                spname=self.tempdata["spaces"][index]["control_zones"][zindex]["luminaire_layout"][row]
            except:
                self.tempdata["spaces"][index]["control_zones"][zindex]["luminaire_layout"].append({})
                spname=self.tempdata["spaces"][index]["control_zones"][zindex]["luminaire_layout"][row]
            try:
                ud=self.tempdata["general"]["display_units"]
                ui=self.tempdata["general"]["import_units"]
            except:
                item.clear()
                QtGui.QMessageBox.warning(self,"Warning", "Please define dimension units first!")
                self.StadicTab.setCurrentIndex(0)

            if col==1:
                mark=0
                mark=self.floatChk(item)
                if mark==0:
                    spname["x"]=self.uconvert(ud,ui,float(item.text()),False)
                else:
                    item.setText("0")
                    # item.setFocus()
            elif col==2:
                mark=0
                mark=self.floatChk(item)
                if mark==0:
                    spname["y"]=self.uconvert(ud,ui,float(item.text()),False)
                else:
                    item.setText("0")
                    # item.setFocus()
            elif col==3:
                mark=0
                mark=self.floatChk(item)
                if mark==0:
                    spname["z"]=self.uconvert(ud,ui,float(item.text()),False)
                else:
                    item.setText("0")
                    # item.setFocus()

            elif col==4:
                mark=0
                mark=self.intChk(item)
                if mark==0:
                    spname["rotation"]=int(item.text())
                else:
                    item.setText("0")
                    # item.setFocus()
            elif col==5:
                mark=0
                mark=self.intChk(item)
                if mark==0:
                    spname["tilt"]=int(item.text())
                else:
                    item.setText("0")
                    # item.setFocus()
            elif col==6:
                mark=0
                mark=self.intChk(item)
                if mark==0:
                    spname["spin_ccw"]=int(item.text())
                else:
                    item.setText("0")
                    # item.setFocus()
            self.WriteToFile()
            # self.LumLayoutDisplay()

    def LOZNCombo(self):
        button = self.sender()
        item = self.TabElecLayoutTable.itemAt(button.pos())
        index=self.TabElecSPComBox.currentIndex()
        zindex=self.TabElecZoneCombox.currentIndex()
        bindex = self.TabElecLayoutTable.indexAt(button.pos())
        widget=self.TabElecLayoutTable.cellWidget(bindex.row(),bindex.column())
        cindex=widget.currentIndex()
        spname=self.tempdata["spaces"][index]["control_zones"]
        if cindex!=zindex:
            choice=QtGui.QMessageBox.question(self, "Warning!", "Verify to move the Luminiare to %s?" %spname[cindex]["name"], QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
            if choice==QtGui.QMessageBox.Yes:
                temp=spname[zindex]["luminaire_layout"][bindex.row()]
                del spname[zindex]["luminaire_layout"][bindex.row()]
                try:
                    spname[cindex]["luminaire_layout"].append(temp)
                except:
                    spname[cindex]["luminaire_layout"]=[]
                    spname[cindex]["luminaire_layout"].append(temp)
                self.WriteToFile()
                # self.lumlayout=True
                self.ElecLOLoad()
                # self.lumlayout=False
            else:
                widget.setCurrentIndex(zindex)

    def ElecLOAdd(self):
        if (self.imported or self.created) and self.TabElecInfoTable.rowCount()>0:
            count=self.TabElecLayoutTable.rowCount()
            index=self.TabElecSPComBox.currentIndex()
            spname=self.tempdata["spaces"][index]["control_zones"]
            zindex=self.TabElecZoneCombox.currentIndex()
            try:
                spname[zindex]["luminaire_layout"].append({})
            except:
                spname[zindex]["luminaire_layout"]=[]
                spname[zindex]["luminaire_layout"].append({})
            lum=len(spname[zindex]["luminaire_layout"])-1
            spname[zindex]["luminaire_layout"][lum]["x"]=0
            spname[zindex]["luminaire_layout"][lum]["y"]=0
            spname[zindex]["luminaire_layout"][lum]["z"]=0
            spname[zindex]["luminaire_layout"][lum]["rotation"]=0
            spname[zindex]["luminaire_layout"][lum]["spin_ccw"]=0
            spname[zindex]["luminaire_layout"][lum]["tilt"]=0
            self.markunit=2
            self.ElecLOLoad()
            self.TabElecLayoutTable.scrollToBottom()
            self.WriteToFile()


    def LumDel(self):
        button = self.sender()
        item = self.TabElecLayoutTable.itemAt(button.pos())
        index=self.TabElecSPComBox.currentIndex()
        bindex = self.TabElecLayoutTable.indexAt(button.pos())
        widget=self.TabElecLayoutTable.cellWidget(bindex.row(),bindex.column())
        zindex=self.TabElecZoneCombox.currentIndex()
        choice=QtGui.QMessageBox.question(self,"Warning", "Are you sure to delete the luminaire?", \
                                              QtGui.QMessageBox.Yes |QtGui.QMessageBox.No)
        if choice==QtGui.QMessageBox.Yes:
            del self.tempdata["spaces"][index]["control_zones"][zindex]["luminaire_layout"][bindex.row()]
            self.WriteToFile()
            # self.lumlayout=True
            self.ElecLOLoad()
            self.TabElecLoad()
            self.TabElecZoneCombox.setCurrentIndex(zindex)
            # self.lumlayout=False

    def LumLayoutDisplay(self):
        if self.imported or self.created:
            try:
                prg=PBar()
                prg.show()
                index=self.TabElecSPComBox.currentIndex()
                spname=self.tempdata["spaces"][index]
                mark=0
                try:
                    for i in range(len(spname["control_zones"])):
                        if spname["control_zones"][i]["luminaire_information"]["ies_file"]:
                            if len(spname["control_zones"][i]["luminaire_layout"])>=1:
                                mark=1
                except:
                    pass
                self.scene.clear()
                prg.update()
                if mark==1:
                    i=0
                    try:
                        try:
                            self.dplayer=spname["layout_base"]
                            # print self.dplayer
                        except:
                            pass
                        index=self.TabElecSPComBox.currentIndex()
                        prg.update()
                        createlumlayout(self.tpfname,index,self.dplayer, 2000)
                        test=True
                        prg.update()
                        prg.update()
                        while (test==True):
                            time.sleep(0.1)
                            try:
                                pth=self.tempdata["general"]["project_directory"]+"temp/room.bmp"
                                img=QtGui.QPixmap(pth)
                                w = img.width()
                                h=img.height()
                                # self.imgQ = img  # we need to hold reference to imgQ, or it will crash
                                # pixMap = QPixmap.fromImage(self.imgQ)
                                self.scene.addPixmap(img)
                                self.view.fitInView(QtCore.QRectF(0, 0, w, h), QtCore.Qt.KeepAspectRatio)
                                self.scene.update()
                                test=False
                            except:
                                test=True
                                # i=i+1
                                # if i>=100:
                                #     QtGui.QMessageBox.warning(self, "Error", "Error!")
                                #     test=False
                        time.sleep(0.1)
                        prg.update()
                    except:
                        QtGui.QMessageBox.warning(self, "Error", "Luminaire layout Error!")
                        prg.val=80
                        prg.update()
            except:
                pass

    def TabCtrlLoad(self):
        if self.imported or self.created:
            try:
                index=self.TabCtrlSPNComBox.currentIndex()
                self.TabCtrlCtrlZComBox.clear()
                spname=self.tempdata["spaces"][index]["control_zones"]
                try:
                    self.TabCtrlCtrlZComBox.currentIndexChanged[int].disconnect()
                except:
                    pass

                try:
                    # print self.tempdata["spaces"][index]["target_illuminance"]
                    self.TabCtrlTgtIllLineEd.setText(str(self.tempdata["spaces"][index]["target_illuminance"]))
                except:
                    self.TabCtrlTgtIllLineEd.setText("")
                for i in range(len(spname)):
                    try:
                        self.TabCtrlCtrlZComBox.addItem(spname[i]["name"])
                    except:
                        pass
                self.ElecCtrlZ()
                self.TabCtrlCtrlZComBox.currentIndexChanged.connect(self.ElecCtrlZ)
            except:
                pass

    def ElecCtrlZ(self):
        index=self.TabCtrlSPNComBox.currentIndex()
        zindex=self.TabCtrlCtrlZComBox.currentIndex()
        # print "ctrlz"
        try:
            spname=self.tempdata["spaces"][index]["control_zones"][zindex]
        except:
            pass
        # self.TabCtrlOptCComBox.setDisabled(1)
        # print spname["name"]
        # try:
        #     print spname["ballast_driver_information"]["ballast_type"]
        # except:
        #     pass
        # try:
        #     print spname["optimum_control"]
        # except:
        #     pass
        try:
            self.TabCtrlOptCComBox.currentIndexChanged[int].disconnect()
        except:
            pass
        try:
            if spname["ballast_driver_information"]["ballast_type"]=="Eplus_dimming":
                try:
                    if spname["optimum_control"]!="EPlus_dim_to_min":
                        spname["optimum_control"]="EPlus_dim_to_min"
                except:
                    spname["optimum_control"]="EPlus_dim_to_min"
                self.TabCtrlOptCComBox.setCurrentIndex(3)
                self.TabCtrlOptCComBox.setDisabled(1)
                self.fimport=True
            elif spname["ballast_driver_information"]["ballast_type"]=="non_dimming":
                try:
                    if spname["optimum_control"]!="on":
                        spname["optimum_control"]="on"
                except:
                    spname["optimum_control"]="on"
                self.TabCtrlOptCComBox.setCurrentIndex(1)
                self.TabCtrlOptCComBox.setDisabled(1)
                self.fimport=True
            else:
                self.TabCtrlOptCComBox.setEnabled(1)
                try:
                    if spname["optimum_control"]!="dim_to_min" and spname["optimum_control"]!="on":
                        spname["optimum_control"]="on"
                        try:
                            del spname["cp_location"]
                        except:
                            pass
                        # print "ochange"
                except:
                    pass
                self.fimport=False
        except:
            self.TabCtrlOptCComBox.setCurrentIndex(1)
            self.TabCtrlOptCComBox.setDisabled(1)
            try:
                del spname["cp_location"]
            except:
                pass

        try:
            if spname["optimum_control"]=="dim_to_min":
                self.TabCtrlOptCComBox.setCurrentIndex(0)
                self.TabCtrlOptCComBox.setEnabled(1)
                # print "dim"
            elif spname["optimum_control"]=="on":
                if spname["ballast_driver_information"]["ballast_type"]=="non_dimming":
                    if self.fimport==False:
                        self.TabCtrlOptCComBox.setCurrentIndex(1)
                        self.TabCtrlOptCComBox.setDisabled(1)
                elif spname["ballast_driver_information"]["ballast_type"]=="linear_dimming":
                    self.TabCtrlOptCComBox.setCurrentIndex(1)
                    self.TabCtrlOptCComBox.setEnabled(1)
            elif spname["optimum_control"]=="EPlus_dim_to_min":
                if self.fimport==False:
                    self.TabCtrlOptCComBox.setCurrentIndex(3)
                    self.TabCtrlOptCComBox.setDisabled(1)
        except:
            try:
                if spname["ballast_driver_information"]["ballast_type"]=="Eplus_dimming":
                    spname["optimum_control"]="EPlus_dim_to_min"
                elif spname["ballast_driver_information"]["ballast_type"]=="non_dimming":
                    spname["optimum_control"]="on"
                else:
                    spname["optimum_control"]="on"
                    self.TabCtrlOptCComBox.setCurrentIndex(1)
                    # print "on"
            except:
                try:
                    self.TabCtrlOptCComBox.currentIndexChanged[int].disconnect()
                except:
                    pass
                self.TabCtrlOptCComBox.setCurrentIndex(-1)
                # self.TabCtrlOptCComBox.currentIndexChanged.connect(self.ElecCtrlAlg)
                self.TabCtrlOptCComBox.setDisabled(1)
                try:
                    self.TabCtrlCtrlZComBox.currentIndexChanged[int].disconnect()
                except:
                    pass
                self.TabCtrlCtrlZComBox.clear()
                # self.TabCtrlCtrlZComBox.currentIndexChanged.connect(self.ElecCtrlZ)
                self.TabCtrlTgtPctgLineEd.clear()
                self.TabCtrlTgtPctgLineEd.setDisabled(1)
                self.TabCtrlCPMtdComBox.setDisabled(1)
                self.TabCtrlQtyComBox.setDisabled(1)
                self.TabCtrlEPtsLineEd.setDisabled(1)
        self.WriteToFile()
        self.ElecCtrlAlg()
        self.TabCtrlOptCComBox.currentIndexChanged.connect(self.ElecCtrlAlg)

    def Tgt(self):
         if self.imported or self.created:
            try:
                index=self.TabCtrlSPNComBox.currentIndex()
                junk=self.tempdatap["general"]["illum_units"]
                self.tempdata["spaces"][index]["target_illuminance"]=int(self.TabCtrlTgtIllLineEd.text())
                self.WriteToFile()
            except:
                self.TabCtrlTgtIllLineEd.clear()
                QtGui.QMessageBox.warning(self, "Warning", "Set Lighting Units!")
                self.StadicTab.setCurrentIndex(0)

    def TgtPctg(self):
        if self.imported or self.created:
            index=self.TabCtrlSPNComBox.currentIndex()
            i=self.TabCtrlCtrlZComBox.currentIndex()
            mark=0
            mark=self.floatChk(self.TabCtrlTgtPctgLineEd, 0,1)
            if mark==0:
                spname=self.tempdata["spaces"][index]["control_zones"][i]
                spname["target_percentage"]=float(self.TabCtrlTgtPctgLineEd.text())
            else:
                self.TabCtrlTgtPctgLineEd.setText("0.1")
                self.TabCtrlTgtPctgLineEd.setFocus()
            self.WriteToFile()


    def CPMtd(self):
        if self.imported or self.created:
            try:
                # print "cpmtd"
                index=self.TabCtrlSPNComBox.currentIndex()
                # print index
                i=self.TabCtrlCtrlZComBox.currentIndex()
                spname=self.tempdata["spaces"][index]["control_zones"][i]
                # print spname["name"]
                if spname["optimum_control"]=="dim_to_min":
                    if self.TabCtrlCPMtdComBox.currentIndex()==1:
                        spname["cp_method"]="manual"
                        # print "manual"
                        self.TabCtrlQtyComBox.setCurrentIndex(0)
                        self.TabCtrlQtyComBox.setDisabled(1)
                        self.TabCtrlTgtPctgLineEd.clear()
                        self.TabCtrlTgtPctgLineEd.setDisabled(1)
                        self.TabCtrlEPtsLineEd.setText("")
                        self.TabCtrlEPtsLineEd.setDisabled(1)
                        self.TabCtrlEPtsBtn.setDisabled(1)
                        try:
                            del spname["target_percentage"]
                        except:
                            pass
                        try:
                            del spname["excluded_points"]
                        except:
                            pass
                        try:
                            for cnt in reversed(range(self.TabCtrl2Grid4.count())):
                                widget = self.TabCtrl2Grid4.takeAt(cnt).widget()
                                if widget is not None:
                                    widget.deleteLater()
                        except:
                            pass
                        self.TabCtrl2Grid4=QtGui.QGridLayout()
                        self.CGrid1.addLayout(self.TabCtrl2Grid4, 8, 2, 1, 1)
                        Lbl = QtGui.QLabel()
                        self.TabCtrl2Grid4.addWidget(Lbl, 1, 0, 1, 1)
                        try:
                            Lbl.setText( "Manual Points Location: Units(%s)" %self.tempdata["general"]["display_units"])
                            Lbl.setFixedWidth(270)
                            Lbl = QtGui.QLabel()
                            self.TabCtrl2Grid4.addWidget(Lbl, 1, 1, 1, 1)
                            Lbl.setText( "X:")
                            Lbl.setFixedWidth(15)
                            self.TabCtrlCPXLineEd=QtGui.QLineEdit()
                            self.TabCtrlCPXLineEd.setValidator(QtGui.QDoubleValidator())
                            self.TabCtrl2Grid4.addWidget(self.TabCtrlCPXLineEd, 1, 2, 1, 1)
                            self.TabCtrlCPXLineEd.setFixedWidth(65)
                            spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
                            self.TabCtrl2Grid4.addItem(spacerItem, 1, 3, 1, 1)
                            Lbl = QtGui.QLabel()
                            Lbl.setText("Y:")
                            Lbl.setFixedWidth(15)
                            self.TabCtrl2Grid4.addWidget(Lbl, 1, 4, 1, 1)
                            self.TabCtrlCPYLineEd=QtGui.QLineEdit()
                            self.TabCtrlCPYLineEd.setValidator(QtGui.QDoubleValidator())
                            self.TabCtrl2Grid4.addWidget(self.TabCtrlCPYLineEd, 1, 5, 1, 1)
                            self.TabCtrlCPYLineEd.setFixedWidth(65)
                            spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
                            self.TabCtrl2Grid4.addItem(spacerItem, 1, 6, 1, 1)
                            Lbl = QtGui.QLabel()
                            Lbl.setText("Z:")
                            Lbl.setFixedWidth(15)
                            self.TabCtrl2Grid4.addWidget(Lbl, 1, 7, 1, 1)
                            self.TabCtrlCPZLineEd=QtGui.QLineEdit()
                            self.TabCtrlCPZLineEd.setValidator(QtGui.QDoubleValidator())
                            self.TabCtrl2Grid4.addWidget(self.TabCtrlCPZLineEd, 1, 8, 1, 1)
                            self.TabCtrlCPZLineEd.setFixedWidth(65)
                            spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
                            self.TabCtrl2Grid4.addItem(spacerItem, 1, 9, 1, 1)
                            ui=self.tempdata["general"]["import_units"]
                            ud=self.tempdata["general"]["display_units"]
                            # try:
                            #     # print spname["cp_location"]["x"]
                            # except:
                            #     pass
                            try:
                                self.setUnitText(self.TabCtrlCPXLineEd,ud,ui,float(spname["cp_location"]["x"]),True)
                            except:
                                pass
                            try:
                                self.setUnitText(self.TabCtrlCPYLineEd,ud,ui,float(spname["cp_location"]["y"]),True)
                            except:
                                pass
                            try:
                                self.setUnitText(self.TabCtrlCPZLineEd,ud,ui,float(spname["cp_location"]["z"]),True)
                            except:
                                pass
                            CPLoc=lambda: self.CPLocdata(self.TabCtrlCPXLineEd,"x")
                            self.TabCtrlCPXLineEd.editingFinished.connect(CPLoc)
                            CPLoc=lambda: self.CPLocdata(self.TabCtrlCPYLineEd,"y")
                            self.TabCtrlCPYLineEd.editingFinished.connect(CPLoc)
                            CPLoc=lambda: self.CPLocdata(self.TabCtrlCPZLineEd,"z")
                            self.TabCtrlCPZLineEd.editingFinished.connect(CPLoc)
                        except:
                            if self.jfimported:
                                try:
                                    if self.markunit>=3:
                                        # print "4.0"
                                        QtGui.QMessageBox.warning(self,"Warning", "Please define dimension units first!")
                                        self.TabCtrlCPMtdComBox.setCurrentIndex(0)
                                        self.StadicTab.setCurrentIndex(0)
                                except:
                                    self.markunit=3
                            elif self.created:
                                QtGui.QMessageBox.warning(self,"Warning", "Please define dimension units first!")
                                self.TabCtrlCPMtdComBox.setCurrentIndex(0)
                                self.StadicTab.setCurrentIndex(0)
                    elif self.TabCtrlCPMtdComBox.currentIndex()==0:
                        spname["cp_method"]="auto"
                        # print "auto"
                        self.TabCtrlQtyComBox.setEnabled(1)
                        self.TabCtrlTgtPctgLineEd.setEnabled(1)
                        self.TabCtrlEPtsLineEd.setEnabled(1)
                        self.TabCtrlEPtsBtn.setEnabled(1)
                        try:
                            self.TabCtrlTgtPctgLineEd.setText(str(spname["target_percentage"]))
                        except:
                            self.TabCtrlTgtPctgLineEd.setText("0")
                            try:
                                spname["target_percentage"]=0
                            except:
                                pass
                        try:
                            for j in range(5):
                                if j+1==spname["quantity"]:
                                    self.TabCtrlQtyComBox.setCurrentIndex(j)
                        except:
                            self.TabCtrlQtyComBox.setCurrentIndex(1)
                            try:
                                spname["quantity"]=2
                            except:
                                pass
                        try:
                            self.TabCtrlEPtsLineEd.setText(spname["excluded_points"])
                        except:
                            try:
                                spname["excluded_points"]="null"
                            except:
                                pass
                            self.TabCtrlEPtsLineEd.setText("null")
                        try:
                            for cnt in reversed(range(self.TabCtrl2Grid4.count())):
                                widget = self.TabCtrl2Grid4.takeAt(cnt).widget()
                                if widget is not None:
                                    widget.deleteLater()
                        except:
                            pass
                        try:
                            # print "del"
                            del spname["cp_location"]
                        except:
                            pass
                    else:
                        pass
                        # print "no"
                elif spname["optimum_control"]=="EPlus_dim_to_min":
                    if self.TabCtrlCPMtdComBox.currentIndex()==0:
                        spname["cp_method"]="EPlus_auto"
                        self.TabCtrlQtyComBox.setCurrentIndex(1)
                        self.TabCtrlQtyComBox.setDisabled(1)
                        self.TabCtrlTgtPctgLineEd.clear()
                        self.TabCtrlTgtPctgLineEd.setDisabled(1)
                        self.TabCtrlEPtsLineEd.setText("")
                        self.TabCtrlEPtsLineEd.setDisabled(1)
                        self.TabCtrlEPtsBtn.setDisabled(1)
                        try:
                            del spname["target_percentage"]
                        except:
                            pass
                        try:
                            del spname["excluded_points"]
                        except:
                            pass
                        try:
                            for cnt in reversed(range(self.TabCtrl2Grid4.count())):
                                widget = self.TabCtrl2Grid4.takeAt(cnt).widget()
                                if widget is not None:
                                    widget.deleteLater()
                        except:
                            pass
                        try:
                            del spname["cp_location"]
                        except:
                            pass
                    elif self.TabCtrlCPMtdComBox.currentIndex()==1:
                        spname["cp_method"]="EPlus_user"
                        self.TabCtrlQtyComBox.setCurrentIndex(0)
                        self.TabCtrlQtyComBox.setDisabled(1)
                        self.TabCtrlTgtPctgLineEd.clear()
                        self.TabCtrlTgtPctgLineEd.setDisabled(1)
                        self.TabCtrlEPtsLineEd.setText("")
                        self.TabCtrlEPtsLineEd.setDisabled(1)
                        self.TabCtrlEPtsBtn.setDisabled(1)
                        try:
                            del spname["target_percentage"]
                        except:
                            pass
                        try:
                            del spname["excluded_points"]
                        except:
                            pass
                        try:
                            for cnt in reversed(range(self.TabCtrl2Grid4.count())):
                                widget = self.TabCtrl2Grid4.takeAt(cnt).widget()
                                if widget is not None:
                                    widget.deleteLater()
                        except:
                            pass
                        self.TabCtrl2Grid4=QtGui.QGridLayout()
                        self.CGrid1.addLayout(self.TabCtrl2Grid4, 8, 2, 1, 1)
                        Lbl = QtGui.QLabel()
                        self.TabCtrl2Grid4.addWidget(Lbl, 1, 0, 1, 1)
                        try:
                            Lbl.setText( "Manual Points Location: Units(%s)" %self.tempdata["general"]["display_units"])
                            Lbl.setFixedWidth(270)
                            Lbl = QtGui.QLabel()
                            self.TabCtrl2Grid4.addWidget(Lbl, 1, 1, 1, 1)
                            Lbl.setText( "X:")
                            Lbl.setFixedWidth(15)
                            self.TabCtrlCPXLineEd=QtGui.QLineEdit()
                            self.TabCtrlCPXLineEd.setValidator(QtGui.QDoubleValidator())
                            self.TabCtrl2Grid4.addWidget(self.TabCtrlCPXLineEd, 1, 2, 1, 1)
                            self.TabCtrlCPXLineEd.setFixedWidth(65)
                            spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
                            self.TabCtrl2Grid4.addItem(spacerItem, 1, 3, 1, 1)
                            Lbl = QtGui.QLabel()
                            Lbl.setText("Y:")
                            Lbl.setFixedWidth(15)
                            self.TabCtrl2Grid4.addWidget(Lbl, 1, 4, 1, 1)
                            self.TabCtrlCPYLineEd=QtGui.QLineEdit()
                            self.TabCtrlCPYLineEd.setValidator(QtGui.QDoubleValidator())
                            self.TabCtrl2Grid4.addWidget(self.TabCtrlCPYLineEd, 1, 5, 1, 1)
                            self.TabCtrlCPYLineEd.setFixedWidth(65)
                            spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
                            self.TabCtrl2Grid4.addItem(spacerItem, 1, 6, 1, 1)
                            Lbl = QtGui.QLabel()
                            Lbl.setText("Z:")
                            Lbl.setFixedWidth(15)
                            self.TabCtrl2Grid4.addWidget(Lbl, 1, 7, 1, 1)
                            self.TabCtrlCPZLineEd=QtGui.QLineEdit()
                            self.TabCtrlCPZLineEd.setValidator(QtGui.QDoubleValidator())
                            self.TabCtrl2Grid4.addWidget(self.TabCtrlCPZLineEd, 1, 8, 1, 1)
                            self.TabCtrlCPZLineEd.setFixedWidth(65)
                            spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
                            self.TabCtrl2Grid4.addItem(spacerItem, 1, 9, 1, 1)
                            ui=self.tempdata["general"]["import_units"]
                            ud=self.tempdata["general"]["display_units"]
                            # print ud
                            try:
                                # print spname["cp_location"]["x"]
                                self.setUnitText(self.TabCtrlCPXLineEd,ud,ui,float(spname["cp_location"]["x"]),True)
                            except:
                                pass
                            try:
                                self.setUnitText(self.TabCtrlCPYLineEd,ud,ui,float(spname["cp_location"]["y"]),True)
                            except:
                                pass
                            try:
                                self.setUnitText(self.TabCtrlCPZLineEd,ud,ui,float(spname["cp_location"]["z"]),True)
                            except:
                                pass
                            CPLoc=lambda: self.CPLocdata(self.TabCtrlCPXLineEd,"x")
                            self.TabCtrlCPXLineEd.editingFinished.connect(CPLoc)
                            CPLoc=lambda: self.CPLocdata(self.TabCtrlCPYLineEd,"y")
                            self.TabCtrlCPYLineEd.editingFinished.connect(CPLoc)
                            CPLoc=lambda: self.CPLocdata(self.TabCtrlCPZLineEd,"z")
                            self.TabCtrlCPZLineEd.editingFinished.connect(CPLoc)
                        except:
                            if self.jfimported:
                                try:
                                    if self.markunit>=4:
                                        # print "5.0"
                                        QtGui.QMessageBox.warning(self,"Warning", "Please define dimension units first!")
                                        self.TabCtrlCPMtdComBox.setCurrentIndex(0)
                                        self.StadicTab.setCurrentIndex(0)
                                except:
                                    self.markunit=4
                            elif self.created:
                                QtGui.QMessageBox.warning(self,"Warning", "Please define dimension units first!")
                                self.TabCtrlCPMtdComBox.setCurrentIndex(0)
                                self.StadicTab.setCurrentIndex(0)
                    else:
                        pass
                else:
                    try:
                        for cnt in reversed(range(self.TabCtrl2Grid4.count())):
                            widget = self.TabCtrl2Grid4.takeAt(cnt).widget()
                            if widget is not None:
                                widget.deleteLater()
                    except:
                        pass
                    # print "no"
                self.WriteToFile()
            except:
                pass

    def CPLocdata(self, object, key):
        try:
            index=self.TabCtrlSPNComBox.currentIndex()
            CIndex=self.TabCtrlCtrlZComBox.currentIndex()
            spname=self.tempdata["spaces"][index]["control_zones"][CIndex]
            ud=self.tempdata["general"]["display_units"]
            ui=self.tempdata["general"]["import_units"]
            try:
                spname["cp_location"][key]=self.uconvert(ud,ui,float(object.text()),False)
            except:
                spname["cp_location"]={}
                spname["cp_location"][key]=self.uconvert(ud,ui,float(object.text()),False)
            self.WriteToFile()
        except:
            object.clear()
            QtGui.QMessageBox.warning(self,"Warning", "Please define dimension units first!")
            self.StadicTab.setCurrentIndex(0)

    def CPExclude(self):
        if self.imported or self.created:
            SFile= QtGui.QFileDialog.getOpenFileName(self,"Import Points File",self.dir,"Points File (*.pts)")
            if SFile:
                index=self.TabCtrlSPNComBox.currentIndex()
                CIndex=self.TabCtrlCtrlZComBox.currentIndex()
                spname=self.tempdata["spaces"][index]["control_zones"][CIndex]
                SPath=os.path.join(self.dir,self.tempdata["spaces"][index]["input_directory"])
                SLine=self.CopyFile(SFile,SPath)
                self.TabCtrlEPtsLineEd.setText(os.path.basename(SLine))
                spname["excluded_points"]=os.path.basename(str(SLine))
                self.WriteToFile()

    def CPQty(self):
        if self.imported or self.created:
            try:
                index=self.TabCtrlSPNComBox.currentIndex()
                spname=self.tempdata["spaces"][index]["control_zones"]
                qindex=self.TabCtrlQtyComBox.currentIndex()
                i=self.TabCtrlCtrlZComBox.currentIndex()
                if qindex!=5:
                    spname[i]["quantity"]=qindex+1
                self.WriteToFile()
            except:
                pass

    def ElecCtrlAlg(self):

        if self.imported or self.created:
            # print "ctrlalg"
            try:
                index=self.TabCtrlSPNComBox.currentIndex()
                zindex=self.TabCtrlCtrlZComBox.currentIndex()
                spname=self.tempdata["spaces"][index]["control_zones"][zindex]
                try:
                    self.TabCtrlCPMtdComBox.currentIndexChanged[int].disconnect()
                except:
                    pass
                try:
                    for cnt in reversed(range(self.TabCtrl2Grid2.count())):
                        widget = self.TabCtrl2Grid2.takeAt(cnt).widget()
                        if widget is not None:
                            widget.deleteLater()
                except:
                    pass
                try:
                    for cnt in reversed(range(self.TabCtrl2Grid3.count())):
                        widget = self.TabCtrl2Grid3.takeAt(cnt).widget()
                        if widget is not None:
                            widget.deleteLater()
                except:
                    pass
                try:
                    for cnt in reversed(range(self.TabCtrl3Grid.count())):
                        widget = self.TabCtrl3Grid.takeAt(cnt).widget()
                        if widget is not None:
                            widget.deleteLater()
                except:
                    pass
                try:
                    for cnt in reversed(range(self.TabCtrl3Grid1.count())):
                        widget = self.TabCtrl3Grid1.takeAt(cnt).widget()
                        if widget is not None:
                            widget.deleteLater()
                except:
                    pass

                try:
                    for cnt in reversed(range(self.TabCtrl2Grid4.count())):
                        widget = self.TabCtrl2Grid4.takeAt(cnt).widget()
                        if widget is not None:
                            widget.deleteLater()
                except:
                    pass
                if self.TabCtrlOptCComBox.currentIndex()==0:
                    spname["optimum_control"]="dim_to_min"
                    # self.TabCtrlCPMtdComBox.setDisabled(1)
                    self.TabCtrlCPMtdComBox.clear()
                    self.TabCtrlCPMtdComBox.addItem("Auto")
                    self.TabCtrlCPMtdComBox.addItem("Manual")

                    try:
                        # print spname["cp_method"]
                        if spname["cp_method"]=="auto":
                            self.TabCtrlCPMtdComBox.setCurrentIndex(0)
                            self.CPMtd()
                        elif spname["cp_method"]=="manual":
                            self.TabCtrlCPMtdComBox.setCurrentIndex(1)
                            self.CPMtd()
                            # print "man"
                        else:
                            self.TabCtrlCPMtdComBox.setCurrentIndex(0)
                            self.CPMtd()
                    except:
                        self.TabCtrlCPMtdComBox.setCurrentIndex(0)
                        self.CPMtd()

                    self.TabCtrl2Grid2=QtGui.QGridLayout()
                    self.CGrid1.addLayout(self.TabCtrl2Grid2, 9, 2, 1, 1)
                    spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
                    self.TabCtrl2Grid2.addItem(spacerItem, 0, 0, 1, 1)
                    self.TabCtrlSenLbl = QtGui.QLabel(self.TabCtrl)
                    self.TabCtrl2Grid2.addWidget(self.TabCtrlSenLbl, 1, 0, 1, 1)
                    self.TabCtrlSenLbl.setText( "Sensor:")
                    self.TabCtrlSenLbl.setFixedWidth(80)
                    self.TabCtrlSenTPLbl = QtGui.QLabel(self.TabCtrl)
                    self.TabCtrl2Grid2.addWidget(self.TabCtrlSenTPLbl, 2, 1, 1, 1)
                    self.TabCtrlSenTPLbl.setText("Sensor Type:")
                    self.TabCtrlSenTPLbl.setFixedWidth(110)
                    self.TabCtrlSenTPComBox = QtGui.QComboBox(self.TabCtrl)
                    self.TabCtrl2Grid2.addWidget(self.TabCtrlSenTPComBox, 2, 2, 1, 1)
                    self.TabCtrlSenTPComBox.addItem("sensitivity file")
                    self.TabCtrlSenTPComBox.addItem("cosine")
                    self.TabCtrlSenTPComBox.setFixedWidth(300)
                    self.TabCtrlSenFLbl = QtGui.QLabel(self.TabCtrl)
                    self.TabCtrl2Grid2.addWidget(self.TabCtrlSenFLbl, 3, 1, 1, 1)
                    self.TabCtrlSenFLbl.setText("File: ")
                    self.TabCtrlSenFLineEd = QtGui.QLineEdit(self.TabCtrl)
                    self.TabCtrl2Grid2.addWidget(self.TabCtrlSenFLineEd, 3, 2, 1, 1)
                    self.TabCtrlSenFLineEd.setFixedWidth(300)
                    self.TabCtrlSenFBtn = QtGui.QPushButton(self.TabCtrl)
                    self.TabCtrl2Grid2.addWidget(self.TabCtrlSenFBtn, 3, 3, 1, 1)
                    self.TabCtrlSenFBtn.setText("Browse")
                    spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
                    self.TabCtrl2Grid2.addItem(spacerItem, 3, 4, 1, 1)
                    self.TabCtrlCalcLbl=QtGui.QLabel(self.TabCtrl)
                    self.TabCtrl2Grid2.addWidget(self.TabCtrlCalcLbl, 5, 1, 1, 1)
                    self.TabCtrlCalcLbl.setText("Calculated:")
                    self.TabCtrlCalcCbx=QtGui.QCheckBox(self.TabCtrl)
                    self.TabCtrl2Grid2.addWidget(self.TabCtrlCalcCbx, 5, 2, 1, 1)
                    self.TabCtrlCalcCbx.stateChanged.connect(self.ElecClbr)

                    self.TabCtrlCPMtdComBox.setEnabled(1)
                    self.TabCtrlSenFBtn.clicked.connect(self.ElecSenF)
                    try:
                        if spname["sensor"]["sensor_type"]=="sensitivity_file":
                            self.TabCtrlSenTPComBox.setCurrentIndex(0)
                            self.ElecSenTP()
                        elif spname["sensor"]["sensor_type"]=="cosine":
                            self.TabCtrlSenTPComBox.setCurrentIndex(1)
                            self.ElecSenTP()
                        else:
                            self.TabCtrlSenTPComBox.setCurrentIndex(-1)
                            self.ElecSenTP()
                    except:
                        self.TabCtrlSenTPComBox.setCurrentIndex(-1)
                        self.TabCtrlSenFLineEd.setDisabled(1)
                        self.TabCtrlSenFBtn.setDisabled(1)
                        self.ElecSenTP()
                    self.TabCtrlSenTPComBox.currentIndexChanged.connect(self.ElecSenTP)
                    self.TabCtrlCPMtdComBox.currentIndexChanged.connect(self.CPMtd)
                elif self.TabCtrlOptCComBox.currentIndex()==1:
                    spname["optimum_control"]="on"
                    self.TabCtrlTgtPctgLineEd.setDisabled(1)
                    self.TabCtrlTgtPctgLineEd.setText("")
                    self.TabCtrlCPMtdComBox.setDisabled(1)
                    # self.TabCtrlCPMtdComBox.setCurrentIndex(-1)
                    self.TabCtrlQtyComBox.setCurrentIndex(-1)
                    self.TabCtrlQtyComBox.setDisabled(1)
                    self.TabCtrlEPtsLineEd.setDisabled(1)
                    self.TabCtrlEPtsLineEd.setText("")
                    self.TabCtrlEPtsBtn.setDisabled(1)
                    try:
                        del spname["sensor"]
                    except:
                        pass
                    try:
                        del spname["open_dimming"]
                    except:
                        pass
                    try:
                        del spname["excluded_points"]
                    except:
                        pass
                    try:
                        del spname["target_percentage"]
                    except:
                        pass
                    try:
                        del spname["cp_method"]
                    except:
                        pass
                    try:
                        del spname["quantity"]
                    except:
                        pass
                elif self.TabCtrlOptCComBox.currentIndex()==3:
                    if spname["ballast_driver_information"]["ballast_type"]!="Eplus_dimming":
                        if self.StadicTab.currentIndex()==6:
                            if self.warning==True:
                                choice=QtGui.QMessageBox.question(self, "Warning!", "All zonal information will be lost! Confirm to continue", QtGui.QMessageBox.Yes |QtGui.QMessageBox.No)
                            else:
                                choice=QtGui.QMessageBox.Yes
                                self.warning=True
                            if choice==QtGui.QMessageBox.Yes:
                                QtGui.QMessageBox.information(self, "Info!", "You may change back to other control algorithms in \"Electric Lighting Control\" Tab!")
                                spname["ballast_driver_information"]["ballast_type"]="Eplus_dimming"
                                try:
                                    del spname["luminaire_layout"]
                                except:
                                    pass
                                temp=copy.deepcopy(spname)
                                del self.tempdata["spaces"][index]["control_zones"]
                                self.tempdata["spaces"][index]["control_zones"]=[]
                                self.tempdata["spaces"][index]["control_zones"].append(temp)
                                self.simchecked=True
                                spname=self.tempdata["spaces"][index]["control_zones"][0]
                                #subject to change
                                try:
                                    del spname["luminaire_information"]["LLF"]
                                except:
                                    pass
                                try:
                                    del spname["luminaire_information"]["lamp_lumens"]
                                except:
                                    pass
                                try:
                                    del spname["ballast_driver_information"]["bf_min"]
                                except:
                                    pass
                                try:
                                    del spname["ballast_driver_information"]["bf_max"]
                                except:
                                    pass
                                try:
                                    del spname["ballast_driver_information"]["ballast_factor"]
                                except:
                                    pass
                                try:
                                    del spname["ballast_driver_information"]["watts_min"]
                                except:
                                    pass
                                try:
                                    del spname["ballast_driver_information"]["watts_max"]
                                except:
                                    pass
                                try:
                                    del spname["ballast_driver_information"]["watts"]
                                except:
                                    pass
                                self.TabElecInfoAddBtn.setDisabled(1)
                                self.TabElecLayoutAddBtn.setDisabled(1)
                                self.WriteToFile()
                                self.TabElecLoad()
                                self.TabCtrlLoad()
                            else:
                                self.TabCtrlLoad()
                        else:
                            self.TabCtrlOptCComBox.setCurrentIndex(1)
                    else:
                        spname["optimum_control"]="EPlus_dim_to_min"
                        self.TabCtrlTgtPctgLineEd.setText("")
                        self.TabCtrlCPMtdComBox.clear()
                        self.TabCtrlCPMtdComBox.addItem("EPlus Auto")
                        self.TabCtrlCPMtdComBox.addItem("EPlus User")
                        self.TabCtrlCPMtdComBox.setEnabled(1)
                        try:
                            if spname["cp_method"]=="EPlus_auto":
                                self.TabCtrlCPMtdComBox.setCurrentIndex(0)
                                self.CPMtd()
                                # print "eauto"
                            elif spname["cp_method"]=="EPlus_user":
                                self.TabCtrlCPMtdComBox.setCurrentIndex(1)
                                self.CPMtd()
                                # print "eman"
                            else:
                                self.TabCtrlCPMtdComBox.setCurrentIndex(0)
                                self.CPMtd()
                        except:
                            self.TabCtrlCPMtdComBox.setCurrentIndex(0)
                            self.CPMtd()
                            # print "eno"
                        self.TabCtrl2Grid3=QtGui.QGridLayout()
                        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
                        self.TabCtrl2Grid3.addItem(spacerItem, 0, 0, 1, 1)
                        Lbl = QtGui.QLabel()
                        self.TabCtrl2Grid3.addWidget(Lbl, 1, 0, 1, 1)
                        Lbl.setText( "EPlus Info:")
                        Lbl.setFixedWidth(100)
                        Lbl = QtGui.QLabel()
                        self.TabCtrl2Grid3.addWidget(Lbl, 2, 1, 1, 1)
                        Lbl.setText( "LPD:")
                        Lbl.setFixedWidth(110)
                        self.TabCtrlLPDLineEd=QtGui.QLineEdit()
                        self.TabCtrlLPDLineEd.setValidator(QtGui.QDoubleValidator())
                        self.TabCtrl2Grid3.addWidget(self.TabCtrlLPDLineEd, 2, 2, 1, 1)
                        self.TabCtrlLPDLineEd.setFixedWidth(150)
                        Lbl = QtGui.QLabel()
                        Lbl.setText("w/m<sup>2</sup>")
                        self.TabCtrl2Grid3.addWidget(Lbl, 2, 3, 1, 1)
                        Lbl.setAlignment(QtCore.Qt.AlignLeft)
                        Lbl = QtGui.QLabel()
                        self.TabCtrl2Grid3.addWidget(Lbl, 3, 1, 1, 1)
                        Lbl.setText( "Minimum Light Output Fraction:")
                        Lbl.setFixedWidth(250)
                        self.TabCtrlMLOLineEd=QtGui.QLineEdit()
                        self.TabCtrl2Grid3.addWidget(self.TabCtrlMLOLineEd, 3, 2, 1, 1)
                        self.TabCtrlMLOLineEd.setFixedWidth(150)
                        Lbl = QtGui.QLabel()
                        self.TabCtrl2Grid3.addWidget(Lbl, 4, 1, 1, 1)
                        Lbl.setText( "Minimum Input Power Fraction:")
                        Lbl.setFixedWidth(250)
                        self.TabCtrlMIPLineEd=QtGui.QLineEdit()
                        self.TabCtrl2Grid3.addWidget(self.TabCtrlMIPLineEd, 4, 2, 1, 1)
                        self.TabCtrlMIPLineEd.setFixedWidth(150)
                        self.CGrid1.addLayout(self.TabCtrl2Grid3, 9, 2, 1, 1)
                        try:
                            self.TabCtrlLPDLineEd.setText(str(spname["ballast_driver_information"]["LPD"]))
                        except:
                            pass
                        try:
                            self.TabCtrlMIPLineEd.setText(str(spname["ballast_driver_information"]["minimum_input_power_fraction"]))
                        except:
                            pass
                        try:
                            self.TabCtrlMLOLineEd.setText(str(spname["ballast_driver_information"]["minimum_light_output_fraction"]))
                        except:
                            pass
                        LPDLBD=lambda: self.LPDdata(self.TabCtrlLPDLineEd,"LPD")
                        self.TabCtrlLPDLineEd.editingFinished.connect(LPDLBD)
                        LPDLBD=lambda: self.LPDdata(self.TabCtrlMIPLineEd,"minimum_input_power_fraction")
                        self.TabCtrlMIPLineEd.editingFinished.connect(LPDLBD)
                        LPDLBD=lambda: self.LPDdata(self.TabCtrlMLOLineEd,"minimum_light_output_fraction")
                        self.TabCtrlMLOLineEd.editingFinished.connect(LPDLBD)
                        self.TabCtrlCPMtdComBox.currentIndexChanged.connect(self.CPMtd)
                        try:
                            del spname["sensor"]
                        except:
                            pass
                        try:
                            del spname["open_dimming"]
                        except:
                            pass

                else:
                    self.TabCtrlTgtPctgLineEd.setDisabled(1)
                    self.TabCtrlTgtPctgLineEd.setText("")
                    self.TabCtrlCPMtdComBox.setDisabled(1)
                    self.TabCtrlCPMtdComBox.setCurrentIndex(-1)
                    self.TabCtrlQtyComBox.setCurrentIndex(-1)
                    self.TabCtrlQtyComBox.setDisabled(1)
                    self.TabCtrlEPtsLineEd.setDisabled(1)
                    self.TabCtrlEPtsLineEd.setText("")
                    self.TabCtrlEPtsBtn.setDisabled(1)
                self.WriteToFile()
            except:
                try:
                    for cnt in reversed(range(self.TabCtrl2Grid2.count())):
                        widget = self.TabCtrl2Grid2.takeAt(cnt).widget()
                        if widget is not None:
                            widget.deleteLater()
                except:
                    pass
                try:
                    for cnt in reversed(range(self.TabCtrl2Grid3.count())):
                        widget = self.TabCtrl2Grid3.takeAt(cnt).widget()
                        if widget is not None:
                            widget.deleteLater()
                except:
                    pass
                try:
                    for cnt in reversed(range(self.TabCtrl2Grid4.count())):
                        widget = self.TabCtrl2Grid4.takeAt(cnt).widget()
                        if widget is not None:
                            widget.deleteLater()
                except:
                    pass
                try:
                    for cnt in reversed(range(self.TabCtrl3Grid.count())):
                        widget = self.TabCtrl3Grid.takeAt(cnt).widget()
                        if widget is not None:
                            widget.deleteLater()
                except:
                    pass
                try:
                    for cnt in reversed(range(self.TabCtrl3Grid1.count())):
                        widget = self.TabCtrl3Grid1.takeAt(cnt).widget()
                        if widget is not None:
                            widget.deleteLater()
                except:
                    pass



    def LPDdata(self,object, key):
        index=self.TabCtrlSPNComBox.currentIndex()
        CIndex=self.TabCtrlCtrlZComBox.currentIndex()
        spname=self.tempdata["spaces"][index]["control_zones"][CIndex]["ballast_driver_information"]
        mark=0
        if key=="minimum_input_power_fraction" or key=="minimum_light_output_fraction":
            mark=self.floatChk(object, 0, 1)
        else:
            mark=0
        if mark==0:
            try:
                spname[key]=float(object.text())
            except:
                pass
        else:
            object.setText("0")
            object.setFocus()
        self.WriteToFile()
        self.TabElecLoad()

    def ElecSenTP(self):
        if self.imported or self.created:
            index=self.TabCtrlSPNComBox.currentIndex()
            zindex=self.TabCtrlCtrlZComBox.currentIndex()
            spname=self.tempdata["spaces"][index]["control_zones"][zindex]
            try:
                ud=self.tempdata["general"]["display_units"]
                ui=self.tempdata["general"]["import_units"]
                if self.TabCtrlSenTPComBox.currentIndex()==0:
                    try:
                        spname["sensor"]["sensor_type"]="sensitivity_file"
                    except:
                        spname["sensor"]={}
                        spname["sensor"]["sensor_type"]="sensitivity_file"
                    self.TabCtrlSenFLineEd.setEnabled(1)
                    self.TabCtrlSenFLineEd.setReadOnly(1)
                    self.TabCtrlSenFBtn.setEnabled(1)
                elif self.TabCtrlSenTPComBox.currentIndex()==1:
                    self.TabCtrlSenFLineEd.setDisabled(1)
                    self.TabCtrlSenFLineEd.setText("")
                    self.TabCtrlSenFBtn.setDisabled(1)
                    try:
                        spname["sensor"]["sensor_type"]="cosine"
                    except:
                        spname["sensor"]={}
                        spname["sensor"]["sensor_type"]="cosine"
                    try:
                        del spname["sensor"]["sensor_file"]
                    except:
                        pass
                try:
                    for cnt in reversed(range(self.TabCtrl3Grid.count())):
                        widget = self.TabCtrl3Grid.takeAt(cnt).widget()
                        if widget is not None:
                            widget.deleteLater()
                except:
                    pass
                # try:
                #     for cnt in reversed(range(self.TabCtrl3Grid.count())):
                #         widget = self.TabCtrl3Grid1.takeAt(cnt).widget()
                #         if widget is not None:
                #             widget.deleteLater()
                # except:
                #     pass
                self.TabCtrl2Grid2.update()
                self.TabCtrl3Grid=QtGui.QGridLayout()
                self.TabCtrl2Grid2.addLayout(self.TabCtrl3Grid, 4, 2, 1, 1)
                self.TabCtrlSenLLbl = QtGui.QLabel(self.TabCtrl)
                self.TabCtrl3Grid.addWidget(self.TabCtrlSenLLbl, 0, 0, 1, 1)
                self.TabCtrlSenLLbl.setText("Location:")
                self.TabCtrlSenLLbl.setFixedWidth(70)
                self.TabCtrlSenLXLbl = QtGui.QLabel(self.TabCtrl)
                self.TabCtrl3Grid.addWidget(self.TabCtrlSenLXLbl, 1, 0, 1, 1)
                self.TabCtrlSenLXLbl.setText("X: (%s)"%ud)
                self.TabCtrlSenLXLbl.setFixedWidth(70)
                self.TabCtrlSenLXLineEd = QtGui.QLineEdit(self.TabCtrl)
                self.TabCtrl3Grid.addWidget(self.TabCtrlSenLXLineEd, 1, 1, 1, 1)
                self.TabCtrlSenLXLineEd.setFixedWidth(70)
                self.TabCtrlSenLXDirLbl = QtGui.QLabel(self.TabCtrl)
                self.TabCtrl3Grid.addWidget(self.TabCtrlSenLXDirLbl, 1, 2, 1, 1)
                self.TabCtrlSenLXDirLbl.setText("X Dir:")
                self.TabCtrlSenLXDirLbl.setFixedWidth(70)
                self.TabCtrlSenLXDirLineEd = QtGui.QLineEdit(self.TabCtrl)
                self.TabCtrl3Grid.addWidget(self.TabCtrlSenLXDirLineEd, 1, 3, 1, 1)
                self.TabCtrlSenLXDirLineEd.setFixedWidth(70)
                self.TabCtrlSenLYLbl = QtGui.QLabel(self.TabCtrl)
                self.TabCtrl3Grid.addWidget(self.TabCtrlSenLYLbl, 2, 0, 1, 1)
                self.TabCtrlSenLYLbl.setText("Y: (%s)"%ud)
                self.TabCtrlSenLYLbl.setFixedWidth(70)
                self.TabCtrlSenLYLineEd = QtGui.QLineEdit(self.TabCtrl)
                self.TabCtrl3Grid.addWidget(self.TabCtrlSenLYLineEd, 2, 1, 1, 1)
                self.TabCtrlSenLYLineEd.setFixedWidth(70)
                self.TabCtrlSenLYDirLbl = QtGui.QLabel(self.TabCtrl)
                self.TabCtrl3Grid.addWidget(self.TabCtrlSenLYDirLbl, 2, 2, 1, 1)
                self.TabCtrlSenLYDirLbl.setText("Y Dir:")
                self.TabCtrlSenLYDirLbl.setFixedWidth(70)
                self.TabCtrlSenLYDirLineEd = QtGui.QLineEdit(self.TabCtrl)
                self.TabCtrl3Grid.addWidget(self.TabCtrlSenLYDirLineEd, 2, 3, 1, 1)
                self.TabCtrlSenLYDirLineEd.setFixedWidth(70)
                self.TabCtrlSenLZLbl = QtGui.QLabel(self.TabCtrl)
                self.TabCtrl3Grid.addWidget(self.TabCtrlSenLZLbl, 3, 0, 1, 1)
                self.TabCtrlSenLZLbl.setText("Z: (%s)"%ud)
                self.TabCtrlSenLZLbl.setFixedWidth(70)
                self.TabCtrlSenLZLineEd = QtGui.QLineEdit(self.TabCtrl)
                self.TabCtrl3Grid.addWidget(self.TabCtrlSenLZLineEd, 3, 1, 1, 1)
                self.TabCtrlSenLZLineEd.setFixedWidth(70)
                self.TabCtrlSenLZDirLbl = QtGui.QLabel(self.TabCtrl)
                self.TabCtrl3Grid.addWidget(self.TabCtrlSenLZDirLbl, 3, 2, 1, 1)
                self.TabCtrlSenLZDirLbl.setText("Z Dir:")
                self.TabCtrlSenLZDirLbl.setFixedWidth(70)
                self.TabCtrlSenLZDirLineEd = QtGui.QLineEdit(self.TabCtrl)
                self.TabCtrl3Grid.addWidget(self.TabCtrlSenLZDirLineEd, 3, 3, 1, 1)
                self.TabCtrlSenLZDirLineEd.setFixedWidth(70)
                self.TabCtrlSenLSpinLbl = QtGui.QLabel(self.TabCtrl)
                self.TabCtrl3Grid.addWidget(self.TabCtrlSenLSpinLbl, 4, 0, 1, 1)
                self.TabCtrlSenLSpinLbl.setText("Spin:")
                self.TabCtrlSenLSpinLbl.setFixedWidth(70)
                self.TabCtrlSenLSpinLineEd = QtGui.QLineEdit(self.TabCtrl)
                self.TabCtrl3Grid.addWidget(self.TabCtrlSenLSpinLineEd, 4, 1, 1, 1)
                self.TabCtrlSenLSpinLineEd.setFixedWidth(70)
                try:
                    self.setUnitText(self.TabCtrlSenLXLineEd,ud,ui,float(spname["sensor"]["location"]["x"]),True)
                except:
                    pass
                try:
                    self.setUnitText(self.TabCtrlSenLYLineEd,ud,ui,float(spname["sensor"]["location"]["y"]),True)
                except:
                    pass
                try:
                    self.setUnitText(self.TabCtrlSenLZLineEd,ud,ui,float(spname["sensor"]["location"]["z"]),True)
                except:
                    pass
                try:
                    self.TabCtrlSenLXDirLineEd.setText(str(spname["sensor"]["location"]["xd"]))
                except:
                    pass
                try:
                    self.TabCtrlSenLYDirLineEd.setText(str(spname["sensor"]["location"]["yd"]))
                except:
                    pass
                try:
                    self.TabCtrlSenLZDirLineEd.setText(str(spname["sensor"]["location"]["zd"]))
                except:
                    pass
                try:
                    self.TabCtrlSenLSpinLineEd.setText(str(spname["sensor"]["location"]["spin_ccw"]))
                except:
                    pass

                SenL=lambda: self.elecctrldata(self.TabCtrlSenLXLineEd,"x")
                self.TabCtrlSenLXLineEd.editingFinished.connect(SenL)
                SenL=lambda: self.elecctrldata(self.TabCtrlSenLYLineEd,"y")
                self.TabCtrlSenLYLineEd.editingFinished.connect(SenL)
                SenL=lambda: self.elecctrldata(self.TabCtrlSenLZLineEd,"z")
                self.TabCtrlSenLZLineEd.editingFinished.connect(SenL)
                SenL=lambda: self.elecctrldata(self.TabCtrlSenLXDirLineEd,"xd")
                self.TabCtrlSenLXDirLineEd.editingFinished.connect(SenL)
                SenL=lambda: self.elecctrldata(self.TabCtrlSenLYDirLineEd,"yd")
                self.TabCtrlSenLYDirLineEd.editingFinished.connect(SenL)
                SenL=lambda: self.elecctrldata(self.TabCtrlSenLZDirLineEd,"zd")
                self.TabCtrlSenLZDirLineEd.editingFinished.connect(SenL)
                SenL=lambda: self.elecctrldata(self.TabCtrlSenLSpinLineEd,"spin_ccw")
                self.TabCtrlSenLSpinLineEd.editingFinished.connect(SenL)
                try:
                    self.TabCtrlSenFLineEd.setText(spname["sensor"]["sensor_file"])
                except:
                    self.TabCtrlSenFLineEd.setText("")
            except:
                if self.jfimported:
                    try:
                        if self.markunit>=5:
                            # print "6.0"
                            QtGui.QMessageBox.warning(self,"Warning", "Please define dimension units first!")
                            self.TabCtrlOptCComBox.setCurrentIndex(1)
                            self.StadicTab.setCurrentIndex(0)
                    except:
                        self.markunit=5
                elif self.created:
                    QtGui.QMessageBox.warning(self,"Warning", "Please define dimension units first!")
                    self.TabCtrlOptCComBox.setCurrentIndex(1)
                    self.StadicTab.setCurrentIndex(0)



    def ElecSenF(self):
        try:
            SFile= QtGui.QFileDialog.getOpenFileName(self,"Import Sensor File",self.dir,"Sensor File (*.sen)")
            if SFile:
                index=self.TabCtrlSPNComBox.currentIndex()
                CIndex=self.TabCtrlCtrlZComBox.currentIndex()
                spname=self.tempdata["spaces"][index]["control_zones"][CIndex]["sensor"]
                SPath=os.path.join(self.dir,self.tempdata["spaces"][index]["input_directory"])
                SLine=self.CopyFile(SFile,SPath)
                self.TabCtrlSenFLineEd.setText(os.path.basename(SLine))
                spname["sensor_file"]=os.path.basename(str(SLine))
                self.WriteToFile()
        except:
            pass

    def elecctrldata(self, object, key):
        index=self.TabCtrlSPNComBox.currentIndex()
        CIndex=self.TabCtrlCtrlZComBox.currentIndex()
        try:
            spname=self.tempdata["spaces"][index]["control_zones"][CIndex]["sensor"]
        except:
            self.tempdata["spaces"][index]["control_zones"][CIndex]["sensor"]={}
            spname=self.tempdata["spaces"][index]["control_zones"][CIndex]["sensor"]
        ui=self.tempdata["general"]["import_units"]
        ud=self.tempdata["general"]["display_units"]
        mark=0
        mark=self.floatChk(object)
        if mark==0:
            try:
                if key=="x" or key=="y" or key=="z":
                    spname["location"][key]=self.uconvert(ud,ui,float(object.text()),False)
                else:
                    spname["location"][key]=float(object.text())
            except:
                spname["location"]={}
                if key=="x" or key=="y" or key=="z":
                    spname["location"][key]=self.uconvert(ud,ui,float(object.text()),False)
                else:
                    spname["location"][key]=float(object.text())
        else:
            object.setText("0")
            object.setFocus()
        self.WriteToFile()

    def ElecClbr(self):
        if self.TabCtrlCalcCbx.checkState():
            index=self.TabCtrlSPNComBox.currentIndex()
            zindex=self.TabCtrlCtrlZComBox.currentIndex()
            spname=self.tempdata["spaces"][index]["control_zones"][zindex]
            try:
                for cnt in reversed(range(self.TabCtrl3Grid.count())):
                    widget = self.TabCtrl3Grid1.takeAt(cnt).widget()
                    if widget is not None:
                        widget.deleteLater()
            except:
                pass
            self.TabCtrl3Grid1=QtGui.QGridLayout()
            self.TabCtrl2Grid2.addLayout(self.TabCtrl3Grid1, 6, 2, 1, 1)
            self.TabCtrlClbrLbl = QtGui.QLabel(self.TabCtrl)
            self.TabCtrl3Grid1.addWidget(self.TabCtrlClbrLbl, 0, 0, 1, 1)
            self.TabCtrlClbrLbl.setFixedWidth(150)
            self.TabCtrlClbrLbl.setText("Calibration:")
            self.TabCtrlOffLbl = QtGui.QLabel(self.TabCtrl)
            self.TabCtrl3Grid1.addWidget(self.TabCtrlOffLbl, 1, 0, 1, 1)
            self.TabCtrlOffLbl.setFixedWidth(150)
            self.TabCtrlOffLbl.setText("Off Signal:")
            self.TabCtrlOffLineEd = QtGui.QLineEdit(self.TabCtrl)
            self.TabCtrl3Grid1.addWidget(self.TabCtrlOffLineEd, 1, 1, 1, 1)
            self.TabCtrlOffLineEd.setFixedWidth(80)
            self.TabCtrlNTSLbl = QtGui.QLabel(self.TabCtrl)
            self.TabCtrl3Grid1.addWidget(self.TabCtrlNTSLbl, 2, 0, 1, 1)
            self.TabCtrlNTSLbl.setFixedWidth(150)
            self.TabCtrlNTSLbl.setText("Night Time Signal:")
            self.TabCtrlNTSLineEd = QtGui.QLineEdit(self.TabCtrl)
            self.TabCtrl3Grid1.addWidget(self.TabCtrlNTSLineEd, 2, 1, 1, 1)
            self.TabCtrlNTSLineEd.setFixedWidth(80)
            self.TabCtrlDTSLbl = QtGui.QLabel(self.TabCtrl)
            self.TabCtrl3Grid1.addWidget(self.TabCtrlDTSLbl, 3, 0, 1, 1)
            self.TabCtrlDTSLbl.setFixedWidth(150)
            self.TabCtrlDTSLbl.setText("Day Time Signal")
            self.TabCtrlDTSLineEd = QtGui.QLineEdit(self.TabCtrl)
            self.TabCtrl3Grid1.addWidget(self.TabCtrlDTSLineEd, 3, 1, 1, 1)
            self.TabCtrlDTSLineEd.setFixedWidth(80)
            Clbr=lambda: self.clbrdata(self.TabCtrlOffLineEd,"off_signal")
            self.TabCtrlOffLineEd.editingFinished.connect(Clbr)
            Clbr=lambda: self.clbrdata(self.TabCtrlNTSLineEd,"minimum_bf_signal")
            self.TabCtrlNTSLineEd.editingFinished.connect(Clbr)
            Clbr=lambda: self.clbrdata(self.TabCtrlDTSLineEd,"maximum_bf_signal")
            self.TabCtrlDTSLineEd.editingFinished.connect(Clbr)
            try:
                self.TabCtrlOffLineEd.setText(str(spname["open_dimming"]["off_signal"]))
                self.TabCtrlNTSLineEd.setText(str(spname["open_dimming"]["minimum_bf_signal"]))
                self.TabCtrlDTSLineEd.setText(str(spname["open_dimming"]["maximum_bf_signal"]))
            except:
                spname["open_dimming"]={}
            self.WriteToFile()
        else:
            index=self.TabCtrlSPNComBox.currentIndex()
            zindex=self.TabCtrlCtrlZComBox.currentIndex()
            spname=self.tempdata["spaces"][index]["control_zones"][zindex]
            try:
                for cnt in reversed(range(self.TabCtrl3Grid1.count())):
                    widget = self.TabCtrl3Grid1.takeAt(cnt).widget()
                    if widget is not None:
                        widget.deleteLater()
            except:
                pass
            try:
                del spname["open_dimming"]
                # self.TabCtrlOffLineEd.setText("")
                # self.TabCtrlNTSLineEd.setText("")
                # self.TabCtrlDTSLineEd.setText("")
            except:
                pass
            self.WriteToFile()


    def clbrdata(self, object, key):
        index=self.TabCtrlSPNComBox.currentIndex()
        CIndex=self.TabCtrlCtrlZComBox.currentIndex()
        spname=self.tempdata["spaces"][index]["control_zones"][CIndex]["open_dimming"]
        mark=0
        mark=self.intChk(object, 0, 100000000000000)
        if mark==0:
            spname[key]=int(object.text())
        else:
            object.setText("0")
            object.setFocus()
        self.WriteToFile()


    def CheckState(self,object,para):
        if not self.TabDMtrGCbx.isChecked():
            index=self.TabDMtrSPNComBox.currentIndex()
            spname=self.tempdata["spaces"][index]
            # if object.checkState():
            if object.isChecked():
                if para=="DF":
                    spname[para]=True
                elif para=="BSDF":
                    WGIndex=self.TabWinWGComBox.currentIndex()
                    spname["window_groups"][WGIndex]["BSDF"]=True
                    ###Subject to change
                    self.TabWinBSDFSetList.setEnabled(1)
                    self.TabWinBSDFBMatComBox.setEnabled(1)
                    try:
                        self.TabWinBSDFSetList.addItem(spname["window_groups"][WGIndex]["bsdf_setting_materials"][0][0])
                        self.TabWinBSDFBMatComBox.addItem(spname["window_groups"][WGIndex]["bsdf_base_materials"][0])
                    except:
                        pass
                else:
                    try:
                        spname[para]["calculate"]=True
                    except:
                        spname[para]={}
                        spname[para]["calculate"]=True
                    if para=="sDA":
                        try:
                            for j in range(len(spname["window_groups"])):
                                try:
                                    junk=spname["sDA"]["window_group_settings"][j]
                                except:
                                    try:
                                        spname["sDA"]["window_group_settings"].append(0)
                                    except:
                                        spname["sDA"]["window_group_settings"]=[]
                                        spname["sDA"]["window_group_settings"].append(0)
                        except:
                            QtGui.QMessageBox.warning(self, "Warning", "No window groups in space: %s" %spname["space_name"])
                            try:
                                del spname[para]
                            except:
                                pass
                            # object.setChecked(0)
            else:
                if para=="DF":
                    spname[para]=False
                elif para=="BSDF":
                    WGIndex=self.TabWinWGComBox.currentIndex()
                    ###Subject to change
                    self.TabWinBSDFSetList.clear()
                    self.TabWinBSDFBMatComBox.clear()
                else:
                    try:
                        spname[para]["calculate"]=False
                    except:

                        spname[para]={}
                        spname[para]["calculate"]=False
                    if para=="sDA":
                        try:
                            for i in range(len(self.tempdata["spaces"])):
                                for j in range(len(self.tempdata["spaces"][i]["window_groups"])):
                                    try:
                                        junk=spname["sDA"]["window_group_settings"][j]
                                    except:
                                        try:
                                            spname["sDA"]["window_group_settings"].append(0)
                                        except:
                                            spname["sDA"]["window_group_settings"]=[]
                                            spname["sDA"]["window_group_settings"].append(0)
                        except:
                            try:
                                del spname[para]
                            except:
                                pass
                            # object.setChecked(0)
            self.TabMtrLoad()
        else:
            spname=self.tempdata["general"]
            if object.isChecked():
                if para=="DF":
                    spname[para]=True
                else:
                    try:
                        spname[para]["calculate"]=True
                    except:
                        spname[para]={}
                        spname[para]["calculate"]=True
            else:
                if para=="DF":
                    spname[para]=False
                else:
                    try:
                        spname[para]["calculate"]=False
                    except:
                        spname[para]={}
                        spname[para]["calculate"]=False
                    if para=="sDA":
                        try:
                            if len(spname["window_groups"])==0:
                                try:
                                    del spname[para]
                                except:
                                    pass

                        except:
                            try:
                                del spname[para]
                            except:
                                pass
            self.mtrGeneral()

        self.WriteToFile()
        self.TabMtrLoad()

    def MtrValue(self,object,mtr, value):
        if self.created or self.imported:
            try:
                junk=self.tempdata["general"]["illum_units"]
                if self.TabDMtrGCbx.isChecked():
                    spname=self.tempdata["general"]
                else:
                    index=self.TabDMtrSPNComBox.currentIndex()
                    spname=self.tempdata["spaces"][index]
                if value!="DA_fraction":
                    spname[mtr][value]=int(object.text())
                else:
                    mark=0
                    mark=self.floatChk(object,0,1)
                    if mark==0:
                        spname[mtr][value]=float(object.text())
                    else:
                        object.setText("0.5")
                        # object.setFocus()
                self.TabMtrLoad()
                self.WriteToFile()
            except:
                object.clear()
                QtGui.QMessageBox.warning(self, "Warning", "Set Lighting Units!")
                self.StadicTab.setCurrentIndex(0)


    def mtrGeneral(self):
        if self.imported or self.created:
            spname=self.tempdata["general"]
            if self.TabDMtrGCbx.checkState():
                self.TabDMtrSPNComBox.setDisabled(1)
                try:
                    lu=self.tempdata["general"]["illum_units"]
                    if lu=="lux":
                        val=300
                        val1=2500
                        val2=100
                    else:
                        val=30
                        val1=250
                        val2=10
                    try:
                        if spname["DA"]["calculate"]:
                            self.TabDMtrDAChkB.setChecked(1)
                            try:
                                self.TabDMtrDATgtLineEd.setText(str(spname["DA"]["illuminance"]))
                            except:
                                self.TabDMtrDATgtLineEd.setText(str(val))
                                spname["DA"]["illuminance"]=val
                            self.WriteToFile()
                            self.TabDMtrDATgtLineEd.setEnabled(1)
                        else:
                            try:
                                junk=spname["DA"]["illuminance"]
                            except:
                                spname["DA"]["illuminance"]=val
                                self.WriteToFile()
                            self.TabDMtrDAChkB.setChecked(0)
                            self.TabDMtrDATgtLineEd.setText(" ")
                            self.TabDMtrDATgtLineEd.setDisabled(1)
                    except:
                        spname["DA"]={}
                        spname["DA"]["calculate"]=False
                        self.WriteToFile()
                        self.mtrGeneral()
                    try:
                        if spname["sDA"]["calculate"]:
                            for i in range(len(self.tempdata["spaces"])):
                                try:
                                    self.tempdata["spaces"][i]["sDA"]["calculate"]=True
                                except:
                                    self.tempdata["spaces"][i]["sDA"]={}
                                    self.tempdata["spaces"][i]["sDA"]["calculate"]=True
                                try:
                                    for j in range(len(self.tempdata["spaces"][i]["window_groups"])):
                                        try:
                                            junk=self.tempdata["spaces"][i]["sDA"]["window_group_settings"][j]
                                        except:
                                            try:
                                                self.tempdata["spaces"][i]["sDA"]["window_group_settings"].append(0)
                                            except:
                                                self.tempdata["spaces"][i]["sDA"]["window_group_settings"]=[]
                                                self.tempdata["spaces"][i]["sDA"]["window_group_settings"].append(0)
                                    self.TabDMtrsDAChkB.setChecked(1)
                                    self.tempdata["spaces"][i]["sDA"]["calculate"]=True
                                except:
                                    del spname["sDA"]
                                    QtGui.QMessageBox.warning(self, "Warning", "No Window Groups found in space: %s!" %self.tempdata["spaces"][i]["space_name"])
                                    self.WriteToFile()
                                    self.mtrGeneral()
                            try:
                                self.TabDMtrsDATgtLineEd.setText(str(spname["sDA"]["illuminance"]))
                            except:
                                try:
                                    self.TabDMtrsDATgtLineEd.setText(str(val))
                                    spname["sDA"]["illuminance"]=val
                                except:
                                    pass
                                self.WriteToFile()
                            try:
                                self.TabDMtrsDAFrcLineEd.setText(str(spname["sDA"]["DA_fraction"]))
                            except:
                                try:
                                    self.TabDMtrsDAFrcLineEd.setText(str(0.5))
                                    spname["sDA"]["DA_fraction"]=0.5
                                except:
                                    pass
                                self.WriteToFile()
                            try:
                                self.TabDMtrsDASTmLineEd.setText(str(spname["sDA"]["start_time"]))
                            except:
                                try:
                                    self.TabDMtrsDASTmLineEd.setText(str(8))
                                    spname["sDA"]["start_time"]=8
                                except:
                                    pass
                                self.WriteToFile()
                            try:
                                if spname["sDA"]["end_time"]<=spname["sDA"]["start_time"]:
                                    spname["sDA"]["end_time"]=spname["sDA"]["start_time"]+1
                                    self.WriteToFile()
                                self.TabDMtrsDAETmLineEd.setText(str(spname["sDA"]["end_time"]))
                            except:
                                try:
                                    self.TabDMtrsDAETmLineEd.setText(str(18))
                                    spname["sDA"]["end_time"]=18
                                except:
                                    pass
                                self.WriteToFile()
                            self.TabDMtrsDATgtLineEd.setEnabled(1)
                            self.TabDMtrsDAFrcLineEd.setEnabled(1)
                            self.TabDMtrsDASTmLineEd.setEnabled(1)
                            self.TabDMtrsDAETmLineEd.setEnabled(1)
                        else:
                            self.TabDMtrsDAChkB.setChecked(0)
                            self.TabDMtrsDATgtLineEd.setText("")
                            self.TabDMtrsDAFrcLineEd.setText("")
                            self.TabDMtrsDASTmLineEd.setText("")
                            self.TabDMtrsDAETmLineEd.setText("")
                            self.TabDMtrsDATgtLineEd.setDisabled(1)
                            self.TabDMtrsDAFrcLineEd.setDisabled(1)
                            self.TabDMtrsDASTmLineEd.setDisabled(1)
                            self.TabDMtrsDAETmLineEd.setDisabled(1)
                            try:
                                junk=spname["sDA"]["illuminance"]
                            except:
                                try:
                                    spname["sDA"]["illuminance"]=val
                                except:
                                    pass
                                self.WriteToFile()
                            try:
                                junk=spname["sDA"]["DA_fraction"]
                            except:
                                try:
                                    spname["sDA"]["DA_fraction"]=0.5
                                except:
                                    pass
                                self.WriteToFile()
                            try:
                                junk=spname["sDA"]["start_time"]
                            except:
                                try:
                                    spname["sDA"]["start_time"]=8
                                except:
                                    pass
                                self.WriteToFile()
                            try:
                                if spname["sDA"]["end_time"]<=spname["sDA"]["start_time"]:
                                    spname["sDA"]["end_time"]=spname["sDA"]["start_time"]+1
                                self.WriteToFile()
                            except:
                                try:
                                    spname["sDA"]["end_time"]=18
                                except:
                                    pass
                                self.WriteToFile()

                            for i in range(len(self.tempdata["spaces"])):
                                try:
                                    for j in range(len(self.tempdata["spaces"][i]["window_groups"])):
                                        try:
                                            junk=self.tempdata["spaces"][i]["sDA"]["window_group_settings"][j]
                                        except:
                                            try:
                                                self.tempdata["spaces"][i]["sDA"]["window_group_settings"].append(0)
                                            except:
                                                self.tempdata["spaces"][i]["sDA"]["window_group_settings"]=[]
                                                self.tempdata["spaces"][i]["sDA"]["window_group_settings"].append(0)
                                except:
                                    del spname["sDA"]
                                    QtGui.QMessageBox.warning(self, "Warning", "No Window Groups found in space: %s!" %self.tempdata["spaces"][i]["space_name"])
                                    self.WriteToFile()
                                    self.mtrGeneral()
                    except:
                        self.TabDMtrsDAChkB.setChecked(0)
                        self.TabDMtrsDATgtLineEd.setText("")
                        self.TabDMtrsDAFrcLineEd.setText("")
                        self.TabDMtrsDASTmLineEd.setText("")
                        self.TabDMtrsDAETmLineEd.setText("")
                        self.TabDMtrsDATgtLineEd.setDisabled(1)
                        self.TabDMtrsDAFrcLineEd.setDisabled(1)
                        self.TabDMtrsDASTmLineEd.setDisabled(1)
                        self.TabDMtrsDAETmLineEd.setDisabled(1)
                        self.WriteToFile()


                    try:
                        if spname["occupied_sDA"]["calculate"]:
                            self.TabDMtrOsDAChkB.setChecked(1)
                            try:
                                self.TabDMtrOsDATgtLineEd.setText(str(spname["occupied_sDA"]["illuminance"]))
                            except:
                                self.TabDMtrOsDATgtLineEd.setText(str(val))
                                spname["occupied_sDA"]["illuminance"]=val
                                self.WriteToFile()
                            try:
                                self.TabDMtrOsDAFrcLineEd.setText(str(spname["occupied_sDA"]["DA_fraction"]))
                            except:
                                spname["occupied_sDA"]["DA_fraction"]=0.5
                                self.TabDMtrOsDAFrcLineEd.setText(str(0.5))
                                self.WriteToFile()
                            self.TabDMtrOsDATgtLineEd.setEnabled(1)
                            self.TabDMtrOsDAFrcLineEd.setEnabled(1)
                        else:
                            try:
                                junk=spname["occupied_sDA"]["illuminance"]
                            except:
                                spname["occupied_sDA"]["illuminance"]=val
                                self.WriteToFile()
                            try:
                                junk=spname["occupied_sDA"]["DA_fraction"]
                            except:
                                spname["occupied_sDA"]["DA_fraction"]=0.5
                                self.WriteToFile()
                            self.TabDMtrOsDAChkB.setChecked(0)
                            self.TabDMtrOsDATgtLineEd.setText("")
                            self.TabDMtrOsDAFrcLineEd.setText("")
                            self.TabDMtrOsDATgtLineEd.setDisabled(1)
                            self.TabDMtrOsDAFrcLineEd.setDisabled(1)
                    except:
                        spname["occupied_sDA"]={}
                        spname["occupied_sDA"]["calculate"]=False
                        self.WriteToFile()
                        self.mtrGeneral()
                    try:
                        if spname["cDA"]["calculate"]:
                            self.TabDMtrcDAChkB.setChecked(1)
                            try:
                                self.TabDMtrcDATgtLineEd.setText(str(spname["cDA"]["illuminance"]))
                            except:
                                self.TabDMtrcDATgtLineEd.setText(str(val))
                                spname["cDA"]["illuminance"]=val
                                self.WriteToFile()
                            self.TabDMtrcDATgtLineEd.setEnabled(1)
                        else:
                            try:
                                junk=spname["cDA"]["illuminance"]
                            except:
                                spname["cDA"]["illuminance"]=val
                                self.WriteToFile()
                            self.TabDMtrcDAChkB.setChecked(0)
                            self.TabDMtrcDATgtLineEd.setText("")
                            self.TabDMtrcDATgtLineEd.setDisabled(1)
                    except:
                        spname["cDA"]={}
                        spname["cDA"]["calculate"]=False
                        self.WriteToFile()
                        self.mtrGeneral()
                    try:
                        if spname["DF"]:
                            self.TabDMtrDFChkB.setChecked(1)
                        else:
                            self.TabDMtrDFChkB.setChecked(0)
                    except:
                        spname["DF"]=False
                        self.WriteToFile()
                        self.mtrGeneral()
                    try:
                        if spname["UDI"]["calculate"]:
                            self.TabDMtrUDIChkB.setChecked(1)
                            try:
                                self.TabDMtrUDIMinLineEd.setText(str(spname["UDI"]["minimum"]))
                            except:
                                spname["UDI"]["minimum"]=val2
                                self.TabDMtrUDIMinLineEd.setText(str(val2))
                                self.WriteToFile()
                            try:
                                if spname["UDI"]["maximum"]<=spname["UDI"]["minimum"]:
                                    spname["UDI"]["maximum"]=spname["UDI"]["minimum"]+1
                                    self.WriteToFile()
                                self.TabDMtrUDIMaxLineEd.setText(str(spname["UDI"]["maximum"]))
                            except:
                                self.TabDMtrUDIMaxLineEd.setText(str(val1))
                                spname["UDI"]["maximum"]=val1
                                self.WriteToFile()
                            self.TabDMtrUDIMaxLineEd.setEnabled(1)
                            self.TabDMtrUDIMinLineEd.setEnabled(1)
                        else:
                            try:
                                junk=spname["UDI"]["minimum"]
                            except:
                                spname["UDI"]["minimum"]=val2
                                self.WriteToFile()
                            try:
                                if spname["UDI"]["maximum"]<=spname["UDI"]["minimum"]:
                                    spname["UDI"]["maximum"]=spname["UDI"]["minimum"]+1
                                    self.WriteToFile()
                                junk=spname["UDI"]["maximum"]
                            except:
                                spname["UDI"]["maximum"]=val1
                                self.WriteToFile()
                            self.TabDMtrUDIChkB.setChecked(0)
                            self.TabDMtrUDIMaxLineEd.setText("")
                            self.TabDMtrUDIMinLineEd.setText("")
                            self.TabDMtrUDIMaxLineEd.setDisabled(1)
                            self.TabDMtrUDIMinLineEd.setDisabled(1)
                    except:
                        spname["UDI"]={}
                        spname["UDI"]["calculate"]=False
                        self.WriteToFile()
                        self.mtrGeneral()
                    try:
                        if spname["Energy"]["calculate"]:
                            self.TabDMtrEgyChkB.setChecked(1)
                        else:
                            self.TabDMtrEgyChkB.setChecked(0)
                    except:
                        spname["Energy"]={}
                        spname["Energy"]["calculate"]=False
                        self.WriteToFile()
                        self.mtrGeneral()
                except:
                    # if self.jfimported:
                    #     try:
                    #         if self.lightingunit>=1:
                    #             QtGui.QMessageBox.warning(self,"Warning!", "Define your lighting units first!")
                    #             self.StadicTab.setCurrentIndex(0)
                    #     except:
                    #         self.lightingunit=1
                    # elif self.created:
                    QtGui.QMessageBox.warning(self,"Warning!", "Define your lighting units first!")
                    self.StadicTab.setCurrentIndex(0)
            else:
                self.TabDMtrSPNComBox.setEnabled(1)
                self.TabMtrLoad()




    def TabMtrLoad(self):
        try:
            index=self.TabDMtrSPNComBox.currentIndex()
            spname=self.tempdata["spaces"][index]
            if self.TabDMtrGCbx.isChecked():
                self.mtrGeneral()
            else:
                try:
                    lu=self.tempdata["general"]["illum_units"]
                    if lu=="lux":
                        val=300
                        val1=2500
                        val2=100
                    else:
                        val=30
                        val1=250
                        val2=10
                    if spname["DA"]["calculate"]:
                        self.TabDMtrDAChkB.setChecked(1)
                        try:
                            self.TabDMtrDATgtLineEd.setText(str(spname["DA"]["illuminance"]))
                        except:
                            self.TabDMtrDATgtLineEd.setText(str(val))
                            spname["DA"]["illuminance"]=val
                            self.WriteToFile()
                        self.TabDMtrDATgtLineEd.setEnabled(1)
                    else:
                        self.TabDMtrDAChkB.setChecked(0)
                        self.TabDMtrDATgtLineEd.setText(" ")
                        self.TabDMtrDATgtLineEd.setDisabled(1)
                        try:
                            junk=spname["DA"]["illuminance"]
                        except:
                            spname["DA"]["illuminance"]=val
                            self.WriteToFile()
                    try:
                        if spname["sDA"]["calculate"]:
                            try:
                                if len(spname["window_groups"])>0:
                                    self.TabDMtrsDAChkB.setChecked(1)
                                    try:
                                        self.TabDMtrsDATgtLineEd.setText(str(spname["sDA"]["illuminance"]))
                                    except:
                                        self.TabDMtrsDATgtLineEd.setText(str(val))
                                        spname["sDA"]["illuminance"]=val
                                        self.WriteToFile()
                                    try:
                                        self.TabDMtrsDAFrcLineEd.setText(str(spname["sDA"]["DA_fraction"]))
                                    except:
                                        self.TabDMtrsDAFrcLineEd.setText(str(0.5))
                                        spname["sDA"]["DA_fraction"]=0.5
                                        self.WriteToFile()
                                    try:
                                        self.TabDMtrsDASTmLineEd.setText(str(spname["sDA"]["start_time"]))
                                    except:
                                        self.TabDMtrsDASTmLineEd.setText(str(8))
                                        spname["sDA"]["start_time"]=8
                                        self.WriteToFile()
                                    try:
                                        if spname["sDA"]["end_time"]<=spname["sDA"]["start_time"]:
                                            spname["sDA"]["end_time"]=spname["sDA"]["start_time"]+1
                                            self.WriteToFile()
                                        self.TabDMtrsDAETmLineEd.setText(str(spname["sDA"]["end_time"]))
                                    except:
                                        self.TabDMtrsDAETmLineEd.setText(str(18))
                                        spname["sDA"]["end_time"]=18
                                        self.WriteToFile()
                                    self.TabDMtrsDATgtLineEd.setEnabled(1)
                                    self.TabDMtrsDAFrcLineEd.setEnabled(1)
                                    self.TabDMtrsDASTmLineEd.setEnabled(1)
                                    self.TabDMtrsDAETmLineEd.setEnabled(1)
                                else:
                                    spname["sDA"]["calculate"]=False
                                    self.WriteToFile()
                                    self.TabMtrLoad()
                            except:
                                del spname["sDA"]
                                self.WriteToFile()
                                self.TabMtrLoad()
                        else:
                            self.TabDMtrsDAChkB.setChecked(0)
                            self.TabDMtrsDATgtLineEd.setText("")
                            self.TabDMtrsDAFrcLineEd.setText("")
                            self.TabDMtrsDASTmLineEd.setText("")
                            self.TabDMtrsDAETmLineEd.setText("")
                            self.TabDMtrsDATgtLineEd.setDisabled(1)
                            self.TabDMtrsDAFrcLineEd.setDisabled(1)
                            self.TabDMtrsDASTmLineEd.setDisabled(1)
                            self.TabDMtrsDAETmLineEd.setDisabled(1)
                            try:
                                junk=(spname["sDA"]["illuminance"])
                            except:
                                spname["sDA"]["illuminance"]=val
                                self.WriteToFile()
                            try:
                                junk=(spname["sDA"]["DA_fraction"])
                            except:
                                spname["sDA"]["DA_fraction"]=0.5
                                self.WriteToFile()
                            try:
                                junk=spname["sDA"]["start_time"]
                            except:
                                spname["sDA"]["start_time"]=8
                                self.WriteToFile()
                            try:
                                junk=spname["sDA"]["end_time"]
                            except:
                                spname["sDA"]["end_time"]=18
                                self.WriteToFile()
                    except:
                        self.TabDMtrsDAChkB.setCheckState(0)
                        self.TabDMtrsDATgtLineEd.setText("")
                        self.TabDMtrsDAFrcLineEd.setText("")
                        self.TabDMtrsDASTmLineEd.setText("")
                        self.TabDMtrsDAETmLineEd.setText("")
                        self.TabDMtrsDATgtLineEd.setDisabled(1)
                        self.TabDMtrsDAFrcLineEd.setDisabled(1)
                        self.TabDMtrsDASTmLineEd.setDisabled(1)
                        self.TabDMtrsDAETmLineEd.setDisabled(1)
                    if spname["occupied_sDA"]["calculate"]:
                        self.TabDMtrOsDAChkB.setChecked(1)
                        try:
                            self.TabDMtrOsDATgtLineEd.setText(str(spname["occupied_sDA"]["illuminance"]))
                        except:
                            self.TabDMtrOsDATgtLineEd.setText(str(val))
                            spname["occupied_sDA"]["illuminance"]=val
                            self.WriteToFile()
                        try:
                            self.TabDMtrOsDAFrcLineEd.setText(str(spname["occupied_sDA"]["DA_fraction"]))
                        except:
                            self.TabDMtrOsDAFrcLineEd.setText(str(0.5))
                            spname["occupied_sDA"]["DA_fraction"]=0.5
                            self.WriteToFile()
                        self.TabDMtrOsDATgtLineEd.setEnabled(1)
                        self.TabDMtrOsDAFrcLineEd.setEnabled(1)
                    else:
                        self.TabDMtrOsDAChkB.setChecked(0)
                        self.TabDMtrOsDATgtLineEd.setText("")
                        self.TabDMtrOsDAFrcLineEd.setText("")
                        self.TabDMtrOsDATgtLineEd.setDisabled(1)
                        self.TabDMtrOsDAFrcLineEd.setDisabled(1)
                        try:
                           junk=str(spname["occupied_sDA"]["illuminance"])
                        except:
                            spname["occupied_sDA"]["illuminance"]=val
                            self.WriteToFile()
                        try:
                            junk=str(spname["occupied_sDA"]["DA_fraction"])
                        except:
                            spname["occupied_sDA"]["DA_fraction"]=0.5
                            self.WriteToFile()
                    if spname["cDA"]["calculate"]:
                        self.TabDMtrcDAChkB.setChecked(1)
                        try:
                            self.TabDMtrcDATgtLineEd.setText(str(spname["cDA"]["illuminance"]))
                        except:
                            self.TabDMtrcDATgtLineEd.setText(str(val))
                            spname["cDA"]["illuminance"]=val
                            self.WriteToFile()
                        self.TabDMtrcDATgtLineEd.setEnabled(1)
                    else:
                        self.TabDMtrcDAChkB.setChecked(0)
                        self.TabDMtrcDATgtLineEd.setText("")
                        self.TabDMtrcDATgtLineEd.setDisabled(1)
                        try:
                            junk=str(spname["cDA"]["illuminance"])
                        except:
                            spname["cDA"]["illuminance"]=val
                            self.WriteToFile()
                    if spname["DF"]:
                        self.TabDMtrDFChkB.setChecked(1)
                    else:
                        self.TabDMtrDFChkB.setChecked(0)
                    try:
                        if spname["Energy"]["calculate"]:
                            self.TabDMtrEgyChkB.setChecked(1)
                        else:
                            self.TabDMtrEgyChkB.setChecked(0)
                    except:
                        pass
                    if spname["UDI"]["calculate"]:
                        self.TabDMtrUDIChkB.setChecked(1)
                        try:
                            if spname["UDI"]["maximum"]<=spname["UDI"]["minimum"]:
                                spname["UDI"]["maximum"]=spname["UDI"]["minimum"]+1
                                self.WriteToFile()
                            self.TabDMtrUDIMaxLineEd.setText(str(spname["UDI"]["maximum"]))
                            self.TabDMtrUDIMinLineEd.setText(str(spname["UDI"]["minimum"]))

                        except:
                            self.TabDMtrUDIMaxLineEd.setText(str(val1))
                            self.TabDMtrUDIMinLineEd.setText(str(val2))
                            spname["UDI"]["minimum"]=val2
                            spname["UDI"]["maximum"]=val1
                            self.WriteToFile()
                        self.TabDMtrUDIMaxLineEd.setEnabled(1)
                        self.TabDMtrUDIMinLineEd.setEnabled(1)

                    else:
                        self.TabDMtrUDIChkB.setChecked(0)
                        self.TabDMtrUDIMaxLineEd.setText("")
                        self.TabDMtrUDIMinLineEd.setText("")
                        self.TabDMtrUDIMaxLineEd.setDisabled(1)
                        self.TabDMtrUDIMinLineEd.setDisabled(1)
                        try:
                            junk=spname["UDI"]["maximum"]
                        except:
                            spname["UDI"]["maximum"]=val1
                            self.WriteToFile()
                        try:
                            junk=spname["UDI"]["minimum"]
                        except:
                            spname["UDI"]["minimum"]=val2
                            self.WriteToFile()
                except:
                    # pass
                    # if self.jfimported:
                    #     try:
                    #         if self.lightingunit>=2:
                    #             QtGui.QMessageBox.warning(self,"Warning!", "Define your lighting units first!")
                    #             self.StadicTab.setCurrentIndex(0)
                    #     except:
                    #         self.lightingunit=2
                    # elif self.created:
                    QtGui.QMessageBox.warning(self,"Warning!", "Define your lighting units first!")
                    self.StadicTab.setCurrentIndex(0)
        except:
            pass

    def tableitem(self, text):
        item=QtGui.QTableWidgetItem()
        text=str(text)
        item.setText(text)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        return item

    def SimuLoad(self):
        if self.imported or self.created:
            try:
                self.TabSimuSunDivLineEd.setText(str(self.tempdata["general"]["sun_divisions"]))
                self.TabSimuSkyDivLineEd.setText(str(self.tempdata["general"]["sky_divisions"]))
                self.TabSimuVabLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["vmx"]["ab"]))
                self.TabSimuVadLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["vmx"]["ad"]))
                self.TabSimuVasLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["vmx"]["as"]))
                self.TabSimuVarLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["vmx"]["ar"]))
                self.TabSimuVaaLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["vmx"]["aa"]))
                self.TabSimuVlrLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["vmx"]["lr"]))
                self.TabSimuVstLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["vmx"]["st"]))
                self.TabSimuVsjLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["vmx"]["sj"]))
                self.TabSimuVlwLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["vmx"]["lw"]))
                self.TabSimuVdjLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["vmx"]["dj"]))
                self.TabSimuVdsLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["vmx"]["ds"]))
                self.TabSimuVdrLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["vmx"]["dr"]))
                self.TabSimuVdpLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["vmx"]["dp"]))
                self.TabSimuVdcLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["vmx"]["dc"]))
                self.TabSimuVdtLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["vmx"]["dt"]))
                self.TabSimuDabLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["dmx"]["ab"]))
                self.TabSimuDadLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["dmx"]["ad"]))
                self.TabSimuDasLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["dmx"]["as"]))
                self.TabSimuDarLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["dmx"]["ar"]))
                self.TabSimuDaaLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["dmx"]["aa"]))
                self.TabSimuDlrLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["dmx"]["lr"]))
                self.TabSimuDstLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["dmx"]["st"]))
                self.TabSimuDsjLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["dmx"]["sj"]))
                self.TabSimuDlwLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["dmx"]["lw"]))
                self.TabSimuDdjLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["dmx"]["dj"]))
                self.TabSimuDdsLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["dmx"]["ds"]))
                self.TabSimuDdrLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["dmx"]["dr"]))
                self.TabSimuDdpLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["dmx"]["dp"]))
                self.TabSimuDdcLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["dmx"]["dc"]))
                self.TabSimuDdtLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["dmx"]["dt"]))
            except:
                pass
            self.TabSimuDefabLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["default"]["ab"]))
            self.TabSimuDefadLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["default"]["ad"]))
            self.TabSimuDefasLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["default"]["as"]))
            self.TabSimuDefarLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["default"]["ar"]))
            self.TabSimuDefaaLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["default"]["aa"]))
            self.TabSimuDeflrLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["default"]["lr"]))
            self.TabSimuDefstLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["default"]["st"]))
            self.TabSimuDefsjLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["default"]["sj"]))
            self.TabSimuDeflwLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["default"]["lw"]))
            self.TabSimuDefdjLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["default"]["dj"]))
            self.TabSimuDefdsLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["default"]["ds"]))
            self.TabSimuDefdrLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["default"]["dr"]))
            self.TabSimuDefdpLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["default"]["dp"]))
            self.TabSimuDefdcLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["default"]["dc"]))
            self.TabSimuDefdtLineEd.setText(str(self.tempdata["general"]["radiance_parameters"]["default"]["dt"]))


    def simuWrite(self, object, case, mx, para, paratp):
        if self.imported or self.created:
            if case==0:
                self.tempdata["general"][para]=int(object.text())
            elif case==1:
                if paratp=="int":
                    self.tempdata["general"]["radiance_parameters"][mx][para]=int(object.text())
                if paratp=="float":
                    self.tempdata["general"]["radiance_parameters"][mx][para]=float(object.text())
            self.WriteToFile()

    def floatChk(self, object, *args):
        if self.imported or self.created:
            try:
                if len(args)==2:
                    if float(object.text())<=float(args[1]) and float(object.text())>=float(args[0]):

                        return 0
                    else:
                        QtGui.QMessageBox.warning(self, "Error","Error! Wrong Entry! Range Error!")
                        return 1
                elif len(args)==0:
                    float(object.text())
                    return 0
            except:
                QtGui.QMessageBox.warning(self, "Error", "Error! Wrong Entry!")
                return 1

    def intChk(self, object, *args):
        if self.imported or self.created:
            try:
                if len(args)==2:
                    if args[1] >= int(object.text()) >= args[0]:
                        return 0
                    else:
                        QtGui.QMessageBox.warning(self, "Error!", "Wrong Entry! Range Error!")
                        return 1
                elif len(args)==0:
                    test=int(object.text())
                    return 0
            except:

                QtGui.QMessageBox.warning(self, "Error", "Error! Wrong Entry!")
                return 1


    ##Checking Missing Info
    def finalCheck(self):
        if self.imported or self.created:
            self.missing="Missing Data: \n"
            self.missing1=""
            try:
                junk=self.tempdata["general"]["illum_units"]
            except:
                self.missing= self.missing +"Lighting Units; \n"
            try:
                junk=self.tempdata["general"]["import_units"]
            except:
                self.missing= self.missing + "Import Units; \n"
            try:
                junk=self.tempdata["general"]["display_units"]
            except:
                self.missing=self.missing+"Display Units; \n"
            try:
                junk=self.tempdata["general"]["epw_file"]
            except:
                self.missing=self.missing+"Weather File; \n"
            try:
                p1=self.dir+"data/"+self.tempdata["general"]["epw_file"]
            except:
                self.missing=self.missing+"Spaces; \n"



            for i in range(len(self.tempdata["spaces"])):
                try:
                    mname=self.tempdata["spaces"][i]["space_name"]
                except:
                    self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+"--> Space Name; \n"
                try:
                    junk=self.tempdata["spaces"][i]["lighting_schedule"]
                except:
                    self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+"--> Lighting Schedule; \n"
                try:
                    junk=self.tempdata["spaces"][i]["geometry_file"]
                except:
                    self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+"--> Geometry File; \n"
                try:
                    fname=os.path.join(self.dir, self.tempdata["spaces"][i]["geometry_directory"], \
                                           self.tempdata["spaces"][i]["material_file"])
                    if not os.path.exists(fname):
                        self.tempdata["spaces"][i]["material_file"]="empty.rad"
                        fname=os.path.join(self.dir, self.tempdata["spaces"][i]["geometry_directory"], \
                                           self.tempdata["spaces"][i]["material_file"])
                        if not os.path.exists(fname):
                            radf=open(fname,"w")
                            radf.close()
                        #     QtGui.QMessageBox.warning(self,"warning", "No existed material rad file found in space: %s directory, empty.rad is created!" %mname)
                        # else:
                        #     QtGui.QMessageBox.warning(self,"warning", "No existed material rad file found in space: %s directory, empty.rad is used!" %mname)
                except:
                    self.tempdata["spaces"][i]["material_file"]="empty.rad"
                    fname=self.dir+"rad/"+"/empty.rad"
                    fp=self.dir+"rad/"
                    if not os.stat(str(fp)):
                        os.mkdir(fp)
                    if not os.path.exists(fname):
                        radf=open(fname,"w")
                        radf.close()
                    #     QtGui.QMessageBox.warning(self,"warning", "No existed material rad file found in space: %s directory, empty.rad is created!" %mname)
                    # else:
                    #     QtGui.QMessageBox.warning(self,"warning", "No existed material rad file found in space: %s directory, empty.rad is used!" %mname)
                try:
                    junk=self.tempdata["spaces"][i]["analysis_points"]
                except:
                    try:
                        self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+"--> Analysis Grid Points; \n"
                    except:
                        self.missing=self.missing+"--> Analysis Grid Points; \n"


                try:
                    if not os.path.exists(str(self.tempdata["general"]["project_directory"]+self.tempdata["spaces"][i]["input_directory"]+ \
                                                  self.tempdata["spaces"][i]["analysis_points"]["files"][0])):
                        listp=["x_spacing", "y_spacing", "offset", "z_offset", "modifier"]
                        for item in listp:
                            try:
                                junk=self.tempdata["spaces"][i]["analysis_points"][item]
                            except:
                                self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+"--> Analysis Grid Points "+item+"; \n"
                except:
                    pass
                try:
                    junk=self.tempdata["spaces"][i]["window_groups"]
                except:
                    self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+"--> Window Groups; \n"
                    try:
                        del self.tempdata["spaces"][i]["sDA"]
                    except:
                        pass

                try:
                    for j in range(len(self.tempdata["spaces"][i]["window_groups"])):
                        try:
                            junk=self.tempdata["spaces"][i]["window_groups"][j]["name"]
                        except:
                            self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+"--> Window Group Name; \n"
                            try:
                                del self.tempdata["spaces"][i]["sDA"]
                            except:
                                pass
                        try:
                            junk=self.tempdata["spaces"][i]["window_groups"][j]["glazing_materials"]
                        except:
                            self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+ " Window Group: "+ \
                                         self.tempdata["spaces"][i]["window_groups"][j]["name"]+"--> Glazing Materials; \n"

                        try:
                            nshade=len(self.tempdata["spaces"][i]["window_groups"][j]["shade_settings"])
                        except:
                            self.missing1=self.missing1+"Space: "+self.tempdata["spaces"][i]["space_name"]+ " Window Group: "+ \
                                         self.tempdata["spaces"][i]["window_groups"][j]["name"]+"--> Shade; \n"
                        try:
                           junk=self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]
                        except:
                           self.missing1=self.missing1+"Space: "+self.tempdata["spaces"][i]["space_name"]+ " Window Group: "+ \
                                         self.tempdata["spaces"][i]["window_groups"][j]["name"]+"--> Shade Control Info; \n"
                        try:
                            if self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]["method"]=="automated_profile_angle":
                                try:
                                    junk=self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]["elevation_azimuth"]
                                except:
                                    self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+ " Window Group: "+ \
                                         self.tempdata["spaces"][i]["window_groups"][j]["name"]+"--> Elevation Azimuth; \n"
                                try:
                                    for k in range(nshade):
                                        junk=self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]["angle_settings"][k]
                                except:
                                    self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+ " Window Group: "+ \
                                         self.tempdata["spaces"][i]["window_groups"][j]["name"]+"--> Angle Settings; \n"
                            elif self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]["method"]=="automated_signal":
                                try:
                                    junk=self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]["sensor"]
                                except:
                                    self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+ " Window Group: "+ \
                                         self.tempdata["spaces"][i]["window_groups"][j]["name"]+"--> Sensor Settings; \n"
                                try:
                                    self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]["sensor"]["sensor_type"]
                                except:
                                    self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+ " Window Group: "+ \
                                         self.tempdata["spaces"][i]["window_groups"][j]["name"]+"--> Sensor Type; \n"
                                try:
                                    self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]["sensor"]["sensor_file"]
                                except:
                                    self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+ " Window Group: "+ \
                                         self.tempdata["spaces"][i]["window_groups"][j]["name"]+"--> Sensor File; \n"
                                try:
                                    self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]["sensor"]["location"]
                                except:
                                    self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+ " Window Group: "+ \
                                         self.tempdata["spaces"][i]["window_groups"][j]["name"]+"--> Sensor Location; \n"
                                listp=["x", "y", "z", "xd", "yd", "zd", "spin_ccw"]
                                for item in listp:
                                    try:
                                        self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]["sensor"]["location"][item]
                                    except:
                                        self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+ " Window Group: "+ \
                                         self.tempdata["spaces"][i]["window_groups"][j]["name"]+" Sensor Location--> "+item+"; \n"
                                try:
                                    for k in range(nshade):
                                        junk=self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]["signal_settings"][k]
                                except:
                                    self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+ " Window Group: "+ \
                                         self.tempdata["spaces"][i]["window_groups"][j]["name"]+"--> Signal Settings; \n"
                            elif self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]["method"]=="automated_profile_angle_signal":
                                try:
                                    junk=self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]["elevation_azimuth"]
                                except:
                                    self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+ " Window Group: "+ \
                                         self.tempdata["spaces"][i]["window_groups"][j]["name"]+"--> Elevation Azimuth; \n"
                                try:
                                    for k in range(nshade):
                                        junk=self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]["angle_settings"][k]
                                except:
                                    self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+ " Window Group: "+ \
                                         self.tempdata["spaces"][i]["window_groups"][j]["name"]+"--> Angle Settings; \n"
                                try:
                                    junk=self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]["sensor"]
                                except:
                                    self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+ " Window Group: "+ \
                                         self.tempdata["spaces"][i]["window_groups"][j]["name"]+"--> Sensor Settings; \n"
                                try:
                                    self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]["sensor"]["sensor_type"]
                                except:
                                    self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+ " Window Group: "+ \
                                         self.tempdata["spaces"][i]["window_groups"][j]["name"]+"--> Sensor Type; \n"
                                try:
                                    self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]["sensor"]["sensor_file"]
                                except:
                                    self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+ " Window Group: "+ \
                                         self.tempdata["spaces"][i]["window_groups"][j]["name"]+"--> Sensor File; \n"
                                try:
                                    self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]["sensor"]["location"]
                                except:
                                    self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+ " Window Group: "+ \
                                         self.tempdata["spaces"][i]["window_groups"][j]["name"]+"--> Sensor Location; \n"
                                listp=["x", "y", "z", "xd", "yd", "zd", "spin_ccw"]
                                for item in listp:
                                    try:
                                        self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]["sensor"]["location"][item]
                                    except:
                                        self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+ " Window Group: "+ \
                                         self.tempdata["spaces"][i]["window_groups"][j]["name"]+" Sensor Location--> "+item+"; \n"
                                try:
                                    for k in range(nshade):
                                        junk=self.tempdata["spaces"][i]["window_groups"][j]["shade_control"]["signal_settings"][k]
                                except:
                                    self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+ " Window Group: "+ \
                                         self.tempdata["spaces"][i]["window_groups"][j]["name"]+"--> Signal Settings; \n"
                        except:
                            pass
                except:
                    self.missing=self.missing+"Space: "+self.tempdata["spaces"][i]["space_name"]+ "--> Window Group Info; \n"

            if self.missing!="Missing Data: \n":
                QtGui.QMessageBox.warning(self,"Missing Information", self.missing+self.missing1)

            for i in range(len(self.tempdata["spaces"])):
                mname=self.tempdata["spaces"][i]["space_name"]
                try:
                    for j in range(len(self.tempdata["spaces"][i]["window_groups"])):
                        if self.tempdata["spaces"][i]["window_groups"][j]["base_geometry"]=="empty.rad":
                            wgn=self.tempdata["spaces"][i]["window_groups"][j]["name"]
                            fname=self.dir+"rad/"+"/empty.rad"
                            fp=self.dir+"rad/"
                            if not os.stat(str(fp)):
                                os.mkdir(fp)
                            if not os.path.exists(fname):
                                radf=open(fname,"w")
                                radf.close()
                except:
                    try:
                        del self.tempdata["sDA"]
                        self.WriteToFile()
                    except:
                        pass
                        #     QtGui.QMessageBox.warning(self,"warning", "No existed window geometry rad file found in space: %s window group: %s, empty.rad is created!" %(mname,wgn) )
                        # else:
                        #     QtGui.QMessageBox.warning(self,"warning", "No existed window geometry rad file found in space: %s window group: %s, empty.rad is used!" %(mname, wgn))
            self.WriteToFile()




    def simurun(self):
        if self.imported or self.created:
            self.finalCheck()
            if self.missing=="Missing Data: \n":
                try:
                    junk=self.tempdata["general"]["target_illuminance"]
                except:
                    if self.tempdata["general"]["illum_units"]=="lux":
                        self.tempdata["general"]["target_illuminance"]=300
                    else:
                        self.tempdata["general"]["target_illuminance"]=30

                p1=self.dir+"data/"+self.tempdata["general"]["epw_file"]
                p2=os.path.dirname(str(self.JFileName))
                try:
                    base=os.path.basename(str(p1))
                    fopath=os.path.dirname(str(p1))
                    fnew=os.path.normpath(os.path.join(p2,base))
                    shutil.copy2(p1, fnew)
                except:
                    pass

                for i in range(len (self.tempdata["spaces"])):
                    self.tempdata["spaces"][i]["space_directory"]=self.tempdata["general"]["project_directory"]
                    try:
                        junk=self.tempdata["spaces"][i]["occupancy_schedule"]
                    except:
                        self.tempdata["spaces"][i]["occupancy_schedule"]=self.tempdata["spaces"][i]["lighting_schedule"]
                    try:
                        junk=self.tempdata["spaces"][i]["target_illuminance"]
                    except:
                        if self.tempdata["general"]["illum_units"]=="lux":
                            self.tempdata["spaces"][i]["target_illuminance"]=300
                        else:
                            self.tempdata["spaces"][i]["target_illuminance"]=30
                    try:
                        for j in range(len(self.tempdata["spaces"][i]["control_zones"])):
                            try:
                                junk=self.tempdata["spaces"][i]["control_zones"][j]["cp_method"]
                                junk=self.tempdata["spaces"][i]["control_zones"][j]["quantity"]
                                junk=self.tempdata["spaces"][i]["control_zones"][j]["excluded_points"]
                                junk=self.tempdata["spaces"][i]["control_zones"][j]["target_percentage"]

                            except:
                                self.tempdata["spaces"][i]["control_zones"][j]["cp_method"]="auto"
                                self.tempdata["spaces"][i]["control_zones"][j]["quantity"]=2
                                self.tempdata["spaces"][i]["control_zones"][j]["excluded_points"]="null"
                                self.tempdata["spaces"][i]["control_zones"][j]["target_percentage"]=0

                            try:
                                junk=self.tempdata["spaces"][i]["control_zones"][j]["sensor"]["sensor_type"]
                            except:
                                try:
                                    del self.tempdata["spaces"][i]["control_zones"][j]["sensor"]
                                except:
                                    pass
                    except:
                        pass
                    try:
                        p1=self.dir+self.tempdata["spaces"][i]["input_directory"]+self.tempdata["spaces"][i]["lighting_schedule"]
                        base=os.path.basename(str(p1))
                        fopath=os.path.dirname(str(p1))
                        fnew=os.path.normpath(os.path.join(p2,base))
                        shutil.copy2(p1, fnew)
                    except:
                        pass
                self.WriteToFile()
                self.SaveAll()

                os.chdir("%s" %self.tempdata["general"]["project_directory"])
                parbat=open("var.bat", "w")
                if self.TabSimuCbx.isChecked():
                    parbat.write("set PATH=./;c:/radiance/bin.\nset RAYPATH=./;c:/radiance/lib.\n")
                parbat.write('dxdaylight %s > out.txt\n' %self.JFileName)
                path=os.path.normpath(self.tempdata["general"]["project_directory"])
                parbat.write("copy %s\\res\\intermediateData\\*.sig %s\\res\\*.sig\n" %(path, path))

                # try:
                #     for j in range(len(self.tempdata["spaces"][0]["window_groups"])):
                #         try:
                #             for k in range(len(self.tempdata["spaces"][0]["window_groups"][j]["shade_settings"])):
                #                 n1=os.path.normpath(os.path.join(self.tempdata["general"]["project_directory"],self.tempdata["spaces"][0]["results_directory"]))+"\\"+ \
                #                    self.tempdata["spaces"][0]["space_name"]+"_"+self.tempdata["spaces"][0]["window_groups"][j]["name"]+ \
                #                     "_set"+str(k+1)+".ill"
                #
                #                 n2=os.path.normpath(os.path.join(self.tempdata["general"]["project_directory"],self.tempdata["spaces"][0]["results_directory"]))+"\\"+ \
                #                    self.tempdata["spaces"][0]["space_name"]+"_"+self.tempdata["spaces"][0]["window_groups"][j]["name"]+ \
                #                     "_set"+str(k)+".ill"
                #                 n3=os.path.normpath(os.path.join(self.tempdata["general"]["project_directory"],self.tempdata["spaces"][0]["results_directory"]))+"\\"+ \
                #                    self.tempdata["spaces"][0]["space_name"]+"_"+self.tempdata["spaces"][0]["window_groups"][j]["name"]+ \
                #                     "_set"+str(k+1)+"_direct.ill"
                #                 n4=os.path.normpath(os.path.join(self.tempdata["general"]["project_directory"],self.tempdata["spaces"][0]["results_directory"]))+"\\"+ \
                #                    self.tempdata["spaces"][0]["space_name"]+"_"+self.tempdata["spaces"][0]["window_groups"][j]["name"]+ \
                #                     "_set"+str(k)+"_direct.ill"
                #                 #parbat.write("##copy %s %s\n" %(n1,n2))
                #                 #parbat.write("##copy %s %s\n" %(n3,n4))
                #                 #parbat.write("##del %s\n" %(n1))
                #                 #parbat.write("##del %s \n" %(n3))
                #         except:
                #             pass
                # except:
                #     pass
                mark=0
                stempfix=copy.deepcopy(self.tempdata)
                try:
                    for i in range(len (self.tempdata["spaces"])):
                        for j in range(len(self.tempdata["spaces"][i]["window_groups"])):
                            # pass
                            try:
                                junk=self.tempdata["spaces"][i]["window_groups"][j]["shade_settings"]
                            except:
                                stempfix["spaces"][i]["window_groups"][j]["shade_settings"]=[]
                                stempfix["spaces"][i]["window_groups"][j]["shade_settings"].append("Null")
                                mark=1
                    parbat.write('dxprocessshade %s\n' %self.JFileName)
                    if mark==1:
                        self.Nstempfix=self.JFileName[:-5]+"_temp.json"
                        # print Nstempfix
                        fs=open(self.Nstempfix, "w")
                        tpall=json.dumps(stempfix,indent=4)
                        fs.write(tpall)
                        fs.close()
                except:
                    pass
                junk=1
                j=0
                a=0
                countlinear=[]
                junkmiss=[]
                try:
                    for i in range(len (self.tempdata["spaces"])):
                        countlinear.append(0)
                        try:
                            for k in range(len(self.tempdata["spaces"][i]["control_zones"])):
                                try:
                                    j=self.tempdata["spaces"][i]["control_zones"][k]["name"]
                                    if j=="" or j==" ":
                                        junk=0
                                        junkmiss.append(("Space: "+ self.tempdata["spaces"][i]["space_name"])+("--> Zone Name"))
                                except:
                                    junk=0
                                    junkmiss.append(("Space: "+ self.tempdata["spaces"][i]["space_name"])+("--> Zone Name"))
                                try:
                                    j=self.tempdata["spaces"][i]["control_zones"][k]["luminaire_information"]["ies_file"]
                                except:
                                    junk=0
                                    if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                        junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> IES files"))
                                    else:
                                        junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> IES files"))
                                try:
                                    j=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["ballast_type"]
                                    if j=="non_dimming" or "linear_dimming":
                                        try:
                                            a=self.tempdata["spaces"][i]["control_zones"][k]["luminaire_information"]["lamp_lumens"]
                                        except:
                                            junk=0
                                            if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                               junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> lamp lumens"))
                                            else:
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> lamp lumens"))
                                        try:
                                            a=self.tempdata["spaces"][i]["control_zones"][k]["luminaire_information"]["LLF"]
                                        except:
                                            junk=0
                                            if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> LLF"))
                                            else:
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> LLF"))
                                        try:
                                            a=self.tempdata["spaces"][i]["control_zones"][k]["luminaire_layout"][0]["x"]
                                        except:
                                            junk=0
                                            if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> Luminaire Information"))
                                            else:
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> Luminaire Information"))
                                        if j=="non_dimming":
                                            try:
                                                a=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["watts"]
                                            except:
                                                junk=0
                                                if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                                    junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> Power"))
                                                else:
                                                    junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> Power"))
                                            try:
                                                a=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["ballast_factor"]
                                            except:
                                                junk=0
                                                if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                                    junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> Ballast Factor"))
                                                else:
                                                    junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> Ballast Factor"))
                                        else:
                                            countlinear[i]=countlinear[i]+1
                                            try:
                                                a=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["watts_min"]
                                            except:
                                                junk=0
                                                if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                                    junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> Minimum Power"))
                                                else:
                                                    junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> Minimum Power"))
                                            try:
                                                a=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["watts_max"]
                                            except:
                                                junk=0
                                                if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                                    junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> Maximum Power"))
                                                else:
                                                    junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> Maximum Power"))
                                            try:
                                                a=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["bf_min"]
                                            except:
                                                junk=0
                                                if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                                    junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> Minimum Ballast Factor"))
                                                else:
                                                    junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> Minimum Ballast Factor"))
                                            try:
                                                a=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["bf_max"]
                                            except:
                                                junk=0
                                                if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                                    junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> Maximum Ballast Factor"))
                                                else:
                                                    junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d"%k+"--> Maximum Ballast Factor"))
                                    else:
                                        try:
                                            a=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["minimum_input_power_fraction"]
                                        except:
                                            junk=0
                                            if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> EPlus Minimum Input Power Fraction."))
                                            else:
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> EPlus Minimum Input Power Fraction."))
                                        try:
                                            a=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["minimum_light_output_fraction"]
                                        except:
                                            junk=0
                                            if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> EPlus Minimum Light Output Fraction"))
                                            else:
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> EPlus Minimum Light Output Fraction"))
                                        try:
                                            a=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["LPD"]
                                        except:
                                            junk=0
                                            if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> EPlus LPD"))
                                            else:
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %d" %k+"--> EPlus LPD"))
                                    # junk=1
                                except:
                                    junk=0
                                    if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                        junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> Ballast_type"))
                                    else:
                                        junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> Ballast Type"))
                        except:
                            pass
                    m1=1
                    for i in range(len(countlinear)):
                        if countlinear[i]>1:
                            junk=0
                            m1=0
                    if m1==0:
                        QtGui.QMessageBox.warning(self, "Warning", "No more than one linear dimming zone is allowed!")
                        self.StadicTab.setCurrentIndex(5)
                    # print junk, j,a, countlinear, ((j!=0 or a!=0) and countlinear<2)
                    if junk!=0 and j!=0:
                        parbat.write('dxelectric %s\n' %self.JFileName)
                    elif ((j!=0 or a!=0) and m1==1):
                        missing=""
                        for item in junkmiss:
                            missing=missing+item+"\n"
                        QtGui.QMessageBox.warning(self, "Warning", "Electric lighting information not complete!\nMissing: \n%s" %missing)
                        self.StadicTab.setCurrentIndex(5)
                except:
                    pass
                try:
                    for i in range(len (self.tempdata["spaces"])):
                        n1=os.path.normpath(os.path.join(self.tempdata["general"]["project_directory"],self.tempdata["spaces"][i]["results_directory"]))+"\\"+ \
                           self.tempdata["spaces"][i]["space_name"]+"_final.ill"
                        n2=os.path.normpath(os.path.join(self.tempdata["general"]["project_directory"],self.tempdata["spaces"][i]["results_directory"]))+"\\"+ \
                            self.tempdata["spaces"][i]["space_name"]+".ill"
                        parbat.write("copy %s %s\n" %(n1,n2))
                    parbat.write('dxmetrics %s\n' %self.JFileName)
                except:
                    pass
                parbat.close()
                if junk!=0 and m1==1 and j!=0:
                    prg=Status("var.bat")
                    prg.show()
                   # os.system("var.bat")
                    prg.exec_()
                else:
                    m2=1
                    for i in range(len(countlinear)):
                        if countlinear[i]!=0:
                            m2=0
                    if j==0 and m2==1:
                        prg=Status("var.bat")
                        prg.show()
                       # os.system("var.bat")
                        prg.exec_()


                self.imported=True
                self.wgcalc=[]
                self.sdcalc=[]
                try:
                    lenS=len(self.tempdata["spaces"])
                    for i in range(lenS):
                        lenWG=len(self.tempdata["spaces"][i]["window_groups"])
                        temp=[]
                        temp1=[]
                        for j in range(lenWG):
                            p1=os.path.normpath(self.tempdata["general"]["project_directory"]+self.tempdata["spaces"][i]["results_directory"]+ \
                                                str(self.tempdata["spaces"][i]["space_name"])+"_"+str(self.tempdata["spaces"][i]["window_groups"][j]["name"])+ "_base.ill")
                            p2=os.path.normpath(self.tempdata["general"]["project_directory"]+self.tempdata["spaces"][i]["results_directory"]+ \
                                                str(self.tempdata["spaces"][i]["space_name"])+"_"+str(self.tempdata["spaces"][i]["window_groups"][j]["name"])+ "_base_direct.ill")
                            if os.path.exists(p1) and os.path.exists(p2):
                                temp.append(False)
                            else:
                                temp.append(True)
                            try:
                                lenSd=len(self.tempdata["spaces"][i]["window_groups"][j]["shade_settings"])
                                tp=[]
                                for k in range(lenSd):
                                    p1=os.path.normpath(self.tempdata["general"]["project_directory"]+self.tempdata["spaces"][i]["results_directory"]+str(self.tempdata["spaces"][i]["space_name"])+"_"+ \
                                       str(self.tempdata["spaces"][i]["window_groups"][j]["name"])+"_set"+str(k+1)+".ill")
                                    p2=os.path.normpath(self.tempdata["general"]["project_directory"]+self.tempdata["spaces"][i]["results_directory"]+str(self.tempdata["spaces"][i]["space_name"])+"_"+ \
                                       str(self.tempdata["spaces"][i]["window_groups"][j]["name"])+"_set"+str(k+1)+"_direct.ill")
                                    if os.path.exists(p1) and os.path.exists(p2):
                                        tp.append(False)
                                    else:
                                        tp.append(True)
                                temp1.append(tp)
                            except:
                                p1=os.path.normpath(str(self.tempdata["spaces"][i]["space_name"])+"_"+str(self.tempdata["spaces"][i]["window_groups"][j]["name"])+ "_set0.ill")
                                p2=os.path.normpath(str(self.tempdata["spaces"][i]["space_name"])+"_"+str(self.tempdata["spaces"][i]["window_groups"][j]["name"])+ "_set0_direct.ill")
                                if os.path.exists(p1) and os.path.exists(p2):
                                    temp1.append(False)
                                else:
                                    temp1.append(True)
                        self.wgcalc.append(temp)
                        self.sdcalc.append(temp1)
                except:
                    pass



    def PShade(self):
        try:
            mark=0
            # print "1", self.sdcalc
            for i in range(len(self.tempdata["spaces"])):
                for j in range(len(self.tempdata["spaces"][i]["window_groups"])):
                    for k in range(len(self.tempdata["spaces"][i]["window_groups"][j]["shade_settings"])):
                        prob=1
                        if self.sdcalc[i][j][k]==False:
                            pass
                        else:
                            mark=1

            for i in range(len(self.tempdata["spaces"])):
                for j in range(len(self.tempdata["spaces"][i]["window_groups"])):
                    if self.wgcalc[i][j]==False:
                        pass
                    else:
                        mark=1
            # print "2"
            self.SaveAll()
            if mark==0 and prob==1:
                os.chdir("%s" %self.tempdata["general"]["project_directory"])
                pdir=self.dir+"pshadeexcu.bat"

                pshadef=open(pdir,"w")
                path=os.path.normpath(self.tempdata["general"]["project_directory"])
                pshadef.write("copy %s\\res\\intermediateData\\*.sig %s\\res\\*.sig\n" %(path, path))
                if self.TabSimuCbx.isChecked():
                    pshadef.write("set PATH=./;c:/radiance/bin.\nset RAYPATH=./;c:/radiance/lib.\n")
                pshadef.write('dxprocessshade %s > out.txt\n' %self.JFileName)
                pshadef.write('dxmetrics %s\n' %self.JFileName)
                pshadef.close()
                # print "t"
                prg=Status("pshadeexcu.bat")
                prg.show()
                prg.exec_()
                # print "3"
            else:
                # print "4"
                QtGui.QMessageBox.warning(self, "Warning", "Information for processing shading is not enough. Try recalc DXDAYLIGHT again.")
        except:
            # print "5"
            QtGui.QMessageBox.warning(self, "Warning", "Information for processing shading is not enough. Try recalc DXDAYLIGHT again.")

    def PMtr(self):
        try:
            mark=0
            # print "1", self.sdcalc
            for i in range(len(self.tempdata["spaces"])):
                for j in range(len(self.tempdata["spaces"][i]["window_groups"])):
                    for k in range(len(self.tempdata["spaces"][i]["window_groups"][j]["shade_settings"])):
                        prob=1
                        if self.sdcalc[i][j][k]==False:
                            pass
                        else:
                            mark=1

            for i in range(len(self.tempdata["spaces"])):
                for j in range(len(self.tempdata["spaces"][i]["window_groups"])):
                    if self.wgcalc[i][j]==False:
                        pass
                    else:
                        mark=1
            # print "2"
            illck=0
            self.SaveAll()
            for i in range(len (self.tempdata["spaces"])):
                n1=os.path.normpath(os.path.join(self.tempdata["general"]["project_directory"],self.tempdata["spaces"][i]["results_directory"]))+"\\"+ \
                   self.tempdata["spaces"][i]["space_name"]+"_final.ill"
                if not os.path.exists(n1):
                    illck=1

            if mark==0 and prob==1:
                os.chdir("%s" %self.tempdata["general"]["project_directory"])
                pdir=self.dir+"pmtrexcu.bat"
                pmtrf=open(pdir,"w")
                for i in range(len (self.tempdata["spaces"])):
                    n1=os.path.normpath(os.path.join(self.tempdata["general"]["project_directory"],self.tempdata["spaces"][i]["results_directory"]))+"\\"+ \
                       self.tempdata["spaces"][i]["space_name"]+"_final.ill"
                    n2=os.path.normpath(os.path.join(self.tempdata["general"]["project_directory"],self.tempdata["spaces"][i]["results_directory"]))+"\\"+ \
                        self.tempdata["spaces"][i]["space_name"]+".ill"
                    pmtrf.write("copy %s %s\n" %(n1,n2))
                if self.TabSimuCbx.isChecked():
                    pmtrf.write("set PATH=./;c:/radiance/bin.\nset RAYPATH=./;c:/radiance/lib.\n")
                pmtrf.write('dxmetrics %s > out.txt\n' %self.JFileName)
                pmtrf.close()
                prg=Status("pmtrexcu.bat")
                prg.show()
               # os.system("var.bat")
                prg.exec_()
                # os.system(str(pdir))
                # print "3"
            else:
                # print "4"
                QtGui.QMessageBox.warning(self, "Warning", "Information for processing metrics is not enough. Try recalc DXDAYLIGHT and DXPROCESSSHADE again.")
        except:
            QtGui.QMessageBox.warning(self, "Warning", "Information for processing metrics is not enough. Try recalc DXDAYLIGHT and DXPROCESSSHADE again.")

    def PElec(self):
        if self.imported or self.created:
            self.finalCheck()
            if self.missing=="Missing Data: \n":
                try:
                    junk=self.tempdata["general"]["target_illuminance"]
                except:
                    if self.tempdata["general"]["illum_units"]=="lux":
                        self.tempdata["general"]["target_illuminance"]=300
                    else:
                        self.tempdata["general"]["target_illuminance"]=30

                p1=self.dir+"data/"+self.tempdata["general"]["epw_file"]
                p2=os.path.dirname(str(self.JFileName))
                try:
                    base=os.path.basename(str(p1))
                    fopath=os.path.dirname(str(p1))
                    fnew=os.path.normpath(os.path.join(p2,base))
                    shutil.copy2(p1, fnew)
                except:
                    pass

                #to be deleted
                for i in range(len (self.tempdata["spaces"])):
                    self.tempdata["spaces"][i]["space_directory"]=self.tempdata["general"]["project_directory"]
                    try:
                        junk=self.tempdata["spaces"][i]["occupancy_schedule"]
                    except:
                        self.tempdata["spaces"][i]["occupancy_schedule"]=self.tempdata["spaces"][i]["lighting_schedule"]
                    try:
                        junk=self.tempdata["spaces"][i]["target_illuminance"]
                    except:
                        if self.tempdata["general"]["illum_units"]=="lux":
                            self.tempdata["spaces"][i]["target_illuminance"]=300
                        else:
                            self.tempdata["spaces"][i]["target_illuminance"]=30
                    try:
                        for j in range(len(self.tempdata["spaces"][i]["control_zones"])):
                            try:
                                junk=self.tempdata["spaces"][i]["control_zones"][j]["cp_method"]
                                junk=self.tempdata["spaces"][i]["control_zones"][j]["quantity"]
                                junk=self.tempdata["spaces"][i]["control_zones"][j]["excluded_points"]
                                junk=self.tempdata["spaces"][i]["control_zones"][j]["target_percentage"]

                            except:
                                self.tempdata["spaces"][i]["control_zones"][j]["cp_method"]="auto"
                                self.tempdata["spaces"][i]["control_zones"][j]["quantity"]=2
                                self.tempdata["spaces"][i]["control_zones"][j]["excluded_points"]="null"
                                self.tempdata["spaces"][i]["control_zones"][j]["target_percentage"]=0

                            try:
                                junk=self.tempdata["spaces"][i]["control_zones"][j]["sensor"]["sensor_type"]
                            except:
                                try:
                                    del self.tempdata["spaces"][i]["control_zones"][j]["sensor"]
                                except:
                                    pass
                    except:
                        pass
                    try:
                        p1=self.dir+self.tempdata["spaces"][i]["input_directory"]+self.tempdata["spaces"][i]["lighting_schedule"]
                        base=os.path.basename(str(p1))
                        fopath=os.path.dirname(str(p1))
                        fnew=os.path.normpath(os.path.join(p2,base))
                        shutil.copy2(p1, fnew)
                    except:
                        pass


                self.WriteToFile()
                self.SaveAll()
            try:
                junk=1
                countlinear=[]
                j=0
                a=0
                junkmiss=[]
                for i in range(len (self.tempdata["spaces"])):
                    try:
                        countlinear.append(0)
                        for k in range(len(self.tempdata["spaces"][i]["control_zones"])):
                            try:
                                j=self.tempdata["spaces"][i]["control_zones"][k]["name"]
                                if j=="" or j==" ":
                                    junk=0
                                    junkmiss.append(("Space: "+ self.tempdata["spaces"][i]["space_name"])+("--> Zone Name\n"))
                            except:
                                junk=0
                                junkmiss.append(("Space: "+ self.tempdata["spaces"][i]["space_name"])+("--> Zone Name\n"))
                            try:
                                j=self.tempdata["spaces"][i]["control_zones"][k]["luminaire_information"]["ies_file"]
                            except:
                                junk=0
                                if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                    junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> IES files\n"))
                                else:
                                    junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> IES files\n"))
                            try:
                                j=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["ballast_type"]
                                if j=="non_dimming" or "linear_dimming":
                                    try:
                                        a=self.tempdata["spaces"][i]["control_zones"][k]["luminaire_information"]["lamp_lumens"]
                                    except:
                                        junk=0
                                        if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                           junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> lamp lumens\n"))
                                        else:
                                            junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> lamp lumens\n "))
                                    try:
                                        a=self.tempdata["spaces"][i]["control_zones"][k]["luminaire_information"]["LLF"]
                                    except:
                                        junk=0
                                        if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                            junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> LLF\n"))
                                        else:
                                            junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> LLF\n"))
                                    try:
                                        a=self.tempdata["spaces"][i]["control_zones"][k]["luminaire_layout"][0]["x"]
                                    except:
                                        junk=0
                                        if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                            junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> Luminaire Information\n"))
                                        else:
                                            junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> Luminaire Information\n"))
                                    if j=="non_dimming":
                                        try:
                                            a=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["watts"]
                                        except:
                                            junk=0
                                            if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> Power\n"))
                                            else:
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> Power\n"))
                                        try:
                                            a=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["ballast_factor"]
                                        except:
                                            junk=0
                                            if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> Ballast Factor\n"))
                                            else:
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> Ballast Factor\n"))
                                    else:
                                        countlinear[i]=countlinear[i]+1
                                        try:
                                            a=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["watts_min"]
                                        except:
                                            junk=0
                                            if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> Minimum Power\n"))
                                            else:
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> Minimum Power\n"))
                                        try:
                                            a=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["watts_max"]
                                        except:
                                            junk=0
                                            if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> Maximum Power\n"))
                                            else:
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> Maximum Power\n"))
                                        try:
                                            a=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["bf_min"]
                                        except:
                                            junk=0
                                            if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> Minimum Ballast Factor\n"))
                                            else:
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> Minimum Ballast Factor\n"))
                                        try:
                                            a=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["bf_max"]
                                        except:
                                            junk=0
                                            if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> Maximum Ballast Factor\n"))
                                            else:
                                                junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d"%k+"--> Maximum Ballast Factor\n"))
                                else:
                                    try:
                                        a=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["minimum_input_power_fraction"]
                                    except:
                                        junk=0
                                        if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                            junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> EPlus Minimum Input Power Fraction\n"))
                                        else:
                                            junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> EPlus Minimum Input Power Fraction.\n"))
                                    try:
                                        a=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["minimum_light_output_fraction"]
                                    except:
                                        junk=0
                                        if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                            junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> EPlus Minimum Light Output Fraction\n"))
                                        else:
                                            junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %k+"--> EPlus Minimum Light Output Fraction\n"))
                                    try:
                                        a=self.tempdata["spaces"][i]["control_zones"][k]["ballast_driver_information"]["LPD"]
                                    except:
                                        junk=0
                                        if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                            junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> EPlus LPD\n"))
                                        else:
                                            junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %d" %k+"--> EPlus LPD\n"))
                                # junk=1
                            except:
                                junk=0
                                if self.tempdata["spaces"][i]["control_zones"][k]["name"]!=" " and self.tempdata["spaces"][i]["control_zones"][k]["name"]!="":
                                    junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: %s" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> Ballast_type\n"))
                                else:
                                    junkmiss.append(("Space: %s" %self.tempdata["spaces"][i]["space_name"])+(" Zone: No.%d" %self.tempdata["spaces"][i]["control_zones"][k]["name"]+"--> Ballast Type\n"))
                    except:
                        pass
                m1=1
                for i in range(len(countlinear)):
                    if countlinear[i]>1:
                        junk=0
                        m1=0
                if m1==0:
                    QtGui.QMessageBox.warning(self, "Warning", "No more than one linear dimming zone is allowed!")
                    self.StadicTab.setCurrentIndex(5)

                if junk!=0 and j!=0:
                    os.chdir("%s" %self.tempdata["general"]["project_directory"])
                    pdir=self.dir+"pelec.bat"
                    pelectric=open(pdir,"w")
                    if self.TabSimuCbx.isChecked():
                        pelectric.write("set PATH=./;c:/radiance/bin.\nset RAYPATH=./;c:/radiance/lib.\n")
                    pelectric.write('dxelectric %s\n' %self.JFileName)
                    # print "t"
                    pelectric.close()
                    prg=Status("pelec.bat")
                    prg.show()
                   # os.system("var.bat")
                    prg.exec_()
                elif ((j!=0 or a!=0) and m1==1):
                    missing=""
                    for item in junkmiss:
                        missing=missing+item
                    QtGui.QMessageBox.warning(self, "Warning", "Electric lighting information not complete! \nMissing: \n%s" %missing)
                    self.StadicTab.setCurrentIndex(5)
            except:
                QtGui.QMessageBox.warning(self, "Warning", "Information for electric lighting calculation is not enough.Add Full luminaire information first.")

    def LaunchOutput(self):
        if self.imported or self.created:
            try:
                if len(self.tempdata["spaces"])>0:
                    index=self.OutputSPCbx2.currentIndex()
                    try:
                        pname=os.path.normpath(str(self.dir+"/"+self.tempdata["spaces"][index]["results_directory"]+"/"+ \
                                               self.tempdata["spaces"][index]["space_name"]+".ill"))
                        if os.path.exists(pname):
                            try:
                                pth=os.path.join(self.owd, "vis\stadicVis.exe")
                                for j in range(len(self.tempdata["spaces"][index]["window_groups"])):
                                    junk=self.tempdata["spaces"][index]["window_groups"][j]["shade_settings"]
                                    # print junk
                                # print "y"
                                subprocess.Popen('%s %s %d' %(pth,self.JFileName, index), shell=True)
                                # print "y1"
                            except:
                                try:
                                    pth=os.path.join(self.owd, "vis\stadicVis.exe")
                                    # print self.Nstempfix, pth
                                    subprocess.Popen('%s %s %d' %(pth,self.Nstempfix, index), shell=True)
                                except:
                                    QtGui.QMessageBox.warning(self, "Warning", "Temp fix required. Please click on the start full simulation button once to trigger! \
                                                                               No actual simulation required if previously processed.")
                            # os.system('%s %s %d' %(pth,self.JFileName, index))
                        else:
                            QtGui.QMessageBox.warning(self, "Warning!", "Not enough information!")
                    except:
                        QtGui.QMessageBox.warning(self, "Warning!", "ERROR!")
            except:
                pass

    def outputCalc(self, index, boollist, vallist):
        try:
            psda=self.tempdata["general"]["project_directory"]+self.tempdata["spaces"][index]["results_directory"]+ \
                 self.tempdata["spaces"][index]["space_name"]+"_sDA.res"
            # print psda
            if os.path.exists(str(psda)):
                boollist[0]=True
                val=open(psda).read()
                # print val
                vallist[0]=val
        except:
            pass
        try:
            posda=self.tempdata["general"]["project_directory"]+self.tempdata["spaces"][index]["results_directory"]+ \
                 self.tempdata["spaces"][index]["space_name"]+"_occupied_sDA.res"
            # print posda
            if os.path.exists(str(posda)):
                boollist[1]=True
                val=open(posda).read()
                # print val
                vallist[1]=val
        except:
            pass
        try:
            pASE=self.tempdata["general"]["project_directory"]+self.tempdata["spaces"][index]["results_directory"]+ \
                 self.tempdata["spaces"][index]["space_name"]+"_ASE.res"
            # print pASE
            if os.path.exists(str(pASE)):
                boollist[2]=True
                val=open(pASE).read()
                # print val
                vallist[2]=val
        except:
            pass
        try:
            pErg=self.tempdata["general"]["project_directory"]+self.tempdata["spaces"][index]["results_directory"]+ \
                 self.tempdata["spaces"][index]["space_name"]+"_Energy.res"
            # print pErg
            if os.path.exists(str(pErg)):
                boollist[3]=True
                val=open(pErg).read().split()
                # print val
                vallist[3]=val[0]
                vallist[4]=val[1]
        except:
            pass
        return boollist,vallist

    def MtrOutput(self):
        if self.imported or self.created:
            index=self.OutputSPCbx.currentIndex()
            boollist=[False,False,False,False]
            vallist=["NA","NA","NA","NA","NA"]
            self.outputCalc(index, boollist, vallist)
            mark=0
            for item in boollist:
                if item==True:
                    mark=1
            if mark==1:
                ovop=Overall(1, boollist,vallist, self.tempdata["spaces"][index]["space_name"])
                ovop.show()
                ovop.exec_()
            else:
                QtGui.QMessageBox.warning(self, "Warning", "Results file not found!")

    # def area(self,x):
    #     a=0
    #     j=0
    #     temp=x[0][0]
    #     array=[]
    #     tp=[]
    #     for i in range(0, len(x)):
    #         if x[i][0]==temp:
    #             tp.append([x[i][0],x[i][1]])
    #         else:
    #             array.append(tp)
    #             temp=x[i][0]
    #             tp=[]
    #             tp.append([x[i][0],x[i][1]])
    #     # print array
    #     array.append(tp)
    #     for i in range(0,len(array)-1):
    #         x1=array[i][0][0]
    #         x2=array[i][len(array[i])-1][0]
    #         x3=array[i+1][0][0]
    #         x4=array[i+1][len(array[i+1])-1][0]
    #         y1=array[i][0][1]
    #         y2=array[i][len(array[i])-1][1]
    #         y3=array[i+1][0][1]
    #         y4=array[i+1][len(array[i+1])-1][1]
    #         # print x1, x2, x3, x4, y1, y2, y3, y4
    #         # print 0.5*(abs(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2))+abs(x1*(y2-y4)+x2*(y4-y1)+x4*(y1-y2)))
    #         a=a+0.5*(abs(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2))+abs(x1*(y2-y4)+x2*(y4-y1)+x4*(y1-y2)))
    #     return a

    def PrjSmry(self):
        if self.imported or self.created:
            try:
                blist=[]
                vlist=[]
                prg=PBar()
                prg.show()
                for index in range(len (self.tempdata["spaces"])):
                    boollist=[False,False,False,False]
                    vallist=["NA","NA","NA","NA","NA"]
                    self.outputCalc(index, boollist, vallist)
                    blist.append(boollist)
                    vlist.append(vallist)

                bcheck=[True, True, True, True]
                v=["NA","NA","NA","NA","NA"]
                for j in range(4):
                    for index in range(len (self.tempdata["spaces"])):
                        bcheck[j]=bcheck[j]*blist[index][j]
                # print bcheck
                N=[]
                A=[]
                sumN=0
                sumA=0
                prg.update()
                for index in range(len (self.tempdata["spaces"])):
                    try:
                        ptspath=self.tempdata["general"]["project_directory"]+self.tempdata["spaces"][index]["input_directory"]+ \
                                self.tempdata["spaces"][index]["analysis_points"]["files"][0]
                        # print ptspath
                        f=open(ptspath)
                        count=0
                        x=[]
                        y=[]
                        corr=[]
                        for lines in f:
                            t=lines.split()
                            # corr.append([float(t[0]), float(t[1])])
                            x.append(float(t[0]))
                            y.append(float(t[1]))
                            count=count+1

                        xx=[item for item in set(x)]
                        # print xx
                        yy=[item for item in set(y)]
                        xsp=xx[1]-xx[0]
                        ysp=yy[1]-yy[0]
                        # print xsp, ysp
                            # x=float(t[0])
                            # y=float(t[1])
                            # if count==0:
                            #     xmin=float(t[0])
                            #     xmax=float(t[0])
                            #     ymax=float(t[1])
                            # else:
                            #     if float(t[0])>xmax:
                            #         xmax=float(t[0])
                            #     if float(t[0])<xmin:
                            #         xmin=float(t[0])
                            #     if float(t[1])>ymax:
                            #         ymax=float(t[1])
                            #     if float(t[1])<ymin:
                            #         ymin=float(t[1])
                            # count=count+1
                        aa=xsp*ysp*count
                    except:
                        pass
                    # print count, xmax, xmin, ymax, ymin
                    N.append(count)
                    sumN=sumN+N[index]
                    A.append(aa)
                    f.close()
                    sumA=sumA+A[index]
                    if len(N)<=2:
                        prg.update()
                if len(N)==1:
                    prg.update()
                prg.update()
                sDA=0
                mark1=0
                mark2=0
                # print sumA
                for index in range(len (self.tempdata["spaces"])):
                    if A[index]==0:
                        mark1=1
                    if N==0:
                        mark2=1
                if mark1==1:
                    sumA=sumN
                    A=N
                if mark2!=1:
                # print sumA
                    if bcheck[0]==True:
                        for index in range(len (self.tempdata["spaces"])):
                            sDA=float(vlist[index][0])*A[index]+sDA
                        v[0]=sDA/sumA

                    osDA=0
                    if bcheck[1]==True:
                        for index in range(len (self.tempdata["spaces"])):
                            osDA=float(vlist[index][1])*A[index]+osDA
                        v[1]=osDA/sumA

                    ASE=0
                    if bcheck[2]==True:
                        for index in range(len (self.tempdata["spaces"])):
                            ASE=float(vlist[index][2])*A[index]+ASE
                        v[2]=ASE/sumA

                    if bcheck[3]==True:
                        energy1=0
                        energy2=0
                        for index in range(len (self.tempdata["spaces"])):
                            energy1=energy1+float(vlist[index][3])
                            energy2=energy2+float(vlist[index][4])
                        v[3]=energy1
                        v[4]=energy2
                prg.update()
                # try:
                #     print vlist, blist
                #     print v, bcheck
                # except:
                #     pass
                mark=0
                for item in bcheck:
                    if item==True:
                        mark=1
                if mark==1:
                    ovop=Overall(0,bcheck,v, self.tempdata["spaces"][index]["space_name"])
                    ovop.show()
                    ovop.exec_()
                else:
                    QtGui.QMessageBox.warning(self, "Warning", "Results file not found!")
            except:
                QtGui.QMessageBox.warning(self, "Warning", "Calculation Error! Required Info not Complete!")

    def closeEvent(self, event):
        if self.imported or self.created:
            reply = QtGui.QMessageBox.question(self, "Save Changes?" ,
                         'Save?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No, QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Yes:
                self.finalCheck()
                self.SaveAll()
                self.tpfile.close()
                os.remove(str(self.tpfname))
                event.accept()
            elif reply == QtGui.QMessageBox.No:
                self.tpfile.close()
                os.remove(str(self.tpfname))
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()




##Start Simulation Dialog
class Status(QtGui.QDialog):
    def __init__(self, name):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.name=str(name)
        # self.setModal(1)
        if self.name=="var.bat":
            self.myLongTask = TaskThreadA()
        elif self.name=="pmtrexcu.bat":
            self.myLongTask = TaskThreadC()
        elif self.name=="pshadeexcu.bat":
            self.myLongTask = TaskThreadB()
        else:
            self.myLongTask = TaskThreadD()

        self.myLongTask.taskFinished.connect(self.onF)


    def setupUi(self, Status):
        self.resize(300, 50)
        self.setWindowTitle(_translate("Status", "Please Wait...", None))
        self.Combo = QtGui.QVBoxLayout()
        self.setLayout(self.Combo)
        self.lbl=QtGui.QLabel()
        self.lbl.setText("Wait")
        self.Combo.addWidget(self.lbl)
        self.status=QtGui.QProgressBar()
        self.Combo.addWidget(self.status)
        self.status.setValue(0)
        self.sbtn=QtGui.QPushButton()
        self.sbtn.setText("Start")
        self.Combo.addWidget(self.sbtn)
        self.sbtn.clicked.connect(self.start)

        self.cbtn=QtGui.QPushButton()
        self.cbtn.setText("Cancel")
        self.Combo.addWidget(self.cbtn)
        self.cbtn.clicked.connect(self.cancel)


    def cancel(self):
        self.myLongTask.terminate()
        self.accept()

    def start(self):
        self.status.setRange(0,0)
        self.myLongTask.start()



    def onF(self):
        self.status.setRange(0,100)
        self.status.setValue(100)
        self.setWindowTitle("Finished")
        self.sbtn.setText("Finished")
        self.sbtn.setDisabled(1)
        self.cbtn.setText("ok")


class TaskThreadA(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal(int)

    def run(self):
        # subprocess.call("var.bat", shell=True)
        # subprocess.Popen('var.bat')
        os.system("var.bat")
        self.taskFinished.emit(100)

class TaskThreadB(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal(int)

    def run(self):
        # subprocess.call('pshadeexcu.bat', shell=True)
        os.system("pshadeexcu.bat")
        self.taskFinished.emit(100)

class TaskThreadC(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal(int)

    def run(self):
        # subprocess.call('pmtrexcu.bat', shell=True)
        os.system("pmtrexcu.bat")
        self.taskFinished.emit(100)

class TaskThreadD(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal(int)

    def run(self):
        # subprocess.call('pelec.bat', shell=True)
        os.system("pelec.bat")
        self.taskFinished.emit(100)

##Material Layer Selection
class Ui_Combo(QtGui.QDialog):
    def __init__(self):
        # super(myWindow, self).__init__(parent)
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.setModal(1)

    def setupUi(self, Ui_Combo):
        self.resize(300, 100)
        self.setWindowTitle(_translate("Ui_Combo", "Material", None))
        self.Combo = QtGui.QVBoxLayout()
        self.setLayout(self.Combo)
        self.cbox = QtGui.QComboBox()
        self.Combo.addWidget(self.cbox)
        self.cbtn=QtGui.QPushButton()
        self.cbtn.setText("Add")
        self.Combo.addWidget(self.cbtn)
        self.cbtn.clicked.connect(self.PtsMatAddBtn)
        self.cancelbtn=QtGui.QPushButton()
        self.cancelbtn.setText("Cancel")
        self.Combo.addWidget(self.cancelbtn)
        self.cancelbtn.clicked.connect(self.cancel)

    def PtsMatAddBtn(self):
        index=self.cbox.currentIndex()
        self.mat=self.cbox.itemText(index)
        self.accept()

    def cancel(self):
        self.accept()



#Luminaire Duplication
class DupUi_Combo(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.setModal(1)

    def setupUi(self, DupUi_Combo):

        self.resize(400, 200)
        self.setWindowTitle("Zone Duplication From:")
        self.Combo = QtGui.QVBoxLayout()
        self.setLayout(self.Combo)
        self.splbl=QtGui.QLabel()
        self.splbl.setText("Space Name:")
        self.Combo.addWidget(self.splbl)
        self.cboxsp = QtGui.QComboBox()
        self.cboxsp.currentIndexChanged.connect(self.sptoz)
        self.Combo.addWidget(self.cboxsp)
        self.zlbl=QtGui.QLabel()
        self.zlbl.setText("Zone Name:")
        self.Combo.addWidget(self.zlbl)
        self.cboxzone = QtGui.QComboBox()
        self.Combo.addWidget(self.cboxzone)
        zlbl=QtGui.QLabel()
        zlbl.setText("New Zone Name:")
        self.Combo.addWidget(zlbl)
        self.zline=QtGui.QLineEdit()
        self.Combo.addWidget(self.zline)
        self.cbtn=QtGui.QPushButton()
        self.cbtn.setText("Duplicate")
        self.Combo.addWidget(self.cbtn)
        self.cbtn.clicked.connect(self.duplicate)
        self.cancelbtn=QtGui.QPushButton()
        self.cancelbtn.setText("Cancel")
        self.Combo.addWidget(self.cancelbtn)
        self.cancelbtn.clicked.connect(self.cancel)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.Combo.addItem(spacerItem)

    def sptoz(self):
        if ex.imported or ex.created:
            self.spi=self.cboxsp.currentIndex()
            self.cboxzone.clear()
            self.zn=[]
            try:
                for zone in ex.tempdata["spaces"][self.spi]["control_zones"]:
                    self.cboxzone.addItem(zone["name"])
                    self.zn.append(zone["name"])
            except:
                pass

    def duplicate(self):
        zi=self.cboxzone.currentIndex()
        self.id=[self.spi, zi]
        name=self.zline.text()
        mark=0
        for n in self.zn:
            if name==n:
                mark=1

        if mark==1:
            QtGui.QMessageBox.warning(self, "Naming Error", "Please rename your new space to a different name than the old!")
            try:
                del self.newname
            except:
                pass
        else:
            self.newname=name
            self.accept()

    def cancel(self):
        self.close()

#Duplicate spaces
class DupSPUi_Combo(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.setModal(1)

    def setupUi(self, DupSPUi_Combo):
        self.resize(400, 200)
        self.setWindowTitle(_translate("Ui_Combo", "Space Duplication From:", None))
        self.Combo = QtGui.QVBoxLayout()
        self.setLayout(self.Combo)
        splbl=QtGui.QLabel()
        splbl.setText("Space Name:")
        self.Combo.addWidget(splbl)
        self.cboxsp = QtGui.QComboBox()
        self.Combo.addWidget(self.cboxsp)
        splbl=QtGui.QLabel()
        splbl.setText("New Space Name:")
        self.Combo.addWidget(splbl)
        self.spline=QtGui.QLineEdit()
        self.Combo.addWidget(self.spline)
        self.cbtn=QtGui.QPushButton("Duplicate")
        self.Combo.addWidget(self.cbtn)
        self.cancelbtn=QtGui.QPushButton("Cancel")
        self.Combo.addWidget(self.cancelbtn)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.Combo.addItem(spacerItem)
        self.cboxsp.currentIndexChanged.connect(self.sptoz)
        self.cbtn.clicked.connect(self.duplicate)
        self.cancelbtn.clicked.connect(self.cancel)

    def sptoz(self):
        if ex.imported or ex.created:
            self.spi=self.cboxsp.currentIndex()

    def duplicate(self):
        self.id=self.spi
        name=str(self.spline.text())
        if name==str(self.cboxsp.currentText()):
            QtGui.QMessageBox.warning(self, "Naming Error", "Please rename your new space to a different name than the old!")
        else:
            self.newname=name
            self.accept()

    def cancel(self):
        self.close()



class PBar(QtGui.QDialog):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.setModal(1)
        self.val=0
        self.progress.setValue(self.val)

    def setupUi(self, DupUi_Combo):
        self.resize(300, 70)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.Combo = QtGui.QVBoxLayout()
        self.setLayout(self.Combo)
        lbl=QtGui.QLabel()
        lbl.setText("Loading...")
        self.Combo.addWidget(lbl)
        self.progress=QtGui.QProgressBar()
        self.Combo.addWidget(self.progress)

    def update(self):
        self.val=self.val+20
        self.progress.setValue(self.val)
        if self.val==100:
            time.sleep(0.1)
            self.accept()


class Overall(QtGui.QDialog):
    def __init__(self, general, blist, vlist,name):
        QtGui.QDialog.__init__(self)
        self.setModal(1)
        self.blist=blist
        self.vlist=vlist
        self.name=name
        self.general=general
        self.setupUi(self)

    def setupUi(self, Status):
        self.setFixedSize(500, 200)
        if self.general==1:
            self.setWindowTitle("Results Summary")
        else:
            self.setWindowTitle("Results Summary (Approximate)")
        Combo = QtGui.QGridLayout()
        self.setLayout(Combo)
        lbl=QtGui.QLabel()
        if self.general==1:
            lbl.setText("Space: %s" %self.name)
        else:
            lbl.setText("Project Summary:")
        lbl.setFixedWidth(150)
        Combo.addWidget(lbl, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Combo.addItem(spacerItem, 1, 0, 1, 1)
        lbl=QtGui.QLabel()
        lbl.setText("sDA:")
        lbl.setFixedWidth(150)
        Combo.addWidget(lbl, 2, 0, 1, 1)
        lbl=QtGui.QLabel()
        try:
            lbl.setText(str(round(float(self.vlist[0])*100,1))+"%")
        except:
             lbl.setText(self.vlist[0])
        lbl.setStyleSheet("color: rgb(0, 0, 255);")
        lbl.setFixedWidth(100)
        Combo.addWidget(lbl, 2, 1, 1, 1)
        lbl=QtGui.QLabel()
        lbl.setText("Occupied_sDA:")
        lbl.setFixedWidth(150)
        Combo.addWidget(lbl, 3, 0, 1, 1)
        lbl=QtGui.QLabel()
        try:
            lbl.setText(str(round(float(self.vlist[1])*100,1))+"%")
        except:
             lbl.setText(self.vlist[1])
        lbl.setStyleSheet("color: rgb(0, 0, 255);")
        Combo.addWidget(lbl, 3, 1, 1, 1)
        lbl=QtGui.QLabel()
        lbl.setText("ASE:")
        lbl.setFixedWidth(150)
        Combo.addWidget(lbl, 4, 0, 1, 1)
        lbl=QtGui.QLabel()
        try:
            lbl.setText(str(round(float(self.vlist[2])*100,1))+"%")
        except:
             lbl.setText(self.vlist[2])
        lbl.setStyleSheet("color: rgb(0, 0, 255);")
        Combo.addWidget(lbl, 4, 1, 1, 1)
        lbl=QtGui.QLabel()
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        Combo.addItem(spacerItem, 5, 0, 1, 1)
        lbl.setText("Energy:")
        lbl.setFixedWidth(150)
        Combo.addWidget(lbl, 6, 0, 1, 1)
        lbl=QtGui.QLabel()
        lbl.setText("Watts Consumed:")
        lbl.setFixedWidth(150)
        Combo.addWidget(lbl, 7, 0, 1, 1)
        lbl=QtGui.QLabel()
        try:
            lbl.setText(str(round(float(self.vlist[3]),2))+" KWH")
        except:
             lbl.setText(self.vlist[3])
        lbl.setStyleSheet("color: rgb(0, 0, 255);")
        Combo.addWidget(lbl, 7, 1, 1, 1)
        lbl=QtGui.QLabel()
        lbl.setText("Watts Saved:")
        lbl.setFixedWidth(150)
        Combo.addWidget(lbl, 7, 2, 1, 1)
        lbl=QtGui.QLabel()
        lbl.setFixedWidth(100)
        try:
            lbl.setText(str(round(float(self.vlist[4]),2))+" KWH")
        except:
             lbl.setText(self.vlist[4])
        lbl.setStyleSheet("color: rgb(0, 0, 255);")
        Combo.addWidget(lbl, 7, 3, 1, 1)





if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    splash_pix = QtGui.QPixmap('1.png')
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.show()
    time.sleep(6)
    splash.close()
    ex=Ui_FormSTADIC()
    ex.show()
    sys.exit(app.exec_())

