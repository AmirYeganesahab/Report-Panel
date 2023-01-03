import sys, os, numpy as np, pandas as pd, datetime,matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
# from colors import colors
colors =['#e7f4f3', '#ceeae8', '#aedcd9', '#85cac5', '#5cb9b2','#e6effb', '#cedef7', '#adc9f2', '#84adec', '#5b92e5','#fff4dd', '#ffeabb', '#ffdc8e', '#ffca55', '#ffb81c','#ffe8dd', '#ffd1bc', '#ffb38f', '#ff8d57', '#ff671f','#f8dee0', '#f2bec1', '#e99398', '#ddc064', '#d22630']


def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
    return layout

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
    def __init__(self, parent=None):
        super(Graph, self).__init__(parent)

    def create_layout(self):
        print('create_layout')
        # a figure instance to plot on
        self.figure = plt.figure()
        self.figure.clear()
        
        self.canvas = FigureCanvas(self.figure)
        toolbar = NavigationToolbar(self.canvas,parent=None)
        # creating a Vertical Box layout
        
        layout = QVBoxLayout()
        # layout =clearLayout(layout=layout)
        # adding tool bar to the layout
        layout.addWidget(toolbar)
        # adding canvas to the layout
        layout.addWidget(self.canvas)
        # setting layout to the main window
        self.figure.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2, wspace=0.5, hspace=0.5)
        # self.generate_plot()
        self.canvas.draw()
        print('create_layout')
        return layout
        
    def generate_plot(self,data,labels, plot_type='bar'):
        thisColors = []
        for i,d in enumerate(data):
            dd = int(round(d/4))
            if dd==25:dd=24
            thisColors.append(colors[dd])
        # clearing old figure
        self.figure.clear()
        # create an axis
        labels = [str(l) for l in labels]
        if plot_type=='bar':
            self.figure.clear()
            self.figure.set_tight_layout(tight=True)
            ax = self.figure.add_subplot(111,position=[0, 0, 1, 1])
            ax.format_coord = lambda x, y: ""
            ax.cla()
            # plot data
            ax.bar(labels,data,color=thisColors)
            ax.set_ylim(top=max(data)+25)
            ax.set_xticks(np.arange(len(labels)),labels,rotation=30)
            xlocs = ax.get_xticks()
            for i, v in enumerate(data):
                ax.text(xlocs[i], v + 0.5, f'{v}%')
        elif plot_type=='pie':
            self.figure.clear()
            self.figure.set_tight_layout(tight=True)
            ax = self.figure.add_subplot(111,position=[0, 0, 1, 1])
            ax.format_coord = lambda x, y: ""
            ax.cla()
            # plot data
            patches,_,_= ax.pie(data,labels=labels,shadow=False, autopct='%1.f%%',startangle=0) # refresh canvas
            legend=ax.legend(patches, labels,bbox_to_anchor=(1.5,0.5), loc='right')
            oldLegPos = legend.get_bbox_to_anchor()._bbox
            # print(oldLegPos.bbox)
            legend.set_draggable(state=True,update='loc',use_blit=False)
            
            legend.bbox_to_anchor = oldLegPos
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

class newClass():
    def __init__(self) -> None:
        pass

class left():
    def __init__(self) -> None:
        self.up = newClass()
        self.down = newClass()
        self.controlPanel = newClass()
        self.graph = Graph()
        self.graph_layout = self.graph.create_layout()
        self.reporttableWidget = QTableWidget()
 
class right():
    def __init__(self) -> None:
        self.up = newClass()
        self.down = newClass()
        self.controlPanel = newClass()
        self.graph = Graph()
        self.graph_layout = self.graph.create_layout()
        self.reporttableWidget = QTableWidget()

