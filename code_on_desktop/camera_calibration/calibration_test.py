import numpy as np
import cv2

# Load the calibration data
calibration_data = np.load("calibration_data.npy", allow_pickle=True).item()
print(f'calibration_data: {calibration_data}')
camera_matrix = np.array(calibration_data["camera_matrix"])
print(f'camera_matrix: {camera_matrix}')
dist_coeffs = np.array(calibration_data["dist_coeffs"])
print(f'dist_coeffs: {dist_coeffs}')

stream_url = "http://192.168.1.44:8000/stream.mjpg"
# Initialize the webcam
cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Get the width and height of the frames
ret, frame = cap.read()
if not ret:
    print("Error: Could not read frame.")
    exit()

h, w = frame.shape[:2]
new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame reading was unsuccessful, break the loop
    if not ret:
        print("Error: Could not read frame.")
        break

    # Undistort the frame
    undistorted_frame = cv2.undistort(frame, camera_matrix, dist_coeffs, None, new_camera_matrix)

    # Crop the image based on the ROI
    x, y, w, h = roi
    undistorted_frame = undistorted_frame[y:y+h, x:x+w]

    # Display the frame with detections
    cv2.imshow("Undistorted Video Stream", undistorted_frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close display windows
cap.release()
cv2.destroyAllWindows()

