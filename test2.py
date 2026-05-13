from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.export(format="engine")

trt_model = YOLO("yolov8n.engine")

results = trt_model("https://ultralytics.com/images/but.jpg")
print(results)