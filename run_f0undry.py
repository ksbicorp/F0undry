#!/usr/bin/env python3
"""
F0undry Launcher Script
Automated API Key & Secret Scanner with Multi-Tool Integration
"""

import sys
import os
from pathlib import Path

def main():
    """Launch F0undry GUI"""
    # Add config and core to path
    BASE_DIR = Path(__file__).parent
    sys.path.insert(0, str(BASE_DIR / "config"))
    sys.path.insert(0, str(BASE_DIR / "core"))
    sys.path.insert(0, str(BASE_DIR / "tools"))

    try:
        from PyQt5.QtWidgets import QApplication
        from core.f0undry_gui import F0undryGUI
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\n📦 Please install dependencies:")
        print("pip install PyQt5 selenium undetected-chromedriver requests telethon playwright")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error importing modules: {e}")
        sys.exit(1)

    try:
        app = QApplication(sys.argv)
        window = F0undryGUI()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"❌ Error launching F0undry: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Set UTF-8 encoding for Windows console
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass

    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║               🔥 F0UNDRY - API SCANNER 🔥                ║
    ║                                                           ║
    ║         Automated Secret Discovery & Validation           ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    main()