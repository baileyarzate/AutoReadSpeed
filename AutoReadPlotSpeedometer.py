import easyocr
import pandas as pd
from tqdm import tqdm
from helpers.get_frames_from_video import get_frames_from_video
from helpers.get_values import get_values
from helpers.get_unit import get_unit
import torch
import warnings
warnings.filterwarnings("ignore", message=".*pin_memory.*")

use_gpu = torch.cuda.is_available() 
reader = easyocr.Reader(['en'], gpu=use_gpu)
video_path = r"C:\Users\baile\Documents\Software\AutoReadPlotSpeedometer\sample_videos\Speedometer Tesla Video.mp4"
frames, timestamp_secs = get_frames_from_video(video_path)
every_how_many_frames = 90

#do the OCR, save values and timestamps
results = []
values = []
rel_timestamps = []
for i in tqdm(range(0,len(frames),90)):
    result = reader.readtext(frames[i])
    rel_timestamps.append(timestamp_secs[i])
    values.append(get_values(result))

#get the one and only unit
unit = get_unit(values)
unit = [unit,]*len(values)

#get the speed value from the nested list
speeds = [speed[0] for speed in values]

print(pd.DataFrame([rel_timestamps,speeds,unit], columns = 'Timestamp', 'Speed', "Unit").T)
