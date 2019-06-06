from PyQt5.QtCore import QAbstractListModel, QModelIndex, QVariant, Qt


class User(QAbstractListModel):

    def __init__(self, parent=None):
        super(User, self).__init__(parent)

        self._data = []

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index: QModelIndex, role=None):

        if not index.isValid() or not 0 <= index.row() < self.rowCount():
            return QVariant()

        row = index.row()

        if role == Qt.DisplayRole:
            return self._data[row]
        if role == Qt.EditRole:
            return self._data[row]
        return QVariant()

    def setData(self, index: QModelIndex, value, role=None):
        if role == Qt.EditRole:
            self._data[index.row()] = value
            return True
        return False

    def flags(self, index: QModelIndex):
        flag = super(User, self).flags(index)
        return flag | Qt.ItemIsEditable

    def insertRows(self, positon, rows=1, index=QModelIndex(), user=""):
        self.beginInsertRows(index, positon, positon + rows -1)
        for row in range(rows):
            self._data.insert(positon + row, user)
        self.endInsertRows()
        return True

    def removeRow(self, positon, rows=1, index=QModelIndex()):
        self.beginRemoveRows(index, positon, positon+rows-1)
        for row in range(rows):
            self._data = self._data[: positon] + self._data[positon+rows: ]
        self.endRemoveRows()

        return True