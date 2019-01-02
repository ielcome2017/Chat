"""
避免与系统的包冲突，因此文件名为thread_
"""
from PyQt5.QtCore import QThread, pyqtSignal

from client.src.tools.tcpsocket import TcpSocket


class Thread(QThread):

    sign_thread_recv = pyqtSignal(str, object)

    sign_thread_send = pyqtSignal(str, object)

    def __init__(self, parent=None):
        super(Thread, self).__init__(parent)

    def run(self):
        socket = TcpSocket()
        socket.sign_recv.connect(self.sign_thread_recv)
        self.sign_thread_send.connect(socket.sign_send)

        self.sign_thread_send.connect(socket.sign_send)

        self.exec_()
