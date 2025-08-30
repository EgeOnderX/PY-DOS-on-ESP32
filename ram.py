class RAM:
    def __init__(self):
        self.memory = {}
        self.total_kb = 128
        self.used_kb = 0

    def load(self, key, value):
        self.memory[key] = value
        self.used_kb = min(self.total_kb, self.used_kb + len(value) // 1024)

    def clear(self):
        self.memory = {}
        self.used_kb = 0

    def get_info(self):
        return {"used_kb": self.used_kb, "total_kb": self.total_kb}
