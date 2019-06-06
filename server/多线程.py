from PyQt5.QtCore import QThread, QMutex, pyqtSignal, Qt, QObject
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QTextEdit, QTextEdit, QHBoxLayout, QApplication, \
    QVBoxLayout
from PyQt5.QtGui import QTextCursor
import sys
import time

class Thread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.m_lock = QMutex()
        self.stoped = False
        self.i = 0
    
    def run(self):
        while not self.stoped:
            self.m_lock.lock()
            time.sleep(0.2)
            print(self.i)
            self.i += 1
            self.m_lock.unlock()

    def pause(self):
        self.m_lock.lock()
    
    def resume(self):
        try:
            self.m_lock.unlock()
        except Exception as e:
            print(e)
    
    def stop(self):
        self.stoped = True
        self.quit()
        self.wait()

    def recovery(self):
        self.stoped = False
        self.start()

    def state(self):
        print("the thread running state is: ", self.isRunning())

class ThreadObject(QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.i = 0
        self.stoped = False
    
    def run(self):
        while not self.stoped:
            time.sleep(0.2)
            print(self.i)
            self.i += 1
        

class EmittingStream(QObject):
        text_written = pyqtSignal(str)
        def write(self, text):
            self.text_written.emit(str(text))

class Form(QWidget):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        self.txt_edit = QTextEdit()

        self.btn_start = QPushButton("开始")
        self.btn_pause = QPushButton("暂停")
        self.btn_resume = QPushButton("恢复")
        self.btn_stop = QPushButton("停止")
        self.btn_recovery = QPushButton("重新开始")
        self.btn_state = QPushButton("状态")
        self.btn_del = QPushButton("删除")

        btn_layout = QVBoxLayout()
        for item in [self.btn_start, self.btn_pause, self.btn_resume, self.btn_stop, self.btn_recovery, self.btn_state, self.btn_del]:
            btn_layout.addWidget(item)

        layout = QHBoxLayout()
        layout.addWidget(self.txt_edit)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        sys.stdout = EmittingStream(text_written = self.normal_output_written)
        sys.stderr = EmittingStream(text_written = self.normal_output_written)

        self.th = Thread(self)
        
        self.btn_pause.clicked.connect(self.th.pause)
        self.btn_resume.clicked.connect(self.th.resume)
        self.btn_stop.clicked.connect(self.th.stop)
        self.btn_recovery.clicked.connect(self.th.recovery)
        self.btn_state.clicked.connect(self.th.state)
        self.btn_del.clicked.connect(self.delete)
        self.th.start()

        print("线程开始")
        # 第二种方法
        # self.obj = ThreadObject()
        # self.th = QThread()
        # self.obj.moveToThread(self.th)
        # self.th.started.connect(self.obj.run)
        # self.btn_start.clicked.connect(self.obj.run)
        # self.th.start()
    
    
    def delete(self):
        if not self.th.isRunning():
            self.th.deleteLater()
        print("thread running state is: ", self.th.isRunning())
    
    def normal_output_written(self, text):
        cursor = self.txt_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.txt_edit.setTextCursor(cursor)
        self.txt_edit.ensureCursorVisible()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())