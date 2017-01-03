#!/usr/bin/python

import sys
import argparse
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as MplBackend

from heart import Heart

parser = argparse.ArgumentParser()
parser.add_argument("--rate-limit", help="Limit rate at which we read samples", action='store_true')

args = parser.parse_args()

SAMPLES=3000
MINY=300
MAXY=850
FRAMERATE=30
DISPLAYX=10
DISPLAYY=10

data = []
for x in range(SAMPLES):
    data.append(512)

heart = Heart()
heart.connect()
heart.setblocking(False)

class Display(QMainWindow):
    def __init__(self, data, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('halp')

        self.frame = QWidget()

        self.mpl_fig = Figure((DISPLAYX, DISPLAYY))
        self.mpl_surface = MplBackend(self.mpl_fig)
        v = QVBoxLayout()
        v.addWidget(self.mpl_surface)
        self.frame.setLayout(v)
        self.setCentralWidget(self.frame)

        self.ax = self.mpl_fig.add_subplot(1, 1, 1)
        self.clear_axes()
        self.ax.plot(data)

        # Magically make us redraw every .1s
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000/FRAMERATE)

    def clear_axes(self):
        self.ax.clear()
        self.ax.set_ylim(MINY, MAXY)

    def read_pacer(self):
        if args.rate_limit == None:
            return lambda: True

        self.pacer_count = 0

        def pacer_func():
            if self.pacer_count >= FRAMERATE:
                return False
            else:
                self.pacer_count += 1
                return True

        return pacer_func

    def update(self):
        global data # yeah

        newsamples = []
        pacer = self.read_pacer()
        while pacer():
            samp = heart.read_sample()
            if samp == None:
                break
            newsamples.append(samp)

        numsamps = len(newsamples)
        data = data[numsamps:]
        newsamples = [x.value for x in newsamples]
        data.extend(newsamples)

        self.clear_axes()
        self.ax.plot(data)
        self.mpl_surface.draw()

app = QApplication(sys.argv)
d = Display(data)
d.show()
app.exec_()
