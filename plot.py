#!/usr/bin/python

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as MplBackend

class Display(QMainWindow):
    def __init__(self, data, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('halp')

        self.frame = QWidget()

        self.mpl_fig = Figure((5, 5))
        self.mpl_surface = MplBackend(self.mpl_fig)
        v = QVBoxLayout()
        v.addWidget(self.mpl_surface)
        self.frame.setLayout(v)
        self.setCentralWidget(self.frame)

        self.ax = self.mpl_fig.add_subplot(1, 1, 1)
        self.ax.plot(data)

data = []
with open(sys.argv[1], "r") as f:
    for x in f.readlines():
        x = x.rstrip('\n')
        x = x.rstrip('\r')
        x = x.rstrip()
        x = x.split(',')
        x = [y.rstrip(',') for y in x]
        x = [int(y) for y in x]
        data.append(x[1])

#plt.plot(data)
#plt.show()

app = QApplication(sys.argv)
d = Display(data)
d.show()
app.exec_()
