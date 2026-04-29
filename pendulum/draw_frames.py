import math
import os

from pendulum import draw_frames

# Create frames for a single oscillation
draw_frames(duration=2, fps=50, freq=math.pi, loop=True)

# Make a video with FFmpeg
# Animate single oscillation
os.system("ffmpeg -r 50 -i ./frames/frame_%04d.png -y once.mp4")
# Repeat to form a loop
os.system("ffmpeg -stream_loop 10 -i once.mp4 -c copy -y loop.mp4")
# Delete the single oscillation
os.system("rm -f once.mp4")
