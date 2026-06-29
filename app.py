from pynput import mouse, keyboard
from pynput.keyboard import Controller as kb_controller
from pynput.mouse import Button, Controller as mouse_controller
import subprocess
import time
from pprint import pprint

mouse_ctl = mouse_controller()
kb_ctl = kb_controller()

recording = False # record movements for hotkey
registering = False # waiting for key to be registered
hotkeys = [] # registered hot keys
cur_thread = None

speed = 2 # 200%

movements = {}
cur_movement = [] # schema: 

cur_time = 0

def millis():
    return round(time.time() * 1000)

def send_notification(message):
  subprocess.run([
    "osascript", "-e", 
    f'display notification "{message}" with title "Shortcut Manager"'
])
    
def toggle_recording():
    global recording, registering, cur_time
    recording = not recording
    cur_time = millis()

    if recording:
        send_notification("Recording screen activity")
    else:
        send_notification("Recording halted")
        registering = True

def run_shortcut(hotkey):
    if hotkey[-1] == "a":
        toggle_recording()
        return
    if hotkey[-1] == "b":
        pprint(movements)
        return
    else:
        for movement in movements[hotkey]:
            movement_type = movement["type"]
            if movement_type == "time":
                time.sleep(movement["millis"] / 1000 / speed)
            elif movement_type == "click":
                mouse_ctl.position = (movement["x"], movement["y"])
                time.sleep(0.2)
                button = movement["button"]
                if button == 1:
                    mouse_ctl.click(Button.left)
                elif button == 3:
                    mouse_ctl.click(Button.right)
            elif movement_type == "scroll":
                mouse_ctl.position = (movement["x"], movement["y"])
                time.sleep(0.2)
                mouse_ctl.scroll(movement["dx"], movement["dy"])

def update_hotkeys(shortcuts):
    h = keyboard.GlobalHotKeys(
        {hotkey:lambda hotkey=hotkey: run_shortcut(hotkey) for hotkey in hotkeys}
    )
    h.start()
    return h

def add_hotkey(hotkey):
    global cur_thread
    hotkeys.append(hotkey)
    if cur_thread:
        cur_thread.stop()
    cur_thread = update_hotkeys(hotkeys)

def on_click(x, y, button, pressed):
    global cur_time

    if recording and pressed:
        cur_movement.append({"type": "time", "millis": millis() - cur_time})
        cur_time = millis()

        cur_movement.append({"type": "click", "x": x, "y": y, "button": 1 if button == Button.left else 3}) # left: 1, right: 3

def on_scroll(x, y, dx, dy):
    global cur_time

    if recording:
        cur_movement.append({"type": "time", "millis": millis() - cur_time})
        cur_time = millis()
        cur_movement.append({"type": "scroll", "x": x, "y": y, "dx": dx, "dy": dy})
       
def on_press(key):
    global registering, movements, cur_movement

    if registering:
        add_hotkey(f'<ctrl>+{key.char}')
        f'<ctrl>+{key.char}'
        movements[f'<ctrl>+{key.char}'] = cur_movement[1:]
        cur_movement = []

        send_notification(f'Saved to {key.char.upper()}')
        registering = False

if __name__ == "__main__":
    cur_time = millis()
    mouse_listener = mouse.Listener(
        on_click=on_click,
        on_scroll=on_scroll
    )
    mouse_listener.start()
    kb_listener = keyboard.Listener(
        on_press=on_press,
        # on_release=on_release,
    )
    kb_listener.start()

    add_hotkey("<ctrl>+a")
    add_hotkey("<ctrl>+b")
    
    while True:
        pass

