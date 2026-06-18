"""
Draw the Earth-Sun and Moon-Earth orbits with body radii to scale.
"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, Ellipse
from matplotlib.lines import Line2D
from matplotlib.image import imread
import numpy as np

import orbits
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


def save_or_show(filename):
    """If filename is given: plt.savefig(). Else: plt.show()."""
    if filename is not None:
        plt.savefig(filename, bbox_inches='tight', dpi=vl.dpi)
    else:
        plt.show()


def earth_moon_size_comparison(filename=None):
    """
    Compare the relative sizes of the Earth and Moon.
    Centers are separated by only one Earth diameter for ease of comparison.

    Args:
        filename (str, optional): See save_or_show() docstring.
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

    save_or_show(filename)


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
        filename (str, optional): See save_or_show() docstring.
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

    save_or_show(filename)


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
        filename (str, optional): See save_or_show() docstring.
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

    save_or_show(filename)


def earth_moon_ellipse_basic(at_focus=True, filename=None):
    """
    Draw the Moon's orbit as an ellipse.

    Args:
        at_focus (bool, optional): Default is to draw the Earth at one focus.
            if False: Draw the Earth at ellipse center for teaching purposes.
        filename (str, optional): See save_or_show() docstring.
    """
    fig, axis = plt.subplots()

    # Width and height of ellipse are twice semi-major/minor axes.
    orbit_ell = Ellipse(xy=(0, 0), width=2*vl.a_m, height=2*vl.b_m,
                        fc='none', ec=vl.ec_orb, lw=0.5)
    axis.add_patch(orbit_ell)

    # Draw the Moon as a circle.
    moon = Circle(xy=(vl.a_m, 0), radius=vl.r_m, fc=vl.fc_m)
    axis.add_patch(moon)

    if at_focus:
        # Draw the Earth at the right side (positive x-axis) focus.
        # Use the linear eccentricity to locate the focus.
        earth = Circle(xy=(vl.c_m, 0), radius=vl.r_e, fc=vl.fc_e)
        # Put a cross at the center of the ellipse.
        axis.scatter([0], [0], marker='+', s=10, color='red', lw=0.35)
    else:
        # Draw the Earth at the center of the ellipse.
        earth = Circle(xy=(0, 0), radius=vl.r_e, fc=vl.fc_e)
    axis.add_patch(earth)

    # The eccentricity is small, so symmetrical limits still work.
    limit = 1.2 * vl.a_m
    axis.set_xlim(-limit, limit)
    axis.set_ylim(-limit, limit)
    setup_figure(fig, axis)

    save_or_show(filename)


def earth_moon_barycenter(filename=None, returns=True):
    """
    Draw the orbit of the Moon around the Earth-Moon barycenter.

    The location of the Earth also reflects a barycentric orbit,
    but the orbit itself is not shown.

    Args:
        filename (str, optional): See save_or_show() docstring.
        returns (bool, optional): If True: return variables for future use.
            These will be used by the function animate_orbit().
    """
    # Calculate the barycentric ellipses.
    tuple1, tuple2 = orbits.ellipse_params(vl.a_m, vl.m_e, vl.m_m, vl.e_m)
    # Unpack.
    a1, b1, c1 = tuple1
    a2, b2, c2 = tuple2

    fig, axis = plt.subplots()

    # Draw the Moon's orbit around the barycenter.
    # The center of this ellipse is at the ORIGIN.
    orbit_moon = Ellipse(xy=(0, 0), width=2*a2, height=2*b2,
                         fc='none', ec=vl.ec_orb, lw=0.5)
    axis.add_patch(orbit_moon)

    # Draw a circle for the Moon.
    moon = Circle(xy=(a2, 0), radius=vl.r_m, fc=vl.fc_m)
    axis.add_patch(moon)

    # Draw a circle for the Earth.
    # Remember, the barycenter is NOT at the origin.
    # Hence the calculation for the Earth's location: c2+c1-a1
    earth = Circle(xy=((c2+c1-a1), 0), radius=vl.r_e, fc=vl.fc_e)
    axis.add_patch(earth)

    # Draw a dot at the barycenter, smaller than the Earth.
    # Location is defined by the linear eccentricity of the Moon's orbit.
    bary = Circle(xy=(c2, 0), radius=0.35*vl.r_e, fc='orange')
    axis.add_patch(bary)

    # Draw a cross at the center of the Moon's orbit.
    center = axis.scatter([0], [0], marker='+', s=10, color='red', lw=0.35)

    # The eccentricity is small, so symmetrical limits still work.
    limit = 1.2 * vl.a_m
    axis.set_xlim(-limit, limit)
    axis.set_ylim(-limit, limit)
    setup_figure(fig, axis)

    if returns:
        # Orbital parameters necessary for animation.
        params = (a1, a2, c1, c2, b1)
        return fig, axis, params, moon, earth, center
    else:
        save_or_show(filename)


