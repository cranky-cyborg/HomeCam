from ultralytics import YOLO

# Load a pretrained YOLOv8n model
model = YOLO('yolov8n.pt')

# Define source as RTSP, RTMP or IP streaming address
source = 'rtsp://ocam02.local:8554/cam01'

# Run inference on the source
results = model(source, stream=True)  # generator of Results objects

model.predict(source, save=True, imgsz=320, conf=0.5)

for r in results:
  boxes = r.boxes
  masks = r.masks
  probs = r.probs
  
#res = model(img)
#res_plotted = res[0].plot()
#cv2.imshow("result", res_plotted)
