from PyQt5 import QtWidgets
from PyQt5.QtNetwork import QHostAddress

import sys
sys.path.insert(0, "/home/lee/Project/Chat/")    # 把上级目录添加到环境变量中

print(sys.path)

from server.src.tools.tcpserver import TcpServer
from server.src.ui.ui_server import UI_Server

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