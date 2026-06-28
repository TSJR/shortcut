from pynput import mouse, keyboard
from pynput.keyboard import Key, KeyCode, Controller as kb_controller
from pynput.mouse import Controller as mouse_controller
import tkinter as tk
from tkinter import Label
from shortcut import Shortcut

mouse_ctl = mouse_controller()
kb_ctl = kb_controller()
recording = False # record movements for hotkey

shortcuts = []
cur_thread = None

def on_activate(to_print):
    print(to_print)

def update_shortcuts(shortcuts):
    h = keyboard.GlobalHotKeys(
        {shortcut.hotkey:lambda: on_activate(shortcut.id) for shortcut in shortcuts}
    )
    h.start()
    return h

def add_shortcut(hotkey):
    global cur_thread
    shortcuts.append(Shortcut(hotkey))
    if cur_thread:
        cur_thread.stop()
        print("thread stopped")
    for shortcut in shortcuts:
        shortcut.dump()
    
    cur_thread = update_shortcuts(shortcuts)

def on_click():
    label_text.set("Clicked")
    pass

def on_press(key):
    pass

def on_release(key):
    pass

if __name__ == "__main__":
    mouse_listener = mouse.Listener(
        on_click=on_click,
    )
    mouse_listener.start()
    kb_listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release,
    )
    kb_listener.start()
    print("Running once")
    add_shortcut("<ctrl>+a")
    add_shortcut("<ctrl>+b")
    add_shortcut("<ctrl>+d")

    
    

    root = tk.Tk()
    root.title("App")
    root.geometry("300x150")
    root.attributes('-topmost', True)
    label_text = tk.StringVar(value="Default Value")

    label = Label(root, textvariable=label_text)
    label.pack()

    root.mainloop()