def update(frame, moon_tuple, earth_tuple):
    """
    Update the position of patches for Earth and Moon.

    This will be called by matplotlib FuncAnimation().

    Args:
        frame (int): frame number
        moon_tuple (tuple): patch and positions for Moon.
        earth_tuple (tuple): patch and positions for Earth.

    Returns:
        moon, earth: FuncAnimation() requires the patches to be returned.
    """
    # Unpack tuples
    moon, x_m, y_m = moon_tuple
    earth, x_e, y_e = earth_tuple 

    # Update positions
    moon.set_center((x_m[frame], y_m[frame]))
    earth.set_center((x_e[frame], y_e[frame]))

    return moon, earth


def animate_orbit(filename=None, validate=False, markcenter=False):
    """
    Animate the orbits of the Earth and Moon around their barycenter.

    Args:
        filename (str, optional): if filename given, save as an MP4 movie.
            else: plt.show()
        validate (bool, optional): if True: validate the program.
            This will exaggerate the eccentricity and Moon's mass so that
            the geometry is more visible.
        markcenter (bool, optional): if True: mark center of Moon's orbit.
    """
    if validate:
        # Exaggerate eccentricity and Moon's mass.
        vl.m_m *= 10
        vl.e_m = 0.5

    # Reuse setup for static plot.
    fig, axis, params, moon, earth, cen = earth_moon_barycenter(returns=True)
    # Unpack orbital parameters.
    a_e, a_m, c_e, c_m, b_e = params

    if not markcenter:
        # Don't mark the center. Move it far away.
        far_away = list(zip([1e9], [1e9]))
        cen.set_offsets(far_away)

    # Timestep in days.
    dt=0.025

    # Orbital positions are calculated from the focus.
    # The focus is NOT at the origin. Determined by linear eccentricity.
    focus = (c_m, 0)
    x_m, y_m = orbits.positions(vl.P_m, vl.e_m, a_m, dt=dt, focus=focus)

    # left = False ensures the center of Earth's orbit is to right of focus.
    x_e, y_e = orbits.positions(vl.P_m, vl.e_m, a_e, dt=dt, focus=focus,
                                left=False)

    # Update the patch positions before starting animation.
    moon.set_center((x_m[0], y_m[0]))
    earth.set_center((x_e[0], y_e[0]))

    # Arguments for the update() function.
    fargs = ((moon, x_m, y_m), (earth, x_e, y_e))

    if validate:
        # Draw an ellipse for the Earth's orbit around the barycenter.
        orbit_earth = Ellipse(xy=(c_m+c_e, 0), width=2*a_e, height=2*b_e,
                              fc='none', ec='yellow', lw=0.5, zorder=-5)
        axis.add_patch(orbit_earth)

    # Tighten up the margins.
    fig.subplots_adjust(bottom=0, top=1, left=0, right=1)

    # Run the animation.
    ani = FuncAnimation(fig=fig, func=update, fargs=fargs, frames=len(x_m),
                        interval=20)

    if filename is not None:
        ani.save(filename=filename, dpi=vl.dpi)
    else:
        plt.show()


def setup_figure_rotation(figure, axis):
    """
    Setup a matplotlib figure for an animation of the Earth's rotation.

    The setup needs to be different than the other figures in this module.
    Hence the separate function.
    """
    # A black background resembles outer space.
    axis.set_facecolor('black')
    figure.set_facecolor('black')

    # An equal aspect ratio ensures the geometry looks correct.
    axis.set_aspect(1)

    # Tighten up the margins.
    figure.subplots_adjust(bottom=0.05, top=0.95, left=0, right=1)

    # Tick marks are unnecessary.
    axis.get_xaxis().set_ticks([])
    axis.get_yaxis().set_ticks([])

    # Loop through all spines.
    for spine in axis.spines.values():
        spine.set_color('white')
        spine.set_linewidth(3)


def update_rotation(frame, line, earth, xx, yy):
    """
    For matplotlib FuncAnimation to update Earth rotation animation.

    Args:
        frame (int): Frame number is the index for position data arrays.
        line (matplotlib Line2D): Like a prime meridian to show Earth's rotation.
        earth (matplotlib Circle): Represents the Earth.
        xx, yy (numpy.ndarray): Position data.
    """
    # Update positions.
    line.set_xdata(xx[frame])
    line.set_ydata(yy[frame])
    earth.set_center((xx[frame][1], yy[frame][1]))


