from ultralytics import YOLO

# Load the YOLO model
model = YOLO("yolo11m.pt")

# Train the model with custom dataset
model.train(data="/content/drive/MyDrive/YOLO/data.yaml", epochs=150)