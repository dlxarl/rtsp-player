# RTSP Stream Player

A modular, lightweight desktop application for playing RTSP video streams. Built using Python, Tkinter (GUI), and OpenCV (Video Decoding). The application supports playlist management, country flag detection based on IP, stream reordering, and connection status monitoring.

## Features

  * **RTSP Playback:** plays standard RTSP streams using TCP transport for stability.
  * **Playlist Management:** Automatically saves and loads streams from a `playlist.json` file.
  * **Country Detection:** Automatically identifies the country of the stream origin based on the IP address and displays the corresponding national flag.
  * **Favorites System:** Mark streams as favorites (indicated by a star) for quick recognition.
  * **Search:** Filter the playlist in real-time using the search bar.
  * **Stream Management:**
      * **Add:** Supports full RTSP URLs or simple IP addresses (prompts for credentials if needed).
      * **Rename:** Change the display name of any stream.
      * **Reorder:** Move streams up and down in the list.
      * **Remove:** Delete streams from the playlist.
  * **Status Bar:** Visual feedback for connection states (Connecting, Connected, Error, Stopped).
  * **Help System:** Built-in documentation accessible via the interface.

## System Requirements

  * **Python:** Version 3.8 or higher.
  * **Operating System:** Windows, macOS, or Linux.

## Installation

### 1\. Clone or Download the Project

Clone repository using Git:
```bash
https://github.com/dlxarl/rtsp-player.git
```

Ensure you have the project files organized in the following structure:

```text
rtsp-player/
├── main.py
├── playlist.json (created automatically)
├── modules/
│   ├── __init__.py
│   ├── geo.py
│   ├── interface.py
│   ├── playlist.py
│   └── video_player.py
└── assets/
    └── icons/
        ├── add.png
        ├── alert.png
        ├── down.png
        ├── find.png
        ├── info.png
        ├── modify.png
        ├── ok.png
        ├── remove.png
        ├── star.png
        ├── sync.png
        ├── up.png
        └── warning.png
```

### 2\. Create a Virtual Environment (Optional)

>If you are not familiar with virtual environments, you can skip this step.

Create a new virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate
`````

### 3\. Install Dependencies

Open your terminal or command prompt and install the required Python libraries:

```bash
pip install reqiurements.txt
```

  * **opencv-python:** Handles video stream connection and decoding.
  * **pillow:** Handles image processing for the GUI (displaying video frames and icons).
  * **requests:** Used for the IP-to-Country API.

## Running the Application

### Windows

1.  Open Command Prompt (cmd) or PowerShell.
2.  Navigate to the project directory:
    ```cmd
    cd path\to\rtsp-player
    ```
3.  Run the application:
    ```cmd
    python main.py
    ```

### macOS

1.  Open Terminal.
2.  Navigate to the project directory:
    ```bash
    cd /path/to/rtsp-player
    ```
3.  Run the application:
    ```bash
    python main.py
    ```

*Note for Apple Silicon (M1/M2/M3): The application uses OpenCV, which works natively on Apple Silicon without requiring Rosetta.*

### Linux (Ubuntu/Debian)

1.  Open Terminal.
2.  Ensure you have the `python3-tk` package installed (required for Tkinter on Linux):
    ```bash
    sudo apt-get install python3-tk
    ```
3.  Navigate to the project directory and run:
    ```bash
    python3 main.py
    ```

## Usage Guide

### Adding a Stream

1.  Click the **+** button in the control panel.
2.  Enter the stream address. You can enter:
      * A full URL: `rtsp://admin:12345@192.168.1.50:554/stream`
      * Just an IP: `192.168.1.50`
3.  If you enter just an IP, the application will automatically prompt you for a **Username** and **Password**, then construct the URL for you.
4.  Enter a name for the stream (e.g., "Backyard Camera").

### Playing a Stream

  * **Method 1:** Double-click the stream name in the list.
  * **Method 2:** Select the stream and click the **Play** button.
  * The video will appear in the main black area. The status bar at the bottom will show "Connecting..." followed by the IP address and "Connected".

### Managing the Playlist

  * **Search:** Type in the top search bar to filter streams by name.
  * **Edit (Pencil Icon):** Select a stream and click this button to rename it.
  * **Favorite (Star Icon):** Select a stream and click this button. A star symbol will appear next to the name, and the status is saved.
  * **Reorder (Up/Down Arrows):** Select a stream and use the arrow buttons to change its position in the list.
  * **Remove (X Icon):** Permanently deletes the selected stream from the playlist.

### Status Bar Indicators

The bar at the bottom of the window provides real-time feedback:

  * **Sync Icon:** The player is attempting to establish a connection.
  * **Checkmark (OK) Icon:** Connection established successfully.
  * **Warning Icon:** The stream was stopped manually or signal was lost.
  * **Alert Icon:** Connection failed (wrong IP, wrong password, or device offline).

## Troubleshooting

**The interface freezes when adding a camera:**
The application uses threading to prevent freezing, but if your internet connection is extremely slow, the initial DNS lookup for the country flag might take a moment. This is normal.

**Video artifacts or gray screen:**
The application forces TCP transport for RTSP to ensure stability. If you still see artifacts, check your network bandwidth.

**"ImportError: No module named..."**
Ensure you have activated your virtual environment (if you use one) and installed all requirements using `pip install opencv-python pillow requests`.

**Icons are missing:**
Ensure the `assets/icons/` folder exists and contains all the required `.png` files listed in the installation section. The images must be 16x16 pixels.