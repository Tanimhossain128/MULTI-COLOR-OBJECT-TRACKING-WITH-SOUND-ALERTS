import cv2
import numpy as np
import winsound  # For sound on Windows
from collections import deque

cap = cv2.VideoCapture(0)

# Setup video writer to save output
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# Define color ranges and labels
colors = {
    'Red': {
        'lower': np.array([0, 120, 70]),
        'upper': np.array([10, 255, 255]),
        'color': (0, 0, 255),
        'beep_freq': 1000,
        'pts': deque(maxlen=100)
    },
    'Green': {
        'lower': np.array([40, 70, 70]),
        'upper': np.array([80, 255, 255]),
        'color': (0, 255, 0),
        'beep_freq': 1200,
        'pts': deque(maxlen=100)
    },
    'Blue': {
        'lower': np.array([100, 150, 0]),
        'upper': np.array([140, 255, 255]),
        'color': (255, 0, 0),
        'beep_freq': 1500,
        'pts': deque(maxlen=100)
    }
}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for name, props in colors.items():
        mask = cv2.inRange(hsv, props['lower'], props['upper'])
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        center = None
        for c in contours:
            if cv2.contourArea(c) > 500:
                (x, y), radius = cv2.minEnclosingCircle(c)
                center = (int(x), int(y))
                radius = int(radius)

                # Save center for drawing path
                props['pts'].appendleft(center)

                # Draw circle and label
                cv2.circle(frame, center, radius, props['color'], 2)
                cv2.circle(frame, center, 5, (255, 255, 255), -1)
                text = f"{name} X:{center[0]} Y:{center[1]}"
                cv2.putText(frame, text, (center[0]+10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, props['color'], 2)

                print(f"{name} Object at: X={center[0]}, Y={center[1]}")
                winsound.Beep(props['beep_freq'], 200)

        # Draw lines connecting the points
        for i in range(1, len(props['pts'])):
            if props['pts'][i - 1] is None or props['pts'][i] is None:
                continue
            cv2.line(frame, props['pts'][i - 1], props['pts'][i], props['color'], 2)

    out.write(frame)  # Save frame to video file
    cv2.imshow("Multi-Color Object Tracker", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key to break
        break

cap.release()
out.release()
cv2.destroyAllWindows()

# ---------- PLAYBACK THE SAVED VIDEO --------------
cap = cv2.VideoCapture('output.avi')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('Replay - Tracked Video', frame)
    if cv2.waitKey(25) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
