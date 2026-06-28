class Shortcut:
    cur_id = 0
    def __init__(self, hotkey):
        self.id = Shortcut.cur_id
        Shortcut.cur_id += 1
        self.hotkey= hotkey

    def dump(self):
        print(self.id, self.hotkey)