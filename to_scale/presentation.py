"""
Run functions to create figures for a presentation about the sizes of the 
Earth, Moon, and Sun to scale, as well as the sizes of the Earth-Moon and
Earth/Moon-Sun orbits.

The figure files are numbered in the order they will be presented.
"""
import os

import draw

# Start with circles representing the Earth and Moon, sizes to scale.
file01 = './figures/figure001-earth_moon_comp.png'
draw.earth_moon_size_comparison(filename=file01)

# Draw the Moon's orbit as a circle of various sizes.
draw.earth_moon_orbit_scaling(fig_start=2)

# Draw the Moon's orbit as a circle at full scale.
# With Earth and Moon as circles rather than images.
file06 = './figures/figure006-earth_moon_circle.png'
draw.earth_moon_circle_full(filename=file06)

# Draw the Moon's orbit as an ellipse with the Earth at the CENTER.
file07 = './figures/figure007-ellipse_center.png'
draw.earth_moon_ellipse_basic(filename=file07, at_focus=False)

# Draw the Moon's orbit as an ellipse with the Earth at ONE FOCUS.
file08 = './figures/figure008-ellipse_focus.png'
draw.earth_moon_ellipse_basic(filename=file08)

# Draw the orbits of the Earth and Moon around their barycenter.
file09 = './figures/figure009_moon_barycenter.png'
draw.earth_moon_barycenter(filename=file09)

# Animate the orbit of the Earth and Moon around their barycenter.
# Use matplotlib to create an MP4 for a single orbit.
draw.animate_orbit(filename='./figures/once.mp4')
# Repeat to form a loop.
file10 = './figures/figure010_earth_moon_animate.mp4'
cmd = "ffmpeg -stream_loop 10 -i ./figures/once.mp4 -c copy -y " + file10
os.system(cmd)
# Delete the single oscillation
os.system("rm -f ./figures/once.mp4")
