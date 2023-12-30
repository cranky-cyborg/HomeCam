import time
import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors

class yoloStreamReader:
  def __init__(self, rtspURL, videoPath):
    self.videoPath = videoPath
    self.model = YOLO('yolov8l.pt')
    self.cap = cv2.VideoCapture(rtspURL)
    self.framerate = 10
    self.frame_width = int(self.cap.get(3))
    self.frame_height = int(self.cap.get(4))
    self.out = cv2.VideoWriter(self.videoPath+'/y-ocam-'+time.strftime("%Y%m%d%H%M%S")+'.mp4', cv2.VideoWriter_fourcc('m','p','4','v'), 10.0, (self.frame_width,self.frame_height))
    
    # self.hourFile = False

  def processStream(self):
    self.model.info()
    framecount = self.framerate
    results = 0
    x_line=100
    # Loop through the video frames
    while self.cap.isOpened():
      # Read a frame from the video
      success, frame = self.cap.read()  
    
      if success:
        if self.framerate != framecount:
          framecount = framecount + 1
        else:
          framecount = 0
          # Run YOLOv8 inference on the frame
          results = self.model(frame)
      else:
          # Break the loop if the end of the video is reached
          print("ERROR: Unsuccesful frame read, exiting")
          break
      
      # Break the loop if 'q' is pressed
      if cv2.waitKey(1) & 0xFF == ord("q"):
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
      if framecount == 0:
        cv2.putText(frame, "YOLOv8 - YES",
                    (8, 65), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 255), 2, cv2.LINE_AA)
      else:
        cv2.putText(frame, "YOLOv8 - NO",
                    (8, 65), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 255), 2, cv2.LINE_AA)
      cv2.imshow("YOLOv8 Inference", frame)
      self.out.write(frame)
      
    #   if self.hourFile == False and time.localtime().tm_min == 0 and time.localtime().tm_sec <= 1:
    #     self.out.release()
    #     self.out = cv2.VideoWriter(self.videoPath+'/y-ocam-'+time.strftime("%Y%m%d%H%M%S")+'.mp4', cv2.VideoWriter_fourcc('m','p','4','v'), 10.0, (self.frame_width,self.frame_height))
    #     self.hourFile = True
    #   else:
    #     self.hourFile = False 

  def __del__(self):
    # Release the video capture object and close the display window
    self.cap.release()
    self.out.release()
    cv2.destroyAllWindows()
    print("destroyer activated")

ystream01 = yoloStreamReader("rtsp://ocam01.local:8554/cam", "../Pictures")
#ystream02 = yoloStreamReader("rtsp://ocam02.local:8554/cam")
ystream01.processStream()
#ystream02.processStream()
del ystream01
#del ystream02
