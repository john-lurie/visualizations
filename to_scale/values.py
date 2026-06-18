"""
Values for plotting the Earth, Moon, and Sun to scale, including orbits.

Sizes and distances are in Earth radii.
Masses are in Earth masses.
"""
import math

# Mean radius of the Earth in kilometers
r_e_km = 6371.0
# Normalize to units of Earth radii
r_e = r_e_km / r_e_km
# Mean radius of the Moon
r_m = 1737.4 / r_e_km
# Equatorial radius of the Sun (mean radius is nearly identical)
r_s = 695700.0 / r_e_km

# Semi-major axis of the Earth's orbit in kilometers
a_e_km = 1.496e8
# Semi-major axis in Earth radii
a_e = a_e_km / r_e_km
# Semi-major axis of the Moon's orbit
a_m = 3.8445e5 / r_e_km

# Eccentricity of Earth's orbit
e_e = 0.0167
# Eccentricity of the Moon's orbit
e_m = 0.0549

# Linear eccentricity of the Earth's orbit
c_e = e_e * a_e
# Linear eccentricity of the Moon's orbit
c_m = e_m * a_m

# Semi-minor axis of the Earth's orbit
b_e = math.sqrt(a_e**2 - c_e**2)
# Semi-minor axis of the Moon's orbit
b_m = math.sqrt(a_m**2 - c_m**2)

# Mass of the Earth in kilograms
m_e_kg = 5.972e24
# Normalize to units of Earth masses
m_e = m_e_kg / m_e_kg
# Mass of the Moon
m_m = 7.346e22 / m_e_kg

# Sidereal period of the Moon's orbit in days.
# In reality the period is 27.322 days.
# Here it's exactly 27 to make the Earth's rotation period commensurate.
P_m = 27.0
# Sideral rotation period of the Earth in days.
# In reality, it's slightly less than 1.0.
P_e = 1.0

# Time step for animation in fraction of a day.
dt = 0.025
# Time interval between frames in the animation, in milliseconds.
interval = 20

# Colors of the objects for plotting
fc_e = '#0652ff' # blue
fc_m = 'white'
fc_s = 'gold'
# Color of the lines for orbits. 
ec_orb = 'darkgreen'

# Global DPI for saving images
dpi = 600
