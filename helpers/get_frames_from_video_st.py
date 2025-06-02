import cv2
import tempfile
def get_frames_from_video_st(video_file, every_n_sec = 3.0) -> list:
    # Create a VideoCapture object and read from input file
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())

    cap = cv2.VideoCapture(tfile.name)

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error opening video stream or file")
        return [], [], 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration_secs = total_frames / fps

    frames = []
    timestamps = []

    if every_n_sec <= 0:
        # Read ALL frames
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
            frames.append(frame)
            timestamps.append(timestamp)
    else:
        # Read frames at intervals
        current_time = 0.0
        while current_time < duration_secs:
            cap.set(cv2.CAP_PROP_POS_MSEC, current_time * 1000)
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
            timestamps.append(current_time)
            current_time += every_n_sec

    cap.release()
    return frames, timestamps, fps
    # frames = []
    # timestamp_secs = []
    # # Read until video is completed
    # while cap.isOpened():
    #     ret, frame = cap.read()
    #     if not ret:
    #         break
    #     frames.append(frame)
    #     timestamp_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
    #     timestamp_secs.append(timestamp_ms / 1000.0)

    # # Release the video capture object
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # cap.release()
    # return frames, timestamp_secs, fps