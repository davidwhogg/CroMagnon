"""
This file is part of the CroMagnon project.
Copyright 2015 David W. Hogg (NYU)
"""

import numpy as np
from matplotlib import pylab as plt
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

def plot_one_image(ax, image, noiselevel):
    ax.imshow(image,
              cmap="gray",
              interpolation="nearest",
              vmin=0.-2*noiselevel, vmax=1.+2*noiselevel)
    return None

if __name__ == "__main__":

    # make truth
    np.random.seed(42)
    Truth = get_Truth()

    # make and show data
    noiselevel = 0.2
    data = make_data(Truth, 1000, noiselevel)
    for ii in range(8):
        plt.clf()
        plot_one_image(plt.gca(), data[ii], noiselevel)
        plt.savefig("data_{:03d}.png".format(ii))

    # initialize model
    model = np.zeros_like(Truth)
    model[2:6,2:6] = np.random.uniform(size=(4,4))
    print(ln_marginal_like(data, model, noiselevel))

    # optimize
