import sys

import numpy as np
from sklearn.decomposition import PCA




def sumTensor(A, axis):
    sumA = np.copy(A)
    for x in axis:
       sumA = np.sum(sumA, axis=x, keepdims=True)
    return sumA


def summarizeLDS(dataTensor, model_dim, cross_val_flag=False):
    T, N, C = dataTensor.shape
    XN = np.reshape(
        np.moveaxis(dataTensor, [0,2,1], [0,1,2]),
        (-1, dataTensor.shape[1]), order='F')
    meanXN = np.mean(XN, axis=0)

    pca = PCA()
    pca.fit_transform(XN)
    PCvectors = pca.components_.T

    maskT1Orig = np.ones((T, 1), dtype=bool)
    maskT1Orig[-1] = 0
    maskT1Orig = np.repeat(maskT1Orig, C, axis=1).T.flatten()

    maskT2Orig = np.ones((T, 1), dtype=bool)
    maskT2Orig[0] = 0
    maskT2Orig = np.repeat(maskT2Orig, C, axis=1).T.flatten()

    if not cross_val_flag:
        PCvector = PCvectors[:, 0:model_dim]
        XNred = np.matmul((XN - meanXN), PCvector)
        dState = XNred[maskT2Orig==1] - XNred[maskT1Orig==1]
        preState = XNred[maskT1Orig==1]
        M = np.matmul(dState.T, np.linalg.pinv(preState.T))
        fitErrorM = dState.T - np.matmul(M, preState.T)
        varDState = np.sum(dState.flatten() ** 2)
        R2 = (varDState - np.sum(fitErrorM.flatten() ** 2)) / varDState

    return R2


def extractFeatures(dataTensor, meanTensor=None):
    T, N, C = dataTensor.shape

    M = {}
    M['T'] = []
    M['TN'] = []
    M['TNC'] = []

    meanT = np.sum(dataTensor, axis=(1,2)) / (C*N)
    meanN = np.sum(dataTensor, axis=(0,2)) / (C*T)
    meanC = np.sum(dataTensor, axis=(0,1)) / (T*N)

    mean = {}
    mean['T'] = meanT
    mean['N'] = meanN
    mean['C'] = meanC

    if meanTensor is None:
        dataTensor0 = np.copy(dataTensor)
        meanT = np.sum(dataTensor0, axis=(1, 2)) / (C * N)
        dataTensor0 = dataTensor0 - meanT[:, np.newaxis, np.newaxis]
        meanN = np.sum(dataTensor0, axis=(0, 2)) / (C * T)
        dataTensor0 = dataTensor0 - meanN[np.newaxis, :, np.newaxis]
        meanC = np.sum(dataTensor0, axis=(0, 1)) / (T * N)
        dataTensor0 = dataTensor0 - meanC[np.newaxis, np.newaxis, :]

        M['TNC'] = dataTensor - dataTensor0
        M['TN'] = np.reshape(
                np.repeat(np.sum(M['TNC'], axis=2) / C, C, axis=1),
            (T, N, C), order='F')
        M['T'] = np.reshape(
            np.repeat(
                np.repeat(
                    np.sum(M['TNC'], axis=(1, 2)) / (N*C),
                    N, axis=0),
                C, axis=0),
            (T, N, C), order='F')

        meanTensor = M['TNC']

    XT = np.reshape(np.moveaxis(dataTensor - meanTensor, [0,1,2], [2,1,0]), (-1, T), order='F')
    XN = np.reshape(np.moveaxis(dataTensor - meanTensor, [0,1,2], [0,2,1]), (-1, N), order='F')
    XC = np.reshape(np.moveaxis(dataTensor - meanTensor, [0,1,2], [0,1,2]), (-1, C), order='F')

    sigma_T = np.matmul(XT.T, XT)
    sigma_N = np.matmul(XN.T, XN)
    sigma_C = np.matmul(XC.T, XC)

    return sigma_T, sigma_N, sigma_C, M


def rewrap(s, v):
    if v.size < s.size:
        return 0
    s = np.reshape(v[0:s.size], s.shape)
    v = v[s.size:]

    return s, v


