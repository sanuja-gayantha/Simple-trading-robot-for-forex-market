from PyQt5 import QtCore, QtGui, QtWidgets
import threading
import sqlite3
import datetime
from PyQt5.QtWidgets import QMessageBox

import sserver
import server_run 
import tester_run
import login
import report



class Ui_ServerWindow(object):

    def show_information_massage_box(self, title, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.exec_()   


    def funTester(self):
        self.widgetTester.show()


    def funServerOn(self):

        self.widgetTester.hide()

        #open new thread for socket connection
        self.t1 = threading.Thread(target = sserver.main_socket, daemon=True)
        self.t1.start()

        #hide server on button after clicked on it
        self.Algorithm_On.setEnabled(False)

    def funServerOff(self):
        self.actionServer_On.setEnabled(True)
        #t1.exit() 



    def fun_test(self):
        
        #get from date
        self.from_date = self.dateFrom.date()
        self.fdate = self.from_date.toPyDate()

        #get to date
        self.to_date = self.dateTo.date()  
        self.tdate = self.to_date.toPyDate()

        self.fdelta = datetime.timedelta(days = 1)

        while (self.fdate <= self.tdate):
            tester_run.Algo(self.fdate)
            self.fdate = self.fdate + self.fdelta

        

        self.show_information_massage_box("Information", "Data Loded successfully")




    def fun_drop_table(self):
        try:
            connection = sqlite3.connect("7Algo.db")
            cursor = connection.cursor()
            cursor.execute("DROP TABLE if exists EXECUTE_ORDERS")
            cursor.execute("DROP TABLE if exists PREVIOUS_EXECUTE_ORDERS")
            cursor.execute("DROP TABLE if exists ALL_ORDERS")
            
            connection.commit()
            cursor.close()
            connection.close()

        except Exception as e:
            print(e)
        self.show_information_massage_box("Information", "Table Droped successfully")     


    def fun_all_trades(self):
        try:
            connection = sqlite3.connect("7Algo.db")
            cursor = connection.cursor()
            #print("Connected to SQLite")
            dquery = """SELECT * FROM ALL_ORDERS """
            result = cursor.execute(dquery)

            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for columhn_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, columhn_number, QtWidgets.QTableWidgetItem(str(data)))

            connection.commit()
            cursor.close()
            connection.close()


            self.fun_trades_sum()


        except Exception as e:
            print(e)


    def fun_win_trades(self):
        try:
            connection = sqlite3.connect("7Algo.db")
            cursor = connection.cursor()
            #print("Connected to SQLite")
            dquery = """SELECT * FROM EXECUTE_ORDERS WHERE TPIPS >= 0"""
            result = cursor.execute(dquery)

            self.tableWidget.setRowCount(0)

            win_pips = 0
            for row_number, row_data in enumerate(result):
                win_pips += row_data[8]

                self.tableWidget.insertRow(row_number)
                for columhn_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, columhn_number, QtWidgets.QTableWidgetItem(str(data)))


            connection.commit()
            cursor.close()
            connection.close()
            

        except Exception as e:
            print(e)



    def fun_loss_trades(self):
        try:
            connection = sqlite3.connect("7Algo.db")
            cursor = connection.cursor()
            #print("Connected to SQLite")
            dquery = """SELECT * FROM EXECUTE_ORDERS WHERE TPIPS < 0"""
            result = cursor.execute(dquery)

           
            self.tableWidget.setRowCount(0)

            loss_pips = 0
            for row_number, row_data in enumerate(result):
                #print(row_data[8])
                loss_pips += row_data[8]

                self.tableWidget.insertRow(row_number)
                for columhn_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, columhn_number, QtWidgets.QTableWidgetItem(str(data)))



            #print(loss_pips)
            connection.commit()
            cursor.close()
            connection.close()



        except Exception as e:
            print(e)


