import tkinter as tk

# --- Configuration ---
FLASH_INTERVAL_SECONDS = 180  # 3 minutes
FLASH_DURATION_SECONDS = 5  # 5 seconds
NORMAL_COLOR = "dark grey"
FLASH_COLOR = "red"
WINDOW_TITLE = "Flashing Timer Window"
WINDOW_GEOMETRY = "400x300"  # Width x Height

# --- Global Variables ---
remaining_time = FLASH_INTERVAL_SECONDS
timer_job_id = None  # To store the ID of the scheduled job for cancellation
is_flashing = False  # Flag to track if currently flashing

# --- Functions ---


def update_countdown():
    """Updates the console countdown timer every second."""
    global remaining_time, timer_job_id

    if not is_flashing and remaining_time > 0:
        # Print remaining time (use \r to overwrite the previous line)
        print(f"\rTime until next flash: {remaining_time} seconds ", end="")
        remaining_time -= 1
        # Schedule the next update
        timer_job_id = root.after(1000, update_countdown)  # 1000ms = 1 second
    elif not is_flashing and remaining_time <= 0:
        # Time is up, but flash hasn't started yet (handled by flash_red)
        print("\rWaiting for flash...                ", end="")
        # Don't reschedule here; flash_red takes over


def flash_red():
    """Changes background to red and schedules return to normal."""
    global is_flashing, timer_job_id

    # Stop the countdown timer if it's running
    if timer_job_id:
        root.after_cancel(timer_job_id)
        timer_job_id = None

    is_flashing = True
    print("\n--- FLASHING RED ---")  # New line for clarity
    root.config(bg=FLASH_COLOR)
    # Schedule return to grey after FLASH_DURATION_SECONDS
    root.after(FLASH_DURATION_SECONDS * 1000, return_to_normal)


def return_to_normal():
    """Returns background to normal, resets timer, and restarts countdown."""
    global remaining_time, is_flashing
    print("--- Returning to Normal ---")
    is_flashing = False
    root.config(bg=NORMAL_COLOR)

    # Reset timer
    remaining_time = FLASH_INTERVAL_SECONDS

    # Restart the main cycle: schedule the next flash
    root.after(FLASH_INTERVAL_SECONDS * 1000, flash_red)

    # Restart the countdown display immediately
    update_countdown()


# --- Main Application Setup ---
root = tk.Tk()
root.title(WINDOW_TITLE)
root.geometry(WINDOW_GEOMETRY)
root.config(bg=NORMAL_COLOR)  # Set initial background

print(f"Window '{WINDOW_TITLE}' opened.")
print(f"Background: {NORMAL_COLOR}")
print(
    f"Will flash {FLASH_COLOR} every {FLASH_INTERVAL_SECONDS} seconds for {FLASH_DURATION_SECONDS} seconds."
)

# --- Start the Cycle ---
# Schedule the first flash
root.after(FLASH_INTERVAL_SECONDS * 1000, flash_red)
# Start the initial countdown display
update_countdown()

# --- Run the Tkinter event loop ---
root.mainloop()

# --- Cleanup (optional, good practice) ---
print("\nWindow closed. Exiting.")
# Attempt to cancel any lingering timer jobs if the window is closed abruptly
if timer_job_id:
    try:
        root.after_cancel(timer_job_id)
    except tk.TclError:
        # Ignore error if root window is already destroyed
        pass
