import numpy as np

def ellipsoid(v: np.array, method='ten-param') -> dict:
    '''
    Magnetic Calibration Technical Note
    Authors: Mark Pedley and Michael Stanley
    Date: September 2014
    Source: https://github.com/memsindustrygroup/Open-Source-Sensor-Fusion

        X = [ x2  y2  z2  xy  yz  zx  x  y  z  1 ]

    Input
        - v: 3 x N

    Output
        - dict: {
            sens, bias, radi, error
        }
    '''

    n = v.shape[1]

    _x, _y, _z = v
    X = np.zeros([n, 10])
    X[:, 0] = _x * _x
    X[:, 1] = _y * _y
    X[:, 2] = _z * _z
    X[:, 3] = _x * _y
    X[:, 4] = _y * _z
    X[:, 5] = _z * _x
    X[:, 6] = _x
    X[:, 7] = _y
    X[:, 8] = _z
    X[:, 9] = 1

    evals, evecs = np.linalg.eig(X.T @ X)
    idx = np.argmin(evals)
    beta = evecs[:, idx]
    beta[[3,4,5]] *= 0.5

    A = beta[[0,3,5,3,1,4,5,4,2]].reshape(3,3)
    if np.linalg.det(A) < 0:
        beta = -beta
        A = -A

    bias = -0.5 * np.linalg.inv(A) @ beta[[6,7,8]].reshape(3,1)

    L, Q = np.linalg.eig(A)
    QLQt = Q @ np.diag(np.sqrt(L)) @ Q.T
    sens = np.linalg.det(QLQt)**(-1/3) * QLQt

    vc = (sens @ (v - bias))
    radi = np.mean(np.linalg.norm(vc, axis=0))

    efit = np.sqrt(np.abs(evals[idx]) / n) / (2 * radi**2)

    return {
        'sens': sens,
        'bias': bias,
        'radi': radi,
        'error': efit,
    }
