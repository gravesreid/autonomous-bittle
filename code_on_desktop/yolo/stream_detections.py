import cv2
import struct
import numpy as np
from ultralytics import YOLO


# Load YOLO
model = YOLO('/home/reid/projects/bittle/autonomous-bittle/code_on_desktop/yolo/runs/detect/train3/weights/best.pt')
model.conf = 0.5

#get output from YOLO V11
def detect_objects(frame):
    results = model([frame], stream=True)
    return results

def draw_boxes(frame, results):
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0]
            cls = int(box.cls[0])
            label = f'{model.names[cls]} {conf:.2f}'
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return frame

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = detect_objects(frame)
        frame = draw_boxes(frame, results)

        cv2.imshow('YOLO Object Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()