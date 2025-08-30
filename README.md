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
