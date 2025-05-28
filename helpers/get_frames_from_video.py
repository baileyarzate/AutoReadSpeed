import cv2
def get_frames_from_video(video_path: str) -> list:
    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture(video_path)

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error opening video stream or file")
        return []

    frames = []
    timestamp_secs = []
    # Read until video is completed
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
        timestamp_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
        timestamp_secs.append(timestamp_ms / 1000.0)

    # Release the video capture object
    cap.release()
    return frames, timestamp_secs