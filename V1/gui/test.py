import sys
from PyQt5.QtWidgets import QWidget, QApplication, qApp, QMainWindow, QGraphicsScene, QGraphicsView, QStatusBar, QGraphicsWidget, QStyle, QGraphicsItem
from PyQt5.QtCore    import Qt, QSizeF, pyqtSignal

class Square(QGraphicsWidget) :

 def __init__(self,*args, name = None, **kvps) :
    super().__init__(*args, **kvps)
    self.radius = 5
    self.name = name
    self.setAcceptHoverEvents(True)
    self.setFlag(self.ItemIsSelectable)
    self.setFlag(self.ItemIsFocusable)

 def sizeHint(self, hint, size):
    size = super().sizeHint(hint, size)
    print(size)
    return QSizeF(50,50)

 def paint(self, painter, options, widget):
    self.initStyleOption(options)
    ink = options.palette.highLight() if options.state == QStyle.State_Selected else options.palette.button()
    painter.setBrush(ink) # ink
    painter.drawRoundedRect(self.rect(), self.radius, self.radius)

 def hoverEnterEvent(self, event) :
    super().hoverEnterEvent(event)
    self.scene().entered.emit(self)
    self.update()

class GraphicsScene(QGraphicsScene) :
 entered = pyqtSignal([QGraphicsItem],[QGraphicsWidget])


class MainWindow(QMainWindow):

 def __init__(self, *args, **kvps) :
    super().__init__(*args, **kvps)
    # Status bar
    self.stat = QStatusBar(self)
    self.setStatusBar(self.stat)
    self.stat.showMessage("Started")
    # Widget(s)
    self.data = GraphicsScene(self)
    self.data.entered.connect(self.itemInfo)
    self.data.focusItemChanged.connect(self.update)
    self.view = QGraphicsView(self.data, self)
    item = Square(name = "A")
    item.setPos( 50,0)
    self.data.addItem(item)
    item = Square(name = "B")
    item.setPos(-50,0)
    self.data.addItem(item)
    self.view.ensureVisible(self.data.sceneRect())
    self.setCentralWidget(self.view)
    # Visibility
    self.showMaximized()

 def itemInfo(self, item):
    print("Here it is -> ", item)

if __name__ == "__main__" :
 # Application
 app = QApplication(sys.argv)
 # Scene Tests
 main = MainWindow()
 main.show()
 # Loop
 sys.exit(app.exec_())