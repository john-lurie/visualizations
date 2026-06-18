"""
Run functions to create figures for a presentation about the sizes of the 
Earth, Moon, and Sun to scale, as well as the sizes of the Earth-Moon and
Earth/Moon-Sun orbits.

The figure files are numbered in the order they will be presented.
"""
import draw

# Directory in which to save figures.
path = './figures/'

# Start with circles representing the Earth and Moon, sizes to scale.
file01 = path + 'figure001-earth_moon_comp.png'
draw.earth_moon_size_comparison(filename=file01)

# Draw the Moon's orbit as a circle of various sizes.
draw.earth_moon_orbit_scaling(fig_start=2)

# Draw the Moon's orbit as a circle at full scale.
# With Earth and Moon as circles rather than images.
file06 = path + 'figure006-earth_moon_circle.png'
draw.earth_moon_circle_full(filename=file06)

# Draw the Moon's orbit as an ellipse with the Earth at the CENTER.
file07 = path + 'figure007-ellipse_center.png'
draw.earth_moon_ellipse_basic(filename=file07, at_focus=False)

# Draw the Moon's orbit as an ellipse with the Earth at ONE FOCUS.
file08 = path + 'figure008-ellipse_focus.png'
draw.earth_moon_ellipse_basic(filename=file08)

# Draw the orbits of the Earth and Moon around their barycenter.
file09 = path + 'figure009-earth_moon_barycenter.png'
draw.earth_moon_barycenter(filename=file09)

# Animate the orbit of the Earth and Moon around their barycenter.
# Use matplotlib to create an MP4 for a single orbit.
file10 = path + 'figure010-earth_moon_animate.mp4'
draw.animate_orbit(filename=file10)

file11 = path + 'figure011-rotate_earth.mp4'
# Animate the rotation of the Earth as it orbits the barycenter.
draw.rotate_earth(filename=file11)

# Draw the Sun, Earth, and Moon to scale.
file12 = path + 'figure012-earth_moon_sun.png'
draw.sun_earth_moon(filename=file12)

# Zoom in to make the Earth and Moon more visible.
file13 = path + 'figure013-earth_moon_sun_zoom.png'
draw.sun_earth_moon(zoom=True, filename=file13)

# Draw the Earth-Sun orbit to scale.
file14 = path + 'figure014-earth_sun_orbit.png'
draw.orbits_sun_earth_moon(filename=file14)

# Zoom in to show the Moon-Earth orbit to scale.
file15 = path + 'figure015-earth_sun_orbit_zoom.png'
draw.orbits_sun_earth_moon(zoom=True, filename=file15)
