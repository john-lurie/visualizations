"""
Calculate and plot the acceleration across an object due to an external field.
"""
import math

import matplotlib.pyplot as plt
import numpy as np


def calculate_accel(source, center, points):
    """
    Calculate the gravitational and tidal accelerations at an array of points.

    The center of the object is treated separately from points on the object's
    surface, because it is assumed that the results will be used to plot the
    acceleration due to gravity at every location as well as the *difference*
    between the acceleration at the surface and the center, i.e. the tidal
    acceleration.

    There are no units in the calculation:
        a_g = 1 / r**2

    Args:
        source (tuple): x,y,z scalar coordinates of the source of gravity.
        center (tuple): x,y,z scalar coordinates of the center of the body.
        points (tuple): x,y,z numpy arrays of coordinates of points.

    Returns:
        a_gc (tuple): x,y,z components of accel. due to gravity at center.
        a_gp (tuple): x,y,z components of accel. due to gravity at points.
        a_tp (tuple): x,y,z components of accel. due to tides at points.
    """
    # Unpack tuples
    x_S, y_S, z_S = source
    x_c, y_c, z_c = center
    x_p, y_p, z_p = points
    # Components of distance from center to source
    r_cx = x_S - x_c
    r_cy = y_S - y_c
    r_cz = z_S - z_c
    # Magnitude of distance
    r_c = math.sqrt(r_cx**2 + r_cy**2 + r_cz**2)

    # Distances (plural) from points to source
    r_px = x_S - x_p
    r_py = y_S - y_p
    r_pz = z_S - z_p
    # Magnitude of distances
    r_p = np.sqrt(r_px**2 + r_py**2 + r_pz**2)

    # Acceleration magnitudes due to gravity of source
    a_gc = 1 / r_c**2
    a_gp = 1 / r_p**2

    # Unit vectors for acceleration directions
    # Center
    u_cx = r_cx / r_c
    u_cy = r_cy / r_c
    u_cz = r_cz / r_c
    # Points
    u_px = r_px / r_p
    u_py = r_py / r_p
    u_pz = r_pz / r_p

    # Components of gravitaional acceleration vectors
    # Center
    a_gcx = a_gc * u_cx
    a_gcy = a_gc * u_cy
    a_gcz = a_gc * u_cz
    # Points
    a_gpx = a_gp * u_px
    a_gpy = a_gp * u_py
    a_gpz = a_gp * u_pz

    # Components of tidal acceleration
    a_tpx = a_gpx - a_gcx
    a_tpy = a_gpy - a_gcy 
    a_tpz = a_gpz - a_gcz

    # Pack it all up as tuples
    a_gc = (a_gcx, a_gcy, a_gcz)
    a_gp = (a_gpx, a_gpy, a_gpz)
    a_tp = (a_tpx, a_tpy, a_tpz)

    return a_gc, a_gp, a_tp


def arrow_2D(axis, xx, yy, a_x, a_y, color, scale=1.0):
    """
    Add a 2D arrow to a matplotlib.axes object.

    Trial and error may be required, adjusting the 'scale' parameter to
    obtain the desired arrow lengths.

    Args:
        axis (matplotlib.axes): axes object
        xx (float): x-coordinate of the arrow tail
        yy (float): y-coordinate of the arrow tail
        a_x (float): x-component of acceleration
        a_y (float): y-component of acceleration
        color (str): arrow color
        scale (float, optional): arrow length = scale * a_x(y)

    Returns:
        None
    """
    # End point of arrow
    end_x = scale * a_x + xx
    end_y = scale * a_y + yy

    # Arrow properties
    props = {'arrowstyle':'-|>', 'fc':color, 'ec':color}

    # matplotlib docs recommend using annotate method rather than arrow
    axis.annotate("", xytext=(xx,yy), xy=(end_x,end_y), arrowprops=props)


