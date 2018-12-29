from PyQt5.QtNetwork import QTcpServer
from src.server.tools import *

from src.server.tools.thread_ import Thread


class TcpServer(QTcpServer):
    sign_server_recv = pyqtSignal(str, object, object)
    sign_send = pyqtSignal(str, object)

    def __init__(self, parent=None):
        super(TcpServer, self).__init__(parent)

        self.sip_list = []

    def incomingConnection(self, sip_voidptr):
        if sip_voidptr not in self.sip_list:
            self.sip_list.append(sip_voidptr)
        thread = Thread(sip_voidptr, self)

        thread.sign_thread_recv.connect(self.sign_server_recv)
        thread.sign_recv.connect(self.slot_recv)

        self.sign_send.connect(thread.sign_thread_send)

        thread.start()

    def slot_recv(self, event_id, event_msg):
        self.sign_send.emit(event_id, event_msg)