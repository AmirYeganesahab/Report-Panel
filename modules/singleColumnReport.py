import sys,os, platform, datetime, pandas as pd,numpy as np,matplotlib.pyplot as plt, warnings
from PyQt5.QtWidgets import *
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

from colors import colors

class radioButtons(QWidget):

    def __init__(self):

        super().__init__()

        # Radio buttons
        self.group = QButtonGroup()
        self.group.setExclusive(False)  # Radio buttons are not exclusive

        self.b1 = QRadioButton('&Bar Chart')
        self.b1.clicked.connect(self.b1Clicked)
        self.group.addButton(self.b1)

        self.b2 = QRadioButton('&Pie Char')
        self.b2.clicked.connect(self.b2Clicked)
        self.group.addButton(self.b2)

        # Layout
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.b1)
        self.layout.addWidget(self.b2)
        # self.layout.addWidget(self.apply)
        self.setLayout(self.layout)

    def b1Clicked(self):
        self.b2.setChecked(False)
        self.b1.setChecked(True)
    def b2Clicked(self):
        self.b1.setChecked(False)
        self.b2.setChecked(True)
        
    def check_buttons(self, radioButton):
        # Uncheck every other button in this group
        
        for button in self.group.buttons():
            if button is not radioButton:
                button.setChecked(False)

class Graph(QDialog):
    def __init__(self,labels,data,plot_type='bar', parent=None):
        super(Graph, self).__init__(parent)
        self.plot_type = plot_type
        self.labels = labels
        self.data = data

    def create_layout(self):
        
        # a figure instance to plot on
        self.figure = plt.figure()
        self.figure.clear()
        
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas,parent=None)
        # creating a Vertical Box layout
        
        layout = QVBoxLayout()
        clearLayout(layout=layout)
        # adding tool bar to the layout
        layout.addWidget(self.toolbar)
        # adding canvas to the layout
        layout.addWidget(self.canvas)
        # setting layout to the main window
        self.figure.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2, wspace=0.5, hspace=0.5)
        self.generate_plot()
        return layout
  
    def generate_plot(self):
        thisColors = []
        print('len(colors):',len(colors))
        for i,d in enumerate(self.data):
            dd = int(round(d*10))
            if dd>=1000:dd=1000-dd
            thisColors.append(colors[dd])
        # clearing old figure
        self.figure.clear()
        # create an axis
        if self.plot_type=='bar':
            self.figure.clear()
            ax = self.figure.add_subplot(111,position=[0, 0, 1, 1])
            ax.format_coord = lambda x, y: ""
            ax.cla()
            # plot data
            labels = [str(l) for l in self.labels]
            ax.bar(labels,self.data,color=thisColors)
            ax.set_ylim(top=max(self.data)+25)
            
            ax.set_xticks(np.arange(len(self.labels)),labels,rotation=90)
            xlocs = ax.get_xticks()
            for i, v in enumerate(self.data):
                ax.text(xlocs[i], v + 0.5, f'{v}%')
        elif self.plot_type=='pie':
            self.figure.clear()
            ax = self.figure.add_subplot(111,position=[0, 0, 1, 1])
            ax.format_coord = lambda x, y: ""
            ax.cla()
            # plot data
            patches,_,_= ax.pie(self.data,labels=self.labels,shadow=False, autopct='%1.f%%',startangle=0) # refresh canvas
            self.figure.legend(patches, self.labels,bbox_to_anchor=(0.8,0.5), loc='right')

        # refresh canvas
        self.canvas.draw()

class MessageBox(QMainWindow):
    def __init__(self,title,message):
        super().__init__()

        dlg = QMessageBox(self)
        dlg.setWindowTitle(f"{title}!")
        dlg.setText(f"{message}")
        button = dlg.exec()

        if button == QMessageBox.Ok:
            print("OK!")

def clearLayout(layout):
  while layout.count():
    child = layout.takeAt(0)
    if child.widget():
      child.widget().deleteLater()

