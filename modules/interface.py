import tkinter as tk
from tkinter import simpledialog, ttk, messagebox
import threading
from PIL import Image, ImageTk
import os
from .playlist import PlaylistManager
from .video_player import VideoPlayer
from . import geo


class RTSPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RTSP Player")
        self.root.geometry("1280x720")
        self.root.configure(bg="white")

        self.playlist_manager = PlaylistManager()
        self.streams = self.playlist_manager.load()
        self.player = VideoPlayer()

        self.ui_icons = {}
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.update_listbox())

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="white",
                        fieldbackground="white",
                        foreground="black",
                        font=("Arial", 11))
        style.map("Treeview", background=[("selected", "#e0e0e0")], foreground=[("selected", "black")])

        self.setup_ui()

    def load_ui_icons(self):
        icon_names = ["up", "down", "modify", "remove", "star", "add",
                      "ok", "sync", "alert", "warning", "find", "info"]
        for name in icon_names:
            path = f"assets/icons/{name}.png"
            if os.path.exists(path):
                try:
                    img = Image.open(path)
                    img = img.resize((16, 16), Image.Resampling.LANCZOS)
                    self.ui_icons[name] = ImageTk.PhotoImage(img)
                except Exception:
                    pass

    def setup_ui(self):
        self.load_ui_icons()

        self.status_frame = tk.Frame(self.root, height=25, bg="#f0f0f0", bd=1, relief=tk.SUNKEN)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = tk.Label(self.status_frame, text="Ready", bg="#f0f0f0", fg="#333", font=("Arial", 9),
                                     compound="left")
        self.status_label.pack(side=tk.LEFT, padx=5)

        self.info_btn = tk.Button(self.status_frame, command=self.show_help, bg="#f0f0f0", relief="flat",
                                  highlightthickness=0, bd=0)
        if "info" in self.ui_icons:
            self.info_btn.config(image=self.ui_icons["info"])
        else:
            self.info_btn.config(text="?")
        self.info_btn.pack(side=tk.RIGHT, padx=5)

        video_frame = tk.Frame(self.root, bg="black")
        video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(video_frame, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        control_panel = tk.Frame(self.root, width=350, bg="white")
        control_panel.pack(side=tk.RIGHT, fill=tk.Y)
        control_panel.pack_propagate(False)

        search_frame = tk.Frame(control_panel, bg="white")
        search_frame.pack(fill=tk.X, padx=10, pady=(15, 5))

        if "find" in self.ui_icons:
            lbl_find = tk.Label(search_frame, image=self.ui_icons["find"], bg="white")
            lbl_find.pack(side=tk.LEFT, padx=(0, 5))

        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                     bg="#f9f9f9", relief="flat", highlightthickness=1, highlightbackground="#ddd")
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.search_entry.insert(0, "Search")
        self.search_entry.config(fg="grey", font=("Arial", 11, "italic"))
        self.search_entry.bind("<FocusIn>", self.on_search_focus_in)
        self.search_entry.bind("<FocusOut>", self.on_search_focus_out)

        self.tree = ttk.Treeview(control_panel, show="tree", selectmode="browse")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.bind('<Double-1>', self.on_play_click)

        list_ops_frame = tk.Frame(control_panel, bg="white")
        list_ops_frame.pack(fill=tk.X, padx=10, pady=5)

        for i in range(6):
            list_ops_frame.columnconfigure(i, weight=1)

        self.create_icon_btn(list_ops_frame, 0, "modify", "Edit", self.rename_stream)
        self.create_icon_btn(list_ops_frame, 1, "star", "★", self.toggle_favorite)
        self.create_icon_btn(list_ops_frame, 2, "up", "▲", self.move_up)
        self.create_icon_btn(list_ops_frame, 3, "down", "▼", self.move_down)
        self.create_icon_btn(list_ops_frame, 4, "remove", "X", self.remove_stream)
        self.create_icon_btn(list_ops_frame, 5, "add", "+", self.add_stream)

        main_btn_frame = tk.Frame(control_panel, bg="white")
        main_btn_frame.pack(fill=tk.X, pady=10, padx=10)

        play_btn = tk.Button(main_btn_frame, text="Play", command=self.play_selected, highlightbackground="white")
        play_btn.pack(fill=tk.X, pady=2)

        stop_btn = tk.Button(main_btn_frame, text="Stop", command=self.stop, highlightbackground="white")
        stop_btn.pack(fill=tk.X, pady=2)

        threading.Thread(target=self.init_playlist_icons, daemon=True).start()

    def show_help(self):
        help_text = (
            "RTSP Player User Guide\n\n"
            "1. Adding a Stream:\n"
            "   Click the (+) button. You can enter:\n"
            "   - IP Address (e.g., 192.168.1.10). You will be prompted for credentials.\n"
            "   - Full RTSP URL (e.g., rtsp://user:pass@192.168.1.10:554/stream).\n\n"
            "2. Playlist Management:\n"
            "   - Edit (Pencil): Rename the selected stream.\n"
            "   - Star: Mark stream as favorite (appears with a ★).\n"
            "   - Up/Down Arrows: Reorder streams in the list.\n"
            "   - Remove (X): Delete the selected stream.\n\n"
            "3. Search:\n"
            "   Use the search bar at the top to filter streams by name.\n\n"
            "4. Playback:\n"
            "   Double-click a stream or select it and press 'Play'.\n"
            "   The status bar at the bottom shows connection progress.\n\n"
            "5. Status Icons:\n"
            "   - Checkmark: Connected successfully.\n"
            "   - Sync: Connecting...\n"
            "   - Warning: Signal lost or stopped.\n"
            "   - Alert: Connection error."
        )
        messagebox.showinfo("Help", help_text)

    def on_search_focus_in(self, event):
        if self.search_entry.get() == "Search":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="black", font=("Arial", 11, "normal"))

    def on_search_focus_out(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search")
            self.search_entry.config(fg="grey", font=("Arial", 11, "italic"))

    def create_icon_btn(self, parent, col, icon_name, fallback_text, cmd):
        btn = tk.Button(parent, command=cmd, highlightbackground="white")
        if icon_name in self.ui_icons:
            btn.config(image=self.ui_icons[icon_name])
        else:
            btn.config(text=fallback_text)
        btn.grid(row=0, column=col, sticky="ew", padx=1)

    def set_status(self, message, status_type="ok"):
        self.root.after(0, lambda: self._update_status_ui(message, status_type))

    def _update_status_ui(self, message, status_type):
        icon = self.ui_icons.get(status_type, None)
        self.status_label.config(text=f" {message}", image=icon)

    def init_playlist_icons(self):
        for i, stream in enumerate(self.streams):
            self.process_stream_icon(i, stream)
            self.root.after(0, self.refresh_tree_item, i)

    def process_stream_icon(self, index, stream):
        if "country_name" not in stream:
            ip = geo.get_ip_from_url(stream["url"])
            name = geo.get_country_name(ip)
            stream["country_name"] = name

        if stream.get("country_name"):
            stream["_icon_obj"] = geo.get_flag_icon(stream["country_name"])

    def refresh_tree_item(self, index):
        self.update_listbox()

    def add_stream(self):
        url_input = simpledialog.askstring("Input", "Enter RTSP URL or IP:")
        if not url_input:
            return

        final_url = url_input
        if not final_url.startswith("rtsp://"):
            final_url = f"rtsp://{final_url}"

        if "@" not in final_url:
            username = simpledialog.askstring("Auth", "Enter Username:")
            if username is None: return
            password = simpledialog.askstring("Auth", "Enter Password:", show='*')
            if password is None: return

            parts = final_url.split("rtsp://")
            final_url = f"rtsp://{username}:{password}@{parts[1]}"

        name = simpledialog.askstring("Name", "Name for this stream:")
        if not name:
            name = final_url

        new_stream = {"name": name, "url": final_url, "favorite": False}
        self.streams.append(new_stream)
        self.playlist_manager.save(self.streams)

        self.update_listbox()
        threading.Thread(target=self.resolve_new_stream, args=(len(self.streams) - 1, new_stream), daemon=True).start()

    def resolve_new_stream(self, idx, stream):
        self.process_stream_icon(idx, stream)
        self.playlist_manager.save(self.streams)
        self.root.after(0, self.update_listbox)

    def rename_stream(self):
        sel = self.tree.selection()
        if not sel: return
        try:
            item_id = sel[0]
            idx = int(item_id)
        except ValueError:
            return

        current_name = self.streams[idx]["name"]
        new_name = simpledialog.askstring("Rename", "New name:", initialvalue=current_name)
        if new_name:
            self.streams[idx]["name"] = new_name
            self.playlist_manager.save(self.streams)
            self.update_listbox()

    def toggle_favorite(self):
        sel = self.tree.selection()
        if not sel: return
        try:
            idx = int(sel[0])
        except ValueError:
            return

        is_fav = self.streams[idx].get("favorite", False)
        self.streams[idx]["favorite"] = not is_fav

        self.playlist_manager.save(self.streams)
        self.update_listbox()

        if str(idx) in self.tree.get_children():
            self.tree.selection_set(str(idx))

    def move_up(self):
        sel = self.tree.selection()
        if not sel: return
        try:
            idx = int(sel[0])
        except ValueError:
            return

        if idx > 0:
            self.streams[idx], self.streams[idx - 1] = self.streams[idx - 1], self.streams[idx]
            self.playlist_manager.save(self.streams)
            self.update_listbox()
            self.tree.selection_set(str(idx - 1))

    def move_down(self):
        sel = self.tree.selection()
        if not sel: return
        try:
            idx = int(sel[0])
        except ValueError:
            return

        if idx < len(self.streams) - 1:
            self.streams[idx], self.streams[idx + 1] = self.streams[idx + 1], self.streams[idx]
            self.playlist_manager.save(self.streams)
            self.update_listbox()
            self.tree.selection_set(str(idx + 1))

    def remove_stream(self):
        sel = self.tree.selection()
        if sel:
            try:
                idx = int(sel[0])
                del self.streams[idx]
                self.playlist_manager.save(self.streams)
                self.update_listbox()
            except ValueError:
                pass

    def play_selected(self):
        sel = self.tree.selection()
        if not sel: return
        try:
            idx = int(sel[0])
            stream = self.streams[idx]
            ip = geo.get_ip_from_url(stream["url"]) or "Stream"
            self.player.play(stream["url"], self.canvas,
                             status_callback=lambda msg, type: self.set_status(f"{ip} - {msg}", type))
        except ValueError:
            pass

    def on_play_click(self, event):
        self.play_selected()

    def stop(self):
        self.player.stop()
        self.set_status("Stopped", "warning")

    def update_listbox(self):
        if not hasattr(self, 'tree'):
            return

        query = self.search_var.get().lower()
        if query == "search":
            query = ""

        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, s in enumerate(self.streams):
            if query and query not in s['name'].lower():
                continue

            icon = s.get("_icon_obj", None)
            prefix = "★ " if s.get("favorite") else ""
            display_text = f" {prefix}{s['name']}"

            if icon:
                self.tree.insert("", "end", iid=str(i), text=display_text, image=icon)
            else:
                self.tree.insert("", "end", iid=str(i), text=display_text)