# Allan Variance Tools

## Array of Windows

```python
avar.windows(K, density=64)
```

This will create an array `M` of integer window sizes. The averaging period
`tau` would equal `M*T`, where `T` is the sampling period. The `density` is the
target number of window sizes in the array per decade. Obviously, in the first
decade it is not possible to have more than 9 window sizes: 1 through 9.

## Signal Allan Variance

```python
avar.variance(y, M)
```

To get the actual Allan variance of a signal `y`, use this function. You must
supply the array of window sizes `M` for which to calculate the Allan variance
values. This function can take for `y` either a one-dimensional array or a
two-dimensional array in which each row will be treated as a data set.

## Ideal Allan Variance

```python
avar.ideal(tau, vc, taub=None)
```

Given a set of five component noise variances `vc`, you can calculate what the
ideal Allan variances would be over an array of averaging periods `tau`. The
five component noises are quantization, white, flicker, walk, and ramp. Any
noise components you wish not to include, set their corresponding variances to
zero. If you wish to treat flicker noise as an idealized, flat Allan variance
over averaging period, leave the first-order, Gauss-Markov (FOGM) time constant,
`taub`, as None. If you wish to treat the flicker noise as a FOGM noise, set the
time constant to some non-zero value.

## Fitting to Signal Allan Variance

```python
avar.fit(tau, va, taub=None, mask=None, tol=0.007)
```

Given the Allan variance curve of some signal, `va`, at various averaging
periods `tau`, you can get the best fit using the five component noises. As with
the `ideal` function, if `taub` is left undefined, the flicker noise will be
treated as the idealized, flat Allan variance over averaging period. Otherwise,
the flicker noise will be treated as a first-order, Gauss-Markov noise. By
default, this function will automatically attempt to determine if certain
component noises are even at play based on the tolerance value `tol`. However,
you can directly control which component noises you wish to include or exclude
with the `mask` array. For each element of `mask` that is `False` the
corresponding component noise will be excluded.

## Noise Generation

```python
avar.noise(vc, K, T, taub=None)
```

Given a five-element array of component noise variances `vc`, you can create an
artificially-generated noise signal of length `K` and sampling period `T`. Each
element of `vc` corresponds to one of the five component noise types:
quantization, white, flicker, walk, and ramp. As with the `ideal` function, if
`taub` is left undefined, the flicker noise will be treated as the idealized,
flat Allan variance over averaging period. Otherwise, the flicker noise will be
treated as a first-order, Gauss-Markov noise.
