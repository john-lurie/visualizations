"""
A module for calculating orbits.
"""
import math

import numpy as np
from scipy import optimize


def ellipse_params(a0, m1, m2, ecc):
    """
    Compute the ellipse parameters for barycentric orbits.

    Args:
        a0 (float): Semi-major axis of secondary orbit around primary. 
        m1 (float): Mass of the primary.
        m2 (float): Mass of the secondary.
        ecc (float): Eccentricity of the orbits. Same for both.
    
    Returns:
        tuple1, tuple2 = (a1, b1, c1), (a2, b2, c2)
        
        a1: semi-major axis of the primary orbit around barycenter.
        a2: semi-major axis of the secondary orbit around barycenter.
        b1: semi-minor axis of the primary.
        b2: semi-minor axis of the secondary.
        c1: linear eccentricity of the primary.
        c2: linear eccentricity of the secondary.
    """
    # Semi-major axis of the primary orbit.
    a1 = a0 * m2 / (m1 + m2)
    # Semimajor axis of the secondary orbit.
    a2 = a0 - a1

    # Linear eccentricities
    c1 = ecc * a1
    c2 = ecc * a2

    # Semi-minor axes
    b1 = math.sqrt(a1**2 - c1**2)
    b2 = math.sqrt(a2**2 - c2**2)

    return (a1, b1, c1), (a2, b2, c2)


def polar_ellipse(angle, semimaj=1.0, ecc=0.0, focus=(0, 0), left=True):
    """
    Compute the polar equation of an ellipse.

    Args:
        angle (numpy.ndarray): Anglular position in radians.
        semimaj (float, optional): Length of the semi-major axis.
        ecc (float, optional): Eccentricity.
        focus (tuple, optional): Location of focus where position is measured.
        left (bool, optional): if True: ellipse center is to left of focus.
            if False: ellipse center is to right of focus.

    Returns
        xx, yy (numpy.ndarray): Cartesian coordinates of ellipse.
    """
    if left:
        dist = (semimaj * (1 - ecc**2)) / (1 + ecc * np.cos(angle))
    else:
        # A minus sign in the denominator.
        dist = (semimaj * (1 - ecc**2)) / (1 - ecc * np.cos(angle))

    # Unpack focus coordinates.
    x0, y0 = focus
    # Convert to Cartesian coordinates.
    xx = dist * np.cos(angle) + x0
    yy = dist * np.sin(angle) + y0

    return xx, yy


def true_from_eccentric(E, e):
    """
    Compute the true anomaly from the eccentric anomaly.

    Args:
        E: eccentric anomaly in radians.
        e: eccentricity of the ellipse.

    Returns:
        nu: true anomaly (Greek nu) in radians.
    """
    # The stuff inside the square root.
    radical = np.sqrt((1 + e)/(1 - e))
    # This formula resolves ambiguity about what Cartesian quadrant E is in.
    nu = 2 * np.arctan(radical * np.tan(E/2))

    return nu


def kepler_eq(E, M, e):
    """
    Kepler's equation relating eccentric and mean anomalies.

    Args:
        E: eccentric anomaly in radians.
        M: mean anomaly in radians.
        e: eccentricity of the ellipse.
    """
    return E - e * np.sin(E) - M


def f_prime(E, M, e):
    """
    The first derivative of Kepler's equation, used in Newton-Raphson method.

    Arguments are the same as Kepler's equation even though M is not used.
    This ensures compatibility with scipy.optimize.newton().
    """
    return 1.0 - e * np.cos(E)


def positions(period, ecc, semimaj, dt=0.1, focus=(0,0), left=True):
    """
    Compute the position as a function of time for an eccentric orbit.

    Args:
        period (float): Orbital period.
        ecc (float): Eccentricity of the orbit.
        semimaj (float): Semi-major axis of the ellipse.
        dt (float, optional): Time step. Same units as period.
        focus (tuple, optional): Location of focus where position is measured.
        left (bool, optional): if True: ellipse center is to left of focus.
            if False: ellipse center is to right of focus.

    Returns:
        xx, yy: Cartesian positons as a function of time.
    """
    # Time array.
    times = np.linspace(0, period, int(period/dt))
    # Convert from time to mean anomaly.
    mean_anoms = (2*np.pi/period) * times

    # Use the mean anomaly as a first guess for eccentric anomaly.
    guesses = mean_anoms.copy()
    # Arguments for the Kepler's equation inside of optimize.newton().
    args = (mean_anoms, ecc,)
    # Solve for the eccentric anomaly.
    ecc_anoms = optimize.newton(kepler_eq, guesses, fprime=f_prime, args=args)
    # Convert to true anomaly.
    true_anoms = true_from_eccentric(ecc_anoms, ecc)

    if not left:
        # The ellipse center is to the right of the focus.
        # So rotate by pi radians = 180 degrees.
        true_anoms += np.pi

    # Convert to Cartesian coordinates.
    xx, yy = polar_ellipse(true_anoms, semimaj, ecc, focus, left=left)

    return xx, yy
