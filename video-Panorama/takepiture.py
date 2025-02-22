import cv2
import os
import time

# Check if the 'inputs' folder exists, if not create it
# If it exists, delete all files in it
if not os.path.exists('inputs'):
    os.makedirs('inputs')
elif os.path.exists('inputs'):
        for root_folder, folders, files in os.walk('inputs'):
            for file in files:
                file_path = os.path.join(root_folder, file)
                os.remove(file_path)

# Create an 'inputs' folder to store images if it doesn't exist
if not os.path.exists('inputs'):
    os.makedirs('inputs')

# Set up the camera (use the default camera, usually the Pi camera)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not access the camera.")
    exit()

# Allow the camera to warm up
time.sleep(2)

take=0
# Start the video capture loop
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # If frame was not captured successfully, break the loop
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Show the current frame
    cv2.imshow("Camera Feed", frame)
    
    # Check for key presses
    key = cv2.waitKey(1) & 0xFF
    
    # If 's' is pressed, save the image
    if key == ord('s'):
        take=take+1
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"inputs/ph_{take}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Saved: {take}")
    
    # If 'q' is pressed, quit the loop
    elif key == ord('q'):
        break

# Release the camera and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()

