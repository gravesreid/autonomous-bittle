import cv2
import os

# Define the directory where you want to save the photos
save_directory = "/home/reid/Projects/bittle/camera_calibration/23NOV2024"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

stream_url = "http://192.168.1.201:8000/stream.mjpg"
# Initialize the webcam
cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)

cv2.namedWindow("Photo Capture")

img_counter = 0

print("Press SPACE to take a photo, ESC to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Photo Capture", frame)

    key = cv2.waitKey(1)
    if key % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif key % 256 == 32:
        # SPACE pressed
        img_name = os.path.join(save_directory, f"photo_{img_counter}.png")
        cv2.imwrite(img_name, frame)
        print(f"{img_name} saved!")
        img_counter += 1

cap.release()
cv2.destroyAllWindows()
 