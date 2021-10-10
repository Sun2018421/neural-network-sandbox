import os
import sys

import PyQt5.QtQml
import PyQt5.QtCore
import PyQt5.QtWidgets
import numpy

from nn_sandbox.bridges import PerceptronBridge, MlpBridge, RbfnBridge, SomBridge ,BpBridge,EggBridge, bridge
import nn_sandbox.backend.utils
from scipy.io import loadmat

from nn_sandbox.bridges.anc_bridge import AncBridge

if __name__ == '__main__':
    os.environ['QT_QUICK_CONTROLS_STYLE'] = 'Default'

    # XXX: Why I Have To Use QApplication instead of QGuiApplication? It seams
    # QGuiApplication cannot load QML Chart libs!
   
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    engine = PyQt5.QtQml.QQmlApplicationEngine()

    bridges = {
        'perceptronBridge': PerceptronBridge(),
        'mlpBridge': MlpBridge(),
        'rbfnBridge': RbfnBridge(),
        'somBridge': SomBridge(),
        'BpBridge': BpBridge(),
        'EggBridge': EggBridge(),
        'AncBridge': AncBridge()
    }
    for name in bridges:
        if name == 'EggBridge':
            data = {}
            data['eeg'] = ((loadmat('./nn_sandbox/assets/data/eegdata.mat')['eegdata']).tolist())[0]
            bridges[name].dataset_dict = data
            bridges[name].dataset_length = len(data['eeg'])
        elif name == 'AncBridge':
            engine.rootContext().setContextProperty(name, bridges[name])
            continue
        else:    
            bridges[name].dataset_dict = nn_sandbox.backend.utils.read_data()
        engine.rootContext().setContextProperty(name, bridges[name])

    engine.load('./nn_sandbox/frontend/main.qml')
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
 