def plot_2D(source, rad_s, center, rad_b, points, accels, collapse='z',
            scale=1.0):
    """
    Plot gravitational AND tidal accelerations in two dimensions.

    Args:
        source (tuple): (x,y,z) coordinates of the source center.
        rad_s (float): Radius of the source.
        center (tuple): (x,y,z) coordinates of the body center.
        rad_b (float): Radius of the body
        points (tuple): (x,y,z) numpy arrays of points on the surface.
        accels (tuple): (x,y,z) numpy arrays of acceleration vectors.
        collapse (str, optional): Dimension along which to collapse plot.
        scale (float, optional): Factor by which to scale vectors.
    Returns:
        None
    """
    # The 3D data is collapsed along one spatial dimension.
    # hh and vv are horizontal and vertical dimensions of plot.
    # x = 0, y = 1, z = 2
    if collapse == 'x':
        hh = 1
        vv = 2
    elif collapse == 'y':
        hh = 0
        vv = 2
    elif collapse == 'z':
        hh = 0
        vv = 1
    else:
        raise ValueError("Invalid dimension for 'collapse'. Must by x,y,z.")

    # Unpack accelerations
    a_gc, a_gp, a_tp = accels

    # Setup plot
    fig, axis = plt.subplots()

    # Draw circles for objects
    source_xy = (source[hh], source[vv])
    circle_s = plt.Circle(source_xy, rad_s, ec='black', fc='None')
    body_xy = (center[hh], center[vv])
    circle_b = plt.Circle(body_xy, rad_b, ec='black', fc='None')
    axis.add_artist(circle_s)
    axis.add_artist(circle_b)

    # Draw arrow for acceleration due to gravity at the center.
    arrow_2D(axis, center[hh], center[vv], a_gc[hh], a_gc[vv], "black",
             scale=scale)

    # Plot arrows for each test particle
    for ii in range(len(points[0])):
        # Horizontal and vertical dimensions on the graph.
        # Not the same as x,y spatial dimensions unless collapse = 'z'.
        horz = points[hh][ii]
        vert = points[vv][ii]

        # Arrow for gravitational acceleration at point.
        arrow_2D(axis, horz, vert, a_gp[hh][ii], a_gp[vv][ii], "blue",
                 scale=scale)
        # Arrow for tidal acceleration at point.
        arrow_2D(axis, horz, vert, a_tp[hh][ii], a_tp[vv][ii], "red",
                 scale=scale)

    axis.set_aspect(1)
    
    # FIXME: Make axis limits responsive to data rather than hardcoded.
    x_right = source[0] + 1.5 * rad_s
    axis.set_xlim(-1.5, x_right)
    axis.set_ylim(-1.5, 1.5)

    plt.show()


def plot_3D(source, rad_s, center, rad_b, points, accels, **kwargs):
    """
    Plot tidal acceleration vectors in three dimensions.

    Trial and error may be required, adjusting the 'scale' parameter to
    obtain the desired arrow lengths.

    Args:
        source (tuple): (x,y,z) coordinates of the source center.
        rad_s (float): Radius of the source.
        center (tuple): (x,y,z) coordinates of the body center.
        rad_b (float): Radius of the body
        points (tuple): (x,y,z) numpy arrays of points on the surface.
        accels (tuple): (x,y,z) numpy arrays of acceleration vectors.
    kwargs:
        scale (float): Factor by which to scale vectors.
        alr (float) Ratio of arrowhead length to arrow length.
    Returns:
        None
    """
    # Check for kwargs
    scale = kwargs.get('scale')
    if scale is None:
        scale = 1.0
    alr = kwargs.get('alr')
    if alr is None:
        alr = 0.25

    # Unpack locations of points
    xx, yy, zz = points
    uu, vv, ww = accels[2]

    # Setup figure
    axis = plt.figure().add_subplot(projection='3d')
    # Draw arrows
    axis.quiver(xx, yy, zz, uu, vv, ww, length=scale, arrow_length_ratio=alr)

    # FIXME: Make axes limits responsive to data rather than hardcoded.
    axis.set_aspect('equal')
    axis.set_xlim(-1, 1)
    axis.set_ylim(-1, 1)
    axis.set_zlim(-1, 1)

    plt.show()
