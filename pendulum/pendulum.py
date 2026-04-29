"""
Animate A Swinging Pendulum
---------------------------
The pendulum module uses a solution for the angular position of a pendulum as
a function of time. It is only valid for the small angle approximation, where
sin(theta) ≈ theta, less than about 15 degrees.

The variable 'freq' is the oscillation frequency of the pendulum in radians
per second. One full oscillation, a swing back and forth, equals 2π radians.
This is NOT the angular speed of the pendulum.
"""
import matplotlib.pyplot as plt
import numpy as np

def calculate_freq(length, gravity):
    """
    Calculate the oscillation frequency.
    
    Args:
        length (float): Pendulum length in meters.
        gravity (float): Acceleration in meters/sec^2. Default 9.80.

    Returns:
        frequency (float): Frequency in radians/sec^2.
    """    
    return math.sqrt(gravity / length)


def angular_position(time_arr, freq, angle_init):
    """
    Calculate the angular position as a function of time.

    Args:
        time_arr (numpy.ndarray): Time in seconds.
        freq (float): Angular frequency in radians/sec.
        angle_init (float): Intial angle in degrees.
    
    Returns:
        position (numpy.ndarray): Angular position degrees.
    """
    message = "Initial angle greater than 15 degrees. " \
    "The small angle approximation is not valid. " \
    "Choose a smaller angle."
    if angle_init > 15.0:
        raise ValueError(message)
    
    return angle_init * np.cos(freq * time_arr)


def draw_frames(duration=4, fps=50, freq=None, length=1.0, gravity=9.8,
                angle_init=10.0, loop=False):
    """
    Draw frames for animation of a pendulum.

    Args:
        duration (int, optional): Duration of animation in seconds. Default 4
        fps (int, optional): Frames per second. Default 50
        freq (float, optional): Oscillation freq. in rad/sec. Default None.
            if None, freq will be calculated based on length and gravity.
        length (float, optional) Pendulum length in meters. Default 1.0.
        gravity (float, optional) Acceleration in m/s^2. Default 9.8.
        angle_init (float, optional): Intial angle in degrees. Default 10.0.
        loop (bool, optional): Set to True if making frames for a loop.
    """
    if freq is None:
        freq = calculate_freq(length, gravity)

    # Forces number of frames to be an integer.
    time_arr = np.linspace(0, duration, int(duration * fps))
    
    # If making frames for a loop, exclude the last frame.
    # Prevents a duplicate frame at end/beginning of loop.
    if loop:
        time_arr = time_arr[:-1]
    
    angles = angular_position(time_arr, freq=freq, angle_init=angle_init)
    # Convert to radians
    radians = np.deg2rad(angles)
    # Calculate x and y positions. Pivot of pendulum is at 0,0.
    x_pos = length * np.sin(radians)
    y_pos = -length * np.cos(radians)

    # Configure the plot.
    fig, ax = plt.subplots()
    ax.set_xlim(-0.5 * length, 0.5 * length)
    ax.set_ylim(-1.05 * length, 0)
    ax.set_aspect(1)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Pendulum is drawn as a mass at the end of a rope.
    rope, = ax.plot([0, x_pos[0]], [0, y_pos[0]], lw=3, color='black')
    mass, = ax.plot([x_pos[0]], [y_pos[0]], '-ok', ms=25)

    # Draw the frames by updating the position data.
    for ii in range(len(radians)):
        rope.set_xdata([0, x_pos[ii]])
        rope.set_ydata([0, y_pos[ii]])
        mass.set_xdata([x_pos[ii]])
        mass.set_ydata([y_pos[ii]])
        fig.canvas.draw()
        plt.savefig(f'./frames/frame_{ii:04d}.png', dpi=400,
                    bbox_inches='tight')
        fig.canvas.flush_events()
