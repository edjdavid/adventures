import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()

im = Image.open('test.jpg').transpose(Image.FLIP_TOP_BOTTOM)
# im = im.resize((im.size[0] // 2, im.size[1] // 2), Image.ANTIALIAS)
data = np.asarray(im, dtype=float)
data = data / np.max(data)
X, Y = np.mgrid[0:data.shape[0], 0:data.shape[1]]

ax = plt.gca(projection='3d', axisbg='gray')
ax.set_axis_off()
opts = {
    'rstride': 1,  # lower = higher quality, higher = faster
    'cstride': 1,
    'cmap': cm.BrBG
}

# ax.view_init(elev=None, azim=None)
for i in range(1, 5, 1):
    # change data here to show different images
    ax.plot_surface(i, Y, X, facecolors=data, **opts)

plt.savefig('output.png')
