import numpy as np
from matplotlib import pyplot as plt

from .utils import minimize, extractFeatures, summarizeLDS, sumTensor


def shuffle(dataTensor, shuffle_mode, fix_mode, cyclicShfl):
    shuffledTensor = np.copy(dataTensor)
    dims = dataTensor.shape
    tensorIxs = np.array(list(range(len(dims))))

    T = dims[shuffle_mode]
    N = dims[fix_mode]

    reorderIx = [fix_mode, shuffle_mode] + list(np.sort(tensorIxs[np.logical_and(tensorIxs != fix_mode, tensorIxs != shuffle_mode)]))
    shuffledTensor = np.reshape(
        np.moveaxis(shuffledTensor, source=reorderIx, destination=tensorIxs),
        newshape=(N, T, -1))

    for n in range(N):
        if cyclicShfl == True:
            st = np.random.randint(T)
            ts = np.array(list(range(st, T)) + list(range(st)))
        else:
            pass
        A = shuffledTensor[n, :, :]
        shuffledTensor[n, :, :] = A[ts]
        pass

    last_dim = tensorIxs[np.logical_and(tensorIxs != fix_mode, tensorIxs != shuffle_mode)][0]
    shuffledTensor = np.reshape(shuffledTensor, newshape=(N, T, dims[last_dim]), order='F')

    ix = np.argsort(reorderIx)
    shuffledTensor = np.moveaxis(shuffledTensor, source=ix, destination=tensorIxs)

    return shuffledTensor


def objFnReadOut(K, surrTensor, targetSigma):
    normalizeTerm = np.trace(np.matmul(targetSigma.T, targetSigma))
    N = surrTensor.shape[0]
    X = np.reshape(surrTensor, newshape=(N, -1)).T
    XK = np.matmul(X, K)
    estSigma = np.matmul(XK.T, XK)

    ER = (targetSigma - estSigma)

    f = np.trace(np.matmul(ER, ER.T)) / normalizeTerm

    # calculate gradient
    XXK = np.matmul(np.matmul(X.T, X), K)
    gradf = (-4 / normalizeTerm) * np.matmul(XXK, ER)

    return f, gradf


def objFnOther(K, surrTensor, targetSigma):
    normalizeTerm = np.trace(np.matmul(targetSigma.T, targetSigma))
    N = surrTensor.shape[0]
    T = surrTensor.shape[1]
    C = int(np.round(surrTensor.size / (T * N)))
    surrTensor = np.reshape(surrTensor, newshape=(N, T, C), order="F")
    X = np.reshape(surrTensor, newshape=(N, T * C), order="F").T
    XK = np.matmul(X, K)

    XTK = np.reshape(
        np.moveaxis(np.reshape(XK.T, newshape=(N, T, C), order="F"), source=[2, 0, 1], destination=[0, 1, 2]),
        newshape=(C * N, T), order="F"
    )

    estSigma = np.matmul(XTK.T, XTK)
    ER = (estSigma - targetSigma)
    f = np.trace(np.matmul(ER.T, ER)) / normalizeTerm

    # calculate gradient
    surrTensorT = np.moveaxis(surrTensor, source=[1, 0, 2], destination=[0, 1, 2])
    ERsurrTensorT = np.reshape(
        np.matmul(ER, np.reshape(surrTensorT, newshape=(T, N * C), order="F")),
        newshape=(T, N, C), order="F"
    )

    gradf = 4 * \
            np.matmul(
                np.matmul(
                    np.reshape(
                        np.moveaxis(surrTensorT, source=[0, 1, 2], destination=[0, 2, 1]),
                        newshape=(T * C, N)
                    ).T,
                    np.reshape(
                        np.moveaxis(ERsurrTensorT, source=[0, 1, 2], destination=[0, 2, 1]),
                        newshape=(T * C, N)
                    )
                ),
                K
            )

    gradf = gradf / normalizeTerm

    return f, gradf


def projEigSpace(grad, v):
    v = v / np.linalg.norm(v, 2)
    N = len(v)
    I = np.eye(N)
    G = np.matmul(grad, (I - np.dot(v[:, np.newaxis], v[:, np.newaxis].T)))

    return G


