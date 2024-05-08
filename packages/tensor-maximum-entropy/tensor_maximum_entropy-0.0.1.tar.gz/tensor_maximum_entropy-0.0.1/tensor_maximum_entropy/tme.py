import numpy as np
from matplotlib import pyplot as plt

from .utils import minimize, summarizeLDS, extractFeatures, sumTensor


def diagKronSum(Ds):
    tensorSize = len(Ds)
    kronSumDs = 0
    for x in range(tensorSize):
        term1 = kronSumDs * np.ones((len(Ds[x]), 1)).T
        term2 = np.ones((1 if type(kronSumDs) == int else len(kronSumDs), 1)) * Ds[x][:, np.newaxis].T
        kronSumDs = term1 + term2
        kronSumDs = kronSumDs.reshape((-1, 1), order='F')

    return kronSumDs

def logObjectiveMaxEntropyTensor(logL, logEigValues):
    normalizeTerm = np.linalg.norm((np.hstack(logEigValues)), 2)**2
    tensorSize = len(logEigValues)
    dim = [[] for _ in range(tensorSize)]
    lagrangians = [[] for _ in range(tensorSize)]
    logLs = [[] for _ in range(tensorSize)]


    tensorIxs = np.array(list(range(tensorSize)))
    for x in tensorIxs:
        dim[x] = len(logEigValues[x])
        logLs[x] = logL[np.array(sum(dim[0:x])+np.array(list(range(dim[x])))).astype(int)]
        lagrangians[x] = np.exp(logLs[x])

    LsTensor = diagKronSum(lagrangians)
    LsTensor = np.reshape(LsTensor, tuple(dim), order='F')
    invLsTensor = 1. / LsTensor
    invSquareLsTensor = 1. / LsTensor ** 2

    error = [[] for _ in range(tensorSize)]
    fx = [[] for _ in range(tensorSize)]
    logSums = [[] for _ in range(tensorSize)]
    for x in tensorIxs:
        nxSet = tensorIxs[tensorIxs != x]
        logSums[x] = np.log(sumTensor(invLsTensor, axis=tuple(nxSet)))
        error[x] = np.reshape(logEigValues[x], logSums[x].shape, order='F') - logSums[x]
        fx[x] = np.reshape(error[x], dim[x], order='F') ** 2

    f = np.sum(np.hstack(fx)) / normalizeTerm


    # build the gradient from the blocks
    gradf_logL = np.zeros((sum(dim), 1))
    for x in tensorIxs:
        nxSet = tensorIxs[tensorIxs != x]
        tensor1 = 2 * error[x] / sumTensor(invLsTensor, axis=tuple(nxSet))
        tensor2 = sumTensor(invSquareLsTensor, axis=tuple(nxSet))
        gradfx_logLx = np.reshape(tensor1 * tensor2, (dim[x], ), order='F') * lagrangians[x].flatten()

        gradfy_logLx = np.zeros((dim[x], tensorSize-1))
        z = 0
        for y in nxSet:
            nySet = tensorIxs[tensorIxs != y]
            nxySet = tensorIxs[np.logical_and(tensorIxs!=x, tensorIxs!=y)]

            tensor1 = 2 * error[y] / sumTensor(invLsTensor, tuple(nySet))
            tensor2 = sumTensor(invSquareLsTensor, tuple(nxySet))
            tensor = sumTensor(tensor1 * tensor2, [y])
            gradfy_logLx[:, z] = np.reshape(tensor, (dim[x],), order='F') * lagrangians[x].flatten()

            z += 1

        gradf_logLx = np.sum(np.hstack([gradfx_logLx[:, np.newaxis], gradfy_logLx]), axis=-1)
        gradf_logL[np.array(sum(dim[0:x])+np.array(list(range(dim[x])))).astype(int)] = gradf_logLx[:, np.newaxis]

    gradf_logL = gradf_logL / normalizeTerm
    return f, gradf_logL




def objectiveMaxEntropyTensor(L, eigValues):
    normalizeTerm = np.linalg.norm((np.hstack(eigValues)), 2) ** 2
    tensorSize = len(eigValues)
    dim = [[] for _ in range(tensorSize)]
    lagrangians = [[] for _ in range(tensorSize)]

    tensorIxs = np.array(list(range(tensorSize)))
    for x in tensorIxs:
        dim[x] = len(eigValues[x])
        lagrangians[x] = L[np.array(sum(dim[0:x]) + np.array(list(range(dim[x])))).astype(int)]

    LsTensor = diagKronSum(lagrangians)
    LsTensor = np.reshape(LsTensor, tuple(dim), order='F')
    invLsTensor = 1. / LsTensor
    invSquareLsTensor = 1. / LsTensor ** 2

    error = [[] for _ in range(tensorSize)]
    fx = [[] for _ in range(tensorSize)]
    Sums = [[] for _ in range(tensorSize)]
    for x in tensorIxs:
        nxSet = tensorIxs[tensorIxs != x]
        Sums[x] = sumTensor(invLsTensor, axis=tuple(nxSet))
        error[x] = np.reshape(eigValues[x], Sums[x].shape, order='F') - Sums[x]
        fx[x] = np.reshape(error[x], dim[x], order='F') ** 2

    f = np.sum(np.hstack(fx)) / normalizeTerm

    # build the gradient from the blocks
    gradf_L = np.zeros((sum(dim), 1))
    for x in tensorIxs:
        nxSet = tensorIxs[tensorIxs != x]
        tensor1 = 2 * error[x]
        tensor2 = sumTensor(invSquareLsTensor, axis=tuple(nxSet))
        gradfx_Lx = np.reshape(tensor1 * tensor2, (dim[x],), order='F')

        gradfy_Lx = np.zeros((dim[x], tensorSize - 1))
        z = 0
        for y in nxSet:
            nxySet = tensorIxs[np.logical_and(tensorIxs != x, tensorIxs != y)]

            tensor1 = 2 * error[y]
            tensor2 = sumTensor(invSquareLsTensor, tuple(nxySet))
            tensor = sumTensor(tensor1 * tensor2, [y])
            gradfy_Lx[:, z] = np.reshape(tensor, (dim[x],), order='F')

            z += 1

        gradfx_Lx = np.sum(np.hstack([gradfx_Lx[:, np.newaxis], gradfy_Lx]), axis=-1)
        gradf_L[np.array(sum(dim[0:x]) + np.array(list(range(dim[x])))).astype(int)] = gradfx_Lx[:, np.newaxis]

    gradf_L = gradf_L / normalizeTerm
    return f, gradf_L

