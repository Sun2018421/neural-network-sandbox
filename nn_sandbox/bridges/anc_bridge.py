import time

import PyQt5.QtCore
from scipy.io.matlab.mio5 import NDT_TAG_FULL

from nn_sandbox.backend.algorithms import NcAlgorithm
from . import Bridge, BridgeProperty
from .observer import Observable


class AncBridge(Bridge):
    ui_refresh_interval = BridgeProperty(0.2)
    dataset_dict = BridgeProperty({})
    plot_idx = BridgeProperty(0)
    momentum_weight = BridgeProperty(0.0)
    training_dataset = BridgeProperty([])
    total_epoches = BridgeProperty(5)
    initial_learning_rate = BridgeProperty(0.5)
    current_iterations = BridgeProperty(0)
    has_finished = BridgeProperty(True)
    red_line = BridgeProperty(0.0)
    blue_line = BridgeProperty(0.0)
    w0 = BridgeProperty(0.0)
    w1 = BridgeProperty(2.0)

    current_time = BridgeProperty(0.0)

    def __init__(self):
        super().__init__()
        self.anc_algorithm = None

    @PyQt5.QtCore.pyqtSlot()
    def start_anc_algorithm(self):
        self.anc_algorithm = ObservableAncAlgorithm(
            self,
            self.ui_refresh_interval,
            plot_idx=self.plot_idx,
            initial_learning_rate=self.initial_learning_rate,
            momentum_weight = self.momentum_weight
        )
        self.anc_algorithm.start()

    @PyQt5.QtCore.pyqtSlot()
    def stop_anc_algorithm(self):
        self.anc_algorithm.stop()




class ObservableAncAlgorithm(Observable, NcAlgorithm):
    def __init__(self, observer, ui_refresh_interval, **kwargs):
        Observable.__init__(self, observer)
        NcAlgorithm.__init__(self, **kwargs)
        self.ui_refresh_interval = ui_refresh_interval

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name in ('current_time','blue_line','red_line','current_iterations','w0','w1'):
            self.notify(name,value)

    def run(self):
        self.notify('has_finished', False)
        super().run()
        self.notify('has_finished', True)

    def _iterate(self):
        super()._iterate()
        # the following line keeps the GUI from blocking
        time.sleep(self.ui_refresh_interval)

