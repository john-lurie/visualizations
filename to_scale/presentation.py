"""
Run functions to create figures for a presentation about the sizes of the 
Earth, Moon, and Sun to scale, as well as the sizes of the Earth-Moon and
Earth/Moon-Sun orbits.

The figure files are numbered in the order they will be presented.
"""
import draw

# Start with circles representing the Earth and Moon, sizes to scale.
file01 = './figures/figure001-earth_moon_comp.png'
draw.earth_moon_size_comparison(filename=file01)

# Draw the Moon's orbit as a circle of various sizes.
draw.earth_moon_orbit_scaling(fig_start=2)
