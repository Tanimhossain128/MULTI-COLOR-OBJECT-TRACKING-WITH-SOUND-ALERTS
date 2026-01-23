🔴🟢🔵 Multi-Color Object Tracking with Sound Alerts

This project implements real-time multi-color object detection and tracking using OpenCV. It detects Red, Green, and Blue objects from a live webcam feed, tracks their movement, draws trajectories, and triggers color-specific sound alerts upon detection. The processed video is also recorded and replayed automatically.

📌 Project Overview

The system uses the HSV color space for robust color detection under varying lighting conditions. For each detected object, its center coordinates are calculated, movement history is stored using a deque, and a beep sound is generated to indicate detection. The application also saves the tracked output as a video file for later playback.

✨ Key Features

-Real-time webcam-based object tracking

-Detection of Red, Green, and Blue colored objects

-HSV color space segmentation

-Trajectory tracking using deque

-Color-specific sound alerts using winsound.Beep()

-Displays object coordinates (X, Y) on the video feed

-Saves processed video (output.avi)

-Automatic replay of the recorded tracking session

🛠️ Technologies Used

Python
OpenCV
NumPy
winsound (Windows audio alerts)
Collections (deque)
