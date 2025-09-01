from hal import *
import time, gc
def bsod(error_code=" "):
    gc.collect() 
    if not error_code or error_code.strip() == "":
        error_code = "UNKNOWN ERROR"
    print(":( PY-DOS ran into a problem and needs to restart.")
    print("Technical information:")
    print(f"*** STOP: {error_code}")
    input("")
    while True:
        time.sleep(1)


def get_abs_path(path, current_dir, disk=None):
    try:
        # Parametreler doğru mu?
        if current_dir is None or not isinstance(current_dir, str):
            bsod("INVALID_CURRENT_DIR")
        if not path or path.strip() == "":
            bsod("EMPTY_PATH")

        # Root path kontrolü
        if current_dir.strip() == "":
            current_dir = "/"

        # Eğer verilen path zaten absolute ise
        if path.startswith("/"):
            abs_path = path
        else:
            abs_path = current_dir.rstrip("/") + "/" + path if current_dir != "/" else "/" + path

        # Eğer disk objesi verilmişse path gerçekten var mı kontrol et
        if disk is not None and not disk.exists(abs_path):
            bsod("PATH_NOT_FOUND")

        return abs_path
    except Exception:
        bsod("INVALID_PATH")


def tree_command(path, disk, prefix="", depth=0, max_depth=8):
    if depth > max_depth:
        print(prefix + "└── [MAX DEPTH REACHED]")
        return
    items = disk.list_dir(path)
    total = len(items)
    for i, item in enumerate(items):
        item_path = path.rstrip("/") + "/" + item if path != "/" else "/" + item
        connector = "└── " if i == total - 1 else "├── "
        print(prefix + connector + item)
        if disk.is_folder(item_path):
            ext = "    " if i == total - 1 else "│   "
            tree_command(item_path, disk, prefix + ext, depth + 1, max_depth)

def start_terminal(ram, disk):
    current_dir = "/"
    print("╔══════════════════════════════╗")
    print("║        PY-DOS v1.0.4         ║")
    print("║       FOR ESP32 CARDS        ║")
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
            elif command == "help":
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
                print("SYSINFO   : Display RAM, and Disk info")
                print("REBOOT    : Save RAM and restart PY-DOS")
                print("PRINT     : Print text to screen (PRINT text)")
                print("EXIT      : Exit PY-DOS")
            elif command == "type" and len(tokens) >= 2:
                print(disk.read_file(get_abs_path(tokens[1], current_dir)))
            elif command == "edit":
                import edit
                edit.start_editor(disk, ram, current_dir)
            elif command == "sysinfo":
                info = ram.get_info()
                print(f"RAM used: {info['used_bytes']} bytes")
                print(f"RAM free: {info['free_bytes']} bytes")
                print(f"RAM total: {info['total_bytes']} bytes")
                print(f"RAM entries: {info['entries']}")
                disk_info = disk.get_info()
                print(f"Disk total: {disk_info['total_bytes']} bytes")
                print(f"Disk used: {disk_info['used_bytes']} bytes")
                print(f"Disk free: {disk_info['free_bytes']} bytes")
            elif command == "print":
                print(" ".join(tokens[1:]))
            else:
                print("Unknown command")
        except KeyboardInterrupt:
            print("\nUse EXIT to quit.")
        except Exception as e:
            print(f"[ERROR] {e}")

def boot():
    ram = RAM()
    disk = Disk()
    start_terminal(ram, disk)

if __name__ == "__main__":
    boot()
