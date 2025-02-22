import cv2
import cv2.aruco as aruco

# Select the ARUCO dictionary for 4x4 markers.
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()

# Open the default camera (device 0)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# A set to store unique detected tag IDs.
detected_ids = set()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect markers in the grayscale image
    corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        # Draw all detected markers
        aruco.drawDetectedMarkers(frame, corners, ids)
        for i, marker_id in enumerate(ids.flatten()):
            # Add the detected tag to the set of unique IDs.
            detected_ids.add(marker_id)
            # Draw the ID text near the first corner of each marker.
            corner_point = tuple(corners[i][0][0].astype(int))
            cv2.putText(frame, f"ID: {marker_id}", corner_point,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Print the unique detected tag IDs to the console.
    if detected_ids:
        print("Detected tag IDs so far:", sorted(detected_ids))

    # Display the frame with markers
    cv2.imshow("Camera Feed", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows.
cap.release()
cv2.destroyAllWindows()

