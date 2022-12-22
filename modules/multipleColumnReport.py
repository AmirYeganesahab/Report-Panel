import sys,os, platform, datetime, pandas as pd,numpy as np,matplotlib.pyplot as plt, warnings
from PyQt5.QtWidgets import *
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon,QFont, QStandardItemModel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from functools import partial
import _io
from typing import *
import sqlite3
from colors import colors
colors =['#e7f4f3', '#ceeae8', '#aedcd9', '#85cac5', '#5cb9b2','#e6effb', '#cedef7', '#adc9f2', '#84adec', '#5b92e5','#fff4dd', '#ffeabb', '#ffdc8e', '#ffca55', '#ffb81c','#ffe8dd', '#ffd1bc', '#ffb38f', '#ff8d57', '#ff671f','#f8dee0', '#f2bec1', '#e99398', '#ddc064', '#d22630']


class radioButtons(QWidget):

    def __init__(self):

        super().__init__()

        # Radio buttons
        self.group = QButtonGroup()
        self.group.setExclusive(False)  # Radio buttons are not exclusive
        # self.group.buttonClicked.connect(self.check_buttons)

        # self.apply = QPushButton('Apply',self)
        # self.apply.setToolTip('click to apply change')

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

    def create_layout(self, title=''):
        
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
        self.generate_plot(title)

        return layout
  
    def generate_plot(self,title):
        thisColors = []
        for i,d in enumerate(self.data):
            dd = int(round(d/4))
            if dd==25: dd=24
            thisColors.append(colors[dd])
        # clearing old figure
        self.figure.clear()
        # create an axis
        labels = [str(l) for l in self.labels]
        if self.plot_type=='bar':
            self.figure.clear()
            self.figure.set_tight_layout(tight=True)
            self.ax = self.figure.add_subplot(111,position=[0, 0, 1, 1])
            self.ax.format_coord = lambda x, y: ""
            self.ax.cla()
            # plot data
            self.ax.set_title(title)
            self.ax.bar(labels,self.data,color=thisColors)
            self.ax.set_ylim(top=max(self.data)+25)
            self.ax.set_xticks(np.arange(len(labels)),labels,rotation=30)
            xlocs = self.ax.get_xticks()
            for i, v in enumerate(self.data):
                self.ax.text(xlocs[i], v + 0.5, f'{v}%')
        elif self.plot_type=='pie':
            self.figure.clear()
            self.figure.set_tight_layout(tight=True)
            self.ax = self.figure.add_subplot(111,position=[0, 0, 1, 1])
            self.ax.format_coord = lambda x, y: ""
            self.ax.cla()
            self.ax.set_title(title)
            # plot data
            patches,_,_= self.ax.pie(self.data,labels=labels,shadow=False, autopct='%1.f%%',startangle=0) # refresh canvas
            legend =self.ax.legend(patches, labels,bbox_to_anchor=(1.5,0.5), loc='right')
            oldLegPos = legend.get_bbox_to_anchor()._bbox
            # print(oldLegPos.bbox)
            legend.set_draggable(state=True,update='loc',use_blit=False)
            
            legend.bbox_to_anchor = oldLegPos
        # refresh canvas
        self.canvas.draw()

def clearLayout(layout):
  while layout.count():
    child = layout.takeAt(0)
    if child.widget():
      child.widget().deleteLater()

class MessageBox(QMainWindow):
    def __init__(self,title,message):
        super().__init__()

        dlg = QMessageBox(self)
        dlg.setWindowTitle(f"{title}!")
        dlg.setText(f"{message}")
        button = dlg.exec()

        if button == QMessageBox.Ok:
            print("OK!")

