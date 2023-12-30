from ultralytics import FastSAM
from ultralytics.fastsam import FastSAMPrompt

model = FastSAM('FastSAM.pt')
model.info()  # display model information
#model.predict('./bus.jpg')  # predict
results = model(
    './bus.jpg',
    device='gpu',
    retina_masks=True,
    imgsz=1024,
    conf=0.4,
    iou=0.9,
)

prompt_process = FastSAMPrompt('./bus.jpg', everything_results, device='gpu')
ann = prompt_process.everything_prompt()
