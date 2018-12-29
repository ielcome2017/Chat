from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket
from PyQt5.QtCore import QDataStream, pyqtSignal, QByteArray, QIODevice

SIZE_OF_UINT16 = 2


class TcpSocket(QTcpSocket):

    sign_recv = pyqtSignal(str, object)
    sign_send = pyqtSignal(str, object)

    def __init__(self, socket_id, parent=None):
        super(TcpSocket, self).__init__(parent)
        self.socket_id = socket_id

        self.readyRead.connect(self.slot_readyRead)
        self.sign_send.connect(self.slot_send)

    def slot_readyRead(self):
        min_block_size = SIZE_OF_UINT16

        while self.state() == QAbstractSocket.ConnectedState:
            stream = QDataStream(self)
            if self.bytesAvailable() >= min_block_size:
                nextblock_size = stream.readUInt16()
            else:
                break
            if nextblock_size <= min_block_size:
                break
            event_id = stream.readQString()
            event_msg = stream.readQVariantList()

            self.sign_recv.emit(event_id, event_msg)

    def slot_send(self, event_id, event_msg):
        reply = QByteArray()
        stream = QDataStream(reply, QIODevice.WriteOnly)
        stream.writeUInt16(0)
        stream.writeQString(event_id)
        stream.writeQVariantList(event_msg)
        stream.writeUInt16(0)

        stream.device().seek(0)
        stream.writeUInt16(reply.size() - SIZE_OF_UINT16)

        self.write(reply)