class CheckableComboBox(QComboBox):
    def __init__(self, parent = None):
        super(CheckableComboBox, self).__init__()
        self.view().pressed.connect(self.handle_item_pressed)
        self.setModel(QStandardItemModel(self))
        
    # when any item get pressed
    def handle_item_pressed(self, index):
        # getting which item is pressed
        item = self.model().itemFromIndex(index)
        # make it check if unchecked and vice-versa
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)
        # calling method
        self.check_items()
    # method called by check_items
    def item_checked(self, index):
        # getting item at index
        item = self.model().item(index, 0)
        # return true if checked else false
        return item.checkState() == Qt.Checked
    # calling method
    def check_items(self):
        
        # blank list
        self.checkedItems = []
        # traversing the items
        for i in range(self.count()):
            # if item is checked add it to the list
            if self.item_checked(i):
                self.checkedItems.append(i)
        self.checkedItems = list(np.unique(self.checkedItems))
            
    # flush
    sys.stdout.flush()
    
class dual_percentage_report(QMainWindow):
    def __init__(self,data, parent=None):
        super(dual_percentage_report, self).__init__(parent)
        self.constructFrame(data=data)
        self.constructSplitter()
        self.fillLayouts()
        self.constructMenues()
        self.initialize()
    
    def constructFrame(self,data):
        self.default_dir =os.getcwd()
        self.data = data
        self._main = QWidget()
        self.setCentralWidget(self._main)
        self.uplyt = QVBoxLayout(self._main)
        self.dnlyt = QVBoxLayout(self._main)
        self.up = QFrame(self)       
        self.up.setFrameShape(QFrame.StyledPanel)
        self.up.setLayout(self.uplyt)
        self.down = QFrame(self)       
        self.down.setFrameShape(QFrame.StyledPanel)
        self.down.setLayout(self.dnlyt)
        self.radiob = radioButtons()
        self.radiob.b1.clicked.connect(self.onChanged)
        self.radiob.b2.clicked.connect(self.onChanged)
        
        self.vlayout = QVBoxLayout(self._main)
        self.vlayout.addWidget(self.radiob)
        
        self.hlayout = QHBoxLayout(self._main)
        
        self.fig = Figure(figsize=(8, 8), dpi=100)
        self.static_canvas = FigureCanvas(self.fig)
        self._static_ax = self.static_canvas.figure.subplots()

    def constructSplitter(self):
        splitter = QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(self.up)
        splitter.addWidget(self.down)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([500, 150])
        self.vlayout.addWidget(splitter)

    def fillLayouts(self):
        self.uplyt.addWidget(self.static_canvas)
        self.setWindowTitle('Cross Check Analysis')
        self.setWindowIcon(QIcon('web-1.png'))
        self.showMaximized()
        self.reporttableWidget = QTableWidget()
        fixedfont = QFont("Roboto")
        fixedfont.setPointSize(12)
        self.reporttableWidget.setFont(fixedfont)
        self.dnlyt.addWidget(self.reporttableWidget)

    def constructMenues(self):
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
        file_menu.addAction(save_file_action)
        file_menu.addAction(exitAction)

    def pair(self,func,text,multiselect=False,set_cols=False):
        # =================================
        label = QLabel(self)
        label.move(0,0)
        label.setText(text)
        label.adjustSize()
        if multiselect:
            combo = CheckableComboBox(self)
        else:
            combo = QComboBox(self)
        combo.move(0, 0)
        if func!=None:
            combo.activated[str].connect(func)
        if set_cols:
            # cols = [d.split(os.sep)[-1] for d in self.data.columns]
            cols = [f'{i}. {d}' for i,d in enumerate(self.data.columns)]
            combo.setMaximumWidth(450)
            # combo.addItems(cols)
            combo.setModel(QStringListModel(cols))
        
        return label,combo

    def onChanged(self,text):
        
        self.create_chart(labels=self.labels,
                                percentages=self.percentages,
                                title=self.title)

    def createTable(self):
        now = datetime.datetime.now()
        self.now = now.strftime("%m-%d-%YT%H-%M-%S")
        try:
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
                
            self.reporttableWidget.move(0,0)
            print('table created')
        except:
            pass
    
    def file_save(self):
        try:
            xlsxName = f'Cross_check-{self.now}.xlsx'
            xlsxName = os.path.join(self.default_dir, xlsxName)
            name = QFileDialog.getSaveFileName(self, 'Save Report File',xlsxName,"xlsx (*.xlsx)")
            self.df.to_excel(name[0])
            # print('______________', name[0])
            pngName = name[0][:-5]+'.png'

            self.graph.ax.figure.savefig(pngName)
            MessageBox(title='File Saved', message=f'table and pie chart saved at {os.path.join(*pngName.split("/")[:-1])}')
        except Exception as e:
            print(e)

    def initialize(self):
        self.ischecked = False
        
        
        # =================================
        self.label1, self.combo1 = self.pair(func=self.populate_combo2,
                                             text='Select First Column »',
                                             set_cols=True,multiselect=False) 
        self.combo1.setCurrentIndex(-1)
        self.label2, self.combo2 = self.pair(func=self.get_query_entity_from_combo23,
                                             text='First Query Entity »',
                                             set_cols=False,multiselect=True) 
        self.combo2.setCurrentIndex(-1)
        self.label3, self.combo3 = self.pair(func=self.populate_combo4,text='Select Second Column »',
                                             set_cols=True,
                                             multiselect=False)
        self.combo3.setCurrentIndex(-1)
        # =================================
        self.box = QCheckBox("Double Cross Check is required!")
        self.box.toggled.connect(self.checkbox_clicked)
        
        self.hlayout.addWidget(self.label1)
        self.hlayout.addWidget(self.combo1)
        
        self.hlayout.addWidget(self.label2)
        self.hlayout.addWidget(self.combo2)

        self.hlayout.addWidget(self.label3)
        self.hlayout.addWidget(self.combo3)

        self.dnlyt.addLayout(self.hlayout)

        self.dnlyt.addWidget(self.box)

    def checkbox_clicked(self):
        cbutton = self.sender()
        self.ischecked = cbutton.isChecked()
        # print(self.ischecked)
        if cbutton.isChecked():
            
            self.hlayout2 = QHBoxLayout(self._main)
            self.label4,self.combo4 = self.pair(func=self.get_query_entity_from_combo1234,
                                                text='Second Query Entity »',
                                                set_cols=False,multiselect=True)
            self.combo4.setCurrentIndex(-1)
            self.populate_combo4()
            self.label5,self.combo5 = self.pair(func=self.get_guery_entity_from_combo12345,
                                                text='Select Third Column »',
                                                set_cols=True,multiselect=False)
            self.combo5.setCurrentIndex(-1)
            self.hlayout2.addWidget(self.label4)
            self.hlayout2.addWidget(self.combo4)
            self.hlayout2.addWidget(self.label5)
            self.hlayout2.addWidget(self.combo5)
        else:
            self.hlayout2.removeWidget(self.label4)
            self.label4.deleteLater()
            self.label4 = None

            self.hlayout2.removeWidget(self.combo4)
            self.combo4.deleteLater()
            self.combo4 = None

            self.hlayout2.removeWidget(self.label5)
            self.label5.deleteLater()
            self.label5 = None
            
            self.hlayout2.removeWidget(self.combo5)
            self.combo5.deleteLater()
            self.combo5 = None

        self.dnlyt.addLayout(self.hlayout2)
        # self.showMaximized()
    def populate_combo4(self,text=None):
        '''
        gets selected index in combo 1 and fills combo 2 according to this selection
        '''
        # index of selected field
        index = self.combo3.currentIndex()
        # get string of the selected field
        column_text = self.data.columns[index]
        # filter the data based on the selected field
        data = self.data[column_text] 
        # get curresponding values of the selected field
        values = list(data.values) 
        # if vlaue is None
        for i,v in enumerate(values):
            if v!=v:
                values[i]='*Not Applicable*'
        # get the fill values for combo2
        first_column = np.unique(values,return_counts=True)
        
        # reset combo4
        try:
            self.combo4.items = [str(d) for d in first_column[0]]
            self.combo4.setCurrentIndex(0)
            # self.combo4.checkedItems=[0]
            self.combo4.clear()
            self.combo4.addItems( [str(d) for d in first_column[0]])
            # self.combo4.setCurrentIndex(0)
            # print('_______combo4___',self.combo4.currentIndex())
        except Exception as e:
            print('705___________',e)

        
        if self.ischecked:
            try:
                self.get_query_entity_from_combo1234()
            except Exception as e:
                print(e)
        else:
            try:
                self.get_query_entity_from_combo23()
            except:
                pass

    def populate_combo2(self,text):
        '''
        gets selected index in combo 1 and fills combo 2 according to this selection
        '''
        # index of selected field
        index = self.combo1.currentIndex()
        # get string of the selected field
        self.first_column_text = self.data.columns[index]
        self.title = self.first_column_text
        # filter the data based on the selected field
        data = self.data[self.first_column_text] 
        # get curresponding values of the selected field
        values = list(data.values) 
        # if vlaue is None
        for i,v in enumerate(values):
            if v!=v:
                values[i]='*Not Applicable*'
        # get the fill values for combo2
        self.first_column = np.unique(values,return_counts=True)
        # reset combo2
        self.combo2.items = [str(d) for d in self.first_column[0]]
        self.combo2.clear()
        self.combo2.addItems(self.combo2.items)
        self.combo2.setCurrentIndex(0)
        ## 
        try:
            self.get_query_entity_from_combo23()
        except:
            pass

    def get_query_entity_from_combo1234(self,text=None):
        print('get_query_entity_from_combo1234')
        # index of selected field
        try:
            index1 = self.combo1.currentIndex()
        except:
            MessageBox(title='Error!',message='Unidentified element for query')
            return
            
        if index1<0:return
        # get string of the selected field
        combo2_txt = self.data.columns[index1]
        data1 = pd.DataFrame()
        self.combo2_selected_items = []
        for index in self.combo2.checkedItems:
            txt = self.combo2.items[index]
            self.combo2_selected_items.append(txt)
            data1 = pd.concat([data1,self.data.loc[self.data[combo2_txt]==txt]])
        self.title = f'{combo2_txt} «« {self.combo2_selected_items}'
        index2 = self.combo3.currentIndex()
        if index2<0:return
        combo3_txt = self.data.columns[index2]
        self.title = f'{self.title} «« {combo3_txt}'
        try:
            self.combo4.checkedItems
        except:
            self.combo4.checkedItems = [0]

        data2 = pd.DataFrame()
        self.combo4_selected_items=[]
        for index in np.unique(self.combo4.checkedItems):
            if index<0:return
            txt = self.combo4.items[index]
            self.combo4_selected_items.append(txt)
            data2 = pd.concat([data2,data1.loc[data1[combo3_txt]==txt]])
            
        self.combo4Table = data2
        self.title = f'{self.title} «« {self.combo4_selected_items}'
        self.get_guery_entity_from_combo12345()

    def get_guery_entity_from_combo12345(self):
        print('get_query_entity_from_combo12345')
        try:
            try:
                index5 = self.combo5.currentIndex()
                if index5<0:return
                # self.combo5.setCurrentIndex(0)
            except:
                pass

            # get string of the selected field
            combo5_txt = self.data.columns[index5]
            self.title = f'{self.title} «« {combo5_txt}'
            # print('????????????????',combo5_txt)
            values = list(self.combo4Table[combo5_txt].values)
            # if vlaue is None
            for i,v in enumerate(values):
                if v!=v:
                    values[i]='not_applicable'
            # get the fill values for graphics and report
            self.labels,self.y = np.unique(values,return_counts=True)
            s = np.sum(self.y)
            # construct graphic
            self.percentages = [100*y_/s for y_ in self.y]

            self.create_chart(labels=self.labels,
                                percentages=self.percentages,
                                title=self.title)
            # construct dataframe
            self.df = pd.DataFrame({'Row Labels':self.labels,'Count':self.y,'percentages':["{:.0%}".format(round(np.sum(p))/100) for p in self.percentages]})
            self.df = pd.concat([self.df, pd.DataFrame.from_records([{'Row Labels':'Grand Total','Count':s,'percentages':"{:.0%}".format(int(round(np.sum(self.percentages)))/100)}])])

            self.createTable()


        except:
            pass
        
    def create_chart(self, labels, percentages,title):
        percentages = [int(round(p)) for p in percentages]
        if (not self.radiob.b1.isChecked()) and (not self.radiob.b2.isChecked()):
            self.radiob.b2.setChecked(True)
        clearLayout(self.uplyt)
        
        if self.radiob.b1.isChecked():            
            self.graph = Graph(labels=labels,data=percentages,plot_type='bar' )
            graph_layout = self.graph.create_layout(title=title)
            self.uplyt.addLayout(graph_layout)
        elif self.radiob.b2.isChecked():
            self.graph = Graph(labels=labels,data=percentages,plot_type='pie' )
            graph_layout = self.graph.create_layout(title=title)
            self.uplyt.addLayout(graph_layout)
        # try:
        #     self._static_ax.cla()
        #     now = datetime.datetime.now()
        #     self.now = now.strftime("%m-%d-%YT%H-%M-%S")
        #     self._static_ax.pie(percentages,labels=labels,shadow=False, autopct='%1.f%%',startangle=90)
        #     self._static_ax.set_title( f'Cross Check From {text} WHERE {self.first_column_text} IS {self.combo2.checkedItems}')
        #     self.static_canvas.draw()
        #     self._main.update()
        #     # self.showMaximized()
        #     self.vlayout.update()
        # except:
        #     pass
        
    def get_query_entity_from_combo23(self,text=None):
        '''
        fills entities in combo3 usin the selected item in combo2
        '''
        # empty data frame
        self.info = pd.DataFrame()
        # get checked fileds in combo2 and put them in self.info
        try:
            self.combo2.checkedItems
        except:
            self.combo2.checkedItems = [0]
        combo2_selected_items = []
        for index in self.combo2.checkedItems:
            self.query_text =  self.first_column[0][index]
            combo2_selected_items.append(self.query_text)
            info = self.data.loc[self.data[self.first_column_text] == self.query_text]
            self.info = pd.concat([self.info,info])
            self.combo2.setCurrentIndex(index)

        self.title = f'{self.first_column_text} «« {combo2_selected_items}'
        # print('___________________cmb23')
        # print(self.info)
        # print('___________________cmb23')

        # get selected field in combo3
        self.index = self.combo3.currentIndex()
        print(self.index)
        if self.index <= 0:
            # MessageBox(title='missing entity', message='Selection of a query entity is required!')
            return
        # get string of the selected field
        try:
            text = self.info.columns[self.index]
        except:
            MessageBox(title='missing entity', message='Selection of at least one query entity is required!')
            return
        # print('line212',text)
        # get curresponding values of the selected field
        values = list(self.info[text].values)
        # if vlaue is None
        for i,v in enumerate(values):
            if v!=v:
                values[i]='not_applicable'
        # get the fill values for graphics and report
        self.labels,self.y = np.unique(values,return_counts=True)
        s = np.sum(self.y)
        # construct graphic
        self.percentages = [int(round(100*y_/s)) for y_ in self.y]

        self.create_chart(labels=self.labels,
                            percentages=self.percentages,
                            title=self.title)

        # construct dataframe
        self.df = pd.DataFrame({'Row Labels':self.labels,'Count':self.y,'percentages':["{:.0%}".format(round(np.sum(p))/100) for p in self.percentages]})
        self.df = pd.concat([self.df, pd.DataFrame.from_records([{'Row Labels':'Grand Total','Count':s,'percentages':"{:.0%}".format(int(round(np.sum(self.percentages)))/100)}])])

        self.createTable()