#-----------------------------------------------------------------------------------------
#calculations for final status
    def fun_trades_sum(self):
        try:
            connection = sqlite3.connect("7Algo.db")
            cursor = connection.cursor()
            #print("Connected to SQLite")
            Pquery = """SELECT * FROM EXECUTE_ORDERS WHERE TPIPS >= 0"""
            Presult = cursor.execute(Pquery)

            win_pips = 0    
            Precords = cursor.fetchall()
            for prow in Precords:
                win_pips += prow[8]

            Nquery = """SELECT * FROM EXECUTE_ORDERS WHERE TPIPS < 0"""
            Nresult = cursor.execute(Nquery)

            loss_pips = 0   
            Nrecords = cursor.fetchall()
            for nrow in Nrecords:
                loss_pips += nrow[8]


            total_win_loss_pips = (win_pips + loss_pips)
            total_win_loss_trades = len(Precords) - len(Nrecords)

            #win_presentage = round(((total_win_loss_pips / (win_pips + abs(loss_pips))) * 100), 2)


                    
            connection.commit()
            cursor.close()
            connection.close()

            self.lblTotalPipsWin.setText(str(win_pips))
            self.lblTotalPipsLoss.setText(str(loss_pips))
            self.lblTotalWin.setText(str(total_win_loss_pips))
            self.lblNumberOfTradesWin.setText(str(len(Precords)))
            self.lblNumberOfTradesLoss.setText(str(len(Nrecords)))
            self.lblTotalWinTrades.setText(str(total_win_loss_trades))

        except Exception as e:
            print(e)

    def fun_clear(self):
        self.tableWidget.setRowCount(0)
        self.lblTotalPipsWin.clear()
        self.lblTotalPipsLoss.clear()
        self.lblTotalWin.clear()
        self.lblNumberOfTradesWin.clear()
        self.lblNumberOfTradesLoss.clear()
        self.lblTotalWinTrades.clear()
        #self.lblWinPresentage.clear()


    def fun_report(self):
        report.report()
        self.show_information_massage_box("Information", "Report generated ")














    def setupUi(self, ServerWindow):
        ServerWindow.setObjectName("ServerWindow")
        ServerWindow.resize(1189, 524)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        ServerWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("qrc_files/Alogo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ServerWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(ServerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widgetTester = QtWidgets.QWidget(self.centralwidget)
        self.widgetTester.setGeometry(QtCore.QRect(10, 10, 1161, 431))
        self.widgetTester.setObjectName("widgetTester")
        self.btnGenerateReport = QtWidgets.QPushButton(self.widgetTester)
        self.btnGenerateReport.setGeometry(QtCore.QRect(10, 310, 161, 31))
        self.btnGenerateReport.setObjectName("btnGenerateReport")
        self.btnWinTrades = QtWidgets.QPushButton(self.widgetTester)
        self.btnWinTrades.setGeometry(QtCore.QRect(10, 230, 161, 30))
        self.btnWinTrades.setObjectName("btnWinTrades")
        self.btnTest = QtWidgets.QPushButton(self.widgetTester)
        self.btnTest.setGeometry(QtCore.QRect(10, 110, 161, 30))
        self.btnTest.setObjectName("btnTest")
        self.btnLossTrades = QtWidgets.QPushButton(self.widgetTester)
        self.btnLossTrades.setGeometry(QtCore.QRect(10, 270, 161, 30))
        self.btnLossTrades.setObjectName("btnLossTrades")
        self.btnDropTable = QtWidgets.QPushButton(self.widgetTester)
        self.btnDropTable.setGeometry(QtCore.QRect(10, 150, 161, 31))
        self.btnDropTable.setObjectName("btnDropTable")
        self.groupBox = QtWidgets.QGroupBox(self.widgetTester)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 161, 81))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 34, 51))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.layoutWidget_2 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget_2.setGeometry(QtCore.QRect(60, 20, 94, 51))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.dateFrom = QtWidgets.QDateEdit(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.dateFrom.setFont(font)
        self.dateFrom.setCalendarPopup(True)
        self.dateFrom.setDate(QtCore.QDate(2020, 1, 1))
        self.dateFrom.setObjectName("dateFrom")

        #add current time to DateEdit
        self.dateFrom.setDateTime(QtCore.QDateTime.currentDateTime())
        
        self.verticalLayout_2.addWidget(self.dateFrom)
        self.dateTo = QtWidgets.QDateEdit(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.dateTo.setFont(font)
        self.dateTo.setCalendarPopup(True)
        self.dateTo.setDate(QtCore.QDate(2020, 1, 1))
        self.dateTo.setObjectName("dateTo")

        #add current time to DateEdit
        self.dateTo.setDateTime(QtCore.QDateTime.currentDateTime())

        self.verticalLayout_2.addWidget(self.dateTo)
        self.btnAllTrades = QtWidgets.QPushButton(self.widgetTester)
        self.btnAllTrades.setGeometry(QtCore.QRect(10, 190, 161, 31))
        self.btnAllTrades.setObjectName("btnAllTrades")
        self.tableWidget = QtWidgets.QTableWidget(self.widgetTester)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setGeometry(QtCore.QRect(200, 20, 951, 251))
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        self.btnGenerateReport_2 = QtWidgets.QPushButton(self.widgetTester)
        self.btnGenerateReport_2.setGeometry(QtCore.QRect(10, 350, 161, 31))
        self.btnGenerateReport_2.setObjectName("btnGenerateReport_2")
        self.groupBoxStatus = QtWidgets.QGroupBox(self.widgetTester)
        self.groupBoxStatus.setGeometry(QtCore.QRect(200, 280, 581, 111))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBoxStatus.setFont(font)
        self.groupBoxStatus.setObjectName("groupBoxStatus")
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBoxStatus)
        self.layoutWidget1.setGeometry(QtCore.QRect(14, 30, 86, 71))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.lblTotalPipsLossValue_4 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblTotalPipsLossValue_4.setFont(font)
        self.lblTotalPipsLossValue_4.setObjectName("lblTotalPipsLossValue_4")
        self.verticalLayout_3.addWidget(self.lblTotalPipsLossValue_4)
        self.layoutWidget2 = QtWidgets.QWidget(self.groupBoxStatus)
        self.layoutWidget2.setGeometry(QtCore.QRect(120, 30, 91, 71))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lblTotalPipsWin = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblTotalPipsWin.setFont(font)
        self.lblTotalPipsWin.setText("")
        self.lblTotalPipsWin.setObjectName("lblTotalPipsWin")
        self.verticalLayout_4.addWidget(self.lblTotalPipsWin)
        self.lblTotalPipsLoss = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblTotalPipsLoss.setFont(font)
        self.lblTotalPipsLoss.setText("")
        self.lblTotalPipsLoss.setObjectName("lblTotalPipsLoss")
        self.verticalLayout_4.addWidget(self.lblTotalPipsLoss)
        self.lblTotalWin = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblTotalWin.setFont(font)
        self.lblTotalWin.setText("")
        self.lblTotalWin.setObjectName("lblTotalWin")
        self.verticalLayout_4.addWidget(self.lblTotalWin)
        self.layoutWidget3 = QtWidgets.QWidget(self.groupBoxStatus)
        self.layoutWidget3.setGeometry(QtCore.QRect(260, 30, 131, 71))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lblTotal = QtWidgets.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblTotal.setFont(font)
        self.lblTotal.setObjectName("lblTotal")
        self.verticalLayout_5.addWidget(self.lblTotal)
        self.lblTotalPipsValue = QtWidgets.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblTotalPipsValue.setFont(font)
        self.lblTotalPipsValue.setObjectName("lblTotalPipsValue")
        self.verticalLayout_5.addWidget(self.lblTotalPipsValue)
        self.lblTotalPipsLossValue_5 = QtWidgets.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblTotalPipsLossValue_5.setFont(font)
        self.lblTotalPipsLossValue_5.setObjectName("lblTotalPipsLossValue_5")
        self.verticalLayout_5.addWidget(self.lblTotalPipsLossValue_5)
        self.layoutWidget4 = QtWidgets.QWidget(self.groupBoxStatus)
        self.layoutWidget4.setGeometry(QtCore.QRect(410, 30, 151, 71))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lblNumberOfTradesWin = QtWidgets.QLabel(self.layoutWidget4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblNumberOfTradesWin.setFont(font)
        self.lblNumberOfTradesWin.setText("")
        self.lblNumberOfTradesWin.setObjectName("lblNumberOfTradesWin")
        self.verticalLayout_6.addWidget(self.lblNumberOfTradesWin)
        self.lblNumberOfTradesLoss = QtWidgets.QLabel(self.layoutWidget4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblNumberOfTradesLoss.setFont(font)
        self.lblNumberOfTradesLoss.setText("")
        self.lblNumberOfTradesLoss.setObjectName("lblNumberOfTradesLoss")
        self.verticalLayout_6.addWidget(self.lblNumberOfTradesLoss)
        self.lblTotalWinTrades = QtWidgets.QLabel(self.layoutWidget4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblTotalWinTrades.setFont(font)
        self.lblTotalWinTrades.setText("")
        self.lblTotalWinTrades.setObjectName("lblTotalWinTrades")
        self.verticalLayout_6.addWidget(self.lblTotalWinTrades)
        ServerWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ServerWindow)
        self.statusbar.setObjectName("statusbar")
        ServerWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(ServerWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1189, 21))
        self.menubar.setObjectName("menubar")
        self.menuExit = QtWidgets.QMenu(self.menubar)
        self.menuExit.setObjectName("menuExit")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        ServerWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(ServerWindow)
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.toolBar.setFont(font)
        self.toolBar.setIconSize(QtCore.QSize(32, 32))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        ServerWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionExit = QtWidgets.QAction(ServerWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(ServerWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.Algorithm_On = QtWidgets.QAction(ServerWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("qrc_files/Algo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Algorithm_On.setIcon(icon1)
        self.Algorithm_On.setObjectName("Algorithm_On")
        self.actionTester = QtWidgets.QAction(ServerWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("qrc_files/line-chart.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTester.setIcon(icon2)
        self.actionTester.setObjectName("actionTester")
        self.menuExit.addAction(self.actionExit)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuExit.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.toolBar.addAction(self.Algorithm_On)
        self.toolBar.addSeparator()
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionTester)
        self.toolBar.addSeparator()

        self.retranslateUi(ServerWindow)


        self.widgetTester.hide()
        self.actionTester.triggered.connect(self.funTester)
        self.Algorithm_On.triggered.connect(self.funServerOn)
        self.btnTest.clicked.connect(self.fun_test)
        self.btnDropTable.clicked.connect(self.fun_drop_table)
        self.btnAllTrades.clicked.connect(self.fun_all_trades)
        self.btnWinTrades.clicked.connect(self.fun_win_trades)
        self.btnLossTrades.clicked.connect(self.fun_loss_trades)
        self.btnGenerateReport_2.clicked.connect(self.fun_clear)
        self.btnGenerateReport.clicked.connect(self.fun_report)
        #self.actionExit.triggered.connect(self.fun_close)

        #self.actionLogout.triggered.connect(self.funLogout)












        QtCore.QMetaObject.connectSlotsByName(ServerWindow)

    def retranslateUi(self, ServerWindow):
        _translate = QtCore.QCoreApplication.translate
        ServerWindow.setWindowTitle(_translate("ServerWindow", "7Algo "))
        self.btnGenerateReport.setText(_translate("ServerWindow", "Generate Report"))
        self.btnWinTrades.setText(_translate("ServerWindow", "Win Trades"))
        self.btnTest.setText(_translate("ServerWindow", "Test"))
        self.btnLossTrades.setText(_translate("ServerWindow", "Loss Trades"))
        self.btnDropTable.setText(_translate("ServerWindow", "Drop Table"))
        self.groupBox.setTitle(_translate("ServerWindow", "Date"))
        self.label.setText(_translate("ServerWindow", "From"))
        self.label_2.setText(_translate("ServerWindow", "To"))
        self.dateFrom.setDisplayFormat(_translate("ServerWindow", "yyyy/M/d"))
        self.dateTo.setDisplayFormat(_translate("ServerWindow", "yyyy/M/d"))
        self.btnAllTrades.setText(_translate("ServerWindow", "All execute trades"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("ServerWindow", "Execute date"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("ServerWindow", "Symbol"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("ServerWindow", "Order type"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("ServerWindow", "TFExecute"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("ServerWindow", "STFExecute"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("ServerWindow", "Open "))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("ServerWindow", "STFClose"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("ServerWindow", "Close"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("ServerWindow", "TPips"))
        self.btnGenerateReport_2.setText(_translate("ServerWindow", "Clear"))
        self.groupBoxStatus.setTitle(_translate("ServerWindow", "Status"))
        self.label_3.setText(_translate("ServerWindow", "Tota Win"))
        self.label_4.setText(_translate("ServerWindow", "Total Loss"))
        self.lblTotalPipsLossValue_4.setText(_translate("ServerWindow", "Total Win / Loss"))
        self.lblTotal.setText(_translate("ServerWindow", "Number Of Trades Win"))
        self.lblTotalPipsValue.setText(_translate("ServerWindow", "Number Of Trades Loss"))
        self.lblTotalPipsLossValue_5.setText(_translate("ServerWindow", "Total Win /  Loss  Trades"))
        self.menuExit.setTitle(_translate("ServerWindow", "File"))
        self.menuAbout.setTitle(_translate("ServerWindow", "Help"))
        self.toolBar.setWindowTitle(_translate("ServerWindow", "toolBar"))
        self.actionExit.setText(_translate("ServerWindow", "Exit"))
        self.actionAbout.setText(_translate("ServerWindow", "About"))
        self.Algorithm_On.setText(_translate("ServerWindow", "Algorithm"))
        self.Algorithm_On.setToolTip(_translate("ServerWindow", "Get connected with trading platform and start trading automatically"))
        self.actionTester.setText(_translate("ServerWindow", "Run Tester"))
        self.actionTester.setToolTip(_translate("ServerWindow", "Test previous data"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ServerWindow = QtWidgets.QMainWindow()
    ui = Ui_ServerWindow()
    ui.setupUi(ServerWindow)
    ServerWindow.show()
    sys.exit(app.exec_())
