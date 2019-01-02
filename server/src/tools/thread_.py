"""
避免与系统的包冲突，因此文件名为thread_
"""
from PyQt5.QtCore import QThread, pyqtSignal

from server.src.tools.tcpsocket import TcpSocket


class Thread(QThread):
    sign_recv = pyqtSignal(str, object)
    sign_thread_recv = pyqtSignal(str, object, object)

    sign_thread_send = pyqtSignal(str, object)

    def __init__(self, socket_id, parent=None):
        super(Thread, self).__init__(parent)
        self.socket_id = socket_id

        self.sign_recv.connect(self.slot_recv)


    def run(self):
        socket = TcpSocket(self.socket_id)
        if not socket.setSocketDescriptor(self.socket_id):
            return
        socket.sign_recv.connect(self.sign_recv)

        self.sign_thread_send.connect(socket.sign_send)

        self.exec_()

    def slot_recv(self, event_id, event_msg):
        self.sign_thread_recv.emit(event_id, self.socket_id, event_msg)