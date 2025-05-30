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
frames, timestamp_secs, fps = get_frames_from_video(video_path)
every_how_many_seconds = 3

#do the OCR, save values and timestamps
results = []
values = []
rel_timestamps = []

next_sample_time = 0.0
for i in tqdm(range(0,len(frames),90)):
    if timestamp_secs[i] >= next_sample_time:
        result = reader.readtext(frames[i])
        rel_timestamps.append(timestamp_secs[i])
        values.append(get_values(result))
        next_sample_time += every_how_many_seconds  # increment next desired timestamp

#get the one and only unit
unit = get_unit(values)
unit = [unit,]*len(values)

#get the speed value from the nested list
speeds = [speed[0] for speed in values]

print(pd.DataFrame([rel_timestamps,speeds,unit], index = ['Timestamp', 'Speed', "Unit"]).T)
