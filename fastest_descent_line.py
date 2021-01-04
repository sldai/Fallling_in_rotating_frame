"""Simulation of the fastest descent line 
"""

import numpy as np
import matplotlib.pyplot as plt

class C:
    r = 10 # [m], cycloid radius
    phi = np.pi*1.3 # [rad], cycloid angle
    g = 9.8 # [m/s^2], gravity
    dt = 0.1 # [s], time step

def invert_cycloid():
    phi = np.linspace(0, C.phi, 100)
    x = C.r*(phi-np.sin(phi))
    y = -C.r*(1-np.cos(phi))
    return x, y

def straight_line():
    x_start, y_start = 0, 0
    x_end = C.r*(C.phi-np.sin(C.phi))
    y_end = -C.r*(1-np.cos(C.phi))
    x = np.linspace(x_start, x_end, 1000)
    y = np.linspace(y_start, y_end, 1000)
    return x, y

def vertical_horizon_line():
    x_start, y_start = 0, 0
    x_end = C.r*(C.phi-np.sin(C.phi))
    y_end = -C.r*(1-np.cos(C.phi))
    x = np.concatenate([np.zeros(50), np.linspace(x_start, x_end, 50)])
    y = np.concatenate([np.linspace(y_start, y_end, 50), np.zeros(50)+y_end])
    return x, y

def simu(x, y):
    """Simulate the process of the object sliding on the curve
    Args:
        x : curve x
        y : curve y 
    
    Returns:
        t : arrivial time for each point in the curve
    """
    tc = 0
    t = [tc]
    for ind in range(1,len(x)):
        v = (np.sqrt(2*C.g*abs(y[ind]))+np.sqrt(2*C.g*abs(y[ind-1])))/2
        tc += np.hypot(x[ind]-x[ind-1], y[ind]-y[ind-1])/v
        t.append(tc)
    return t

def find_closet(t_tar, x, y, t):
    """Given target t, find the closest point
    """
    ind = np.argmin(np.abs(t_tar-t))
    return x[ind], y[ind], t[ind]

def main():
    x_ic, y_ic = invert_cycloid()
    x_st, y_st = straight_line()
    x_vh, y_vh = vertical_horizon_line()
    
    # trajectories
    t_ic = simu(x_ic, y_ic)
    t_st = simu(x_st, y_st)
    t_vh = simu(x_vh, y_vh)
    max_t = np.max([t_ic[-1], t_st[-1], t_vh[-1]])
    print([t_ic[-1], t_st[-1], t_vh[-1]])
    imgs = []
    for t_ref in np.arange(0, max_t+C.dt, C.dt):
        plt.cla()
        plt.plot(x_ic, y_ic+0.5, c='white')
        plt.plot(x_ic, y_ic, c='tab:red')
        plt.plot(x_st, y_st, c='tab:blue')
        plt.plot(x_vh, y_vh, c='tab:blue')
        x,y,t = find_closet(t_ref, x_ic, y_ic, t_ic)
        plt.plot(x, y+0.5, '-o', c='tab:red')
        x,y,t = find_closet(t_ref, x_st, y_st, t_st)
        plt.plot(x, y+0.5, '-o', c='tab:blue')
        x,y,t = find_closet(t_ref, x_vh, y_vh, t_vh)
        plt.plot(x, y+0.5, '-o', c='tab:blue')

        plt.axis('equal')
        plt.axis('off')
        plt.tight_layout()
        # plt.pause(C.dt/2)
        plt.savefig('tmp.png')
        imgs.append(plt.imread('tmp.png'))
    imageio.mimsave('fastest_line.gif',imgs,duration=C.dt)
    # plt.show()
import imageio
if __name__ == "__main__":
    main()    