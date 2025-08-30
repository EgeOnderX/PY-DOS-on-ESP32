import time
from ram import RAM
from disk import Disk

def get_abs_path(path, current_dir):
    try:
        if not path or path.strip() == "":
            raise ValueError("Empty path")
        if path.startswith("/"):
            return path
        if current_dir == "/":
            return "/" + path
        return current_dir.rstrip("/") + "/" + path
    except Exception:
        bsod("INVALID_PATH")

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

# --- Mini Editor ---
def start_editor(disk, ram, current_dir="/"):
    current_file = None
    buffer = []
    print("══════════════════ Mini Editor ═════════════════════")
    print("Type text or commands starting with ':'")
    print("Commands: :open, :new, :del, :show, :save, :exit")
    print("────────────────────────────────────────────────────")
    while True:
        line = input().rstrip()
        if line.startswith(":"):
            cmd = line[1:].strip()
            if cmd.startswith("open "):
                filename = cmd[5:].strip()
                abs_path = filename if filename.startswith("/") else f"{current_dir}/{filename}"
                content = disk.read_file(abs_path)
                if content in ("[File not found]", "[Is a directory]"):
                    print(f"File not found: {filename}")
                    buffer = []
                    current_file = None
                else:
                    buffer = content.splitlines()
                    current_file = abs_path
                    print(f"Opened {filename}")
            elif cmd.startswith("new "):
                filename = cmd[4:].strip()
                current_file = filename if filename.startswith("/") else f"{current_dir}/{filename}"
                buffer = []
                print(f"New file created: {current_file}")
            elif cmd.startswith("del "):
                try:
                    index = int(cmd[4:]) - 1
                    removed = buffer.pop(index)
                    print(f"Deleted line {index+1}: {removed}")
                except:
                    print("Invalid line number.")
            elif cmd == "show":
                for i, l in enumerate(buffer):
                    print(f"{i+1}: {l}")
            elif cmd == "save":
                if current_file:
                    content = "\n".join(buffer)
                    ram.load(current_file, content)
                    disk.write_file(current_file, content)
                    print(f"Saved: {current_file}")
                else:
                    print("No file to save.")
            elif cmd in ("exit", "quit"):
                break
            else:
                print("Unknown command.")
        else:
            buffer.append(line)

def record_command(cmd, ram):
    cmd_lower = cmd.lower()
    if cmd_lower not in command_history:
        command_history[cmd_lower] = 0
    command_history[cmd_lower] += 1
    if command_history[cmd_lower] > 300:
        print(f"[AMS ALERT] Command '{cmd_lower}' executed {command_history[cmd_lower]} times!")
        while True:
            choice = input("Do you want to clear the ram or reboot the system? (To exit type 'e') (c/r/e): ").strip().lower()
            if choice == "c":
                print("[AMS] Clearing ram...")
                if not disk_obj.is_folder("/ams"):
                    disk_obj.mkdir("/ams")
                disk_obj.write_file("/ams/amslog", "command_history[cmd_lower] > 300:!!!userinput:t;out:break,ramclear!")
                ram.clear()
                break
            elif choice == "r":
                print("[AMS] Rebooting the system...")
                if not disk_obj.is_folder("/ams"):
                    disk_obj.mkdir("/ams")
                disk_obj.write_file("/ams/amslog", "command_history[cmd_lower] > 300:!!!userinput:r;out:break,boot,ramclear!")
                ram.clear()
                boot()
                break
            elif choice == "e":
                print("[AMS] Exiting...")
                if not disk_obj.is_folder("/ams"):
                    disk_obj.mkdir("/ams")
                disk_obj.write_file("/ams/amslog", "command_history[cmd_lower] > 300:!!!userinput:e;out:break!")
                break
            else:
                print("Please type c/r/e ")
                if command_history[cmd_lower] > 600:
                    bsod("COMMAND_FLOOD_ERR")

# --- Anti-Malware Service Deluxe ---
def ams_scan(ram, disk=None, silent=False, delete=False):
    if not silent:
        print("=== Anti-Malware Service Deluxe ===")
    suspicious_found = False

    # RAM taraması
    for key in list(ram.memory.keys()):
        if "format" in ram.memory[key].lower():
            suspicious_found = True
            if not silent:
                print(f"[ALERT] Suspicious 'format' command in RAM key: {key}")
            if delete:
                ram.memory.pop(key)
                if not silent:
                    print(f"[REMOVED] RAM entry {key} deleted")
                if silent:
                    print(f"[REMOVED] RAM entry {key} deleted")

    # Disk taraması
    if disk is not None:
        def scan_folder(path):
            nonlocal suspicious_found
            items = disk.list_dir(path)
            for item in items:
                item_path = path.rstrip("/") + "/" + item if path != "/" else "/" + item
                if disk.is_folder(item_path):
                    scan_folder(item_path)
                else:
                    content = disk.read_file(item_path)
                    if content != "[File not found]" and "format," in content.lower():
                        suspicious_found = True
                        if not silent:
                            print(f"[ALERT] Suspicious 'format' command found in {item_path}")
                        if silent:
                            print(f"[ALERT] Suspicious 'format' command found in {item_path}")
                        if delete:
                            disk.delete_file(item_path)
                            ram.memory.pop(item_path, None)
                            if not silent:
                                print(f"[REMOVED] {item_path} deleted")
                            if silent:
                                print(f"[REMOVED] {item_path} deleted")
                    
        scan_folder("/")
    if not suspicious_found and not silent:
        print("No suspicious activity found.")
