import numpy as np
def noisedata(data):
    N, f, max_t = 3.33, 60, 0.5
    s = N * f
    ts = s * max_t + 1
    A1, A2, theta1, theta2, k = 1, 0.75, np.pi / 2, np.pi / 2.5, 0.00001

    data = data[:,:int(ts)+1]
    i = np.arange(ts).reshape(1, -1)
    noise1, noise2 = 1.2 * np.sin(2 * np.pi * (i - 1) / N), 0.6 * np.sin(4 * np.pi * (i - 1) / N)
    noise = noise1 + noise2
    filtered_noise1 = A1 * 1.20 * np.sin(2 * np.pi * (i - 1) / N + theta1)
    filtered_noise2 = A2 * 0.6 * np.sin(4 * np.pi * (i - 1) / N + theta1)
    filtered_noise = filtered_noise1 + filtered_noise2
    noisy_signal = data + filtered_noise

    time = np.arange(1, ts + 1) / ts * max_t
    P_ = np.zeros((21, 101))
    for i in range(21):
        P_[i, i + 1:] = noise[:, :101 - i - 1]
    P_ = np.array(P_)
    T = noisy_signal[:]