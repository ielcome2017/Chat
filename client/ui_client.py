from PyQt5 import QtWidgets, QtCore, QtGui

PORT = 10086
class UI_Client(object):
    def setupUI(self, Form: QtWidgets.QWidget):

        Form.setObjectName("Form")

        # 整体布局
        hboxlayer_1 = QtWidgets.QHBoxLayout()

        # set ip
        self.lb_ip = QtWidgets.QLabel("服务器IP：")
        self.txt_ip = QtWidgets.QLineEdit("localhost")

        self.lb_port = QtWidgets.QLabel("服务器端口:")
        self.txt_port = QtWidgets.QLineEdit(str(PORT))
        self.btn_set = QtWidgets.QPushButton("连接")
        self.btn_set.setObjectName("btnSet")
        self.btn_close = QtWidgets.QPushButton("关闭")
        self.btn_close.setObjectName("btnClose")

        ip_hboxlayer = QtWidgets.QHBoxLayout()
        for item in [self.lb_ip, self.txt_ip]:
            ip_hboxlayer.addWidget(item)
        port_hboxlayer = QtWidgets.QHBoxLayout()
        for item in [self.lb_port, self.txt_port, self.btn_set, self.btn_close]:
            port_hboxlayer.addWidget(item)
        # hboxlayer.addWidget(self.lb_ip)
        # hboxlayer.addWidget(self.txt_ip)
        # hboxlayer.addWidget(self.btn_setip)

        # 用户列表
        vboxlayer_1 = QtWidgets.QVBoxLayout()
        self.lb_userlist= QtWidgets.QLabel()
        self.lv_userlist = QtWidgets.QListView()
        vboxlayer_1.addWidget(self.lb_userlist)
        vboxlayer_1.addWidget(self.lv_userlist)

        #设置用户名
        user_hboxlayer = QtWidgets.QHBoxLayout()
        self.lb_name = QtWidgets.QLabel("用户名")
        self.txt_name = QtWidgets.QLineEdit("default")
        self.btn_name = QtWidgets.QPushButton("重命名")
        self.btn_name.setObjectName("btnName")
        for item in [self.lb_name, self.txt_name, self.btn_name]:
            user_hboxlayer.addWidget(item)

        # 聊天记录
        vboxlayer_2 = QtWidgets.QVBoxLayout()
        self.lb_msg = QtWidgets.QLabel()
        self.tbrs_msg = QtWidgets.QTextEdit()

        # ip, port控件添加
        vboxlayer_2.addLayout(ip_hboxlayer)
        vboxlayer_2.addLayout(port_hboxlayer)
        vboxlayer_2.addLayout(user_hboxlayer)
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
        self.btn_name.setText(_translate("Form", "重命名"))