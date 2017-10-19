from __future__ import print_function
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.text import Text
from matplotlib.image import AxesImage
import numpy as np
from numpy.random import rand

def line_picker(line, mouseevent):
    """
    find the points within a certain distance from the mouseclick in
    data coords and attach some extra attributes, pickx and picky
    which are the data points that were picked
    """
    if mouseevent.xdata is None:
        return False, dict ()
    xdata = line.get_xdata ()
    ydata = line.get_ydata ()
    maxd = 0.05
    d = np.sqrt ((xdata - mouseevent.xdata) ** 2. + (ydata - mouseevent.ydata) ** 2.)

    ind = np.nonzero (np.less_equal (d, maxd))
    if len (ind):
        pickx = np.take (xdata, ind)
        picky = np.take (ydata, ind)
        props = dict (ind=ind, pickx=pickx, picky=picky)
        return True, props
    else:
        return False, dict ()


def onpick2(event):
    print(event.artist)


fig, ax = plt.subplots ()
ax.set_title ('custom picker for line data')
line, = ax.plot (rand (2), rand (2), picker=line_picker)
fig.canvas.mpl_connect ('pick_event', onpick2)
plt.show()