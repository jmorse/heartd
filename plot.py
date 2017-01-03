#!/usr/bin/python

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as MplBackend

from heart import Heart

data = []
for x in range(1000):
    data.append(512)

heart = Heart()
heart.connect()
heart.setblocking(False)

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
        self.ax.set_ylim(300, 850)
        self.ax.plot(data)

        # Magically make us redraw every .1s
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def update(self):
        global data # yeah

        newsamples = []
        while True:
            samp = heart.read_sample()
            if samp == None:
                break
            newsamples.append(samp)

        numsamps = len(newsamples)
        data = data[numsamps:]
        newsamples = [x.value for x in newsamples]
        data.extend(newsamples)

        self.ax.clear()
        self.ax.set_ylim(300, 850)
        self.ax.plot(data)
        self.mpl_surface.draw()

app = QApplication(sys.argv)
d = Display(data)
d.show()
app.exec_()