class ComparisonWindow(QWidget):

    def __init__(self,data=None, parent=None):
        super(ComparisonWindow, self).__init__()
        self.default_dir =os.getcwd()
        self.data = data
        self.initUI()

    def initUI(self):
        self.constructMenues()
        self.left_pannel = left()
        self.right_pannel = right()
        # construct figure plot and table widget
        # construct main window with frames etc.
        self.constructFrames()
        # generate main window with splitters
        splitter = self.constructSplitters()
        # apply splitter on main window
        self.constructWindow(splitter)
        self.showMaximized()
        # self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Comparison')
        self.show()
    
    def constructMenues(self):
        save_file_action = QAction("Save", self)
        save_file_action.setShortcut('Ctrl+S')
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        self.menubar = QMenuBar()
        file_menu = QMenu("&File", self)
        self.menubar.addMenu(file_menu)
        file_menu.addAction(save_file_action)
        file_menu.addAction(exitAction)

    def file_save(self):
        now = datetime.datetime.now()
        self.now = now.strftime("%m-%d-%YT%H-%M-%S")
        try:
            xlsxName = f'Cross_check-{self.now}'
            xlsxName = os.path.join(self.default_dir, xlsxName)
            name = QFileDialog.getSaveFileName(self, 'Save Report File',xlsxName,"xlsx (*.xlsx)")
            try:
                self.df_left.to_excel(name[0]+'_left.xlsx')
                pngName_left = name[0][:-5]+'_left.png'
                self.left_pannel.graph.figure.savefig(pngName_left)
            except:
                pass
            try:
                self.df_right.to_excel(name[0]+'_right.xlsx')
                pngName_right = name[0][:-5]+'_right.png'
                self.right_pannel.graph.figure.savefig(pngName_right)
            except:
                pass
            
            MessageBox(title='File Saved', message=f'table and pie chart saved at {os.path.join(*pngName_left.split("/")[:-1])}')
        except Exception as e:
            print(e)
    
    def constructWindow(self,splitter):
        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.menubar)
        self.vbox.addWidget(splitter)
        self.setLayout(self.vbox)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        
    def constructSplitters(self):
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.left_pannel.up)
        splitter1.addWidget(self.right_pannel.up)
        
        splitter2 = QSplitter(Qt.Horizontal)
        splitter2.addWidget(self.left_pannel.bottom)
        splitter2.addWidget(self.right_pannel.bottom)

        splitter3 = QSplitter(Qt.Horizontal)
        splitter3.addWidget(self.left_pannel.controlPanel)
        splitter3.addWidget(self.right_pannel.controlPanel)
        
        splitter4 = QSplitter(Qt.Vertical)
        splitter4.addWidget(splitter1)
        splitter4.addWidget(splitter2)
        splitter4.addWidget(splitter3)
        
        return splitter4
    
    def constructFrames(self):
        # Layouts for canvas (charts)
        self.tl = QVBoxLayout()
        self.left_radiob = radioButtons()
        self.left_radiob.b1.toggled.connect(self.create_left_chart)
        # self.left_radiob.b2.clicked.connect(self.create_left_chart)
        
        self.tltop = QVBoxLayout()                   
        self.tltop.addWidget(self.left_radiob)
        self.tl.addLayout(self.tltop)
        
        self.tlbottom = QVBoxLayout()
        self.tl.addLayout(self.tlbottom)
        
        self.tr = QVBoxLayout()
        self.right_radiob = radioButtons()
        self.right_radiob.b1.clicked.connect(self.create_right_chart)
        self.right_radiob.b2.clicked.connect(self.create_right_chart)
        
        self.trtop = QVBoxLayout()
        self.trtop.addWidget(self.right_radiob)
        self.trbottom = QVBoxLayout()
        # self.trbottom.addWidget(self.right_pannel.graph)

        self.tr.addLayout(self.trtop)
        self.tr.addLayout(self.trbottom)
        
        # Layouts for tables
        bl = QVBoxLayout()
        bl.addWidget(self.left_pannel.reporttableWidget)
        br = QVBoxLayout()
        br.addWidget(self.right_pannel.reporttableWidget)
        
        # controllers (labes+comos+checkbox)
        (label1l,label2l,label3l), (self.left_pannel.combo1,self.left_pannel.combo2,self.left_pannel.combo3), _= self.__panel__(side='left')
        
        lcontrolpanel1 = QHBoxLayout()
        lcontrolpanel1.addWidget(label1l)
        lcontrolpanel1.addWidget(self.left_pannel.combo1)
        lcontrolpanel1.addWidget(label2l)
        lcontrolpanel1.addWidget(self.left_pannel.combo2)
        lcontrolpanel1.addWidget(label3l)
        lcontrolpanel1.addWidget(self.left_pannel.combo3)
        
        (label1r,label2r,label3r), (self.right_pannel.combo1,self.right_pannel.combo2,self.right_pannel.combo3), (self.left_pannel.box,self.right_pannel.box) = self.__panel__(side='right')
        rcontrolpanel1 = QHBoxLayout()
        rcontrolpanel1.addWidget(label1r)
        rcontrolpanel1.addWidget(self.right_pannel.combo1)
        rcontrolpanel1.addWidget(label2r)
        rcontrolpanel1.addWidget(self.right_pannel.combo2)
        rcontrolpanel1.addWidget(label3r)
        rcontrolpanel1.addWidget(self.right_pannel.combo3)
        
        # construct pannel in an order
        self.lpanel = QVBoxLayout()
        self.lpanel.addLayout(lcontrolpanel1)
        self.lpanel.addWidget(self.left_pannel.box)
        
        self.rpanel = QVBoxLayout()
        self.rpanel.addLayout(rcontrolpanel1)
        self.rpanel.addWidget(self.right_pannel.box)
        
        #Tope Frames
        self.left_pannel.up = QFrame()
        self.left_pannel.up.setFrameShape(QFrame.StyledPanel)
        self.left_pannel.up.setLayout(self.tl)
        
        self.right_pannel.up = QFrame()
        self.right_pannel.up.setFrameShape(QFrame.StyledPanel)
        self.right_pannel.up.setLayout(self.tr)
        
        #Bottom trains
        self.left_pannel.bottom = QFrame()
        self.left_pannel.bottom.setFrameShape(QFrame.StyledPanel)
        self.left_pannel.bottom.setLayout(bl)
        
        self.right_pannel.bottom = QFrame()
        self.right_pannel.bottom.setFrameShape(QFrame.StyledPanel)
        self.right_pannel.bottom.setLayout(br)
        
        self.left_pannel.controlPanel = QFrame()
        self.left_pannel.controlPanel.setFrameShape(QFrame.StyledPanel)
        self.left_pannel.controlPanel.setLayout(self.lpanel)
        
        self.right_pannel.controlPanel = QFrame()
        self.right_pannel.controlPanel.setFrameShape(QFrame.StyledPanel)
        self.right_pannel.controlPanel.setLayout(self.rpanel)
        
        self.tlbottom.addLayout(self.left_pannel.graph_layout)
        self.trbottom.addLayout(self.right_pannel.graph_layout)

    def __panel__(self,side='left'):
        self.ischecked = False
        # =================================
        if side=='left':
            func1 = self.populate_left_combo2
            func2 = self.get_query_entity_from_left_combo23
            func3 = self.populate_left_combo4
        if side=='right':
            func1 = self.populate_right_combo2
            func2 = self.get_query_entity_from_right_combo23
            func3 = self.populate_right_combo4
            
        label1, combo1 = self.pair(func=func1,
                                    text='Column 1 »',
                                    set_cols=True,multiselect=False) 
        combo1.setCurrentIndex(-1)

        label2, combo2 = self.pair(func=func2,
                                    text='Query 1 »',
                                    set_cols=False,multiselect=True) 
        combo2.setCurrentIndex(-1)
        label3, combo3 = self.pair(func=func3,text='Column 2 »',
                                             set_cols=True,
                                             multiselect=False)
        combo3.setCurrentIndex(-1)
        # =================================
        lbox = QCheckBox("Double Cross Check is required!")
        lbox.toggled.connect(self.left_checkbox_clicked)
        
        rbox = QCheckBox("Double Cross Check is required!")
        rbox.toggled.connect(self.right_checkbox_clicked)
        
        return (label1,label2,label3), (combo1,combo2,combo3), (lbox,rbox)
 
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
            cols = [f'{i}. {d}' for i,d in enumerate(self.data.columns)]
            combo.setMaximumWidth(250)
            combo.setModel(QStringListModel(cols))
        combo.setEditable(True)
        line_edit = combo.lineEdit()
        line_edit.setAlignment(Qt.AlignRight)
        line_edit.setReadOnly(True)
        # combo.setEditable(False)
        return label,combo
    
    def left_checkbox_clicked(self):
        cbutton = self.sender()
        self.ischecked = cbutton.isChecked()
        # print(self.ischecked)
        if cbutton.isChecked():
            
            self.hlayout2 = QHBoxLayout()
            self.left_pannel.label4,self.left_pannel.combo4 = self.pair(func=self.get_query_entity_from_left_combo1234,
                                                text='Query 2 »',
                                                set_cols=False,multiselect=True)
            self.left_pannel.combo4.setCurrentIndex(-1)
            self.populate_left_combo4()
            self.left_pannel.label5,self.left_pannel.combo5 = self.pair(func=self.get_guery_entity_from_left_combo12345,
                                                text='Column 3 »',
                                                set_cols=True,multiselect=False)
            self.left_pannel.combo5.setCurrentIndex(-1)
            self.hlayout2.addWidget(self.left_pannel.label4)
            self.hlayout2.addWidget(self.left_pannel.combo4)
            self.hlayout2.addWidget(self.left_pannel.label5)
            self.hlayout2.addWidget(self.left_pannel.combo5)
        else:
            self.hlayout2.removeWidget(self.left_pannel.label4)
            self.left_pannel.label4.deleteLater()
            self.left_pannel.label4 = None

            self.hlayout2.removeWidget(self.left_pannel.combo4)
            self.left_pannel.combo4.deleteLater()
            self.left_pannel.combo4 = None

            self.hlayout2.removeWidget(self.left_pannel.label5)
            self.left_pannel.label5.deleteLater()
            self.left_pannel.label5 = None
            
            self.hlayout2.removeWidget(self.left_pannel.combo5)
            self.left_pannel.combo5.deleteLater()
            self.left_pannel.combo5 = None

        self.lpanel.addLayout(self.hlayout2)
        # self.showMaximized()

    def right_checkbox_clicked(self):
        cbutton = self.sender()
        self.ischecked = cbutton.isChecked()
        # print(self.ischecked)
        if cbutton.isChecked():
            
            self.hlayout3 = QHBoxLayout()
            self.right_pannel.label4,self.right_pannel.combo4 = self.pair(func=self.get_query_entity_from_right_combo1234,
                                                text='Query 2 »',
                                                set_cols=False,multiselect=True)
            self.right_pannel.combo4.setCurrentIndex(-1)
            self.populate_right_combo4()
            self.right_pannel.label5,self.right_pannel.combo5 = self.pair(func=self.get_guery_entity_from_right_combo12345,
                                                text='Column 3 »',
                                                set_cols=True,multiselect=False)
            self.right_pannel.combo5.setCurrentIndex(-1)
            self.hlayout3.addWidget(self.right_pannel.label4)
            self.hlayout3.addWidget(self.right_pannel.combo4)
            self.hlayout3.addWidget(self.right_pannel.label5)
            self.hlayout3.addWidget(self.right_pannel.combo5)
        else:
            self.hlayout3.removeWidget(self.right_pannel.label4)
            self.right_pannel.label4.deleteLater()
            self.right_pannel.label4 = None

            self.hlayout3.removeWidget(self.right_pannel.combo4)
            self.right_pannel.combo4.deleteLater()
            self.right_pannel.combo4 = None

            self.hlayout3.removeWidget(self.right_pannel.label5)
            self.right_pannel.label5.deleteLater()
            self.right_pannel.label5 = None
            
            self.hlayout3.removeWidget(self.right_pannel.combo5)
            self.right_pannel.combo5.deleteLater()
            self.right_pannel.combo5 = None

        self.rpanel.addLayout(self.hlayout3)
        # self.showMaximized()

    def populate_right_combo4(self,text=None):
        '''
        gets selected index in combo 1 and fills combo 2 according to this selection
        '''
        # index of selected field
        index = self.right_pannel.combo3.currentIndex()
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
            self.right_pannel.combo4.items = [str(d) for d in first_column[0]]
            self.right_pannel.combo4.setCurrentIndex(0)
            # self.combo4.checkedItems=[0]
            self.right_pannel.combo4.clear()
            self.right_pannel.combo4.addItems( [str(d) for d in first_column[0]])
            # self.combo4.setCurrentIndex(0)
            # print('_______combo4___',self.combo4.currentIndex())
        except Exception as e:
            print('705___________',e)

        if self.ischecked:
            try:
                self.get_query_entity_from_right_combo1234()
            except Exception as e:
                print(e)
        else:
            try:
                self.get_query_entity_from_right_combo23()
            except:
                pass

    def populate_left_combo4(self,text=None):
        '''
        gets selected index in combo 1 and fills combo 2 according to this selection
        '''
        
        # index of selected field
        index = self.left_pannel.combo3.currentIndex()
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

        if self.ischecked:
            self.left_pannel.combo4.items = [str(d) for d in first_column[0]]
            self.left_pannel.combo4.setCurrentIndex(0)
            # self.combo4.checkedItems=[0]
            self.left_pannel.combo4.clear()
            self.left_pannel.combo4.addItems( [str(d) for d in first_column[0]])
            try:
                self.get_query_entity_from_left_combo1234()
            except Exception as e:
                print('line 408\n',e)
        else:
            try:
                self.get_query_entity_from_left_combo23()
            except Exception as e:
                print('line 412\n', e)

    def populate_left_combo2(self,text):
        '''
        gets selected index in combo 1 and fills combo 2 according to this selection
        '''
        
        # index of selected field
        index = self.left_pannel.combo1.currentIndex()
        # get string of the selected field
        self.first_column_text = self.data.columns[index]
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
        self.left_pannel.combo2.items = [str(d) for d in self.first_column[0]]
        self.left_pannel.combo2.clear()
        self.left_pannel.combo2.addItems(self.left_pannel.combo2.items)
        self.left_pannel.combo2.setCurrentIndex(0)
        ## 
        try:
            self.get_query_entity_from_left_combo23()
        except Exception as e:
            print('line 445 \n', e)
            
    def populate_right_combo2(self,text):
        '''
        gets selected index in combo 1 and fills combo 2 according to this selection
        '''
        # index of selected field
        index = self.right_pannel.combo1.currentIndex()
        # get string of the selected field
        self.first_column_text = self.data.columns[index]
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
        self.right_pannel.combo2.items = [str(d) for d in self.first_column[0]]
        self.right_pannel.combo2.clear()
        self.right_pannel.combo2.addItems(self.right_pannel.combo2.items)
        print('474-----------------------------------')
        self.right_pannel.combo2.setCurrentIndex(0)
        print('476-----------------------------------')
        ## 
        try:
            print('479-----------------------------------')
            self.get_query_entity_from_right_combo23()
            print('481-----------------------------------')
        except:
            pass
        
    def get_query_entity_from_right_combo23(self,text=None):
        
        '''
        fills entities in combo3 usin the selected item in combo2
        '''
        # empty data frame
        self.info = pd.DataFrame()
        # get checked fileds in combo2 and put them in self.info
        try:
            self.right_pannel.combo2.checkedItems
        except:
            self.right_pannel.combo2.checkedItems = [0]

        for index in self.right_pannel.combo2.checkedItems:
            self.query_text =  self.first_column[0][index]
            info = self.data.loc[self.data[self.first_column_text] == self.query_text]
            self.info = pd.concat([self.info,info])
            self.right_pannel.combo2.setCurrentIndex(index)

        # get selected field in combo3
        self.index = self.right_pannel.combo3.currentIndex()
        print(self.index)
        if self.index < 0:
            return
        # get string of the selected field
        try:
            text = self.info.columns[self.index]
        except:
            MessageBox(title='missing entity', message='Selection of at least one query entity is required!')
            return
        # get curresponding values of the selected field
        values = list(self.info[text].values)
        # if vlaue is None
        for i,v in enumerate(values):
            if v!=v:
                values[i]='not_applicable'
        # get the fill values for graphics and report
        self.rlabels,self.ry = np.unique(values,return_counts=True)
        s = np.sum(self.ry)
        # construct graphic
        self.rpercentages = [int(round(100*y_/s)) for y_ in self.ry]

        self.create_right_chart()
    
        # construct dataframe
        self.df_right = pd.DataFrame({'Row Labels':self.rlabels,'Count':self.ry,'percentages':["{:.0%}".format(round(np.sum(p))/100) for p in self.rpercentages]})
        self.df_right = pd.concat([self.df_right, pd.DataFrame.from_records([{'Row Labels':'Grand Total','Count':s,'percentages':"{:.0%}".format(int(round(np.sum(self.rpercentages)))/100)}])])
        try:
            self.create_right_table()
        except Exception as e:
            print('line 582 :',e)
            pass
        
    def get_query_entity_from_left_combo23(self,text=None):
        
        '''
        fills entities in combo3 usin the selected item in combo2
        '''
        try:
            # empty data frame
            self.info = pd.DataFrame()
            # get checked fileds in combo2 and put them in self.info
            try:
                self.left_pannel.combo2.checkedItems
            except:
                self.left_pannel.combo2.checkedItems = [0]

            for index in self.left_pannel.combo2.checkedItems:
                self.query_text =  self.first_column[0][index]
                info = self.data.loc[self.data[self.first_column_text] == self.query_text]
                self.info = pd.concat([self.info,info])
                self.left_pannel.combo2.setCurrentIndex(index)

            # get selected field in combo3
            self.index = self.left_pannel.combo3.currentIndex()
            if self.index <= 0:
                return
            # get string of the selected field
            try:
                text = self.info.columns[self.index]
            except:
                MessageBox(title='missing entity', message='Selection of at least one query entity is required!')
                return
            # get curresponding values of the selected field
            values = list(self.info[text].values)
            # if vlaue is None
            for i,v in enumerate(values):
                if v!=v:
                    values[i]='not_applicable'
            # get the fill values for graphics and report
            self.llabels,self.ly = np.unique(values,return_counts=True)
            s = np.sum(self.ly)
            # construct graphic
            self.lpercentages = [int(round(100*y_/s)) for y_ in self.ly]
            
            self.create_left_chart()
            # construct dataframe
            self.df_left = pd.DataFrame({'Row Labels':self.llabels,'Count':self.ly,'percentages':["{:.0%}".format(round(np.sum(p))/100) for p in self.lpercentages]})
            self.df_left = pd.concat([self.df_left, pd.DataFrame.from_records([{'Row Labels':'Grand Total','Count':s,'percentages':"{:.0%}".format(int(round(np.sum(self.lpercentages)))/100)}])])
            
            self.create_left_table()
        
        except Exception as e:
            print('get_query_entity_from_left_combo23 \n',e)

    def get_query_entity_from_right_combo1234(self,text=None):
        print('get_query_entity_from_combo1234')
        # index of selected field
        index1 = self.right_pannel.combo1.currentIndex()
        if index1<0:return
        # get string of the selected field
        combo2_txt = self.data.columns[index1]
        data1 = pd.DataFrame()
        for index in self.right_pannel.combo2.checkedItems:
            txt = self.right_pannel.combo2.items[index]
            data1 = pd.concat([data1,self.data.loc[self.data[combo2_txt]==txt]])
        
        index2 = self.right_pannel.combo3.currentIndex()
        if index2<0:return
        combo3_txt = self.data.columns[index2]

        try:
            self.right_pannel.combo4.checkedItems
        except:
            self.right_pannel.combo4.checkedItems = [0]

        data2 = pd.DataFrame()
        for index in np.unique(self.right_pannel.combo4.checkedItems):
            if index<0:return
            txt = self.right_pannel.combo4.items[index]
            data2 = pd.concat([data2,data1.loc[data1[combo3_txt]==txt]])
            
        self.right_combo4Table = data2

        self.get_guery_entity_from_right_combo12345()
        
    def get_query_entity_from_left_combo1234(self,text=None):
        print('get_query_entity_from_combo1234')
        # index of selected field
        index1 = self.left_pannel.combo1.currentIndex()
        if index1<0:return
        # get string of the selected field
        combo2_txt = self.data.columns[index1]
        data1 = pd.DataFrame()
        for index in self.left_pannel.combo2.checkedItems:
            txt = self.left_pannel.combo2.items[index]
            data1 = pd.concat([data1,self.data.loc[self.data[combo2_txt]==txt]])
        
        index2 = self.left_pannel.combo3.currentIndex()
        if index2<0:return
        combo3_txt = self.data.columns[index2]

        try:
            self.left_pannel.combo4.checkedItems
        except:
            self.left_pannel.combo4.checkedItems = [0]

        data2 = pd.DataFrame()
        for index in np.unique(self.left_pannel.combo4.checkedItems):
            if index<0:return
            txt = self.left_pannel.combo4.items[index]
            data2 = pd.concat([data2,data1.loc[data1[combo3_txt]==txt]])
            
        self.left_combo4Table = data2

        self.get_guery_entity_from_left_combo12345()

    def get_guery_entity_from_right_combo12345(self):
        
        print('get_query_entity_from_combo12345')
        
        try:
            index5 = self.right_pannel.combo5.currentIndex()
            if index5<0:return
            # self.combo5.setCurrentIndex(0)
        except:
            pass
        # get string of the selected field
        combo5_txt = self.data.columns[index5]
        # print('????????????????',combo5_txt)
        values = list(self.right_combo4Table[combo5_txt].values)
        # if vlaue is None
        for i,v in enumerate(values):
            if v!=v:
                values[i]='not_applicable'
        # get the fill values for graphics and report
        self.rlabels,self.ry = np.unique(values,return_counts=True)
        s = np.sum(self.ry)
        # construct graphic
        self.rpercentages = [100*y_/s for y_ in self.ry]

        self.create_right_chart()
        # construct dataframe
        self.df_right = pd.DataFrame({'Row Labels':self.rlabels,'Count':self.y,'percentages':["{:.0%}".format(round(np.sum(p))/100) for p in self.rpercentages]})
        self.df_right = pd.concat([self.df_right, pd.DataFrame.from_records([{'Row Labels':'Grand Total','Count':s,'percentages':"{:.0%}".format(int(round(np.sum(self.rpercentages)))/100)}])])
        
        self.create_right_table()
    
    def get_guery_entity_from_left_combo12345(self):
        
        print('get_query_entity_from_combo12345')
        try:
            index5 = self.left_pannel.combo5.currentIndex()
            if index5<0:return
            # self.combo5.setCurrentIndex(0)
        except:
            pass
        # get string of the selected field
        combo5_txt = self.data.columns[index5]
        # print('????????????????',combo5_txt)
        values = list(self.left_combo4Table[combo5_txt].values)
        # if vlaue is None
        for i,v in enumerate(values):
            if v!=v:
                values[i]='not_applicable'
        # get the fill values for graphics and report
        self.llabels,self.ly = np.unique(values,return_counts=True)
        s = np.sum(self.ly)
        # construct graphic
        self.lpercentages = [100*y_/s for y_ in self.ly]

        self.create_left_chart()
        # construct dataframe
        self.df_left = pd.DataFrame({'Row Labels':self.llabels,'Count':self.ly,'percentages':["{:.0%}".format(round(np.sum(p))/100) for p in self.lpercentages]})
        self.df_left = pd.concat([self.df_left, pd.DataFrame.from_records([{'Row Labels':'Grand Total','Count':s,'percentages':"{:.0%}".format(int(round(np.sum(self.lpercentages)))/100)}])])

        self.create_left_table()

    def create_left_chart(self):
        percentages = [int(round(p)) for p in self.lpercentages]
        if (not self.left_radiob.b1.isChecked()) and (not self.left_radiob.b2.isChecked()):
            self.left_radiob.b2.setChecked(True)

        if self.left_radiob.b1.isChecked():
            plot_type='bar'
        elif self.left_radiob.b2.isChecked():
            plot_type='pie'
        self.left_pannel.graph.generate_plot(labels=self.llabels,data=percentages,plot_type=plot_type)
            
    def create_right_chart(self):
        percentages = [int(round(p)) for p in self.rpercentages]
        if (not self.right_radiob.b1.isChecked()) and (not self.right_radiob.b2.isChecked()):
            self.right_radiob.b2.setChecked(True)
        
        if self.right_radiob.b1.isChecked(): 
            plot_type='bar'           
            
        elif self.right_radiob.b2.isChecked():
            plot_type='pie'
            
        self.right_pannel.graph.generate_plot(labels=self.rlabels,data=percentages,plot_type=plot_type)

    def create_left_table(self):
        try:
            ncols = len(self.df_left.columns)
            nrows = len(self.df_left)
            self.left_pannel.reporttableWidget.setRowCount(nrows)
            self.left_pannel.reporttableWidget.setColumnCount(ncols)
            self.left_pannel.reporttableWidget.setHorizontalHeaderLabels(self.df_left.columns)
            
            for i,col in enumerate(self.df_left.columns):
                for j,d in enumerate(self.df_left[col]):
                    if type(d)==pd._libs.tslibs.timestamps.Timestamp:
                        d = pd.Timestamp.strftime(d,'%Y-%m-%d %X')
                    try:
                        self.left_pannel.reporttableWidget.setItem(j,i, QTableWidgetItem(str(d)))
                    except Exception as e:
                        print('____________________')
                        print(e)
                        print('____________________')
            self.left_pannel.reporttableWidget.move(0,0)
            print('table created')
        except Exception as e:
            print('in create_left_table \n',e)
    
    def create_right_table(self):
        try:
            ncols = len(self.df_right.columns)
            nrows = len(self.df_right)
            self.right_pannel.reporttableWidget.setRowCount(nrows)
            self.right_pannel.reporttableWidget.setColumnCount(ncols)
            self.right_pannel.reporttableWidget.setHorizontalHeaderLabels(self.df_right.columns)
            
            for i,col in enumerate(self.df_right.columns):
                for j,d in enumerate(self.df_right[col]):
                    if type(d)==pd._libs.tslibs.timestamps.Timestamp:
                        d = pd.Timestamp.strftime(d,'%Y-%m-%d %X')
                    try:
                        self.right_pannel.reporttableWidget.setItem(j,i, QTableWidgetItem(str(d)))
                    except Exception as e:
                        print('____________________')
                        print(e)
                        print('____________________')
                
            self.right_pannel.reporttableWidget.move(0,0)
            print('table created')
        except Exception as e:
            print('in create_right_table \n',e)

    
        
def main():
   app = QApplication(sys.argv)
   ex = ComparisonWindow()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()