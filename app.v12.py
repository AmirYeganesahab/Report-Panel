import sys,os, platform, datetime, pandas as pd,numpy as np,matplotlib.pyplot as plt, warnings
from PyQt5.QtWidgets import (QApplication, QWidget,QMenu,QMainWindow,
                             QAction,QFileDialog,QTableWidget,
                             QTableWidgetItem,QVBoxLayout,QHBoxLayout,QComboBox,
                             QLabel,QFrame,QSplitter,QMessageBox, QCheckBox,
                             )
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtCore import pyqtSlot,Qt
from PyQt5.QtGui import QIcon,QFont, QStandardItemModel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from functools import partial
import _io
from typing import *
import sqlite3
from modules.singleColumnReport import *
from modules.multiple_questions import *

from modules.multipleColumnReport import *
from modules.comparison import *

warnings.filterwarnings("ignore")

class MessageBox(QMainWindow):
    def __init__(self,title,message):
        super().__init__()

        dlg = QMessageBox(self)
        dlg.setWindowTitle(f"{title}!")
        dlg.setText(f"{message}")
        button = dlg.exec()

        if button == QMessageBox.Ok:
            print("OK!")
            
class APP(QMainWindow):
    cwd:str
    recent_reports_path:str
    recent_file_path:str
    fileNames:List[str]
    fileNames_new:List[str]
    fileNames_added:List[str]
    tableWidget:QTableWidget
    layout:QVBoxLayout
    new_recentAction:QMenu
    add_recentAction:QMenu
    data:pd.core.frame.DataFrame
    
    def __init__(self, parent=None) -> None:
        QMainWindow.__init__(self,parent)
        self.cwd =os.getcwd()
        self.recent_reports_path = os.path.join(self.cwd,'recent_reports.history')
        f:_io.TextIOWrapper = open(self.recent_reports_path,'w')
        f.write('[]')
        f.close()
        self.recent_file_path = os.path.join(self.cwd,'recent_files.history')
        self.read_recent()
        #if platform.system=='Windows':self.initila_conf()
        central_widget:QWidget = QWidget()
        self.setCentralWidget(central_widget)
        self.initialize()
        
    def update_recent(self):
        self.populateOpenRecent()
        f:_io.TextIOWrapper = open(self.recent_file_path,'w')
        f.write(str(self.fileNames))

    def read_recent(self):
        e:str
        print('recent files are being read ...')
        if os.path.exists(self.recent_file_path):
            f:_io.TextIOWrapper = open(self.recent_file_path,'r')
            try:
                #print(f.readline())
                self.fileNames = eval(f.readline())
                print('recent files are read ...')
            except Exception as e:
                print(e)
                
            f.close()
        
    def openFileNameDialog(self):
        e:str
        options:QFileDialog.Options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileNames_new, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileName()", "","xlsx (*.xlsx);;csv (*.csv);;sql (*.sql);;sqlite (*.sqlite)", options=options)
        if len(self.fileNames_new)==0:return
        try:
            self.fileNames.extend(self.fileNames_new)
        except Exception as e:
            print(e)
            self.fileNames = self.fileNames_new
        #self.fileNames = np.unique(self.fileNames)
        # print('new file opended:',self.fileNames_new)
        self.update_recent()
        self.createTable()
        self.setCentralWidget(self.tableWidget) 
    
    def addFileDialog(self):
        options:QFileDialog.Options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileNames_added, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileName()", "","xlsx (*.xlsx);;csv (*.csv);;sql (*.sql);;sqlite (*.sqlite)", options=options)
        print('new file opended:',self.fileNames_added)
        if len(self.fileNames_added)==0:return
        try:
            self.fileNames.extend(self.fileNames_added)
        except:
            self.fileNames = self.fileNames_added
        #self.fileNames = np.unique(self.fileNames)
        self.update_recent()
        self.updateTable()
        self.setCentralWidget(self.tableWidget) 

    def closeEvent(self, event):
        close:Union[QMessageBox,int]
        close = QMessageBox()
        close.setText("You Sure You want to Exit the Application?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()
        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    def initialize(self):
        self.showMaximized()
        self.setWindowTitle('Report Panel')
        self.setWindowIcon(QIcon('web-1.png'))
        self.tableWidget = QTableWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        #self.setLayout(self.layout) 
        # Creating menus using a QMenu object
        menuBar:QtWidgets.QMenuBar = self.menuBar()
        fileMenu:QMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        # Create new action
        openAction:QAction = QAction(QIcon('folder_open.png'), '&New File', self)        
        openAction.setShortcut('Ctrl+N')
        openAction.setStatusTip('New document')
        openAction.triggered.connect(self.openFileNameDialog)
        
        appendAction:QAction = QAction(QIcon('folder_open.png'), '&Add File', self)        
        appendAction.setShortcut('Ctrl+A')
        appendAction.setStatusTip('Add New document')
        appendAction.triggered.connect(self.addFileDialog)

        self.new_recentAction = QMenu('&Open Recent', self)        
        self.new_recentAction.triggered.connect(self.populateOpenRecent)
        
        self.add_recentAction = QMenu('&Add Recent', self)        
        self.add_recentAction.triggered.connect(self.populateOpenRecent)

        # Create exit action
        exitAction:QAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        fileMenu.addAction(openAction)
        fileMenu.addAction(appendAction)
        fileMenu.addMenu(self.new_recentAction)
        fileMenu.addMenu(self.add_recentAction)
        fileMenu.addAction(exitAction)
        
        # Creating menus using a title
        reportMenu:QMenu = menuBar.addMenu("&Reports")
        
        frequencyMenu:QMenu=QMenu('&Frequency Analysis',parent=self)
        frequencyMenu.setIcon(QIcon('data-frequency-table-4291007-3580418.webp'))
        reportMenu.addMenu(frequencyMenu)
        single_column_report_Action:QAction = QAction(QIcon('pie.png'), '&Single Selection ', self)        
        single_column_report_Action.setShortcut('Ctrl+S')
        single_column_report_Action.setStatusTip('Frequency Report Application')
        single_column_report_Action.triggered.connect(self.percentage_report)
        frequencyMenu.addAction(single_column_report_Action)
        
        multipleQuestions_Action:QAction = QAction(QIcon('pie.png'), '&Multiple Selection ', self)        
        multipleQuestions_Action.setShortcut('Ctrl+M')
        multipleQuestions_Action.setStatusTip('Frequency Report Application')
        multipleQuestions_Action.triggered.connect(self.multipeQuestion_report)
        frequencyMenu.addAction(multipleQuestions_Action)

        dual_column_report_Action:QAction = QAction(QIcon('pie.png'), '&Cross Check', self)        
        dual_column_report_Action.setShortcut('Ctrl+R+D')
        dual_column_report_Action.setStatusTip('Cross Check Report Application')
        dual_column_report_Action.triggered.connect(self.dual_percentage_report)
        reportMenu.addAction(dual_column_report_Action)
        
        comparison_report_Action:QAction = QAction(QIcon('pie.png'), 'Com&parison', self)        
        comparison_report_Action.setShortcut('Ctrl+C+V')
        comparison_report_Action.setStatusTip('Comparison of Cross Check Reports')
        comparison_report_Action.triggered.connect(self.comparison)
        reportMenu.addAction(comparison_report_Action)
        
        crossCheck:QAction = QAction(QIcon('pie.png'), '&Cross Check', self)        
        crossCheck.setShortcut('Ctrl+R+D')
        crossCheck.setStatusTip('Cross Check Report Application')
        crossCheck.triggered.connect(self.dual_percentage_report)
        reportMenu.addAction(dual_column_report_Action)
        
        helpMenu:QMenu = menuBar.addMenu("&Help")
        openAction.trigger()

    def populateOpenRecent(self):
        filename:str
        # Step 1. Remove the old options from the menu
        self.new_recentAction.clear()
        self.add_recentAction.clear()
        # Step 2. Dynamically create the actions
        new_actions:List[QAction] = []
        add_actions:List[QAction] = []
        for filename in self.fileNames:
            newaction:QAction = QAction(filename, self)
            addaction:QAction = QAction(filename, self)
            newaction.triggered.connect(partial(self.open_with_recent, filename))
            addaction.triggered.connect(partial(self.update_with_recent, filename))
            new_actions.append(newaction)
            add_actions.append(addaction)
        # Step 3. Add the actions to the menu
        self.new_recentAction.addActions(new_actions)
        self.add_recentAction.addActions(add_actions)

    def update_with_recent(self,fileName:str):
        try:
            self.fileNames_added.append(fileName)
        except:
            try:
                self.fileNames_added = self.fileNames_new
                self.fileNames_added.append(fileName)
            except:
                self.fileNames_added = [fileName]
        self.updateTable()
        self.setCentralWidget(self.tableWidget) 

    def open_with_recent(self,fileName:str):
        self.fileNames_new = [fileName]
        self.createTable()
        self.setCentralWidget(self.tableWidget) 

    def dual_percentage_report(self):
        self.reports = dual_percentage_report(parent =self,data = self.data)

    def percentage_report(self):
        self.reports = percentage_report(parent =self,data = self.data)

    def multipeQuestion_report(self):
        self.reports = multipleQuestions(parent =self,data = self.data)


    def comparison(self):
        self.reports = ComparisonWindow(parent=self,data = self.data)
        self.reports.show()

    def updateTable(self)->None:
        i:int
        j:int
        col:Union[str,float]
        d:Union[pd._libs.tslibs.timestamps.Timestamp,str]
        e:str
        
        new_data = pd.DataFrame()
        for p in self.fileNames_added:
            p_ = p.split(os.sep)[-1].split('.')[-1]
            # print('__________________________',p_)
            if 'xlsx' in p_:
                
                data = pd.read_excel(p, engine='openpyxl',header=0)
            elif 'sql' in p_:
                conn = sqlite3.connect(p)
                data = pd.read_sql_query("SELECT * FROM UN", conn)
            new_data:pd.core.frame.DataFrame = pd.concat([new_data,data])
        
        self.data = pd.concat([self.data,new_data])
        del(new_data)
        ncols:int = len(self.data.columns)
        nrows:int = len(self.data)
        self.tableWidget.setRowCount(nrows)
        self.tableWidget.setColumnCount(ncols)
        self.tableWidget.setHorizontalHeaderLabels(self.data.columns)
        
        for i,col in enumerate(self.data.columns):
            for j,d in enumerate(self.data[col]):
                if type(d)==pd._libs.tslibs.timestamps.Timestamp:
                    d = pd.Timestamp.strftime(d,'%Y-%m-%d %X')
                try:
                    self.tableWidget.setItem(j,i, QTableWidgetItem(str(d)))
                except Exception as e:
                    print('____________________')
                    print(e)
                    # print(type(d))
                    print('____________________')
            
        self.tableWidget.move(0,0)
        print('table updated')

    def createTable(self)->None:
        i:int
        j:int
        col:Union[str,float]
        d:Union[pd._libs.tslibs.timestamps.Timestamp,str]
        e:str
        self.data = pd.DataFrame()
        for p in self.fileNames_new:
            p_ = p.split(os.sep)[-1].split('.')[-1]
            # print('__________________________',p_)
            if 'xlsx' in p_:
                
                data = pd.read_excel(p, engine='openpyxl',header=0)
            elif 'sql' in p_:
                conn = sqlite3.connect(p)
                data = pd.read_sql_query("SELECT * FROM UN", conn)
            self.data:pd.core.frame.DataFrame = pd.concat([self.data,data])
        # self.data = pd.concat([pd.read_excel(p, engine='openpyxl',header=0) for p in self.fileNames_new])
        ncols:int = len(self.data.columns)
        nrows:int = len(self.data)
        self.tableWidget.setRowCount(nrows)
        self.tableWidget.setColumnCount(ncols)
        self.tableWidget.setHorizontalHeaderLabels(self.data.columns)
        
        for i,col in enumerate(self.data.columns):
            for j,d in enumerate(self.data[col]):
                if type(d)==pd._libs.tslibs.timestamps.Timestamp:
                    d = pd.Timestamp.strftime(d,'%Y-%m-%d %X')
                try:
                    self.tableWidget.setItem(j,i, QTableWidgetItem(str(d)))
                except Exception as e:
                    print('____________________')
                    print(e)
                    # print(type(d))
                    print('____________________')
            
        self.tableWidget.move(0,0)
        print('table created')


if __name__=='__main__':
    app = QApplication(sys.argv)
    e = APP()
    e.show()
    e.activateWindow()
    e.raise_()
    sys.exit(app.exec_())