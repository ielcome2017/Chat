from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QDataStream, QByteArray, QIODevice, pyqtSlot, QThread
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket

from src.client.ui.ui_client import UI_Client
from src.client.tools.thread_ import Thread


class Client(QtWidgets.QWidget, UI_Client):

    sign_recv = pyqtSignal(str, object)
    sign_send = pyqtSignal(str, object)

    def __init__(self, parent=None):
        super(Client, self).__init__(parent)
        self.setupUI(self)

        self.start_thread()

        self.sign_recv.connect(self.recv)

    def start_thread(self):
        thread = Thread(self)
        thread.sign_thread_recv.connect(self.sign_recv)
        self.sign_send.connect(thread.sign_thread_send)
        thread.start()

    @pyqtSlot()
    def on_btnSend_clicked(self):
        name = "default"
        msg = self.txt_input.text()
        event_id = "0001"
        event_msg = [name, msg]
        print(event_msg)
        self.sign_send.emit(event_id, event_msg)

    def recv(self, event_id, event_msg):
        user_name, msg = event_msg
        data = "%s: %s"%(user_name, msg)
        self.tbrs_msg.append(data)






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlg = Client()
    dlg.show()
    sys.exit(app.exec_())