# 🚗 AutoReadSpeed – AI Speedometer Reader

AutoReadSpeed is a Streamlit-based app that uses computer vision and OCR to extract speedometer readings from uploaded videos (**digital odometers currently supported; analog odometers may be implemented in a future release**). It's designed for use in **automotive testing, data logging, intelligent driving analysis, and by driving enthusiasts**.

---

## Demo
![Demo](sample_videos/demo.gif)

---

## 🧠 Features

- 📹 Upload a video of a speedometer
- ⏱️ Sample frames at customizable intervals (e.g., every 3 seconds)
- 🔍 On the backend, the app uses EasyOCR or Tesseract to extract speed values from each frame
- 📈 View speed trends through interactive plots
- 📤 Export results to .XLSX

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/baileyarzate/AutoReadSpeed.git
cd AutoReadSpeed
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install required packages
```bash
pip install -r requirements.txt
```

### 4. Launch the app from the CLI
```bash
streamlit run streamlit_app_AutoReadSpeed.py
```

---

📂 Outputs
- A .xlsx file with timestamps and detected speed values
- Line plots showing speed over time

🧪 Future Improvements
- Support for analog odometer detection (via dial or needle tracking)
- Visual feedback for OCR bounding boxes
- Batch processing for multiple videos
- Enhanced model filtering for noisy inputs
- Enhanced data analysis
- Optional video playback with overlayed speed values

📄 License
- This project is licensed under the MIT License.

🙋‍♀️ About the Author
- Created by @baileyarzate, a Data Scientist working for the U.S. Air Force as a civil servant with a passion for machine learning, vision systems, and intelligent automation.
