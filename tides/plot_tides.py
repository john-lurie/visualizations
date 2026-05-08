import numpy as np

import tides

# Radius of source
rad_s = 0.25
# Radius of body
rad_b = 1.0

# Location of source in x,y,z
source = (4.0, 0.0, 0.0)
# Location of center of body in x,y,z
center = (0.0, 0.0, 0.0)

def do_2D():
    # Locations (plural) of points in x,y,z
    points = (np.array([ 0,  0, -1,  1]),
              np.array([-1,  1,  0,  0]),
              np.array([ 0,  0,  0,  0]))

    # Calculate accelerations
    accels = tides.calculate_accel(source, center, points)
    for axis in ['x', 'y', 'z']:
        tides.plot_2D(source, rad_s, center, rad_b, points, accels,
                      collapse=axis, scale=10.0)


def do_3D():
    # Number of latitude intervals to plot.
    n_lats = 9

    # Setup a grid of latitude and longitude.
    lat = np.radians(np.linspace(0, 180, n_lats))
    # Twice as many longitude lines as latitude.
    lon = np.radians(np.linspace(0, 360, 2*n_lats))
    lat, lon = np.meshgrid(lat, lon)

    # Convert spherical coordinates to Cartesian.
    xx = rad_b * np.sin(lat) * np.cos(lon)
    yy = rad_b * np.sin(lat) * np.sin(lon)
    zz = rad_b * np.cos(lat)
    points = (xx, yy, zz)

    # Calculate accelerations
    accels = tides.calculate_accel(source, center, points)

    tides.plot_3D(source, rad_s, center, rad_b, points, accels, scale=5)

do_2D()
do_3D()