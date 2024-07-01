#!/usr/bin/env python3

# ... (other imports)

# import live_plotter as lv   # Custom live plotting library (commented out)

# ... (other imports)

def exec_waypoint_nav_demo(args):
    # ... (code before live plotting setup)

    #############################################
    # Vehicle Trajectory Live Plotting Setup
    #############################################
    # Uses the live plotter to generate live feedback during the simulation
    # The two feedback includes the trajectory feedback and
    # the controller feedback (which includes the speed tracking).
    # lp_traj = lv.LivePlotter(tk_title="Trajectory Trace") (commented out)
    # lp_1d = lv.LivePlotter(tk_title="Controls Feedback") (commented out)

    ###
    # Add 2D position / trajectory plot
    ###
    # trajectory_fig = lp_traj.plot_new_dynamic_2d_figure( (commented out)
    #         title='Vehicle Trajectory',
    #         figsize=(FIGSIZE_X_INCHES, FIGSIZE_Y_INCHES),
    #         edgecolor="black",
    #         rect=[PLOT_LEFT, PLOT_BOT, PLOT_WIDTH, PLOT_HEIGHT])

    # ... (other commented out lines related to live plotting setup)

    # live plotter is disabled, hide windows
    # if not enable_live_plot:
    #     lp_traj._root.withdraw()
    #     lp_1d._root.withdraw()

    # ... (code before the main loop)

    for frame in range(TOTAL_EPISODE_FRAMES):
        # ... (code before live plotting update)

        # Skip the first frame (so the controller has proper outputs)
        if skip_first_frame and frame == 0:
            pass
        else:
            # Update live plotter with new feedback
            # trajectory_fig.roll("trajectory", current_x, current_y) (commented out)
            # trajectory_fig.roll("car", current_x, current_y) (commented out)
            # ... (other commented out lines related to live plotting update)
            # forward_speed_fig.roll("forward_speed", (commented out)
            #                        current_timestamp,
            #                        current_speed)
            # forward_speed_fig.roll("reference_signal", (commented out)
            #                        current_timestamp,
            #                        controller._desired_speed)

            # throttle_fig.roll("throttle", current_timestamp, cmd_throttle) (commented out)
            # brake_fig.roll("brake", current_timestamp, cmd_brake) (commented out)
            # steer_fig.roll("steer", current_timestamp, cmd_steer) (commented out)

            # Refresh the live plot based on the refresh rate
            # set by the options
            # if enable_live_plot and \
            #    live_plot_timer.has_exceeded_lap_period():
            #     lp_traj.refresh()
            #     lp_1d.refresh()
            #     live_plot_timer.lap()

        # ... (code after live plotting update)

    # ... (code after the main loop)

# ... (rest of the code)