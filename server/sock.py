from PyQt5.QtCore import QThread, QMutex
from PyQt5.QtNetwork import  QTcpSocket, QAbstractSocket
from PyQt5.QtCore import QDataStream, pyqtSignal, QByteArray, QIODevice

SIZE_OF_UINT16 = 2
class Thread(QThread):
    """
    sign_thread_recv信号向上连接tcpServer中的sign_server_recv函数，下接tcpSocket中的sign_recv信号
    sign_thread_send信号从上得到信息，发送给socket的sign_send信号
    """
    sign = pyqtSignal(str, object)
    sign_stop = pyqtSignal()

    def __init__(self, socket_id, parent=None):
        super(Thread, self).__init__(parent)
        self.socket_id = socket_id
        self.socket = QTcpSocket()
        
        self.stoped = False
        self.m_lock = QMutex()
        self.sign.connect(self.slot_send)
        self.finished.connect(self.stop)
        

    def stop(self):
        print("the thread running state is: ", self.isRunning())

    def run(self):
        if not self.socket.setSocketDescriptor(self.socket_id):
            return
        min_block_size = SIZE_OF_UINT16
        print("connected")
        while not self.stoped:
            try:
                state = self.socket.state() == QAbstractSocket.ConnectedState
                if not state:
                    self.stoped = True
                    return
                stream = QDataStream(self.socket)
                # 如果可接受字符串比这个更小就直接丢弃
                if self.socket.waitForReadyRead() and self.socket.bytesAvailable() >= min_block_size:
                    # 读取接下来信息流的长度，因为信息流第一个位置写入的是长度，为UInt16类型
                    nextblock_size = stream.readUInt16()
                else:
                    continue
                if nextblock_size == 0:
                    self.socket.waitForReadyRead()
                # 如果 nextblock_size 比这个还小说明接受错误
                if nextblock_size <= min_block_size:

                    continue
                event_id = stream.readQString()
                event_msg = stream.readQVariantList()

                # 读取结尾
                _ = stream.readUInt16()

                self.sign.emit(event_id, event_msg)
            except Exception as e:
                print(e)


    def slot_send(self, event_id, event_msg):
        # 定义一个字节列表
        reply = QByteArray()
        # 使用QDateaStream向列表写入
        stream = QDataStream(reply, QIODevice.WriteOnly)
        # 为什么接受的最小长度是2个字节，是因为这里收尾都写入了0
        stream.writeUInt16(0)
        stream.writeQString(event_id)
        stream.writeQVariantList(event_msg)
        stream.writeUInt16(0)

        # 寻找到首部的0，写入字节流的真实长度
        stream.device().seek(0)
        stream.writeUInt16(reply.size() - SIZE_OF_UINT16)

        # 发送
        self.socket.write(reply)
