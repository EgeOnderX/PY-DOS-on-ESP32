# ram.py
class RAM:
    def __init__(self):
        self.memory = {}

    def load(self, key, value):
        self.memory[key] = value

    def get(self, key):
        return self.memory.get(key, None)

    def clear(self):
        self.memory.clear()

    def get_info(self):
        # Tahmini değerler, MicroPython'da gerçek RAM ölçümü yok
        total_kb = 32000  # ESP32 tipik RAM ~32KB (MicroPython heap)
        used_kb = sum(len(str(v)) for v in self.memory.values()) // 1024
        free_kb = total_kb - used_kb
        return {"total_kb": total_kb, "used_kb": used_kb, "free_kb": free_kb}