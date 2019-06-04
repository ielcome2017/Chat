from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

import sys
module_path = sys.path.insert(0, "../../")


from client.src.ui.ui_client import UI_Client
from client.src.tools.thread_ import Thread
from client.src.model.user import User


class Client(QtWidgets.QWidget, UI_Client):

    sign_recv = pyqtSignal(str, object)
    sign_send = pyqtSignal(str, object)
    sign_update_name = pyqtSignal(str)

    sign_set = pyqtSignal(str, int)

    def __init__(self, parent=None):
        super(Client, self).__init__(parent)
        # 界面定义
        self.setupUI(self)
        self.user_model = User()
        self.lv_userlist.setModel(self.user_model)

        # 参数
        self.name = "default"
        self.ip = "localhost"
        self.port = self.txt_port.text()

        self.btn_set.clicked.connect(self.on_btnSet_cliced)

        # 开启线程
        self.start_thread()
    
    @pyqtSlot()
    def on_btnSet_cliced(self):
        self.ip = self.txt_ip.text()
        self.port = int(self.txt_port.text())
        self.sign_set.emit(self.ip, self.port)

    def start_thread(self):
        thread = Thread(self)
        thread.start()
        self.sign_set.connect(thread.sign_thread_set)
        # 把用户交互的数据通过sign_send传递给thread.sign_thread_send
        self.sign_send.connect(thread.sign_thread_send)
        # 把其他用户交互的数据通过thread.sign_thread_recv交付给sign_recv
        thread.sign_thread_recv.connect(self.sign_recv)
        self.sign_recv.connect(self.recv)

        # 线程开启后给主界面发送信号，主界面更新信息
        thread.sign_thread_start.connect(self.update_name)

    def update_name(self, addr):
        name = self.name
        msg = self.txt_input.text()
        event_id = "0002"
        event_msg = [name, addr]
        self.sign_send.emit(event_id, event_msg)
        print("finish")

    @pyqtSlot()
    def on_btnSend_clicked(self):
        name = self.name
        msg = self.txt_input.text()
        event_id = "0001"
        event_msg = [name, msg]
        print(event_id)

        self.sign_send.emit(event_id, event_msg)

    def recv(self, event_id, event_msg):
        user_name, msg = event_msg
        if event_id == "0001":

            data = "%s: %s"%(user_name, msg)
            self.tbrs_msg.append(data)

        else:
            user = "%s: %s"%(user_name, msg)
            self.add_user(user)

    def add_user(self, user):
        print("insert")
        model = self.user_model
        row = model.rowCount()
        model.insertRows(row, 1, user=user)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlg = Client()
    dlg.show()
    sys.exit(app.exec_())