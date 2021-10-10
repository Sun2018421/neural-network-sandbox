import numpy as np

from . import PredictiveAlgorithm

class NcAlgorithm(PredictiveAlgorithm):
    def __init__(self, plot_idx=0, initial_learning_rate=0.2, momentum_weight=0.0):
        N, f, max_t = 3, 60, 0.5
        s = N * f
        self.ts = s * max_t + 1
        A, theta, k = 0.1, np.pi / 2, 0.2
        self.signal_ = k * (2 * np.random.uniform(0, 1, (1, int(self.ts))) - 1)
        i = np.arange(self.ts).reshape(1, -1)
        noise = 1.2 * np.sin(2 * np.pi * (i - 1) / N + theta)
        filtered_noise = A * 1.20 * np.sin(2 * np.pi * (i - 1) / N + theta)
        delayed_noise = np.array([list(noise.reshape(-1)), [0] + list(noise.reshape(-1))[:-1]])
        noisy_signal = self.signal_ + filtered_noise
        
        self.time = np.arange(1, self.ts + 1) / self.ts * max_t
        self.P = delayed_noise
        self.T = noisy_signal[:]
        # A = 2 * np.dot(self.P, self.P.T)
        # d = -2 * np.dot(self.P, self.T.T)
        # c = np.dot(self.T, self.T.T)

        # x = np.linspace(-2.1, 2.1, 30)
        # y = np.copy(x)
        # X, Y = np.meshgrid(x, y)
        # F = (A[0, 0] * X ** 2 + (A[0, 1] + A[1, 0]) * X * Y + A[1, 1] * Y ** 2) / 2 + d[0, 0] * X + d[1, 0] * Y + c
        self.mc = momentum_weight
        self.lr = initial_learning_rate
        self.dataset_length = len(self.signal_[0])
        dataset = self.signal_[0]
        total_epoches = 1
        test_ratio = 0
        search_iteration_constant = len(self.time)
        most_correct_rate = False
        super().__init__(dataset, total_epoches, most_correct_rate,
                         initial_learning_rate, search_iteration_constant, test_ratio, need_best_neurons=False)
        self.plot_idx = plot_idx
        self._momentum_weight = momentum_weight

    def _initialize_neurons(self):
        self.w = np.array([0, 2])
        self.e = np.zeros((int(self.ts),))
        self.w1_data, self.w2_data = [self.w[0]], [self.w[1]]
    
    def _iterate(self):
        idx = self.current_iterations
        a = np.dot(self.w, self.P[:, idx])
        self.e[idx] = self.T[0, idx] - a
        self.w0 = self.w[0]
        self.w1 = self.w[1]
        self.w = self.w + self.mc * self.w + (1 - self.mc) * self.lr * self.e[idx] * self.P[:, idx].T

        self.w1_data.append(self.w[0])
        self.w2_data.append(self.w[1])
        self.current_time = self.time[idx]
        
        self.blue_line = self.signal_[0, idx]
        if(self.plot_idx == 0):
            self.red_line = self.e[idx]
        else:
            self.red_line = (self.signal_ - self.e)[0, idx]


    def _correct_rate(self, dataset):
        pass