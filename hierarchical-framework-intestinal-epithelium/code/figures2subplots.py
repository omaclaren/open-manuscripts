"""Arrange existing matplotlib figures into subplots"""
import numpy as np
from matplotlib.figure import *


def multisubplot(figures=[], ratio=1.0, wspace=0.0, hspace=0.0):
    """Arrange existing matplotlib figures into subplots
    
    Source
    ------
    http://www.mail-archive.com/matplotlib-users@lists.sourceforge.net/msg06032.html
    """

    fig = Figure()

    n = len(figures)
    if n < 2:
        fig.add_subplot(111)
        return fig

    # calculate number of rows and columns
    columns = int(np.ceil(np.sqrt(float(n)/(ratio))))
    rows = int(np.ceil(float(n)/float(columns)))

    # resize the new figure
    w_inches = figures[0].get_size_inches()[0]*(columns)
    h_inches = figures[0].get_size_inches()[1]*(rows)

    fig.set_size_inches(w_inches, h_inches, forward=True)

    print fig.get_size_inches()

    # calculate the spacing
    wspace = wspace / (float(columns))
    hspace = hspace / (float(rows))

    # calculate the l,b,w,h of all subplots
    width = 1/float(columns) - wspace
    height = 1/float(rows) - hspace

    positions = []
    for i in range(rows):
        for j in range(columns):
            positions.append([(j)*(width + wspace) + wspace/2, \
                    (rows-i-1)*(height + hspace) + hspace/2 , \
                    width, height])

    # hack broken axes scaling
    for pos in positions:
        print ''
        #pos[0] = pos[0] * (columns)
        #pos[1] = pos[1] * (rows)
        #pos[2] = pos[2] * (columns)
        #pos[3] = pos[3] * (rows)

    print n
    print 'columns', columns, 'rows', rows
    print 'wspace', wspace, 'hspace', hspace
    print 'width', width, 'height', height
    for pos in positions:
        print pos

    for i in xrange(rows):
        for j in xrange(columns):
            x = i*(columns) + j
            if x < n:
                for ax in figures[x].axes:
                    figures[x].delaxes(ax)
                    ax.set_figure(fig)
                    fig.add_axes(ax)
                    ax.set_position(positions[x])

    return fig

if __name__ == '__main__':

    #create some figures to pass to our function
    pl = []
    for i in range(13):
        fig = Figure()
        ax = fig.add_subplot(111)
        ax.plot([1,np.sin(i),2])
        pl.append(fig)

    figsub = multisubplot(pl,ratio=1, wspace=0.1, hspace=0.1)
