# disk.py
import uos


class Disk:
    def __init__(self, root="/"):
        self.root = root
        self.format_disk()  # Başlangıçta disk kontrolü

    def _full_path(self, path):
        if path.startswith("/"):
            return path
        return self.root.rstrip("/") + "/" + path

    def list_dir(self, path=None):
        path = self._full_path(path or self.root)
        try:
            return uos.listdir(path)
        except:
            return []

    def is_folder(self, path):
        path = self._full_path(path)
        try:
            return uos.stat(path)[0] & 0x4000 != 0
        except:
            return False

    def read_file(self, path):
        path = self._full_path(path)
        try:
            with open(path, "r") as f:
                return f.read()
        except:
            return "[File not found]"

    def write_file(self, path, content):
        path = self._full_path(path)
        try:
            # Alt dizinler yoksa oluştur
            parts = path.split("/")
            for i in range(1, len(parts)):
                subpath = "/".join(parts[:i])
                try:
                    uos.mkdir(subpath)
                except:
                    pass
            with open(path, "w") as f:
                f.write(content)
        except Exception as e:
            print(f"[ERROR] Cannot write file {path}: {e}")

    def delete_file(self, path):
        path = self._full_path(path)
        try:
            uos.remove(path)
        except:
            pass

    def mkdir(self, path):
        path = self._full_path(path)
        try:
            uos.mkdir(path)
        except:
            pass

    def format_disk(self):
        # MicroPython ESP32'daki gerçek flash için format yok, silme mantığı
        try:
            for f in uos.listdir("/"):
                try:
                    uos.remove(f)
                except:
                    try:
                        self._rmdir_recursive(f)
                    except:
                        pass
        except:
            pass

    def _rmdir_recursive(self, path):
        for f in uos.listdir(path):
            fp = path.rstrip("/") + "/" + f
            if self.is_folder(fp):
                self._rmdir_recursive(fp)
            else:
                uos.remove(fp)
        uos.rmdir(path)

    def get_info(self):
        # MicroPython'da detaylı disk alanı yok, sadece dosya sayısı
        files = uos.listdir(self.root)
        total_files = len(files)
        return {"max_kb": None, "used_kb": None, "free_kb": None, "file_count": total_files}

    def write_bulk(self, data_dict):
        for k, v in data_dict.items():
            self.write_file(k, v)
