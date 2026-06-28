class Shortcut:
    cur_id = 0
    def __init__(self, hotkey):
        self.id = Shortcut.cur_id
        self.hotkey= hotkey