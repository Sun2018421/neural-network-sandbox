import time

import PyQt5.QtCore

from nn_sandbox.backend.algorithms.eeg_algorithm import EegAlgorithm

from . import Bridge, BridgeProperty
from .observer import Observable
import numpy as np

class EggBridge(Bridge):
    dataset_dict = BridgeProperty({})
    eeg_time = BridgeProperty([])
    dataset_length = BridgeProperty(1)
    initial_learning_rate = BridgeProperty(0.02)
    current_learning_rate = BridgeProperty(0.0)
    initial_delays = BridgeProperty(10)
    current_delays = BridgeProperty(0.0)
    current_time = BridgeProperty(0.0)
    has_finished = BridgeProperty(True)
    current_iterations = BridgeProperty(0)
    ui_refresh_interval = BridgeProperty(0.0)
    red_line = BridgeProperty(0.0)
    plot_idx = BridgeProperty(0) # 用来区分
    def __init__(self):
        super().__init__()
        self.eeg_algorithm = None
        N, f, max_t = 3.33, 60, 0.5
        s = N * f
        ts = s * max_t + 1
        A1, A2, theta1, k = 1, 0.75, np.pi / 2, 0.00001
        self.eeg_time = (np.arange(1, ts + 1)/ ts * max_t).tolist()

    @PyQt5.QtCore.pyqtSlot()
    def start_eeg_algorithm(self):
        self.eeg_algorithm = ObservableEggAlgorithm(
            self,
            dataset = self.dataset_dict['eeg'],
            initial_learning_rate = self.initial_learning_rate,
            delays= self.initial_delays,
            plot_idx = self.plot_idx
        )
        self.eeg_algorithm.start()
    
    @PyQt5.QtCore.pyqtSlot()
    def stop_eeg_algorithm(self):
        self.eeg_algorithm.stop()
    
 


class ObservableEggAlgorithm(Observable , EegAlgorithm):
    def __init__(self,observer,ui_refresh_interval=0.2, **kwargs):
        Observable.__init__(self,observer)
        EegAlgorithm.__init__(self,**kwargs)
        self.ui_refresh_interval = ui_refresh_interval
    
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name in ('current_time','current_iterations','dataset_length','red_line'):
            self.notify(name, value)
    
    def run(self):
        self.notify("has_finished",False)
        super().run()
        self.notify("has_finished",True)
    
    def _iterate(self):
        super()._iterate()
        time.sleep(self.ui_refresh_interval)
    