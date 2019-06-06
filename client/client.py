from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket, QHostAddress, QNetworkInterface
from PyQt5.QtCore import QDataStream, pyqtSignal, QByteArray, QIODevice
from PyQt5.QtGui import QTextCursor

from user import User
# from stream import EmittingStream
from ui_client import UI_Client

PORT = 10086
SIZE_OF_UINT16 = 2
class Client(QtWidgets.QWidget, UI_Client):

    def __init__(self, parent=None):
        super(Client, self).__init__(parent)
        # 界面定义
        self.setupUI(self)
        self.user_model = User()
        self.lv_userlist.setModel(self.user_model)

        # 参数
        self.name = "default"
        # 定义socket
        self.socket = QTcpSocket()
        self.socket.connectToHost("localhost", PORT)
        self.socket.readyRead.connect(self.slot_readyRead)
        print("socket 接口打开")

        self.addr = "127.0.0.1"
        addr = QNetworkInterface.allAddresses()
        for a in addr:
            if a != QHostAddress.LocalHost and a.toIPv4Address():
                self.addr = a.toString()
                break
        

    def slot_readyRead(self):
        min_block_size = SIZE_OF_UINT16

        while self.socket.state() == QAbstractSocket.ConnectedState:
            stream = QDataStream(self.socket)
            if self.socket.bytesAvailable() >= min_block_size:
                nextblock_size = stream.readUInt16()
            else:
                break
            if nextblock_size < min_block_size:
                break
            event_id = stream.readQString()
            event_msg = stream.readQVariantList()
            self.recv(event_id, event_msg)
    
    def slot_send(self, event_id, event_msg):
        try:
            print(event_id, event_msg)
            reply = QByteArray()
            stream = QDataStream(reply, QIODevice.WriteOnly)
            stream.writeUInt16(0)
            stream.writeQString(event_id)
            stream.writeQVariantList(event_msg)
            stream.writeUInt16(0)

            stream.device().seek(0)
            stream.writeUInt16(reply.size() - SIZE_OF_UINT16)
            self.socket.write(reply)   
        except Exception as e:
            print(e)

    @pyqtSlot()
    def on_btnSet_clicked(self):
        print("重新连接")
        try:
            self.thread_stoped = True
            ip, port = self.txt_ip.text(), int(self.txt_port.text())
            # self.socket.readyRead.disconnect(self.slot_readyRead)
            self.socket.close()
            self.socket.deleteLater()
            self.socket = QTcpSocket()
            self.socket.connectToHost(ip, port)
            self.socket.readyRead.connect(self.slot_readyRead)
        except Exception as e:
            print(e)
            
    @pyqtSlot()
    def on_btnClose_clicked(self):
        self.socket.close()
        
    @pyqtSlot()
    def on_btnName_clicked(self):
        self.name = self.txt_name.text()
        self.update_name(self.addr)

    def update_name(self, addr):
        name = self.name
        msg = self.txt_input.text()
        event_id = "0002"
        event_msg = [name, addr]
        print("用户名更新为: %s"%self.name)
        self.slot_send(event_id, event_msg)
        

    @pyqtSlot()
    def on_btnSend_clicked(self):
        try:
            name = self.name
            msg = self.txt_input.text()
            event_id = "0001"
            event_msg = [name, msg]
            self.slot_send(event_id, event_msg)
        except Exception as e:
            print(e)


    def recv(self, event_id, event_msg):
        user_name, msg = event_msg
        print(event_id, event_msg)
        if event_id == "0001":
            data = "%s: %s"%(user_name, msg)
            self.tbrs_msg.append(data)
        else:
            user = "%s: %s"%(user_name, msg)
            self.add_user(user)

    def add_user(self, user):
        print("insert")
        model = self.user_model
        row = model.rowCount()
        model.insertRows(row, 1, user=user)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlg = Client()
    dlg.show()
    sys.exit(app.exec_())