import tkinter as tk
import os
from src.gui.kag_tools import KagTools

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("src/cookies", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("drivers", exist_ok=True)

    root = tk.Tk()
    app = KagTools(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()