from PyQt5 import QtWidgets, QtCore, QtGui


class UI_Client(object):
    def setupUI(self, Form: QtWidgets.QWidget):

        Form.setObjectName("Form")

        # 整体布局
        hboxlayer_1 = QtWidgets.QHBoxLayout()

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

        # 输入信息
        hboxlayer_2 = QtWidgets.QHBoxLayout()
        self.txt_input = QtWidgets.QLineEdit()
        self.btn_send = QtWidgets.QPushButton()
        self.btn_send.setObjectName("btnSend")
        hboxlayer_2.addWidget(self.txt_input, stretch=5)
        hboxlayer_2.addWidget(self.btn_send, stretch=1)

        vboxlayer_3 = QtWidgets.QVBoxLayout()
        vboxlayer_3.addLayout(vboxlayer_2)
        vboxlayer_3.addLayout(hboxlayer_2)

        hboxlayer_1.addLayout(vboxlayer_1, stretch=2)
        hboxlayer_1.addLayout(vboxlayer_3, stretch=3)

        Form.setLayout(hboxlayer_1)
        Form.resize(500, 400)

        self.retranslateUI(Form)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUI(self, Form: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Client"))
        self.lb_userlist.setText(_translate("Form", "用户列表"))
        self.lb_msg.setText(_translate("Form", "聊天记录"))

        self.btn_send.setText(_translate("Form", "Send"))