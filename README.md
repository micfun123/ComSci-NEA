## Key Features:

    2D Physics Simulation: The project accurately simulates 2D collisions between circular billiard balls, considering their mass and velocity.

    Customizable Ball Properties: Users can add new balls with custom initial velocities, positions, and masses.

    Adjustable Damping: The damping factor, which influences the energy loss during collisions, can be modified by the user.

    Interactive Controls:

        Pause/Play: Press the Spacebar to toggle between pausing and playing the simulation.

        Add Ball: Press the Up arrow key to introduce a new ball into the simulation. You'll be prompted to input its initial x and y velocity, x and y location, and mass.

        Clear Balls: Press the C key to remove all balls from the simulation.

        Change Damping: Press the D key to open a dialog box and set a new damping factor (between 0.0 and 1.0).

        Export Velocity Data: Press the G key to export the velocity history of each ball to a CSV file.

    Real-time Visualization: The simulation is displayed graphically using Pygame, showing the balls, their movement, and collision responses.

    Grid Overlay: A grid is displayed on the simulation area to help with visual positioning and understanding distances.

    Velocity and Mass Display: Each ball displays its current velocity and mass for easy monitoring.

## How to Run:

    Dependencies: Ensure you have pygame and tkinter installed. You can install Pygame using pip:
    Bash

    pip install pygame

    Tkinter is usually included with Python installations.

    Execute the Script: Run the Python script. A Pygame window will open, displaying the simulation.

Controls within the Simulation:

    SPACEBAR: Pause/Play the simulation.

    UP Arrow: Add a new ball (prompts for velocity, position, and mass).

    C: Clear all balls from the simulation.

    D: Change the damping factor (prompts for a value between 0.0 and 1.0).

    G: Export ball velocity history to a CSV file named VEL_HITST.csv.