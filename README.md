# A Trick Designed for Chinese Valentine's Day on Aug. 10th 2024

# Debugging

Firstly, you can compile `love_heart_demo1.py` to test whether this program meets your need. The annotation in the script is explicit. Therefore, you can modify it easily.

# Encapsulating

To encapsulate python program, you should first install required package `pyinstaller`. Run the instruction:

```bash
pip install pyinstaller
```

**For MacOS:**
```bash
pyinstaller -F -w -i love_heart_icon.ico love_heart_demo1.py
```

**For Windows:**
```bash
pyinstaller -F --onefile -w -i love_heart_icon.ico love_heart_demo1.py
```

Or you can choose any icon you like.

# Final
You can extract your program from `dist/`.