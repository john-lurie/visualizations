"""
A module for calculating orbits.
"""
import math


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