class percentage_report(QMainWindow):
    default_dir:str
    recent_reports_path:str
    def __init__(self,data, parent=None):
        super(percentage_report, self).__init__(parent)
        self.default_dir =os.getcwd()
        self.recent_reports_path = os.path.join(self.default_dir,'recent_reports.history')
        self.read_recent_reports()
        
        self.data = data
        self._main = QWidget()
        self.setCentralWidget(self._main)
        self.radiob = radioButtons()
        self.radiob.b1.clicked.connect(self.onChanged)
        self.radiob.b2.clicked.connect(self.onChanged) 
        
        self.uplyt = QVBoxLayout(self._main)
        self.dnlyt = QVBoxLayout(self._main)
        self.up = QFrame(self)       
        self.up.setFrameShape(QFrame.StyledPanel)
        self.up.setLayout(self.uplyt)
        
        self.down = QFrame(self)       
        self.down.setFrameShape(QFrame.StyledPanel)
        self.down.setLayout(self.dnlyt)
        
        self.layout = QVBoxLayout(self._main)
        self.layout.addWidget(self.radiob)
        self.fig = Figure(figsize=(5, 4), dpi=100)

        self.static_canvas = FigureCanvas(self.fig)
        self.uplyt.addWidget(self.static_canvas)
        
        splitter = QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(self.up)
        splitter.addWidget(self.down)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([500, 150])
        self.layout.addWidget(splitter)

        self._static_ax = self.static_canvas.figure.subplots()

        self.initialize()
        self.update_recent_reports()
    
    def initialize(self):
        self.setWindowTitle('Single Selection')
        self.setWindowIcon(QIcon('web-1.png'))
        self.showMaximized()
        self.reporttableWidget = QTableWidget()
        fixedfont = QFont("Roboto")
        fixedfont.setPointSize(12)
        self.reporttableWidget.setFont(fixedfont)
        self.dnlyt.addWidget(self.reporttableWidget)
        
        self.new_recentAction = QMenu('&Recent Reports', self)        
        self.new_recentAction.triggered.connect(self.populateRecent)

        save_file_action = QAction("Save", self)
        save_file_action.setShortcut('Ctrl+S')
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        menuBar = self.menuBar()
        file_menu = QMenu("&File", self)
        menuBar.addMenu(file_menu)

        file_menu.addMenu(self.new_recentAction)
        file_menu.addAction(save_file_action)
        file_menu.addAction(exitAction)

        self.label = QLabel(self)
        self.label.move(50,16)
        self.label.setText('Select Column to be Analyzed')
        self.label.adjustSize()
        
        self.combo = QComboBox(self)
        self.combo.move(50, 50)
        
        self.combo.activated[str].connect(self.onChanged)
        cols = [d.split(os.sep)[-1] for d in self.data.columns]
        self.combo.addItems(cols)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo)
        
        self.show()
    
    def update_recent_reports(self):
        self.populateRecent()
        f = open(self.recent_reports_path,'w')
        f.write(str(self.action_history))
        f.close()

    def read_recent_reports(self):
        print('recent reports are being read ...')
        if os.path.exists(self.recent_reports_path):
            f = open(self.recent_reports_path,'r')
            try:
                #print(f.readline())
                self.action_history = eval(f.readline())
                # print('recent_reports: ',self.action_history)
            except Exception as e:
                print(e)
                
            f.close()
        
    def populateRecent(self):
        # Step 1. Remove the old options from the menu
        self.new_recentAction.clear()
        # Step 2. Dynamically create the actions
        new_actions = []
        for actions in self.action_history:
            newaction = QAction(actions, self)
            newaction.triggered.connect(partial(self.onChanged, actions))
            new_actions.append(newaction)
        # Step 3. Add the actions to the menu
        self.new_recentAction.addActions(new_actions)
    
    def file_save(self):
        try:
            xlsxName = f'Frequencies-{self.now}.xlsx'
            xlsxName = os.path.join(self.default_dir, xlsxName)
            name = QFileDialog.getSaveFileName(self, 'Save Report File',xlsxName,"xlsx (*.xlsx)")
            self.df.to_excel(name[0])
            # print('_________________',name[0])
            png_path = name[0][:-5]+'.png'

            self.graph.ax.figure.savefig(png_path)
            
            MessageBox(title='File Saved', message=f'table and pie chart saved at {os.path.join(*png_path.split("/")[:-1])}')
        except Exception as e:
            print(e)

    def onChanged(self,text):
        
        index = self.combo.currentIndex()
        text = self.data.columns[index]
        try:
            self.action_history.append(text)
        except:
            self.action_history = [text]
        self.update_recent_reports()
        self.populateRecent()
        data = self.data[text]
        keys = list(data.keys())
        values = list(data.values)
        for i,v in enumerate(values):
            if v!=v or isinstance(v,type(None)):
                values[i]='not_applicable'
        categories = np.unique(values,return_counts=True)
        # print(np.where(categories == np.nan))
        self.labels = categories[0]
        self.y = categories[1]
        s = np.sum(self.y)
        self.percentages = [100*y_/s for y_ in self.y]
        clearLayout(self.uplyt)
        try:
            del self.graph
        except:
            pass
        percentages = [int(round(p)) for p in self.percentages]
        if not (self.radiob.b1.isChecked() or self.radiob.b2.isChecked()):
            self.radiob.b1.setChecked(True)
        if self.radiob.b1.isChecked():            
            self.graph = Graph(labels=self.labels,data=percentages,plot_type='bar' )
            graph_layout = self.graph.create_layout()
            self.uplyt.addLayout(graph_layout)
        elif self.radiob.b2.isChecked():
            self.graph = Graph(labels=self.labels,data=percentages,plot_type='pie' )
            graph_layout = self.graph.create_layout()
            self.uplyt.addLayout(graph_layout)
        
        # self._static_ax.cla()
        # now = datetime.datetime.now()
        # self.now = now.strftime("%m-%d-%YT%H-%M-%S")
        # self._static_ax.pie(self.percentages,labels=self.labels,shadow=False, autopct='%1.f%%',startangle=90)
        # self._static_ax.set_title( text)
        # self.static_canvas.draw_idle()
        self._main.update()
        self.showMaximized()

        self.df = pd.DataFrame({'Row Labels':self.labels,'Count':self.y,'Frequencies':["{:.0%}".format(round(np.sum(p))/100) for p in self.percentages]})
        self.df = pd.concat([self.df, pd.DataFrame.from_records([{'Row Labels':'Grand Total','Count':s,'Frequencies':"{:.0%}".format(int(round(np.sum(self.percentages)))/100)}])])
        self.createTable()
        
    def createTable(self):
        now = datetime.datetime.now()
        self.now = now.strftime("%m-%d-%YT%H-%M-%S")
        ncols = len(self.df.columns)
        nrows = len(self.df)
        self.reporttableWidget.setRowCount(nrows)
        self.reporttableWidget.setColumnCount(ncols)
        self.reporttableWidget.setHorizontalHeaderLabels(self.df.columns)
        
        for i,col in enumerate(self.df.columns):
            for j,d in enumerate(self.df[col]):
                if type(d)==pd._libs.tslibs.timestamps.Timestamp:
                    d = pd.Timestamp.strftime(d,'%Y-%m-%d %X')
                try:
                    self.reporttableWidget.setItem(j,i, QTableWidgetItem(str(d)))
                except Exception as e:
                    print('____________________')
                    print(e)
                    # print(type(d))
                    print('____________________')
            
        print('table created')
