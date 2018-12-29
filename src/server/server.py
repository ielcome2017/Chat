from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtNetwork import QHostAddress

from src.server.tools.tcpserver import TcpServer
from src.server.ui.ui_server import UI_Server


PORT = 10086


class Server(QtWidgets.QWidget, UI_Server):

    def __init__(self, parent=None):
        super(Server, self).__init__(parent)
        self.setupUI(self)

        ss = TcpServer(self)
        ss.listen(QHostAddress("0.0.0.0"), PORT)

        ss.sign_server_recv.connect(self.slot_recv)

    def slot_recv(self, event_id, socket_id, event_msg):
        user_name, msg = event_msg
        data = "%s: %s"%(user_name, msg)
        self.tbrs_msg.append(data)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlg = Server()
    dlg.show()
    sys.exit(app.exec_())