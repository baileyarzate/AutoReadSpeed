import streamlit as st
import pandas as pd
import numpy as np
import easyocr
import pandas as pd
from tqdm import tqdm
from helpers.get_frames_from_video_st import get_frames_from_video_st
from helpers.get_values import get_values
from helpers.get_unit import get_unit
import torch
import warnings
warnings.filterwarnings("ignore", message=".*pin_memory.*")
use_gpu = torch.cuda.is_available() 
reader = easyocr.Reader(['en'], gpu=use_gpu)

@st.cache_data
def __cache__():
    return 0

st.title("AI Speedometer Reader") 
video = st.file_uploader("Choose Video", type=["mp4", "mov", "avi"])

left, right = st.columns(2)
if video:
    
    frames, timestamp_secs, fps = get_frames_from_video_st(video)
    every_how_many_seconds = st.number_input("Get a frame every how many seconds?", min_value=0.01, max_value=60.00, value = 3.00)

    generated_output = False
    if left.button("Generate Excel Output"):
        
        results = []
        values = []
        rel_timestamps = []

       # progress_bar = st.progress(0, text="Processing...")

        next_sample_time = 0.0
        for i in tqdm(range(len(frames))):
            if timestamp_secs[i] >= next_sample_time:
                result = reader.readtext(frames[i])
                rel_timestamps.append(timestamp_secs[i])
                values.append(get_values(result))
                #progress_bar.progress(i + 1, text=f"Progress: {i + 1}%")
                next_sample_time += every_how_many_seconds  # increment next desired timestamp
        unit = get_unit(values)
        unit = [unit,]*len(values)

        #get the speed value from the nested list
        speeds = [speed[0] for speed in values]
        df = pd.DataFrame([rel_timestamps,speeds,unit], index = ['Timestamp', 'Speed', "Unit"]).T
        st.write(df)
        generated_output = True
        st.download_button("Download Excel", df.to_csv(index=False), file_name="output.csv")

    if right.button("Generate Plots"):
        if generated_output == False:
            st.write("You must generate the excel output first!")
        st.line_chart(df.set_index("Time")["Speed"])
        left.markdown('Generated plots')