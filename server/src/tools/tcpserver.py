from PyQt5.QtNetwork import QTcpServer
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from server.src.tools.thread_ import Thread


class TcpServer(QTcpServer):
    """
    sign_server_recv 该信号被thread的sign_thread_recv连接， 当sign_thread_recv信号被触发，该信号就触发
    sign_send 该信号在slot_recv函数中被触发， 因为slot_recv接受来自所有thread传来的信息，它要把信息转发给所有的thread, 因此其连接着thread.sign_thread_send
    tcpServer.slot_recv <-- thread.sign_thread_recv [thread1, thread2, ...] (箭头表示数据刘方向)
    slot_recv --> sign_send --> sign_thread_send [thread1, thread2, ...]
    """
    sign_server_recv = pyqtSignal(str, object, object)
    sign_send = pyqtSignal(str, object)

    def __init__(self, parent=None):
        super(TcpServer, self).__init__(parent)
        self.sip_list = []
        # 转发信号，得到信息就向所有线程转发
        self.sign_server_recv.connect(self.slot_recv)

    def incomingConnection(self, sip_voidptr):
        if sip_voidptr not in self.sip_list:
            self.sip_list.append(sip_voidptr)

        # 开启一个线程
        thread = Thread(sip_voidptr, self)
        thread.start()

        # thread中接受信息的信号连接到tcpServer中的接受信号
        thread.sign_thread_recv.connect(self.sign_server_recv)
        # 转发信号要连接到各个线程中的发送信号
        self.sign_send.connect(thread.sign_thread_send)

    def slot_recv(self, event_id, event_msg):
        self.sign_send.emit(event_id, event_msg)