def bsod(error_code=" "):
    if not error_code or error_code.strip() == "":
        error_code = "UNKNOWN ERROR"
    print(":( PY-DOS ran into a problem and needs to restart.")
    print("Technical information:")
    print(f"*** STOP: {error_code}")
    input("")
    sys.exit(1)
def start_terminal(ram, disk):
    current_dir = "/"
    print("╔══════════════════════════════╗")
    print("║        PY-DOS v1.4           ║")
    print("║      FOR  ESP32 CARDS        ║")
    print("╚══════════════════════════════╝")
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
                print("=== PY-DOS HELP ===")
                print("DIR, HELPALL, TREE, TYPE, WRITE, DEL, RENAME, COPY, MKDIR, CD, RUN, SAVE, RAMLOAD, RAMCLEAR, RAMSHOW, SYSINFO, REBOOT, FORMAT, PRINT, CLEARCPU, AMS, EXIT")
            elif command == "bsod":
                bsod("none")
            elif command == "dir":
                items = disk.list_dir(current_dir)
                if items:
                    for item in items:
                        item_path = current_dir.rstrip("/") + "/" + item if current_dir != "/" else "/" + item
                        print(f"<DIR> {item}" if disk.is_folder(item_path) else f" {item}")
                else:
                    print("No files or directories.")
            elif command == "tree":
                tree_command(current_dir, disk)
            elif command == "mkdir" and len(tokens) >= 2:
                disk.mkdir(get_abs_path(tokens[1], current_dir))
            elif command == "cd" and len(tokens) >= 2:
                arg = tokens[1]
                if arg == "..":
                    if current_dir != "/":
                        current_dir = current_dir.rstrip("/")
                        idx = current_dir.rfind("/")
                        if idx == 0:
                            current_dir = "/"
                        else:
                            current_dir = current_dir[:idx]
                else:
                    target = get_abs_path(arg, current_dir)
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
            elif command == "run" and len(tokens) >= 2:
                filename = get_abs_path(tokens[1], current_dir)
                source = disk.read_file(filename)
                if source in ("[File not found]", "[Is a directory]"):
                    print("File not found or is a directory.")
                else:
                    try:
                        exec(source, {})
                    except Exception as e:
                        print(f"[ERROR] {e}")
            elif command == "helpall":
                print("======================= PY-DOS HELP ===========================")
                print("DIR       : List files and directories in the current folder")
                print("TREE      : Show folder structure recursively")
                print("TYPE      : Display content of a file (TYPE filename)")
                print("WRITE     : Create or overwrite a file (WRITE filename content)")
                print("DEL       : Delete a file (DEL filename)")
                print("RENAME    : Rename a file (RENAME old_name new_name)")
                print("COPY      : Copy a file (COPY source_file dest_file)")
                print("MKDIR     : Create a new folder (MKDIR foldername)")
                print("CD        : Change directory (CD foldername, CD ..)")
                print("RUN       : Execute a file (RUN filename)")
                print("SAVE      : Save RAM contents to disk")
                print("RAMLOAD   : Load key-value into RAM (RAMLOAD key value)")
                print("RAMCLEAR  : Clear all RAM contents")
                print("RAMSHOW   : Show current RAM contents")
                print("SYSINFO   : Display CPU, RAM, and Disk info")
                print("REBOOT    : Save RAM and restart PY-DOS")
                print("FORMAT    : Format the disk")
                print("PRINT     : Print text to screen (PRINT text)")
                print("CLEARCPU  : Reset CPU cycles to 0")
                print("AMS       : Run Anti-Malware Service scan")
                print("EXIT      : Exit PY-DOS")
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
            elif command == "ams":  
                ams_scan(ram, disk=None, silent=False, delete=True)
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
    ram = RAM()
    disk = Disk()
    print("Boot successful!\n")
    start_terminal(ram, disk)

if __name__ == "__main__":
    boot()
