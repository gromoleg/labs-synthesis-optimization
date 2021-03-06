import sys

if sys.version_info[0] == 2:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
else:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
from labs.lab3 import methods


class LabWidget(QWidget):
    def __init__(self):
        super(LabWidget, self).__init__()
        layout = QVBoxLayout()
        tabs = QTabWidget()
        for method in sorted(methods.methods_list, key=lambda method: method.name):
            tabs.addTab(method(), method.name)
        layout.addWidget(tabs)
        self.setLayout(layout)
