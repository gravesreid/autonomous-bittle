from ultralytics import YOLO

model = YOLO('yolov8n.pt') # pass any model type
results = model.train(data='Object-Detection-1/data.yaml', epochs=5)
