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