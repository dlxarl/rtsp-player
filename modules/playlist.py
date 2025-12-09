import json
import os


class PlaylistManager:
    def __init__(self, filename="playlist.json"):
        self.filename = filename

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return []

    def save(self, streams):
        clean_streams = []

        for stream in streams:
            stream_copy = stream.copy()

            if "_icon_obj" in stream_copy:
                del stream_copy["_icon_obj"]

            clean_streams.append(stream_copy)

        # Записуємо тільки текстові дані
        with open(self.filename, "w") as f:
            json.dump(clean_streams, f, indent=4)