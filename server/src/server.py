from PyQt5 import QtWidgets
from PyQt5.QtNetwork import QHostAddress

import sys
sys.path.insert(0, "../../")    # 把上级目录添加到环境变量中

from server.src.tools.tcpserver import TcpServer
from server.src.ui.ui_server import UI_Server

PORT = 10086


class Server(QtWidgets.QWidget, UI_Server):

    def __init__(self, parent=None):
        super(Server, self).__init__(parent)
        self.setupUI(self)

        ss = TcpServer(self)
        # 绑定地址，端口
        ss.listen(QHostAddress("0.0.0.0"), PORT)

        # tcpServer接受到信息，在界面表示出来，就绑定slot_recv，但是转发那一层就不用在这里表示出来了
        ss.sign_server_recv.connect(self.slot_recv)

    def slot_recv(self, event_id, event_msg, socket_id):
        user_name, msg = event_msg
        data = "%s: %s"%(user_name, msg)
        self.tbrs_msg.append(data)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlg = Server()
    dlg.show()
    sys.exit(app.exec_())