import cv2
import apriltag
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Global variables for storing tag positions
positions = []

def update_plot(frame):
    """Update the matplotlib plot with the latest positions."""
    if positions:
        x, y = zip(*positions)
        line.set_data(x, y)
    return line,

def detect_apriltags_from_video():
    global positions

    # Open the video stream from the USB camera
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    # Define camera parameters (you need to calibrate your camera to get these values)
    camera_matrix = np.array([[600, 0, 320], [0, 600, 240], [0, 0, 1]], dtype="double")
    dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion

    # Define the size of the AprilTag (in meters)
    tag_size = 0.1  # Example: 10 cm

    # Create the AprilTag detector
    detector = apriltag.Detector()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # If frame reading was unsuccessful, break the loop
        if not ret:
            print("Error: Could not read frame.")
            break

        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect tags
        results = detector.detect(gray_frame)

        # Process detections
        for r in results:
            (cX, cY) = (int(r.center[0]), int(r.center[1]))
            cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)

            # Estimate the position of the tag in 3D space
            object_points = np.array([
                [-tag_size/2, -tag_size/2, 0],
                [ tag_size/2, -tag_size/2, 0],
                [ tag_size/2,  tag_size/2, 0],
                [-tag_size/2,  tag_size/2, 0]
            ], dtype="double")

            image_points = np.array([r.corners[0], r.corners[1], r.corners[2], r.corners[3]], dtype="double")

            _, rvec, tvec = cv2.solvePnP(object_points, image_points, camera_matrix, dist_coeffs)
            position = tvec.flatten()

            # Append the 2D position (x, y) to the list for visualization
            positions.append((position[0], position[1]))

        # Display the frame with detections
        cv2.imshow("AprilTags Detected", frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close display windows
    cap.release()
    cv2.destroyAllWindows()

# Set up the matplotlib plot
fig, ax = plt.subplots()
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1.5)
line, = ax.plot([], [], 'ro-', label="Tag Path")
ax.legend()
ax.set_title("AprilTag Path")
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")

# Set up the animation
ani = FuncAnimation(fig, update_plot, blit=True, interval=50)

if __name__ == "__main__":
    import threading
    # Run AprilTag detection in a separate thread
    thread = threading.Thread(target=detect_apriltags_from_video, daemon=True)
    thread.start()
    # Start the matplotlib animation
    plt.show()

