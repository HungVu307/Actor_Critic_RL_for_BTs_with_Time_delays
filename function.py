import numpy as np

def M(q, Theta):
    M11 = Theta[0] + 2 * Theta[1] * np.cos(q[1])
    M12 = Theta[2] + Theta[1] * np.cos(q[1])
    M21 = M12
    M22 = Theta[2]
    M = np.array([[M11, M12], [M21, M22]])
    return M

def C(q, dq, Theta):
    C11 = -Theta[1] * dq[1] * np.sin(q[1])
    C12 = -Theta[1] * (dq[1] + dq[0]) * np.sin(q[1])
    C21 = Theta[1] * dq[0] * np.sin(q[1])
    C22 = 0
    C = np.array([[C11, C12], [C21, C22]])
    return C

def G(q, Theta):
    G1 = Theta[3] * np.cos(q[0]) + Theta[4] * np.cos(q[0] + q[1])
    G2 = Theta[4] * np.cos(q[0] + q[1])
    G = np.array([G1, G2])
    return G

def gradPhi1(x):
    a = np.array([
        [2 * x[0], 0],
        [x[1], x[0]],
        [0, 2 * x[1]],
        [2 * x[0] * x[2]**2, 0],
        [0, 2 * x[1] * x[3]**2],
        [2 * x[0] * x[4]**2, 0],
        [0, 2 * x[1] * x[5]**2]
    ])
    return a

def gradPhi2(x):
    a = np.array([
        [0, 0],
        [0, 0],
        [0, 0],
        [2 * x[2] * x[0]**2, 0],
        [0, 2 * x[3] * x[1]**2],
        [0, 0],
        [0, 0]
    ])
    return a

def gradPhi3(x):
    a = np.array([
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [2 * x[4] * x[0]**2, 0],
        [0, 2 * x[5] * x[1]**2]
    ])
    return a

def torque_Hu(t, i, tu):
    if 10000 < i <= 11000:
        return np.array([-10, -10])
    elif 11000 < i <= 11500:
        return np.array([-10, -10 + 5.1 * (1 - np.exp(-10 * (t[i - 11000])))])
    elif 11500 < i <= 12200:
        return np.array([
            -10 + 2 * (1 - np.exp(-5 * (t[i - 11500]))),
            tu[11500][1] + 1 * (1 - np.exp(-10 * (t[i - 11500])))
        ])
    elif 12200 < i <= 13000:
        return np.array([
            tu[12200][0] + 1.5 * (1 - np.exp(-10 * (t[i - 12200]))),
            tu[12200][1]
        ])
    elif 13000 < i <= 20000:
        return tu[13000]
    elif 20000 < i <= 20200:
        return np.array([
            10 * np.exp(-3 * (t[i - 20000])),
            10
        ])
    elif 20200 < i <= 20600:
        return tu[20150]
    elif 20600 < i <= 22000:
        return np.array([
            tu[20600][0] * np.exp(-1 * (t[i - 20600])),
            10
        ])
    elif 22000 < i <= 27000:
        return np.array([
            tu[20600][0] * np.exp(-1 * (t[i - 20600])),
            tu[22000][1] * np.exp(-1 * (t[i - 22000]))
        ])
    else:
        return np.array([0, 0])
    

def torque_En(t, i, te):
    if 13000 < i <= 13800:
        return np.array([
            -4.8 + np.exp(-4 * (t[i - 13000])),
            -2.5 + np.exp(-3 * (t[i - 13000]))
        ])
    elif 13800 < i <= 14000:
        return np.array([
            te[13800][0] + np.exp(-10 * (t[i - 13800])) - 1,
            -2.5 + np.exp(-3 * (t[i - 13000]))
        ])
    elif 14000 < i <= 14800:
        return np.array([
            te[13800][0] + np.exp(-10 * (t[i - 13800])) - 0.3,
            te[14000][1] + np.exp(-6 * (t[i - 14000])) - 1
        ])
    elif 14800 < i < 21000:
        return te[14800]
    else:
        return np.array([0, 0])