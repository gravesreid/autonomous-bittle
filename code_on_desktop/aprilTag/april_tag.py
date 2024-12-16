import cv2
import apriltag
import numpy as np

def detect_apriltags_from_video():
    # Open the video stream from the USB camera
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    # Define camera parameters (you need to calibrate your camera to get these values)
    camera_matrix = np.array([[1.58644533e+03, 0.00000000e+00, 1.09010209e+03],
                              [0.00000000e+00, 1.58999207e+03, 5.54331347e+02],
                              [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]], dtype="double")
    dist_coeffs = np.array([[ 6.67373874e-01, -3.70098568e+00,  5.15550204e-03,  5.80996850e-02,
                              5.60129213e+00]], dtype="double")

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

        # Get frame dimensions
        frame_height, frame_width = frame.shape[:2]
        #print(f"Frame dimensions: Width={frame_width}, Height={frame_height}")

        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect tags
        results = detector.detect(gray_frame)

        # Process detections
        for i,r in enumerate(results):
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
            rotation_matrix, _ = cv2.Rodrigues(rvec)

            roll = np.arctan2(rotation_matrix[2][1], rotation_matrix[2][2])
            pitch = np.arctan2(-rotation_matrix[2][0], np.sqrt(rotation_matrix[2][1]**2 + rotation_matrix[2][2]**2))
            yaw = np.arctan2(rotation_matrix[1][0], rotation_matrix[0][0])


            cx = results[i].center[0]
            cy = results[i].center[1]
            print(f"AprilTag detected at: X={cx:.0f}, Y={cy:.0f} tag id: {results[i].tag_id}")
            print(f'Tag orientation: {np.degrees(yaw):.0f} tag id: {results[i].tag_id}')

            # Print the 2D position (x, y) to the serial monitor
            #print(f"AprilTag detected at: X={position[0]:.2f}, Y={position[1]:.2f}")

        # Display the frame with detections
        cv2.imshow("AprilTags Detected", frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close display windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_apriltags_from_video()

