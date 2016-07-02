import sys

if sys.version_info[0] == 2:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
else:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
__author__ = 'Oleg Gromyak'
from labs import labs
import constants


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Labs')
        layout = QVBoxLayout()
        tabs = QTabWidget()
        for lab in sorted(labs, key=lambda x: x[0]):
            tabs.addTab(lab[1].LabWidget(), lab[0])
        layout.addWidget(tabs)
        btn_layout = QHBoxLayout()
        btn_about = QPushButton('About')
        btn_about.clicked.connect(lambda: self.mbox_about())
        btn_layout.addWidget(btn_about)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def mbox_about(self):
        mbox = QMessageBox(QMessageBox.Information, 'About', constants.about_information, QMessageBox.Ok, self)
        mbox.setIcon(QMessageBox.Information)
        mbox.setTextFormat(Qt.RichText)
        mbox.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
