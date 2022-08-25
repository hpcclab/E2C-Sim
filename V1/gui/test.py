from PyQt5 import QtWidgets, QtCore, QtGui

class Model(QtGui.QStandardItemModel):

    def __init__(self, rows, columns, parent = None):
        super().__init__(rows, columns, parent)
        self._editable = True

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        flags = super().flags(index)
        if not self._editable:
            flags = flags &~ QtCore.Qt.ItemIsEditable
        return flags

    def setEditable(self, editable):
        print(editable)
        self._editable = editable

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    model = Model(4, 3)

    widget = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout()
    
    view = QtWidgets.QTableView()
    view.setModel(model)
    view.show()

    checkBox = QtWidgets.QCheckBox("Editable")
    checkBox.setChecked(True)
    checkBox.clicked.connect(model.setEditable)

    layout.addWidget(view)
    layout.addWidget(checkBox)
    widget.setLayout(layout)
    widget.show()
    
    app.exec()