def fitMaxEntropy(margCov, meanTensor):
    tensorSize = len(margCov)
    eigVectors = [[] for _ in range(tensorSize)]
    eigValues = [[] for _ in range(tensorSize)]
    traceSigmas = [[] for _ in range(tensorSize)]

    dim = list(meanTensor.shape)
    for i in range(tensorSize):
        trace = np.trace(margCov[i])

    for i in range(tensorSize):
        sigma = margCov[i]

        Q, S, Vh = np.linalg.svd(sigma)

        S = np.sort(S)[::-1]
        ix = np.argsort(S)[::-1]
        Q = Q[:, ix]

        eigVectors[i] = Q
        eigValues[i] = S
        traceSigmas[i] = np.trace(sigma)


    # if the marginal covariances are low rank then the number of variables
    # that we solve for are less. If full rank the number of variables that we
    # solve for are equal to the sum of the tensor dimensions.
    tensorSize = len(eigValues)
    threshold = -10

    for i in range(tensorSize):
        dim[i] = len(eigValues[i])

    # print(dim)
    preScale = np.sum(eigValues[1]) / np.mean(dim)
    # print(preScale)
    logEigValues = [[] for _ in range(tensorSize)]
    optDim = [[] for _ in range(tensorSize)]

    for x in range(tensorSize):
        logEigValues[x] = np.log(eigValues[x] / preScale)
        logEigValues[x] = logEigValues[x][logEigValues[x] > threshold]
        optDim[x] = len(logEigValues[x])

    # instead of solving for the largrangians directly we optimize latent variables that is equal to the log of the lagrangians
    # initialization of the optimization variables
    logL0 = [[] for _ in range(tensorSize)]
    tensorIxs = np.array(list(range(tensorSize)))
    optDim = np.array(optDim)
    for x in tensorIxs:
        nxSet = tensorIxs[tensorIxs!=x]
        logL0[x] = np.log(np.sum(optDim[nxSet])) - logEigValues[x]

    # optimization step
    maxiter = 10000

    logL, logObjperIter, i = minimize(logObjectiveMaxEntropyTensor, np.hstack(logL0), maxiter, logEigValues)
    L = np.exp(logL)

    lagrangians = [[] for _ in range(tensorSize)]
    for x in tensorIxs:
        a1 = L[np.array(sum(optDim[0:x]) + np.array(list(range(optDim[x])))).astype(int)]
        a2 = np.inf * np.ones(shape=(dim[x]-optDim[x], ))
        lagrangians[x] = np.concatenate([a1, a2], axis=0) / preScale

    objCost, _ = objectiveMaxEntropyTensor(np.concatenate(lagrangians), eigValues)
    logObjCost, _ = logObjectiveMaxEntropyTensor(logL, logEigValues)

    return lagrangians, objCost, logObjperIter, meanTensor, eigVectors


def kron_mvprod(As, b):
    x = np.copy(b)
    numDraws = b.shape[1]
    CTN = x.shape[0]

    for d in range(len(As)):
        A = As[d]
        Gd = len(A)
        X = np.reshape(x, (Gd, int(CTN*numDraws/Gd)), order='F')
        Z = np.matmul(A, X)
        Z = Z.T
        x = np.reshape(Z, (CTN, numDraws), order='F')

    x = np.reshape(x, (CTN, numDraws), order='F')

    return x



def sampleTME(lagrangians, objCost, logObjperIter, meanTensor, eigVectors, numSurrogates=None):
    if numSurrogates is None:
        numSurrogates = 1

    dim = [len(eigVectors[i]) for i in range(len(eigVectors))]

    D = 1/diagKronSum(lagrangians)

    x = np.random.randn(np.prod(dim), numSurrogates)
    # x = np.ones((np.prod(dim), numSurrogates)) / 10
    x = np.sqrt(D) * x

    x = kron_mvprod(eigVectors, x)

    x = x.flatten() + np.repeat(meanTensor.T.flatten(), numSurrogates)
    surrTensors = np.reshape(x, tuple(dim + [numSurrogates]), order='F')

    return surrTensors



def TME(dataTensor, mask, model_dim, numSurrogates=1000):
    dims = dataTensor.shape
    dataTensor = dataTensor.reshape(dims, order='F')

    R2_data = summarizeLDS(dataTensor[mask.flatten()], model_dim)
    targetSigmaT, targetSigmaN, targetSigmaC, M = extractFeatures(dataTensor)
    meanTensor = M['TNC']

    lagrangians, objCost, logObjperIter, meanTensor, eigVectors = fitMaxEntropy((targetSigmaT, targetSigmaN, targetSigmaC), meanTensor)

    R2_surr = [[] for _ in range(numSurrogates)]

    for i in range(numSurrogates):
        print(f"Surrogate {i + 1}/{numSurrogates}")
        surrTensor = sampleTME(lagrangians, objCost, logObjperIter, meanTensor, eigVectors)
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
    TME(dataTensor, mask, model_dim)
