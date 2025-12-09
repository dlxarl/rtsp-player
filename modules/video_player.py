import cv2
import threading
import time
from PIL import Image, ImageTk


class VideoPlayer:
    def __init__(self):
        self.cap = None
        self.canvas = None
        self.running = False
        self.photo = None
        self.frame = None
        self.lock = threading.Lock()
        self.thread = None
        self.status_callback = None

    def play(self, url, canvas, status_callback=None):
        self.stop()
        self.canvas = canvas
        self.status_callback = status_callback
        self.running = True

        if self.status_callback:
            self.status_callback("Connecting...", "sync")

        self.thread = threading.Thread(target=self._reader, args=(url,), daemon=True)
        self.thread.start()

        self.update_ui()

    def _reader(self, url):
        try:
            self.cap = cv2.VideoCapture(url)

            if self.cap.isOpened():
                if self.status_callback:
                    self.status_callback("Connected", "ok")
            else:
                if self.status_callback:
                    self.status_callback("Connection Failed", "alert")
                self.running = False
                return

            while self.running and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    with self.lock:
                        self.frame = frame
                else:
                    if self.status_callback:
                        self.status_callback("Signal Lost / Retrying...", "warning")
                    time.sleep(1)

        except Exception as e:
            if self.status_callback:
                self.status_callback(f"Error: {str(e)}", "alert")
            self.running = False

    def update_ui(self):
        if not self.running:
            return

        with self.lock:
            current_frame = self.frame

        if current_frame is not None:
            try:
                w = self.canvas.winfo_width()
                h = self.canvas.winfo_height()

                if w > 1 and h > 1:
                    current_frame = cv2.resize(current_frame, (w, h))
                    current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(current_frame)
                    self.photo = ImageTk.PhotoImage(image=img)
                    self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
            except:
                pass

        self.canvas.after(30, self.update_ui)

    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)

        if self.cap:
            self.cap.release()
            self.cap = None

        if self.canvas:
            self.canvas.delete("all")