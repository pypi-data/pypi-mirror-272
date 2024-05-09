"""
Copyright 2024 David Woodburn

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__author__ = "David Woodburn"
__license__ = "MIT"
__date__ = "2024-05-08"
__maintainer__ = "David Woodburn"
__email__ = "david.woodburn@icloud.com"
__status__ = "Development"

import numpy as np
import scipy.optimize as opt


def windows(K, density=64):
    """
    Build an array of averaging window sizes for Allan variances analysis.

    Parameters
    ----------
    K : int
        Number of time samples.
    density : int, default 64
        Desired number of window sizes per decade.

    Returns
    -------
    M : integer np.ndarray
        Array of averaging window sizes.

    Notes
    -----
    Because the elements of `M` should be unique, it cannot be guaranteed that
    there will be exactly `density` sizes in each decade.
    """

    e_max = np.log10(np.floor(K/2))
    M_real = np.logspace(0, e_max, round(e_max*density))
    M = np.unique(np.round(M_real)).astype(int)
    return M


def variance(y, M):
    """
    Calculate the Allan variance of y with the array of averaging window sizes
    specified by M.

    Parameters
    ----------
    y : (K,) or (J, K) float np.ndarray
        Array of `K` values in time or matrix of rows of such arrays.
    M : (I,) integer np.ndarray
        Array of `I` averaging window sizes. Each element of `M` must be an
        integer.

    Returns
    -------
    v : (I,) float np.ndarray
        Array of `I` Allan variances.
    """

    if np.ndim(y) == 1:
        v = np.zeros(len(M))
        Y = np.cumsum(y)
        for n_tau, m in enumerate(M):
            Yc = Y[(2*m - 1):] # Ending integrals
            Yb = Y[(m - 1):(-m)] # Middle integrals
            Yj = Y[:(1 - 2*m)] # Beginning integrals
            yj = y[:(1 - 2*m)] # Beginning
            delta = (Yc - 2*Yb + Yj - yj)/m
            v[n_tau] = np.mean(delta**2)/2
    else:
        J, K = y.shape
        v = np.zeros((J, len(M)))
        Y = np.cumsum(y, axis=1)
        for n_tau, m in enumerate(M):
            Yc = Y[:, (2*m - 1):] # Ending integrals
            Yb = Y[:, (m - 1):(-m)] # Middle integrals
            Yj = Y[:, :(1 - 2*m)] # Beginning integrals
            yj = y[:, :(1 - 2*m)] # Beginning
            delta = (Yc - 2*Yb + Yj - yj)/m
            v[:, n_tau] = np.mean(delta**2, axis=1)/2

    return v


def ideal(tau, vc, taub=None):
    """
    Generate an ideal Allan variance curve given the component variances.

    Parameters
    ----------
    tau : (I,) np.ndarray
        Array of averaging periods (s).
    vc : (5,) np.ndarray
        Component variances: quantization, white, flicker, walk, and ramp.
    taub : float, default None
        The time constant of the first-order, Gauss-Markov noise. If it is
        `None` then a constant-amplitude Allan variance curve is used.

    Returns
    -------
    va : (I,) np.ndarray
        Array of ideal Allan variances.
    va_comps : (5, I) np.ndarray
        Matrix of the 5 ideal Allan variance components.
    """

    # Get the flicker Allan variance.
    if (taub is None) or (taub == 0.0):
        flkr = (2*np.log(2))/np.pi + 0*tau
    else:
        p = np.exp(-tau[0]/taub)
        M = tau/tau[0]
        flkr = 1.0/M**2*(M*(1 - p)**2 + 2*p*M*(1 - p) - 2*p*(1 - p**M)
            - p*(1 - p**M)**2)/(1 - p)**2

    # Build the total Allan variance.
    va_comps = np.array([vc[0]*3/(tau**2), vc[1]*1/tau,
        vc[2]*flkr, vc[3]*tau/3, vc[4]*(tau**2)/2])
    va = np.sum(va_comps, axis=0)

    return va, va_comps


def fit(tau, va, taub=None, mask=None, tol=0.007):
    """
    Fit component variances to an Allan variance curve.

    Parameters
    ----------
    tau : (I,) np.ndarray
        Array of averaging periods (s).
    va : (I,) or (J, I) np.ndarray
        Array of Allan variances or matrix of rows of such arrays.
    taub : float, default None
        The time constant of the first-order, Gauss-Markov noise. If it is
        `None` then a constant-amplitude Allan variance curve is used.
    mask : (5,) bool array_like, default None
        Array to mask which component variances to use. If it is `None`, then no
        mask will be applied. When it is not `None`, the function will still
        return an array of 5 values for `vc`, but the values corresponding to
        `False` or `0` should be `0`.
    tol : float, default 0.007
        Normalized mean absolute error tolerance to meet as various combinations
        of the component noises are applied to the fitting.

    Returns
    -------
    vf : (I,) np.ndarray
        Fitted Allan variance curve.
    vc : (5,) np.ndarray
        Component variances: quantization, white, flicker, walk, and ramp.

    Notes
    -----
    Fit using non-negative least squares solver. It is better to normalize the
    `H` matrix by the `va` vector this way because it produces better results
    than fitting with `opt.nnls(H, va)[0]`.
    """

    # Get the flicker Allan variance based on whether a FOGM tau was given.
    if taub is None:
        flkr = 2*np.log(2)/np.pi + 0*tau
    else:
        p = np.exp(-tau[0]/taub)
        M = tau/tau[0]
        flkr = 1.0/M**2*(M*(1 - p)**2 + 2*p*M*(1 - p) - 2*p*(1 - p**M)
            - p*(1 - p**M)**2)/(1 - p)**2

    # Build the other component Allan variance factors.
    qnt = 3/(tau**2)
    wht = 1/tau
    bwn = tau/3
    rmp = (tau**2)/2

    # Assemble the full, normalized Allan variance factor matrix.
    H_full = np.array([qnt, wht, flkr, bwn, rmp]).T

    # Get size of va.
    if np.ndim(va) == 1:
        J = 0
        I = len(va)
    else:
        J, I = va.shape

    # Estimate the component variances.
    if (mask is not None) and (len(mask) == 5) and (np.sum(mask) < 5):
        H = H_full[:, mask]
        N = H.shape[1] # number of components to consider
        if J == 0:
            vcp = opt.nnls(H/va[:, None], np.ones(len(tau)))[0]
            vf = H @ vcp # fitted Allan variance
            vc = np.zeros(5) # complete array of component variances
            vc[mask] = vcp # copy into the appropriate places
        else:
            vc = np.zeros((J, 5)) # complete array of component variances
            vf = np.zeros((J, I))
            for j in range(J):
                vcp = opt.nnls(H/va[j:j+1].T, np.ones(len(tau)))[0]
                vf[j] = H @ vcp # fitted Allan variance
                vc[j, mask] = vcp # copy into the appropriate places
    else:
        valg = np.log10(va)
        span = np.max(valg, axis=-1) - np.min(valg, axis=-1)
        mask_values = np.concatenate((np.arange(15)*2 + 2, np.arange(16)*2 + 1))
        if J == 0:
            vc = np.zeros(5) # complete array of component variances
            vf = np.zeros(I) # fitted Allan variance
            nmae_min = np.inf # minimum normalized mean absolute error
            for m in mask_values:
                mask = [bool((m >> i) & 1) for i in range(5)]
                H = H_full[:, mask]
                try:
                    vcp = opt.nnls(H/va[:, None], np.ones(len(tau)))[0]
                except ValueError or RuntimeError:
                    continue
                vfp = H @ vcp # fitted Allan variance
                er = valg - np.log10(vfp)
                nmae = np.mean(np.abs(er))/span
                if nmae < nmae_min: # save the best
                    nmae_min = nmae
                    vf = vfp.copy() # save this fitted Allan variance
                    vc[mask] = vcp # copy into the appropriate places
                if nmae < tol: # quit early
                    break
        else:
            vc = np.zeros((J, 5))
            vf = np.zeros((J, I))
            for j in range(J):
                nmae_min = np.inf # minimum normalized mean absolute error
                for m in mask_values:
                    mask = [bool((m >> i) & 1) for i in range(5)]
                    H = H_full[:, mask]
                    try:
                        vcp = opt.nnls(H/va[j:j+1].T, np.ones(len(tau)))[0]
                    except ValueError or RuntimeError:
                        continue
                    vfp = H @ vcp # fitted Allan variance
                    er = valg[j] - np.log10(vfp)
                    nmae = np.mean(np.abs(er))/span[j]
                    if nmae < nmae_min: # save the best
                        nmae_min = nmae
                        vf[j] = vfp.copy() # save this fitted Allan variance
                        vc[j, mask] = vcp # copy into the appropriate places
                    if nmae < tol: # quit early
                        break

    return vf, vc


def noise(vc, K, T, taub=None):
    """
    Generate noise using the 5 component variances of the Allan variance
    analysis. The component noises are generated as the following:

        Type            Implementation
        ------------    ---------------------------------------
        quantization    differentiated white, Gaussian noise
        white           white, Gaussian noise
        flicker         first-order, Gauss-Markov (FOGM) noise
        walk            integrated white, Gaussian noise
        ramp            doubly integrated white, Gaussian noise

    Parameters
    ----------
    vc : (5,) np.ndarray
        Component variances: quantization, white, flicker, walk, and ramp.
    K : int
        Number of samples.
    T : float
        Sampling period (s).
    taub : float, default None
        The time constant of the FOGM noise (s). If it is None, it will default
        to the `T sqrt(K/2)`.

    Returns
    -------
    n : (K,) np.ndarray
        Array of noise values over time.

    Notes
    -----
    Vectorizing this function to generate multiple rows of noise data does not
    actually improve the computation time above calling this function within a
    loop.

    Doubly integrated white noise grows faster the longer the signal. Therefore,
    in order to get the Allan variance of this generated noise to match the
    expected ideal Allan variance magnitude, the amplitude of the noise signal
    is scaled according to the number of samples.

    The scaling factors for the quantization and ramp noises have been empiric-
    ally, not analytically, derived. However, given their simplicity (`1` and
    `sqrt(2)`, respectively) and the very small errors between the average Allan
    variance curves of 10 thousand Monte-Carlo samples of noise and the ideal
    Allan variance curve, it seems they are correct.
    """

    # Initialize the noise array.
    n = np.zeros(K)

    # Quantization noise
    if vc[0] != 0:
        w = np.random.randn(K + 1)
        n += np.sqrt(vc[0])*np.diff(w)/T

    # White noise
    if vc[1] != 0:
        w = np.random.randn(K)
        n += np.sqrt(vc[1]/T)*w

    # Bias instability (flicker)
    if vc[2] != 0:
        if taub is None:
            taub = T*np.sqrt(K/2)
        ka = np.exp(-T/taub)
        kb = np.sqrt(vc[2]*(1 - np.exp(-2*T/taub)))
        eta = kb*np.random.randn(K)
        x = np.sqrt(vc[2])*np.random.randn() # state
        for k in range(K):
            n[k] += x
            x = ka*x + eta[k]

    # Random walk noise
    if vc[3] != 0:
        w = np.random.randn(K)
        n += np.cumsum(np.sqrt(vc[3]*T)*w)

    # Ramp noise
    if vc[4] != 0:
        eta = np.sqrt(2*vc[4]/K) * T * np.random.randn(K)
        n += np.cumsum(np.cumsum(eta))

    return n
