# PY-DOS-on-ESP32
PY-DOS on ESP32 is a lightweight command-line OS ported to MicroPython. It runs on resource-limited ESP32 boards and provides a simple DOS-like experience via a serial terminal.

> Developed from scratch by **Ege**  
> Licensed under the **MIT License**

## Version Plan:
- One more update will be released for this repository within this month. This update marks the transition from a simple PY-DOS simulator to a fully working PY-DOS for ESP32.
- After version **1.0.5** (this repository is currently at **1.0.4**, as it continues from PY-DOS **1.0.3**), development will move to a new repository:  
  **[Espy32](https://github.com/EgeOnderX/Espy32)**
- In that repository, PY-DOS will evolve into a complete operating system for ESP32, written entirely in Python, capable of running Python scripts natively, and no longer a simulator.

---

## Features

- **Editor app**: Type Python scripts and more.  
- **RUN command**: Still exists, but now runs Python scripts instead of PY-DOS original commands.  
- ⚠️ **Warning**: FORMAT command is dangerous — it erases everything on the flash, including system files.
- Added dead screen.
- **Disk** and **ram.py** do not simulate!  
  - **Disk** connects to the flash/SD card via `boot.py`.  
  - **RAM** stores data in variables, which are actually kept in the real RAM.
 
### Original PY-DOS commands are still available:

- **DIR** – List files and directories  
- **TREE** – Display directory tree  
- **TYPE** – Show file content  
- **WRITE** – Write text to a file (RAM + Disk)  
- **DEL** – Delete a file from RAM and Disk  
- **RENAME** – Rename a file  
- **COPY** – Copy a file  
- **MKDIR** – Create a new directory  
- **CD / CCD** – Change current directory  
- **RUN** – Run a script or application  
- **RAMLOAD** – Load a key-value into RAM  
- **RAMCLEAR** – Clear all RAM contents  
- **RAMSHOW** – Display RAM contents  
- **REBOOT** – Reboot the system  
- **FORMAT** – Format (reset) the disk  
- **PRINT** – Print text to screen  
- **AMS** – Run Anti-Malware Scan (RAM & Disk)  
- **HELP** – Display all available commands  
- **EXIT** – Exit PY-DOS

---


## How to Install
Copy these files to the ESP32's flash: **ram.py**, **disk.py**, **boot.py**, then reset the ESP32.

> **Note:** Using **Thonny** is **not recommended** as it can sometimes cause instability issues like this error:

  - wait until it completes current work;  
  - use Ctrl+C to interrupt current work;  
  - reset the device and try again;  
  - check connection properties;  
  - make sure the device has suitable MicroPython / CircuitPython / firmware;  
  - make sure the device is not in bootloader mode.

However, if you don't want to use **PuTTY** and prefer **Thonny**, you should **disable these options** in Thonny to reduce errors:  
**Tools → Options → Interpreter →**  
- Uncheck **"Use local time in real-time clock"**  
- Uncheck **"Synchronize device's real-time clock"**

---

## All Commands

To see the full list of available commands, simply type helpall into the command line.

---

## Future Plans

- SD card support  
- LCD screen (4x16) support  
- Possibly TFT screen support  
- Separate the kernel from the bootloader  
- Implement a proper filesystem

## ⚠️ As far as public sources and existing projects show, no other ESP32 project offers a Python-based, fully interactive DOS-like operating system like PY-DOS. This makes it a first-of-its-kind project in the ESP32 ecosystem.
