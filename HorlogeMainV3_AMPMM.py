import time  # To use time.sleep and get the current time
import keyboard  # For pause functionality using keyboard input
from threading import Event

# Global variables for pause functionality
paused = False
pause_event = Event()
pause_event.set()

def request_ampm_format():
    """Ask the user if they want to use AM/PM format."""
    global ampm_format
    ampm_format = None
    while ampm_format is None:
        choice = input("Would you like to use the AM/PM format? (Y/N): ").strip().upper()
        if choice == "Y":
            ampm_format = True
        elif choice == "N":
            ampm_format = False
        else:
            print("Invalid response. Please enter Y or N.")

def predefined_request():
    """Ask the user if they want a predefined clock."""
    while True:
        val = input("Would you like to use a predefined clock? (Y/N): ").strip().upper()
        if val in ("Y", "N"):
            return val
        else:
            print("Invalid response. Please enter Y or N.")

def manual_config():
    """Allow the user to manually configure the clock."""
    while True:
        try:
            hour = int(input("Enter the hour (0-23): "))
            minute = int(input("Enter the minute (0-59): "))
            if 0 <= hour < 24 and 0 <= minute < 60:
                if ampm_format:
                    while True:
                        period = input("AM or PM? ").strip().upper()
                        if period in ("AM", "PM"):
                            return hour, minute, 0, period
                        print("Invalid response. Please enter AM or PM.")
                return hour, minute, 0, None
            else:
                print("Invalid time. Please enter valid hour and minute values.")
        except ValueError:
            print("Invalid input. Please enter numbers only.")

def set_alarm():
    """Allow the user to set an alarm."""
    print("Welcome to the alarm feature!")
    while True:
        alarm_time = input("Enter the alarm time (HH:MM): ").strip()
        try:
            alarm_hour, alarm_minute = map(int, alarm_time.split(":"))
            if 0 <= alarm_hour < 24 and 0 <= alarm_minute < 60:
                print(f"Alarm set for {alarm_hour:02d}:{alarm_minute:02d}.")
                return alarm_hour, alarm_minute
            else:
                print("Invalid time. Please enter a valid hour and minute.")
        except ValueError:
            print("Invalid format. Please enter the time in HH:MM format.")

def toggle_pause(e):
    """Toggle the pause state when the spacebar is pressed."""
    global paused
    paused = not paused
    if paused:
        pause_event.clear()
        print("\nClock paused.")
    else:
        pause_event.set()
        print("\nClock resumed.")

def run_clock(hour, minute, second, alarm=None):
    """Run the clock with optional alarm functionality."""
    global paused
    keyboard.on_press_key("space", toggle_pause)
    alarm_triggered = False

    try:
        print("\nPress the spacebar to pause/resume the clock.")
        while True:
            if not paused:
                if alarm and not alarm_triggered:
                    alarm_hour, alarm_minute = alarm
                    if hour == alarm_hour and minute == alarm_minute:
                        print(f"\nALARM! It's {hour:02d}:{minute:02d}! Time to act!")
                        alarm_triggered = True

                print_time = f"{hour:02d}:{minute:02d}:{second:02d}"
                if ampm_format:
                    period = "AM" if hour < 12 else "PM"
                    display_hour = hour if hour <= 12 else hour - 12
                    if display_hour == 0:
                        display_hour = 12
                    print_time = f"{display_hour:02d}:{minute:02d}:{second:02d} {period}"

                print(print_time, end="\r")

                time.sleep(1)
                second += 1
                if second == 60:
                    second = 0
                    minute += 1
                    if minute == 60:
                        minute = 0
                        hour += 1
                        if hour == 24:
                            hour = 0
    except KeyboardInterrupt:
        print("\nGoodbye!")
    finally:
        keyboard.unhook_all()

def main():
    """Main function to run the clock program."""
    request_ampm_format()
    predefined = predefined_request()

    if predefined == "Y":
        current_time = time.localtime()
        hour, minute, second = current_time.tm_hour, current_time.tm_min, current_time.tm_sec
    else:
        hour, minute, second, _ = manual_config()

    alarm_choice = input("Would you like to set an alarm? (Y/N): ").strip().upper()
    alarm = None
    if alarm_choice == "Y":
        alarm = set_alarm()

    
    run_clock(hour, minute, second, alarm)
    
    
    
if __name__ == "__main__":
    main()