def objFnMarginalCov(K, params):
    surrTensor, marg_cov = params[0], params[1]
    normFactor = len(marg_cov)
    f = 0
    gradf = 0
    dims = surrTensor.shape
    tensorIxs = np.array(list(range(1, len(dims))))  # exclude readout mode

    f, gradf = objFnReadOut(K, surrTensor, marg_cov[0])

    for i in tensorIxs:
        reorderIx = [0, i] + list(np.sort(tensorIxs[tensorIxs != i]))
        fi, gradfi = objFnOther(K, np.moveaxis(surrTensor, source=reorderIx, destination=list(range(len(dims)))), marg_cov[i])

        f = f + fi
        gradf = gradf + gradfi

    f = f / normFactor
    gradf = gradf / normFactor
    gradf = projEigSpace(gradf, np.ones(shape=(K.shape[1],)))

    return f, gradf


def optMarginalCov(surrTensor, marg_cov):
    dims = surrTensor.shape
    N = dims[0]  # readout mode dimensionality
    meanN = sumTensor(surrTensor, axis=tuple(list(range(1, len(dims))))) / np.prod(dims[1:])

    surrTensor = surrTensor - meanN

    K = np.eye(N)
    K = np.matmul(K, (np.eye(N) - np.ones(N) / N))

    maxiter = 100

    K, f, i = minimize(objFnMarginalCov, K, maxiter, [surrTensor, marg_cov])

    surrTensorOut = np.reshape(
        np.matmul(K.T,
                  np.reshape(surrTensor, (N, -1), order='F')
                  ),
        newshape=tuple([N] + list(dims[1:])),
        order="F"
    )

    return surrTensorOut, f, K


def sampleCFR(dataTensor, meanTensor, margCov, shuffle_mode, fix_mode, readout_mode):
    dims = dataTensor.shape
    tensorIxs = np.array(list(range(len(dims))))

    surrTensor0 = shuffle(dataTensor, shuffle_mode, fix_mode, cyclicShfl=True)

    reorderIx = [readout_mode] + list(np.sort(tensorIxs[tensorIxs != readout_mode]))

    surrTensor1 = np.moveaxis(surrTensor0, source=reorderIx, destination=tensorIxs)
    marg_cov = []
    for i in reorderIx:
        marg_cov.append(margCov[i])
    surrTensor, f, K = optMarginalCov(surrTensor1, marg_cov)

    ix = np.argsort(reorderIx)
    surrTensor = np.moveaxis(surrTensor, source=ix, destination=tensorIxs)
    surrTensor = surrTensor + meanTensor

    return surrTensor, f


def CFR(dataTensor, mask, model_dim, numSurrogates=100):
    dims = dataTensor.shape
    dataTensor = dataTensor.reshape(dims, order='F')

    shuffle_mode = 2
    fix_mode = 1
    readout_mode = 1

    R2_data = summarizeLDS(dataTensor[mask.flatten()], model_dim)
    targetSigmaT, targetSigmaN, targetSigmaC, M = extractFeatures(dataTensor)
    meanTensor = M['TNC']

    R2_surr = [[] for _ in range(numSurrogates)]

    for i in range(numSurrogates):
        print(f"Surrogate {i + 1}/{numSurrogates}")
        surrTensor, _ = sampleCFR(dataTensor, meanTensor, margCov=(targetSigmaT, targetSigmaN, targetSigmaC), shuffle_mode=shuffle_mode, fix_mode=fix_mode, readout_mode=readout_mode)
        surrTensor = surrTensor.squeeze()
        R2_surr[i] = summarizeLDS(surrTensor[mask.flatten()], model_dim)

    P = np.mean(R2_data <= R2_surr)
    if P >= 0.05:
        print(f'P value = {P}\n', )
    else:
        print(f'P value < {(P < 0.001) * 0.001 + (P < 0.01 and P >= 0.001) * 0.01 + (P < 0.05 and P >= 0.01) * 0.05}\n', )

    x = np.arange(0, 1, 0.03)
    plt.hist(R2_surr, x, label='surrogate data')
    plt.scatter(R2_data, 0, c='k', s=100, marker='o', label="original data")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    model_dim = 10

    import scipy.io

    data = scipy.io.loadmat('./exampleData.mat')
    dataTensor = data['dataTensor']
    print(dataTensor.shape)
    t = data['t']

    mask = np.logical_and(t > - 50, t < 350)
    CFR(dataTensor, mask, model_dim)

