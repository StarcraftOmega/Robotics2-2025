#!/usr/bin/env python3
import cv2
import cv2.aruco as aruco
import os
import subprocess
import time

# Set the target tag IDs.
target_ids = {0, 1, 2, 3}

# --- Setup FIFO and xterm ---
fifo_path = '/tmp/aruco_output'
if os.path.exists(fifo_path):
    os.remove(fifo_path)
os.mkfifo(fifo_path)

# Launch xterm to show the FIFO contents using a fixed font.
xterm_proc = subprocess.Popen(['xterm', '-fn', 'fixed', '-hold', '-e', f'cat {fifo_path}'])
fifo = open(fifo_path, 'w', buffering=1)  # line-buffered

# Write an initial message.
fifo.write("Waiting for ARUCO tag detection...\n")
fifo.flush()

# --- Setup ARUCO detection ---
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()

# Open the default camera.
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Convert frame to grayscale.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect markers.
    corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # Prepare a dictionary for tag status.
    tag_status = {tag_id: "Not Detected" for tag_id in target_ids}

    if ids is not None:
        # Draw markers on the frame.
        aruco.drawDetectedMarkers(frame, corners, ids)
        # Update tag_status for detected tags (filtering by target_ids).
        for i, marker_id in enumerate(ids.flatten()):
            if marker_id in target_ids:
                tag_status[marker_id] = "Detected"
                # Optionally, draw the ID text near the marker.
                corner_point = tuple(corners[i][0][0].astype(int))
                cv2.putText(frame, f"ID: {marker_id}", corner_point,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Update the FIFO output.
    # Using ANSI escape sequences to clear the terminal and return the cursor home.
    fifo.write("\033[2J\033[H")
    for tag in sorted(target_ids):
        fifo.write(f"Tag {tag}: {tag_status[tag]}\n")
    fifo.flush()

    # Display the frame.
    cv2.imshow("Camera Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
fifo.close()
xterm_proc.terminate()
