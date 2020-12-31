"""
Simulation of the object falling in a rotating frame
"""
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

class C:
    g = 9.8 # [m], gravity
    omega = np.pi*2/24/3600 # [rad], angular velocity of the earth
    r = 6378.0*1000/2 # [m], the earth radius
    draw_r = 800 # [m], the earth radius for plot
    h = 158.5 # [m], object init height


def state_dot(x, t):
    """ODE of the falling object
    Args:
        x (array): [r, theta, r_dot, theta_dot]
        t : time
    """
    r, theta, r_dot, theta_dot = x
    
    r_dot = r_dot
    theta_dot = theta_dot
    r_dot_dot = r*theta_dot**2 - C.g
    theta_dot_dot = (-2*r_dot*theta_dot)/r

    x_dot = np.array([r_dot, theta_dot, r_dot_dot, theta_dot_dot])
    return x_dot

def draw_earth(theta):
    angles = np.linspace(theta, np.pi*2+theta, 100)
    outer_circle = np.array([np.cos(angles)*(C.draw_r+C.h), np.sin(angles)*(C.draw_r+C.h)])
    inner_circle = np.array([np.cos(angles)*(C.draw_r), np.sin(angles)*(C.draw_r)])
    
    plt.plot(inner_circle[0,:], inner_circle[1,:], '->',c='k')
    plt.plot(outer_circle[0,:], outer_circle[1,:], c='white')

def draw_object_people(object_x, p):
    """
    x : object state
    p : people state
    """
    def polar2xy(r, theta):
        r = r - C.r + C.draw_r
        theta = (theta-np.pi/2) * 3600 + np.pi/2
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return x, y
    x, y = polar2xy(object_x[0], object_x[1])    
    plt.plot(x,y, '-o', c='tab:red')
    x, y = polar2xy(p[0], p[1])    
    plt.plot(x,y, '-x', c='tab:blue')
    Arrow(0,0,math.atan2(y,x),C.draw_r-100,'k')

class Arrow:
    def __init__(self, x, y, theta, L, c):
        angle = np.deg2rad(30)
        d = 0.4 * L
        w = 2

        x_start = x
        y_start = y
        x_end = x + L * np.cos(theta)
        y_end = y + L * np.sin(theta)

        theta_hat_L = theta + math.pi - angle
        theta_hat_R = theta + math.pi + angle

        x_hat_start = x_end
        x_hat_end_L = x_hat_start + d * np.cos(theta_hat_L)
        x_hat_end_R = x_hat_start + d * np.cos(theta_hat_R)

        y_hat_start = y_end
        y_hat_end_L = y_hat_start + d * np.sin(theta_hat_L)
        y_hat_end_R = y_hat_start + d * np.sin(theta_hat_R)

        plt.plot([x_start, x_end], [y_start, y_end], color=c, linewidth=w)
        plt.plot([x_hat_start, x_hat_end_L],
                 [y_hat_start, y_hat_end_L], color=c, linewidth=w)
        plt.plot([x_hat_start, x_hat_end_R],
                 [y_hat_start, y_hat_end_R], color=c, linewidth=w)

def main():
    x0 = np.array([C.r+C.h, np.pi/2, 0, C.omega])
    p = np.array(x0)
    x = np.array(x0)
    dt = 0.1

    plt.figure('earth')
    plt.figure('ground')
    seq_x = []
    seq_p = []
    for i in range(100):
        t = i*dt
        x = odeint(state_dot, x, [0, dt])[-1]
        p[1] += dt * p[3]
        # seq_x.append(x.copy())
        # seq_p.append(p.copy())
        if x[0] <= C.r:
            break

        # plot
        plt.figure('earth')
        plt.cla()
        draw_earth((p[1]-np.pi/2) * 3600 + np.pi/2)
        draw_object_people(x, p)
        plt.axis('equal')
        plt.axis('off')
        plt.title('Earth view')

        plt.figure('ground')
        plt.cla()
        ground_object_x = - x[0] * np.sin(x[1] - p[1])
        ground_object_y = x[0] * np.cos(x[1] - p[1]) - p[0] + C.h
    
        plt.plot(ground_object_x*100, ground_object_y, '-o', c='tab:red')
        plt.plot(0, C.h, '-x', c='tab:blue')
        plt.axis([-10,10, 0,200])
        plt.xlabel('X (cm)')
        plt.ylabel('Height (m)')
        plt.title('Ground view')
        plt.pause(dt)
    plt.show()

if __name__ == "__main__":
    main()