import cv2
import numpy as np
import glob

# Set the size of the checkerboard pattern
checkerboard_size = (8, 6)  # (number of inner corners per row, number of inner corners per column)
square_size = 23 / 1000  # size of a square in meters (23 mm)

# Define the world coordinates for 3D points
objp = np.zeros((checkerboard_size[0] * checkerboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:checkerboard_size[0], 0:checkerboard_size[1]].T.reshape(-1, 2)
objp *= square_size

# Arrays to store object points and image points from all the images
objpoints = []  # 3D points in real world space
imgpoints = []  # 2D points in image plane

# Read all images for calibration (supports .jpg and .png)
image_files = glob.glob('/home/reid/projects/bittle/camera_calibration/11DEC2024/*.png')

if len(image_files) == 0:
    print("No calibration images found.")
    exit()

for image_file in image_files:
    img = cv2.imread(image_file)
    if img is None:
        print(f"Error reading image: {image_file}")
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners using standard method and an alternative method
    ret, corners = cv2.findChessboardCorners(gray, checkerboard_size, None)

    if not ret:
        # Try using the alternative method
        ret, corners = cv2.findChessboardCornersSB(gray, checkerboard_size)

    # If found, add object points, image points (after refining them)
    if ret:
        objpoints.append(objp)

        # Refine image points
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), 
                                    (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        imgpoints.append(corners2)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, checkerboard_size, corners2, ret)
        cv2.imshow('Image', img)
        cv2.waitKey(500)
    else:
        print(f"Checkerboard not detected in image: {image_file}")

cv2.destroyAllWindows()

# Ensure there are enough points for calibration
if len(objpoints) == 0 or len(imgpoints) == 0:
    print("No checkerboard corners detected in any image. Calibration failed.")
    exit()

# Camera calibration
ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Save the camera calibration result for later use
calibration_data = {
    "camera_matrix": camera_matrix.tolist(),
    "dist_coeffs": dist_coeffs.tolist(),
}
np.save("calibration_data.npy", calibration_data)

print("Camera matrix:")
print(camera_matrix)
print("\nDistortion coefficients:")
print(dist_coeffs)


