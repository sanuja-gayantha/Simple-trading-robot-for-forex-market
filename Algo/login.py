from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import AlgoServer

class Ui_LoginWindow(object):


    def show_warning_massage_box(self, title, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        #msgBox.setStandardButtons(QtWidgets.QMessageBox.OK)
        msgBox.exec_()

    def show_information_massage_box(self, title, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.exec_()        


    def user_login_check(self):
        uname = self.txtUserName.text()
        upassword = self.txtPassword.text()
        #print(uname ,upassword)
        if((len(uname) > 0) and (len(upassword) > 0)):
            connection = sqlite3.connect("7Algo.db")
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE if not exists USER_LOGIN (USER_NAME TEXT NOT NULL, PASSWORD TEXT)")

            #checking data equality
            result = cursor.execute("SELECT * FROM USER_LOGIN WHERE USER_NAME = ? AND PASSWORD = ?", (uname, upassword))
            if (len(result.fetchall()) > 0):
                #print("User found !")

                #calling 7AlgoServer window
                self.AlgoServerWindow = QtWidgets.QMainWindow()
                self.ui1 =  AlgoServer.Ui_ServerWindow()
                self.ui1.setupUi(self.AlgoServerWindow)
                LoginWindow.hide()
                self.AlgoServerWindow.show()
                self.show_information_massage_box("Information", "Login successful")



            else:
                self.show_warning_massage_box("Warrning", "Invalid User Name or Password")

            cursor.close()
            connection.close()

            self.txtUserName.clear()
            self.txtPassword.clear()

        else:
            self.show_warning_massage_box("Warrning", "Some fields are empty !!!")
        self.txtUserName.clear()
        self.txtPassword.clear()



    def create_user_login(self):
        Aname = self.txtCreateUserAdminName.text()
        Apassword = self.txtCreateUserAdminPassword.text()
        ucname = self.txtCreateUserName.text()
        ucpassword = self.txtCreateUserPassword.text()
        ucrpassword = self.txtCreatUserReEnterPassword.text()
        
        if((len(ucname) > 0) and (len(ucpassword) > 0) and (len(ucrpassword) > 0) and (len(Aname) > 0) and (len(Apassword) > 0)):

            connection = sqlite3.connect("7Algo.db")
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE if not exists USER_LOGIN (USER_NAME TEXT NOT NULL, PASSWORD TEXT)")

            #checking admin
            result = cursor.execute("SELECT * FROM USER_LOGIN WHERE USER_NAME = ? AND PASSWORD = ?", (Aname, Apassword))
            if (len(result.fetchall()) > 0):
                if (ucpassword == ucrpassword and 'Admin' == Aname):

                    #create if there is no table called USER_LOGIN in database
                    connection.execute("CREATE TABLE if not exists USER_LOGIN (USER_NAME TEXT NOT NULL, PASSWORD TEXT)")

                    #insert values to database table
                    connection.execute("INSERT INTO USER_LOGIN VALUES(?, ?)", (ucname, ucpassword))
                    connection.commit()
                    connection.close()
                    self.show_information_massage_box("Information", "Create account successfully")



                else:
                    self.show_warning_massage_box("Warrning", "Admin data are not match !!!")
                self.txtCreateUserAdminName.clear()
                self.txtCreateUserAdminPassword.clear()
                self.txtCreateUserName.clear()
                self.txtCreateUserPassword.clear()
                self.txtCreatUserReEnterPassword.clear()


            else:
                self.show_warning_massage_box("Warrning", "Admin data are not match !!!")

            self.txtCreateUserAdminName.clear()
            self.txtCreateUserAdminPassword.clear()
            self.txtCreateUserName.clear()
            self.txtCreateUserPassword.clear()
            self.txtCreatUserReEnterPassword.clear()

        else:
            self.show_warning_massage_box("Warrning", "Some fields are empty !!!")
        self.txtCreateUserAdminName.clear()
        self.txtCreateUserAdminPassword.clear()
        self.txtCreateUserName.clear()
        self.txtCreateUserPassword.clear()
        self.txtCreatUserReEnterPassword.clear()


    def delete_user_login(self):
        Aname = self.txtDeleteUserAdminName.text()
        Apassword = self.txtDeleteUserAdminPassword.text()
        ucname = self.txtDeleteUserUserName.text()

        
        if((len(ucname) > 0)  and (len(Aname) > 0) and (len(Apassword) > 0)):

            connection = sqlite3.connect("7Algo.db")
            cursor = connection.cursor()

            #create if there is no table called USER_LOGIN in database
            cursor.execute("CREATE TABLE if not exists USER_LOGIN (USER_NAME TEXT NOT NULL, PASSWORD TEXT)")

            #checking admin
            result = cursor.execute("SELECT * FROM USER_LOGIN WHERE USER_NAME = ? AND PASSWORD = ?", (Aname, Apassword))
            if (len(result.fetchall()) > 0):
                if ('Admin' == Aname):

                    #checking user avalability
                    result1 = cursor.execute("SELECT * FROM USER_LOGIN WHERE USER_NAME = ? ",(Aname,))
                    if (len(result1.fetchall()) > 0):

                        #delete values from database
                        cursor.execute("DELETE from USER_LOGIN WHERE USER_NAME = ? ", (ucname,))
                        connection.commit()
                        connection.close()
                        self.show_information_massage_box("Information", "User account delete successfully")

                    else:
                        self.show_warning_massage_box("Warrning", "User not found !!!")
                    self.txtDeleteUserAdminName.clear()
                    self.txtDeleteUserAdminPassword.clear()
                    self.txtDeleteUserUserName.clear()


                else:
                    self.show_warning_massage_box("Warrning", "Admin data are not match !!!")
                self.txtDeleteUserAdminName.clear()
                self.txtDeleteUserAdminPassword.clear()
                self.txtDeleteUserUserName.clear()


            else:
                self.show_warning_massage_box("Warrning", "Admin data are not match !!!")
            self.txtDeleteUserAdminName.clear()
            self.txtDeleteUserAdminPassword.clear()
            self.txtDeleteUserUserName.clear()


        else:
            self.show_warning_massage_box("Warrning", "Some fields are empty !!!")
        self.txtDeleteUserAdminName.clear()
        self.txtDeleteUserAdminPassword.clear()
        self.txtDeleteUserUserName.clear()



















    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(378, 475)
        LoginWindow.setMinimumSize(QtCore.QSize(378, 475))
        LoginWindow.setMaximumSize(QtCore.QSize(378, 475))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("qrc_files/Alogo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LoginWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(20, 10, 341, 451))
        self.tabWidget.setMinimumSize(QtCore.QSize(341, 451))
        self.tabWidget.setMaximumSize(QtCore.QSize(341, 451))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(90, 80, 171, 171))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("qrc_files/user.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(80, 20, 171, 51))
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(28)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(30, 260, 271, 131))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.btnLogin = QtWidgets.QPushButton(self.groupBox)
        self.btnLogin.setGeometry(QtCore.QRect(154, 80, 101, 31))
        self.btnLogin.setObjectName("btnLogin")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(15, 50, 241, 23))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.txtPassword = QtWidgets.QLineEdit(self.layoutWidget)
        self.txtPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txtPassword.setObjectName("txtPassword")
        self.horizontalLayout_2.addWidget(self.txtPassword)
        self.layoutWidget_2 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget_2.setGeometry(QtCore.QRect(15, 20, 241, 23))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.txtUserName = QtWidgets.QLineEdit(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.txtUserName.setFont(font)
        self.txtUserName.setObjectName("txtUserName")
        self.horizontalLayout.addWidget(self.txtUserName)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(20, 20, 291, 51))
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(28)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_2.setGeometry(QtCore.QRect(7, 80, 321, 221))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.btnCreateUser = QtWidgets.QPushButton(self.groupBox_2)
        self.btnCreateUser.setGeometry(QtCore.QRect(200, 170, 101, 31))
        self.btnCreateUser.setObjectName("btnCreateUser")
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(14, 20, 291, 136))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_5.addWidget(self.label_8)
        self.txtCreateUserAdminName = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.txtCreateUserAdminName.setFont(font)
        self.txtCreateUserAdminName.setObjectName("txtCreateUserAdminName")
        self.horizontalLayout_5.addWidget(self.txtCreateUserAdminName)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_9 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_6.addWidget(self.label_9)
        self.txtCreateUserAdminPassword = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtCreateUserAdminPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txtCreateUserAdminPassword.setObjectName("txtCreateUserAdminPassword")
        self.horizontalLayout_6.addWidget(self.txtCreateUserAdminPassword)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.txtCreateUserName = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.txtCreateUserName.setFont(font)
        self.txtCreateUserName.setObjectName("txtCreateUserName")
        self.horizontalLayout_4.addWidget(self.txtCreateUserName)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.txtCreateUserPassword = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtCreateUserPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txtCreateUserPassword.setObjectName("txtCreateUserPassword")
        self.horizontalLayout_3.addWidget(self.txtCreateUserPassword)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_10 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_7.addWidget(self.label_10)
        self.txtCreatUserReEnterPassword = QtWidgets.QLineEdit(self.layoutWidget1)
        self.txtCreatUserReEnterPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txtCreatUserReEnterPassword.setObjectName("txtCreatUserReEnterPassword")
        self.horizontalLayout_7.addWidget(self.txtCreatUserReEnterPassword)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_3)
        self.groupBox_3.setGeometry(QtCore.QRect(7, 80, 321, 171))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.btnDeleteUser = QtWidgets.QPushButton(self.groupBox_3)
        self.btnDeleteUser.setGeometry(QtCore.QRect(200, 120, 101, 31))
        self.btnDeleteUser.setObjectName("btnDeleteUser")
        self.layoutWidget_8 = QtWidgets.QWidget(self.groupBox_3)
        self.layoutWidget_8.setGeometry(QtCore.QRect(14, 20, 291, 81))
        self.layoutWidget_8.setObjectName("layoutWidget_8")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget_8)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_11 = QtWidgets.QLabel(self.layoutWidget_8)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_8.addWidget(self.label_11)
        self.txtDeleteUserAdminName = QtWidgets.QLineEdit(self.layoutWidget_8)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.txtDeleteUserAdminName.setFont(font)
        self.txtDeleteUserAdminName.setObjectName("txtDeleteUserAdminName")
        self.horizontalLayout_8.addWidget(self.txtDeleteUserAdminName)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_12 = QtWidgets.QLabel(self.layoutWidget_8)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_9.addWidget(self.label_12)
        self.txtDeleteUserAdminPassword = QtWidgets.QLineEdit(self.layoutWidget_8)
        self.txtDeleteUserAdminPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txtDeleteUserAdminPassword.setObjectName("txtDeleteUserAdminPassword")
        self.horizontalLayout_9.addWidget(self.txtDeleteUserAdminPassword)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_13 = QtWidgets.QLabel(self.layoutWidget_8)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_10.addWidget(self.label_13)
        self.txtDeleteUserUserName = QtWidgets.QLineEdit(self.layoutWidget_8)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.txtDeleteUserUserName.setFont(font)
        self.txtDeleteUserUserName.setObjectName("txtDeleteUserUserName")
        self.horizontalLayout_10.addWidget(self.txtDeleteUserUserName)
        self.verticalLayout_2.addLayout(self.horizontalLayout_10)
        self.label_16 = QtWidgets.QLabel(self.tab_3)
        self.label_16.setGeometry(QtCore.QRect(20, 20, 291, 51))
        font = QtGui.QFont()
        font.setFamily("Candara")
        font.setPointSize(28)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.tabWidget.addTab(self.tab_3, "")
        LoginWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LoginWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 378, 21))
        self.menubar.setObjectName("menubar")
        LoginWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LoginWindow)
        self.statusbar.setObjectName("statusbar")
        LoginWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LoginWindow)
        self.tabWidget.setCurrentIndex(0)

        ################### Butten Event ##################################
        self.btnLogin.clicked.connect(self.user_login_check)
        self.btnCreateUser.clicked.connect(self.create_user_login)
        self.btnDeleteUser.clicked.connect(self.delete_user_login)


        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Login"))
        self.label.setText(_translate("LoginWindow", "User Login"))
        self.btnLogin.setText(_translate("LoginWindow", "Login"))
        self.label_4.setText(_translate("LoginWindow", "Password  "))
        self.label_3.setText(_translate("LoginWindow", "User Name"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("LoginWindow", "User Login"))
        self.label_5.setText(_translate("LoginWindow", "Create User Login"))
        self.btnCreateUser.setText(_translate("LoginWindow", "Create"))
        self.label_8.setText(_translate("LoginWindow", "Admin Name       "))
        self.label_9.setText(_translate("LoginWindow", "Admin Password "))
        self.label_7.setText(_translate("LoginWindow", "User Name          "))
        self.label_6.setText(_translate("LoginWindow", "User Password    "))
        self.label_10.setText(_translate("LoginWindow", "Re enter User Password  "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("LoginWindow", "Create User"))
        self.btnDeleteUser.setText(_translate("LoginWindow", "Delete"))
        self.label_11.setText(_translate("LoginWindow", "Admin Name       "))
        self.label_12.setText(_translate("LoginWindow", "Admin Password "))
        self.label_13.setText(_translate("LoginWindow", "User Name          "))
        self.label_16.setText(_translate("LoginWindow", "Delete User Login"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("LoginWindow", "Delete User"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LoginWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(LoginWindow)
    LoginWindow.show()
    sys.exit(app.exec_())
