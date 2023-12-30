import time
import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors

model = YOLO('yolov8x.pt')
model.info()  # display model information

# Open the video file
video_path = "rtsp://ocam01.local:8554/cam"
cap = cv2.VideoCapture(video_path)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter('./ocam-vid-'+time.strftime("%Y%m%d%H%M%S")+'.mp4', cv2.VideoWriter_fourcc('m','p','4','v'), 10.0, (frame_width,frame_height))
framerate = 10
framecount = framerate
results = 0
x_line=100

# Loop through the video frames
while cap.isOpened():
  # Read a frame from the video
  success, frame = cap.read()

  if framerate != framecount:
    framecount = framecount + 1

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
      break
  elif success:
    framecount = 0
    # Run YOLOv8 inference on the frame
    results = model(frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
      break
  else:
      # Break the loop if the end of the video is reached
      break
  
  frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  annotator = Annotator(frame)
  # Visualize the results on the frame
  for r in results:
    for box in r.boxes:
      b = box.xyxy[0]
      if b[1] > x_line:
        c = box.cls
        annotator.box_label(b, f"{r.names[int(c)]} {float(box.conf):.2}", color=colors(box.cls))

  frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
  if framecount == 0 :
    cv2.putText(frame, "Yolov8",
                  (125, 50), cv2.FONT_HERSHEY_SIMPLEX,
                  1, (255, 255, 255), 2, cv2.LINE_AA)
  else:
    cv2.putText(frame, "Non-Yolov8",
                  (125, 50), cv2.FONT_HERSHEY_SIMPLEX,
                  1, (255, 255, 255), 2, cv2.LINE_AA)
  cv2.imshow("YOLOv8 Inference", frame)
  out.write(frame)

# Release the video capture object and close the display window
cap.release()
out.release()
cv2.destroyAllWindows()
