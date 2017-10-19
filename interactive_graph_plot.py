
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D


class DraggableEdge:
    def __init__(self, edge, max_d=.1):
        self.edge = edge
        self.press = None
        self.max_d = max_d

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.edge.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.edge.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.edge.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):

        d = np.sqrt ((self.edge.get_xdata() - event.xdata) ** 2. +
                     (self.edge.get_ydata() - event.ydata) ** 2.)

        ind = np.nonzero (np.less_equal (d, self.max_d))
        if len (ind):
            print ind
            self.press = ind, self.edge.get_xdata(), self.edge.get_ydata()

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None:
            return


        dx = event.xdata - self.press[1][self.press[0]]
        dy = event.ydata - self.press[2][self.press[0]]

        self.press[1][self.press[0]]+=dx
        self.press[2][self.press[0]]+=dy

        print dx, dy
        self.edge.set_data(self.press[1], self.press[2])
        self.edge.figure.canvas.draw()


    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.edge.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)


class DraggableRectangle:
    def __init__(self, rect):
        self.rect = rect
        self.press = None

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):

        contains, attrd = self.rect.contains(event)
        if not contains: return
        x0, y0 = self.rect.center
        self.press = x0, y0, event.xdata, event.ydata

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.rect.axes: return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        #print('x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f' %
        #      (x0, xpress, event.xdata, dx, x0+dx))
        self.rect.center = x0+dx, y0+dy


        self.rect.figure.canvas.draw()


    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.rect.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)

fig = plt.figure()
ax = fig.add_subplot(111)
fig.patch.set_visible(False)
ax.axis('off')
ax.set_xlim(0,1)
ax.set_ylim(0,1)
plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
circles = [Circle((x,y), radius=.1, clip_on=False) for x,y in np.random.random(size=(10,2))]

line, = ax.plot(np.random.rand(2), np.random.rand(2))
drs = []
ed = DraggableEdge(line)
ed.connect()

line1, = ax.plot(np.random.rand(2), np.random.rand(2))
drs = []
ed1 = DraggableEdge(line1)
ed1.connect()
for rect in circles:
    ax.add_patch (rect)
    dr = DraggableRectangle(rect)
    dr.connect()
    drs.append(dr)

plt.show()
