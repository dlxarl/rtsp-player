import tkinter as tk
import os
from modules.interface import RTSPApp

if __name__ == "__main__":
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"

    root = tk.Tk()
    app = RTSPApp(root)
    root.mainloop()