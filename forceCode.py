# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 10:45:51 2021

@author: EKirkpatrick
"""

import matplotlib, pandas, scipy
from scipy import signal
import matplotlib.pyplot as plotter
import numpy as np
import fileOpener
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
import sys

"""Variable declarations"""
fs = 3000
AODtonmx = 1070E-9
AODtonmy = 1178E-9
kB = 1.3807E-23
T = 294
a = 500E-9
mu = 0.001
h = 1.5E-6
denom = 1 - ((9/16)*(a/h) + (1/8)*((a/h) ** 3) - ((45/256)*((a/h) ** 4)) - ((1/16)*((a/h) ** 5)))
mu = mu/denom
beta = 6*np.pi*mu*a
asz = 100


def main():
    
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)        
    ex = fileOpener.pathCall()
    trace = np.genfromtxt(ex.tracePath[0])
    voltage = np.genfromtxt(ex.calPath[0])
    stiffness = np.genfromtxt(ex.sPath[0])

    Vx = trace[:, 0]
    Vy = trace[:, 1]

    calx = voltage[:, 0]
    caly = voltage[:, 1]

    kxvar = stiffness[2] * 10 ** -3
    kyvar = stiffness[3] * 10 ** -3

    nmx = AODtonmx * (calx[0] + calx[1] * Vx + calx[2] * Vy + calx[3] * Vx ** 2 + calx[4] * Vy ** 2 + calx[
        5] * Vx ** 3 + calx[6] * Vy ** 3 + calx[7] * Vx ** 4 + calx[8] * Vy ** 4 + calx[9] * Vx ** 5 + calx[
        10] * Vy ** 5 + calx[11] * Vx * Vy + calx[12] * Vx ** 2. * Vy + calx[13] * Vx * Vy ** 2 + calx[
        14] * Vx ** 3. * Vy + calx[15] * Vx ** 2. * Vy ** 2 + calx[16] * Vx * Vy ** 3 + calx[
        17] * Vx ** 4. * Vy + calx[18] * Vx ** 3. * Vy ** 2 + calx[19] * Vx ** 2. * Vy ** 3 + calx[20] * Vx * Vy ** 4)
    nmy = AODtonmy * (caly[0] + caly[1] * Vx + caly[2] * Vy + caly[3] * Vx ** 2 + caly[4] * Vy ** 2 + caly[
        5] * Vx ** 3 + caly[6] * Vy ** 3 + caly[7] * Vx ** 4 + caly[8] * Vy ** 4 + caly[9] * Vx ** 5 + caly[
        10] * Vy ** 5 + caly[11] * Vx * Vy + caly[12] * Vx ** 2. * Vy + caly[13] * Vx * Vy ** 2 + caly[
        14] * Vx ** 3. * Vy + caly[15] * Vx ** 2. * Vy ** 2 + caly[16] * Vx * Vy ** 3 + caly[
        17] * Vx ** 4. * Vy + caly[18] * Vx ** 3. * Vy ** 2 + caly[19] * Vx ** 2. * Vy ** 3 + caly[20] * Vx * Vy ** 4)

    psdx = -(nmx*(np.cos(np.pi/4)) - nmy*np.sin(np.pi/4))
    psdy = -(nmy*(np.cos(np.pi/4)) - nmx*np.sin(np.pi/4))

    psdx = psdx - np.mean(psdx[1:asz])
    psdy = psdy - np.mean(psdy[1:asz])

    psdx_dec25 = scipy.signal.decimate(psdx, 25)
    psdy_dec25 = scipy.signal.decimate(psdy, 25)
    psdx_dec25_avg10 = np.convolve(psdx_dec25, np.ones(10), 'valid')
    psdy_dec25_avg10 = np.convolve(psdy_dec25, np.ones(10), 'valid')

    time = np.array(list(range(0, len(psdy)))) * (1/fs)
    time_dec25 = scipy.signal.decimate(time, 25)
    fx = psdx * kyvar * 10 ** 12
    fy = psdy * kxvar * 10 ** 12

    fy_avg = psdy_dec25_avg10 * kxvar * 10 ** 12


    fx_avg = psdx_dec25_avg10 * kyvar * 10 ** 12

    xplotforce = plotter.figure(1)
    plotter.xlabel('time (sec)')
    plotter.ylabel('force x (pN)')
    plotter.plot(time, fx)
    yplotforce = plotter.figure(2)
    plotter.xlabel('time (sec)')
    plotter.ylabel('force y (pN)')
    plotter.plot(time, fy)
    xplotdist = plotter.figure(3)
    plotter.xlabel('time (sec)')
    plotter.ylabel('distance x (nm)')
    plotter.plot(time, psdx*10**9)
    yplotdist = plotter.figure(4)
    plotter.xlabel('time (sec)')
    plotter.ylabel('distance y (nm)')
    plotter.plot(time, psdy*10**9)
    plotter.savefig('distance y', dpi=500)
    plotter.ion()
    plotter.show()


    app.exec_()

    
    
if __name__ == '__main__':
    main()        