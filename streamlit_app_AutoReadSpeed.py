import streamlit as st
import pandas as pd
import numpy as np
import easyocr
import pandas as pd
import torch
import warnings
import gc
import os
import pytesseract
#helper functions
from helpers.get_frames_from_video_st import get_frames_from_video_st
from helpers.get_values import get_values
from helpers.get_unit import get_unit
from helpers.preprocess_image import *
from helpers.plotting import _generate_plots_
from helpers.write_statistics import _write_statistics_

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe' 
warnings.filterwarnings("ignore", message=".*pin_memory.*")
#use_gpu = torch.cuda.is_available() 
#reader = easyocr.Reader(['en'], gpu=use_gpu)

@st.cache_resource
def load_reader():
    model_dir = os.path.join(os.getcwd(), '.easyocr_models')
    os.makedirs(model_dir, exist_ok=True)
    return easyocr.Reader(['en'], gpu=False, model_storage_directory=model_dir)

reader = load_reader()

if reader is None:
    st.stop()

@st.cache_data
def __cache__():
    return 0

st.title("AI Speedometer Reader") 
video = st.file_uploader("Choose Video", type=["mp4", "mov", "avi"])
fastgood_slowbad = st.selectbox('Do you want your output to be quick but less accurate or slower but more accurate:',
                                ["Slow & Accurate", "Fast & Inaccurate","TEST"],
                                index = 0)
every_how_many_seconds = float(st.number_input("Get a frame every how many seconds? 0 for entire video."))

if "df" not in st.session_state:
    st.session_state.df = None
if "show_table" not in st.session_state:
    st.session_state.show_table = False
if "show_plots" not in st.session_state:
    st.session_state.show_plots = False

if video and every_how_many_seconds and st.button("Generate Tabular Output"):
    @st.cache_data
    def load_frames(video):
        return get_frames_from_video_st(video, every_how_many_seconds)
    frames, timestamp_secs, fps = load_frames(video)
    results = []
    values = []
    rel_timestamps = []
    target_times = np.arange(0, timestamp_secs[-1], every_how_many_seconds)
    frame_indices = [np.searchsorted(timestamp_secs, t) for t in target_times]
    if fastgood_slowbad == "Slow & Accurate":
        for idx in frame_indices:
            frame = frames[idx]
            try:
                values.append(get_values(reader.readtext(frame)))
            except:
                values.append(['error','error'])
            rel_timestamps.append(timestamp_secs[idx])
            del frame
            gc.collect()
    elif fastgood_slowbad == "Fast & Inaccurate":
        for idx in frame_indices:
            frame = frames[idx]
            speed_val, unit_val = extract_speed_and_unit_from_frame(frame)
            values.append(speed_val)
            rel_timestamps.append(timestamp_secs[idx])
            del frame
            gc.collect()
    else:
        values = [4,8,12,4,5]
        values = list(zip(values,[None,]*len(values)))
        rel_timestamps = [5,10,15,20,25]

    unit = get_unit(values)
    unit = [unit,]*len(values)

    #get the speed value from the nested list
    speeds = [speed[0] for speed in values]
    df = pd.DataFrame([rel_timestamps,speeds,unit], index = ['Elapsed_Time', 'Speed', "Unit"]).T
    st.session_state.df = df
    st.session_state.show_table = True
    st.session_state.show_plots = False

if st.session_state.show_table and st.session_state.df is not None:
    st.subheader("Tabular Output")
    st.write(st.session_state.df)
    st.download_button("Download Excel", st.session_state.df.to_csv(index=False), file_name="output.csv")
    if st.button("Generate Plots"):
        st.session_state.show_plots = True
    
if st.session_state.show_plots:
    df = st.session_state.df
    @st.cache_data
    def generate_plots_write_statistics(df):
        _generate_plots_(df)
        _write_statistics_(df)
    generate_plots_write_statistics(df)
    
            
st.markdown("---")
if st.button("🔁 Reset Session"):
    st.session_state.clear()