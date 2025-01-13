import numpy as np
import matplotlib.pyplot as plt

def tripuls(t, width, shift):
    return np.where(np.logical_and(-width/2 <= t - shift, t - shift <= width/2), 1, 0)

def rectpuls(t, width):
    return np.where(np.logical_and(-width/2 <= t, t <= width/2), 1, 0)

def CTFT(Nt, Nw, t_min, t_max, w_min, w_max, f):
    t = np.linspace(t_min, t_max, Nt)
    w = np.linspace(w_min, w_max, Nw)
    F = np.fft.fftshift(np.fft.fft(np.fft.ifftshift(f))) / Nt
    return w, F

t = np.linspace(-1, 1, 500)
w = np.linspace(-50, 50, 1000)
width = 1
E = 1
f = tripuls(t, width, 0)
g = np.sqrt(2*E/width)*rectpuls(t, width/2)

plt.subplot(2, 4, 1)
plt.plot(t, f, 'r', t, g, 'b')
plt.legend(['f(x)', 'g(x)'])

ctft1_w, ctft1_F = CTFT(500, 1000, -1, 1, -50, 50, f)
plt.subplot(2, 4, 2)
plt.plot(ctft1_w, ctft1_F, 'r')
plt.legend(['F(w)'])
plt.subplot(2, 4, 5)
plt.plot(ctft1_w, ctft1_F, 'r')
plt.legend(['F(w)'])

ctft2_w, ctft2_G = CTFT(500, 1000, -1, 1, -50, 50, g)
plt.subplot(2, 4, 3)
plt.plot(ctft2_w, ctft2_G, 'b')
plt.legend(['G(w)'])

Ge = ctft2_G * ctft2_G
plt.subplot(2, 4, 6)
plt.plot(ctft2_w, Ge, 'b')
plt.legend(['Ge(w)'])

gg = (4/999) * np.convolve(g, g, mode='same')
t_conv = np.linspace(-2, 2, 999)
plt.subplot(2, 4, 4)
plt.plot(t_conv, gg, 'c:', t, f, 'r--')
plt.legend(['gg(x)', 'f(x)'])

ctft3_w, ctft3_Fe = CTFT(999, 1000, -2, 2, -50, 50, gg)
plt.subplot(2, 4, 7)
plt.plot(ctft3_w, ctft3_Fe)
plt.legend(['Fe(w)'])

plt.subplot(2, 4, 8)
plt.plot(ctft3_w, ctft1_F, 'r:', ctft3_w, Ge, 'g--', ctft3_w, ctft3_Fe, 'b-.')
plt.legend(['F(w)', 'Ge(w)', 'Fe(w)'])

plt.show()
