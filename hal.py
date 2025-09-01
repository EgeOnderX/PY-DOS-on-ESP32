import gc, uos, os

class RAM:
    def __init__(self):
        self.update_info()
        self.memory = {}

    def update_info(self):
        gc.collect()
        self.used_bytes = gc.mem_alloc()
        self.free_bytes = gc.mem_free()
        self.total_bytes = self.used_bytes + self.free_bytes

    def load(self, key, value):
        self.memory[key] = value
        self.update_info()

    def clear(self):
        self.memory = {}
        gc.collect()
        self.update_info()

    def get_info(self):
        self.update_info()
        return {
            "used_bytes": self.used_bytes,
            "free_bytes": self.free_bytes,
            "total_bytes": self.total_bytes,
            "entries": len(self.memory)
        }

class Disk:
    def list_dir(self, path):
        try:
            return os.listdir(path)
        except:
            return []

    def is_folder(self, path):
        try:
            return (os.stat(path)[0] & 0x4000) != 0
        except:
            return False

    def mkdir(self, path):
        try:
            os.mkdir(path)
        except:
            pass

    def write_file(self, path, content):
        with open(path, 'w') as f:
            f.write(content)

    def read_file(self, path):
        try:
            with open(path, 'r') as f:
                return f.read()
        except:
            return "[File not found]"

    def del_file(self, path):
        try:
            os.remove(path)
        except:
            pass

    def get_info(self):
        try:
            st = os.statvfs('/')
            total = st[0] * st[2]   # block size * total blocks
            free = st[0] * st[3]    # block size * free blocks
            used = total - free
            return {"total_bytes": total, "used_bytes": used, "free_bytes": free}
        except:
            return {"total_bytes": 0, "used_bytes": 0, "free_bytes": 0}
