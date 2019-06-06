"""
避免与系统的包冲突，因此文件名为thread_
"""
from PyQt5.QtCore import QThread, pyqtSignal

from tcpsocket import TcpSocket

class Thread(QThread):
    """
    sign_thread_recv信号向上连接tcpServer中的sign_server_recv函数，下接tcpSocket中的sign_recv信号
    sign_thread_send信号从上得到信息，发送给socket的sign_send信号
    """
    sign_thread_recv = pyqtSignal(str, object, object)
    sign_thread_send = pyqtSignal(str, object)

    def __init__(self, socket_id, parent=None):
        super(Thread, self).__init__(parent)
        self.socket_id = socket_id

    def run(self):
        print("thread running......")
        socket = TcpSocket(self.socket_id)
        if not socket.setSocketDescriptor(self.socket_id):
            return

        # socket中sing_recv信号被触发，就意味着得到信息，传递给线程，线程再交付给tcpServer
        socket.sign_recv.connect(self.sign_thread_recv)
        # 线程得到tcpServer中的信息，然后交付给socket发送出去
        self.sign_thread_send.connect(socket.sign_send)
        socket.disconnected.connect(self.finished)
        socket.disconnected.connect(self.close)

        self.exec_()

    def close(self):
        self.exit()
        print("thread running state is: ", self.isRunning())

