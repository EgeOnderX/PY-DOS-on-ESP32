import os

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

    def format_disk(self):
        for f in os.listdir('/'):
            if f not in ('boot.py', 'main.py', 'ram.py', 'disk.py'):
                try:
                    os.remove('/' + f)
                except:
                    pass