def minimize(fun, X, maxiter, *args):
    INT = 0.1                   # don't reevaluate within 0.1 of the limit of the current bracket
    EXT = 3.0                   # extrapolate maximum 3 times the current step-size
    MAX = 20                    # max 20 function evaluations per line search
    RATIO = 10                  # maximum allowed slope ratio
    SIG = 0.1
    RHO = SIG/2                 # SIG and RHO are the constants controlling the Wolfe-Powell conditions.

    red = 1
    if maxiter > 0:
        S = 'Linesearch'
    else:
        S = 'Function evaluation'

    i = 0                                          # zero the run length counter
    ls_failed = 0                                  # no previous line search has failed
    f0, df0 = fun(X, *args)
    Z = X
    # get function value and gradient


    fX = f0
    i = i + int(maxiter < 0)
    s = np.copy(-df0)
    d0 = np.dot(-s.flatten(), s.flatten())
    x3 = red / (1-d0)

    while i < abs(maxiter):
        i = i + int(maxiter>0)

        X0 = np.copy(X)
        F0 = f0
        dF0 = np.copy(df0)
        if maxiter > 0:
            M = MAX
        else:
            M = min(MAX, -maxiter-i)

        while True:
            x2 = 0
            f2 = f0
            d2 = d0
            f3 = f0
            df3 = np.copy(df0)
            success = 0

            while not success and M > 0:
                M = M-1
                i = i + int(maxiter < 0)
                s1, v1 = rewrap(Z, X+(x3*s).squeeze())
                f3, df3 = fun(s1, *args)

                if np.isnan(f3) or np.isinf(f3) or np.any(np.isnan(df3) + np.isinf(df3)):
                    x3 = (x2+x3)/2
                else:
                    success = 1
            if f3 < F0:
                X0 = X+(x3*s).squeeze()
                F0 = f3
                dF0 = df3

            d3 = np.dot(df3.flatten(), s.flatten())

            if d3 > SIG * d0 or f3 > f0 + x3 * RHO * d0 or M == 0:
                break

            x1,f1,d1 = x2,f2,d2;                        # move point 2 to point 1
            x2,f2,d2 = x3,f3,d3;                        # move point 3 to point 2
            A = 6*(f1-f2)+3*(d2+d1)*(x2-x1)                  # make cubic extrapolation
            B = 3*(f2-f1)-(2*d1+d2)*(x2-x1)
            # a warning might appear from this line, due to the sqrt resulting in complex number -> it would be a nan here
            # nevertheless, this is the original implementation, the next if verifies if the number is not real and modifies the value of x3
            # the warning can be suppressed
            x3 = x1-d1*(x2-x1)**2/(B+np.sqrt(B*B-A*d1*(x2-x1)))

            if not np.isreal(x3) or np.isnan(x3) or np.isinf(x3) or x3 < 0: # num prob | wrong sign?
              x3 = x2*EXT                                 # extrapolate maximum amount
            elif x3 > x2*EXT:                  # new point beyond extrapolation limit?
              x3 = x2*EXT                                 # extrapolate maximum amount
            elif x3 < x2+INT*(x2-x1):         # new point too close to previous point?
              x3 = x2+INT*(x2-x1)

        pass

        while (abs(d3) > - SIG*d0 or f3 > f0+x3*RHO*d0) and M>0:
            if d3>0 or f3>f0+x3*RHO*d0:
                x4,f4,d4 = x3,f3,d3
            else:
                x2,f2,d2 = x3,f3,d3

            if f4>f0:
                x3 = x2-(0.5*d2*(x4-x2)**2) / (f4-f2-d2*(x4-x2))
            else:
                A = 6*(f2-f4)/(x4-x2)+3*(d4+d2)                    # cubic interpolation
                B = 3*(f4-f2)-(2*d2+d4)*(x4-x2)
                x3 = x2+(np.sqrt(B*B-A*d2*(x4-x2)**2)-B)/A        # num. error possible, ok!

            if np.isnan(x3) or np.isinf(x3):
                x3 = (x2+x4) / 2

            x3 = max(min(x3, x4-INT*(x4-x2)), x2+INT*(x4-x2))

            s1, v1 = rewrap(Z, X + (x3 * s).squeeze())
            f3, df3 = fun(s1, *args)

            if f3 < F0:
                X0 = X + (x3 * s).squeeze()
                F0 = f3
                dF0 = df3

            M = M-1
            i = i+int(maxiter<0)
            d3 = np.dot(df3.flatten(), s.flatten())

        if abs(d3) < -SIG*d0 and f3 < f0+x3*RHO*d0:         # if line search succeeded
            X = X+(x3*s).squeeze()
            f0 = f3

            if type(fX) == list:
                fX.append(f0)
            else:
                fX = [fX, f0]

            s = ((np.dot(df3.flatten(), df3.flatten())
                 -np.dot(df0.flatten(), df3.flatten()))
                 /(np.dot(df0.flatten(), df0.flatten()))*s - df3)   # Polack-Ribiere CG direction
            df0 = np.copy(df3)                                             # swap derivatives
            d3 = d0
            d0 = np.dot(df0.flatten(), s.flatten())
            if d0 > 0:                                      # new slope must be negative
              s = -df0
              d0 = np.dot(-s.flatten(), s.flatten())                  # otherwise use steepest direction
            x3 = x3 * min(RATIO, d3/(d0-sys.float_info.min))          # slope ratio but max RATIO
            ls_failed = 0                              # this line search did not fail
        else:
            X = np.copy(X0)
            f0 = F0
            df0 = np.copy(dF0)                     # restore best point so far
            if ls_failed or i > abs(maxiter):        # line search failed twice in a row
                break                            # or we ran out of time, so we give up
            s = -df0
            d0 = np.dot(-s.flatten(), s.flatten())                                         # try steepest
            x3 = 1/(1-d0)
            ls_failed = 1                                    # this line search failed

    return X, fX, i
