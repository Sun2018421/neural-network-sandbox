import numpy as np

from . import PredictiveAlgorithm

PACKAGE_PATH = r""

class EegAlgorithm(PredictiveAlgorithm):
    def __init__(self, dataset, plot_idx=0, initial_learning_rate=0.02, delays=10):
        N, f, max_t = 3.33, 60, 0.5
        s = N * f
        self.ts = s * max_t + 1
        A1, A2, theta1, k = 1, 0.75, np.pi / 2, 0.00001
        # print(dataset)
        self.signal_ = k * (np.array(dataset).reshape(1,-1))[:, :int(self.ts) + 1]
        # print(self.signal_)
        i = np.arange(self.ts).reshape(1, -1)
        noise1, noise2 = 1.2 * np.sin(2 * np.pi * (i - 1) / N), 0.6 * np.sin(4 * np.pi * (i - 1) / N)
        noise = noise1 + noise2
        filtered_noise1 = A1 * 1.20 * np.sin(2 * np.pi * (i - 1) / N + theta1)
        filtered_noise2 = A2 * 0.6 * np.sin(4 * np.pi * (i - 1) / N + theta1)
        filtered_noise = filtered_noise1 + filtered_noise2
        noisy_signal = self.signal_ + filtered_noise
        self.time = np.arange(1, self.ts + 1) / self.ts * max_t
        self.P_ = np.zeros((21, 101))
        for i in range(21):
            self.P_[i, i + 1:] = noise[:, :101 - i - 1]
        self.P_ = np.array(self.P_)
        self.T = noisy_signal[:]

        self.R, self.P = None, None
        self.a, self.e = None, None        

        self.dataset_length = len(self.signal_[0])
        total_epoches = 1
        test_ratio = 0
        search_iteration_constant = len(self.time)
        most_correct_rate = False
        super().__init__(self.signal_[0], total_epoches, most_correct_rate, initial_learning_rate, 
            search_iteration_constant, test_ratio, need_best_neurons=False)
        self.plot_idx = plot_idx
        self.delays = delays
        self.lr = initial_learning_rate

    def _initialize_neurons(self):
        self.R = self.delays + 1
        self.P = self.P_[:self.R]
        self.w = np.zeros((1, self.R))
        self.a, self.e = np.zeros((1, 101)), np.zeros((1, 101))
    
    def _iterate(self):
        idx = self.current_iterations
        p = self.P[:, idx]
        self.a[0, idx] = np.dot(self.w, p)
        self.e[0, idx] = self.T[0, idx] - self.a[0, idx]
        self.w += self.lr * self.e[0, idx] * p.T   
        self.current_time = self.time[idx]     
        self.blue_line = self.signal_[0, idx]
        if(self.plot_idx == 0):
            self.red_line = self.e[0, idx]            
        else:
            self.red_line = (self.signal_ - self.e)[0, idx]

    def _correct_rate(self, dataset):
        pass