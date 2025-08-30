# boot.py
import time
from ram import RAM
from disk import Disk

def get_abs_path(path, current_dir):
    if path.startswith("/"):
        return path
    if current_dir == "/":
        return "/" + path
    return current_dir.rstrip("/") + "/" + path

def tree_command(path, disk, prefix=""):
    items = disk.list_dir(path)
    total = len(items)
    for i, item in enumerate(items):
        item_path = path.rstrip("/") + "/" + item if path != "/" else "/" + item
        connector = "└── " if i == total - 1 else "├── "
        print(prefix + connector + item)
        if disk.is_folder(item_path):
            ext = "    " if i == total - 1 else "│   "
            tree_command(item_path, disk, prefix + ext)

def start_editor(disk, ram, current_dir="/"):
    current_file = None
    buffer = []
    print("═══ Mini Editor ═══")
    print("Commands start with ':' like :open, :new, :save, :exit")
    while True:
        line = input().rstrip()
        if line.startswith(":"):
            cmd = line[1:].strip()
            if cmd.startswith("open "):
                filename = get_abs_path(cmd[5:].strip(), current_dir)
                content = disk.read_file(filename)
                if content == "[File not found]":
                    print(f"File not found: {filename}")
                    buffer = []
                    current_file = None
                else:
                    buffer = content.splitlines()
                    current_file = filename
                    print(f"Opened {filename}")
            elif cmd.startswith("new "):
                filename = get_abs_path(cmd[4:].strip(), current_dir)
                buffer = []
                current_file = filename
                print(f"New file: {current_file}")
            elif cmd == "show":
                for i, l in enumerate(buffer):
                    print(f"{i+1}: {l}")
            elif cmd == "save":
                if current_file:
                    content = "\n".join(buffer)
                    disk.write_file(current_file, content)
                    ram.load(current_file, content)
                    print(f"Saved: {current_file}")
                else:
                    print("No file to save")
            elif cmd in ("exit", "quit"):
                break
            else:
                print("Unknown command")
        else:
            buffer.append(line)

def start_terminal(ram, disk):
    current_dir = "/"
    print("PY-DOS v1.0 - MicroPython Edition")
    print("Type HELP for commands.\n")
    while True:
        try:
            cmd_input = input(f"C:{current_dir}> ").strip()
            if not cmd_input:
                continue
            tokens = cmd_input.split()
            command = tokens[0].lower()

            if command == "exit":
                print("Exiting PY-DOS...")
                break
            elif command == "help":
                print("DIR, TREE, TYPE, WRITE, DEL, MKDIR, CD, EDIT, RAMLOAD, RAMCLEAR, RAMSHOW, SYSINFO, FORMAT, PRINT, EXIT")
            elif command == "dir":
                for f in disk.list_dir(current_dir):
                    print(f)
            elif command == "tree":
                tree_command(current_dir, disk)
            elif command == "mkdir" and len(tokens) >= 2:
                disk.mkdir(get_abs_path(tokens[1], current_dir))
            elif command == "cd" and len(tokens) >= 2:
                target = get_abs_path(tokens[1], current_dir)
                if disk.is_folder(target):
                    current_dir = target
                else:
                    print("Directory not found")
            elif command == "write" and len(tokens) >= 3:
                filename = get_abs_path(tokens[1], current_dir)
                content = " ".join(tokens[2:])
                disk.write_file(filename, content)
                ram.load(filename, content)
                print(f"Written: {filename}")
            elif command == "type" and len(tokens) >= 2:
                print(disk.read_file(get_abs_path(tokens[1], current_dir)))
            elif command == "edit":
                start_editor(disk, ram, current_dir)
            elif command == "ramload" and len(tokens) >= 3:
                ram.load(tokens[1], " ".join(tokens[2:]))
                print(f"Loaded into RAM: {tokens[1]}")
            elif command == "ramclear":
                ram.clear()
                print("RAM cleared")
            elif command == "ramshow":
                for k, v in ram.memory.items():
                    print(f"{k} : {v}")
            elif command == "sysinfo":
                info = ram.get_info()
                print(f"RAM used: {info['used_kb']} KB / {info['total_kb']} KB")
            elif command == "print":
                print(" ".join(tokens[1:]))
            elif command == "format":
                confirm = input("Format disk? (y/n): ").strip().lower()
                if confirm == "y":
                    disk.format_disk()
                    print("Disk formatted")
            else:
                print("Unknown command")
        except KeyboardInterrupt:
            print("\nUse EXIT to quit.")
        except Exception as e:
            print(f"[ERROR] {e}")

def boot():
    print("Booting PY-DOS v1.0...")
    time.sleep(0.1)
    ram = RAM()
    disk = Disk()
    print("Boot successful!\n")
    start_terminal(ram, disk)

if __name__ == "__main__":
    boot()