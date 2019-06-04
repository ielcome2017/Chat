"""
避免与系统的包冲突，因此文件名为thread_
"""
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtNetwork import QHostInfo

from client.src.tools.tcpsocket import TcpSocket


class Thread(QThread):

    sign_thread_recv = pyqtSignal(str, object)

    sign_thread_send = pyqtSignal(str, object)

    sign_thread_start = pyqtSignal(object)

    sign_thread_set = pyqtSignal(str, int)

    def __init__(self, parent=None):
        super(Thread, self).__init__(parent)
    def run(self):
        socket = TcpSocket()

        self.sign_thread_set.connect(socket.ip_port_set)
        socket.sign_recv.connect(self.sign_thread_recv)
        self.sign_thread_send.connect(socket.sign_send)

        # 获取ip
        hostname = QHostInfo.localHostName()
        info = QHostInfo.fromName(hostname)

        self.sign_thread_start.emit(info.addresses()[0].toString())
        self.exec_()
