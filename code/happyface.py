"""
This file is part of the CroMagnon project.
Copyright 2015 David W. Hogg (NYU)
"""

import numpy as np
from matplotlib import pylab as plt
plt.rcParams['figure.figsize'] = 10, 10
from scipy.misc import logsumexp

def get_Truth():
    Truth = np.zeros((8,8))
    Truth[3,2] = 1.
    Truth[5,2] = 1.
    Truth[3:6,4] = 1.
    return Truth

def make_data(Truth, nimages, noiselevel):
    ny, nx = Truth.shape
    shape = (nimages, ny, nx)
    data = np.zeros(shape)
    for ii in range(nimages):
        foo = np.rot90(Truth, np.random.randint(4)) # magic 4
        foo = np.roll(foo, np.random.randint(ny), axis=0)
        foo = np.roll(foo, np.random.randint(nx), axis=1)
        data[ii,:,:] = foo + noiselevel * np.random.normal(size=(ny, nx))
    return data

def ln_marginal_like(data, model, noiselevel):
    """
    ## bugs:
    - needs serious vetting
    """
    nimages, ny, nx = data.shape
    mu = np.reshape(model, (ny, nx))
    ln_like_vec = np.zeros((4 * ny * nx, nimages)) # magic 4
    ii = 0
    for rotation in range(4): # magic 4
        mu = np.rot90(mu, rotation)
        for yshift in range(ny):
            mu = np.roll(mu, yshift, axis=0)
            for xshift in range(nx):
                mu = np.roll(mu, xshift, axis=1)
                chi = (data - mu[None,:,:]) / noiselevel
                ln_like_vec[ii,:] = -0.5 * np.sum(np.sum(chi * chi, axis=2), axis=1)
                ii += 1
    return np.sum(logsumexp(ln_like_vec, axis=0))

def objective(model, data, noiselevel):
    return -2. * ln_marginal_like(data, model, noiselevel)

def plot_one_image(ax, image, noiselevel):
    return ax.imshow(image,
                     cmap="gray",
                     interpolation="nearest",
                     vmin=0.-2*noiselevel, vmax=1.+2*noiselevel)

def hogg_savefig(fn):
    print("saving {}".format(fn))
    return plt.savefig(fn)

if __name__ == "__main__":

    # make truth
    np.random.seed(42)
    Truth = get_Truth()
    ny, nx = Truth.shape

    # make and show data
    noiselevel = 0.2
    data = make_data(Truth, 1000, noiselevel)
    plt.clf()
    foo, axes = plt.subplots(4, 4, sharex='col', sharey='row')
    axes = axes.flatten()
    for ii, ax in enumerate(axes):
        plot_one_image(ax, data[ii], noiselevel)
    hogg_savefig("data.png")

    # initialize model
    model0 = np.zeros_like(Truth)
    model0[2:6,2:6] = np.random.uniform(size=(4,4))
    model0 = model0.ravel()
    plt.clf()
    foo, axes = plt.subplots(4, 4, sharex='col', sharey='row')
    axes = axes.flatten()
    plot_one_image(axes[0], model0.reshape((ny, nx)), noiselevel)
    hogg_savefig("model.png")

    # optimize
    from scipy import optimize as op
    for ii in range(16):
        result = op.minimize(objective, model0, args=(data, noiselevel),
                             options={"maxiter": 1})
        model0 = result["x"]
        plot_one_image(axes[ii+1], model0.reshape((ny, nx)), noiselevel)
        hogg_savefig("model.png")