def rotate_earth(filename=None):
    """
    Animate the Earth rotating as it orbits the Earth-Moon barycenter.

    A line on the Earth is a prime meridian, making the rotation visible.

    Args:
        filename (str, optional): if filename given, save as an MP4 movie.
    """
    # Compute the motion of the Earth's center around barycenter.
    # FIXME: Hardcode the semi-major axis in the values module, not here.
    # In this case, the barycenter IS at the origin.
    x_e, y_e = orbits.positions(vl.P_m, vl.e_m, 0.733, dt=vl.dt, focus=(0,0),
                                left=False)

    # Array of times for one complete orbit of the Moon.
    times = np.linspace(0, vl.P_m, int(vl.P_m/vl.dt))
    # Specify a line representing a prime meridian on the Earth.
    # The line will rotate CCW through 2pi radians.
    angles = (2 * np.pi / vl.P_e) * times
    # The coordinates of the line are: x = [x1, 0.0, x2], y = [y1, 0.0, y2]
    # Compute the Cartesian coordinates.
    # The position of Earth's center is added, moving the line with Earth.
    x1 = -vl.r_e * np.cos(angles) + x_e
    x2 =  vl.r_e * np.cos(angles) + x_e
    y1 = -vl.r_e * np.sin(angles) + y_e
    y2 =  vl.r_e * np.sin(angles) + y_e
    # The center of the line.
    zero_x = np.zeros(len(angles)) + x_e
    zero_y = np.zeros(len(angles)) + y_e

    # Stack the data.
    xx = np.column_stack((x1, zero_x, x2))
    yy = np.column_stack((y1, zero_y, y2))

    # Create the figure.
    fig, axis = plt.subplots()

    # Initialize the line using the first values in the arrays.
    x_init = np.array([-vl.r_e, 0.0, vl.r_e]) + x_e[0]
    y_init = np.array([0.0, 0.0, 0.0]) + y_e[0]
    # capstyle = 'butt' ensures the line does not extend past edge of Earth.
    line = Line2D(xdata=x_init, ydata=y_init, lw=5, zorder=2, color='firebrick',
                  solid_capstyle='butt')
    axis.add_artist(line)

    # Initialize the circle for the Earth.
    earth = Circle(xy=(x_e[0], y_e[0]), radius=vl.r_e, fc=vl.fc_e)
    axis.add_patch(earth)

    # Draw a dot at the barycenter, in this case at the origin.
    bary = Circle(xy=(0, 0), radius=0.1*vl.r_e, fc='orange', zorder=3)
    axis.add_patch(bary)

    # Set the axes limits.
    axis.set_xlim(-2, 2)
    axis.set_ylim(-2, 2)

    # Additional figure setup.
    setup_figure_rotation(fig, axis)

    # Arguments to pass to update_rotation()
    fargs = (line, earth, xx, yy)
    # Run the animation.
    ani = FuncAnimation(fig=fig, func=update_rotation, fargs=fargs,
                        frames=len(angles), interval=vl.interval)

    if filename is not None:
        ani.save(filename, dpi=vl.dpi)
    else:
        plt.show()


def sun_earth_moon(zoom=False, filename=None):
    """
    Draw the Sun, Earth, and Moon to scale.

    Args:
        zoom (bool, optional): if True: zoom in so Earth and Moon are bigger.
        filename (str, optional): See save_or_show() docstring.
    """
    fig, axis = plt.subplots()

    # Centers of the circles are along the x-axis, offset horizontally.
    earth = Circle(xy=(5*vl.r_e, 0), radius=vl.r_e, fc=vl.fc_e)
    moon = Circle(xy=(8*vl.r_e, 0), radius=vl.r_m, fc=vl.fc_m)
    sun = Circle(xy=(-1*vl.r_s, 0), radius=vl.r_s, fc=vl.fc_s)

    axis.add_patch(sun)
    axis.add_patch(earth)
    axis.add_patch(moon)

    setup_figure(fig, axis)

    if zoom:
        axis.set_xlim(-0.2*vl.r_s, 0.1*vl.r_s)
        axis.set_ylim(-0.1*vl.r_s, 0.1*vl.r_s)
    else:
        axis.set_xlim(-2.1*vl.r_s, 0.1*vl.r_s)
        axis.set_ylim(-1.1*vl.r_s, 1.1*vl.r_s)

    save_or_show(filename)


def orbits_sun_earth_moon(zoom=False, filename=None):
    """
    Draw Earth-Sun and Moon-Earth orbits to scale.

    Args:
        zoom (bool, optional): if True: zoom in to show the Moon-Earth orbit.
        filename (str, optional): See save_or_show() docstring.
    """
    fig, axis = plt.subplots()

    # The Earth's orbit is an ellipse centered at the origin.
    # Width and height are twice the semi-major/minor axes, respectively.
    orbit_earth = Ellipse(xy=(0,0), width=2*vl.a_e, height=2*vl.b_e,
                          ec='purple', fc='none', lw=0.5)
    axis.add_patch(orbit_earth)
    # The Sun is located at the right hand focus.
    sun = Circle(xy=(vl.c_e, 0), radius=vl.r_s, fc=vl.fc_s)
    axis.add_patch(sun)
    # For refence, put a cross at the center of the ellipse.
    axis.scatter([0], [0], marker='+', s=4, color='red', lw=0.35)

    if zoom:
        # For simplicity, make the Moon's orbit a circle.
        # The orbit is so small that the eccentricty doesn't matter.
        orbit_moon = Circle(xy=(vl.a_e, 0), radius=vl.a_m, ec=vl.ec_orb,
                            fc='none', lw=0.5, zorder=5)
        axis.add_patch(orbit_moon)
        axis.set_xlim(0.01*vl.a_e, 1.025*vl.a_e)
        axis.set_ylim(-0.3*vl.a_e, 0.3*vl.a_e)
    else:
        axis.set_xlim(-1.05*vl.a_e, 1.05*vl.a_e)
        axis.set_ylim(-1.05*vl.a_e, 1.05*vl.a_e)

    setup_figure(fig, axis)
    save_or_show(filename)
