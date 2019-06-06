from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork
from PyQt5.QtCore import pyqtSlot,pyqtSignal, QByteArray, QDataStream


class UI_Server(object):

    def setupUI(self, Form: QtWidgets.QWidget):

        Form.setObjectName("Form")

        # 用户列表
        vboxlayer_1 = QtWidgets.QVBoxLayout()
        self.lb_userlist= QtWidgets.QLabel()
        self.lv_userlist = QtWidgets.QListView()
        vboxlayer_1.addWidget(self.lb_userlist)
        vboxlayer_1.addWidget(self.lv_userlist)

        # 聊天记录
        vboxlayer_2 = QtWidgets.QVBoxLayout()
        self.lb_msg = QtWidgets.QLabel()
        self.tbrs_msg = QtWidgets.QTextBrowser()
        vboxlayer_2.addWidget(self.lb_msg)
        vboxlayer_2.addWidget(self.tbrs_msg)


        hboxlayer_1 = QtWidgets.QHBoxLayout()
        hboxlayer_1.addLayout(vboxlayer_1, stretch=2)
        hboxlayer_1.addLayout(vboxlayer_2, stretch=3)

        Form.setLayout(hboxlayer_1)
        Form.resize(500, 400)

        self.retranslateUI(Form)

        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUI(self, Form: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Server"))
        self.lb_userlist.setText(_translate("Form", "用户列表"))
        self.lb_msg.setText(_translate("Form", "聊天记录"))


