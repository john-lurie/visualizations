"""
Draw the Earth-Sun and Moon-Earth orbits with body radii to scale.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.image import imread

import values as vl

def setup_figure(figure, axis):
    """
    Modify matplotlib figure and axis objects for astronomical diagrams.
    """
    # A black background resembles outer space.
    axis.set_facecolor('black')
    figure.set_facecolor('black')

    # An equal aspect ratio ensures the geometry looks correct.
    axis.set_aspect(1)

    # Tick marks and spines are unnecessary.
    axis.get_xaxis().set_ticks([])
    axis.get_yaxis().set_ticks([])
    axis.spines['left'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.spines['top'].set_visible(False)


def earth_moon_size_comparison(filename=None):
    """
    Compare the relative sizes of the Earth and Moon.
    Centers are separated by only one Earth diameter for ease of comparison.

    Args:
        filename (str, optional): Name of the image file. If None: plt.show().
    """
    fig, axis = plt.subplots()
    
    # Earth is centered at the origin.
    earth = Circle(xy=(0, 0), radius=vl.r_e, fc=vl.fc_e)
    axis.add_patch(earth)
    # Moon is centered one Earth diameter (two radii) away on x-axis.
    moon = Circle(xy=(2*vl.r_e, 0), radius=vl.r_m, fc=vl.fc_m)
    axis.add_patch(moon)

    # Use the Earth's radius as basis for axis limits.
    axis.set_xlim(-1.5*vl.r_e, 3*vl.r_e)
    axis.set_ylim(-1.5*vl.r_e, 1.5*vl.r_e)
    setup_figure(fig, axis)

    if filename is not None:
        plt.savefig(filename, bbox_inches='tight', dpi=vl.dpi)
    else:
        plt.show()


def earth_moon_circle_orbit(scale=1.0, filename=None):
    """
    Draw the Moon's orbit as a circle with option to scale down orbit size.

    Because the Moon's orbit is so large relative to the diameters of the 
    Earth and Moon, it can be helpful to scale down the orbit size for the
    purpose of illustration.

    Args:
        scale (float, optional): Factor by which to scale down orbit.
            Orbital radius will be divided by this factor.
            Default is 1.0, no scaling.
        filename (str, optional): Name of the image file. If None plt.show().
    """
    fig, axis = plt.subplots()

    # Load images of Earth and Moon.
    img_e = imread('./assets/earth_north.jpg')
    img_m = imread('./assets/moon_north.jpg')

    # Define the rectangular extent of the image of the Earth.
    # Coordinates are [x_min, x_max, y_min, y_max].
    # This creates a square with sides that are twice the Earth radius.
    # The Earth is centered at the origin. 
    rect_e = [-vl.r_e, vl.r_e, -vl.r_e, vl.r_e]
    # Insert the image of the Earth. 
    axis.imshow(img_e, extent=rect_e, aspect='auto')

    # Scale down the Moon's semi-major axis by some factor.
    a_m = vl.a_m / scale

    # Define the rectangle for the Moon image.
    # The Moon is located on x-axis, at a distance equal to semi-major axis.
    x_m = a_m
    y_m = 0.0
    rect_m = [x_m - vl.r_m, x_m + vl.r_m, y_m - vl.r_m, y_m + vl.r_m]
    # Insert the Moon image.
    axis.imshow(img_m, extent=rect_m, aspect='auto', cmap='gray')

    # Draw the orbit of the Moon as a circle.
    orbit_moon = Circle(xy=(0, 0), radius=a_m, ec=vl.ec_orb, fc='none',
                        lw=0.5, zorder=-10)
    axis.add_patch(orbit_moon)

    # The orbit is a circle, so use symmetrical axes limits.
    limit = 1.2 * a_m
    axis.set_xlim(-limit, limit)
    axis.set_ylim(-limit, limit)

    setup_figure(fig, axis)

    if filename is not None:
        plt.savefig(filename, bbox_inches='tight', dpi=vl.dpi)
    else:
        plt.show()


def earth_moon_orbit_scaling(fig_start=None):
    """
    Draw the orbit of the Moon at range of different scales.

    The purpose of this function is to show the orbit of Moon much smaller 
    than it is in reality, and then to incrementally increase the size of the 
    orbit until it reaches the true size. This is an effective way of showing 
    just how far the Moon is from the Earth.

    The effect of this progression is to steadily decrease the apparent sizes 
    of the Earth and Moon.

    Args:
        fig_start (int, optional): Starting figure number.
            For example, if fig_start=2, starting filename is figure002...
    """
    # Scales
    scl = (25, 10, 5, 1)
        
    if fig_start is not None:
        # Iterate over scales.
        for ii in range(len(scl)):
            # Figure numbers start at fig_start.
            num = fig_start + ii
            # filename format is figure000-scale00.png
            filename = f"./figures/figure{num:03d}-scale{scl[ii]:02d}.png"
            earth_moon_circle_orbit(scale=scl[ii], filename=filename)
    else:
        for ii in range(len(scl)):
            earth_moon_circle_orbit(scale=scl[ii])


def earth_moon_circle_full(filename=None):
    """
    Draw the Earth and Moon as circles with a circular orbit at full scale.

    This serves as a brief transition from the scaling demonstration.
    The problem is that the images used in earth_moon_circle_orbit()
    have poor contrast and are hard to see at full scale. So generic
    circles are used here instead.

    Args:
        filename (str, optional): Name of the image file. If None plt.show().
    """
    fig, axis = plt.subplots()

    # Draw the orbit of the Moon as a circle.
    orbit_moon = Circle(xy=(0, 0), radius=vl.a_m,
                        ec=vl.ec_orb, fc='none', lw=0.5)
    axis.add_patch(orbit_moon)

    # Draw the Earth and Moon as circles.
    earth = Circle(xy=(0, 0), radius=vl.r_e, fc=vl.fc_e)
    axis.add_patch(earth)
    moon = Circle(xy=(vl.a_m, 0), radius=vl.r_m, fc=vl.fc_m)
    axis.add_patch(moon)

    # The orbit is a circle, so use symmetrical axes limits.
    limit = 1.2 * vl.a_m
    axis.set_xlim(-limit, limit)
    axis.set_ylim(-limit, limit)
    setup_figure(fig, axis)

    if filename is not None:
        plt.savefig(filename, bbox_inches='tight', dpi=vl.dpi)
    else:
        plt.show()
