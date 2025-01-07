# 🎧 PDF to Audiobook Converter 📚🎙️

This project converts PDF documents into:
- ✅ **PDF OCR** (Readable PDF with extracted text using OCR).
- ✅ **Audiobook** (In AAC format, with the option to split into 15MB chunks).
- ✅ **Customizable Volume** using FFmpeg.

---

## 📦 **Requirements**

Make sure you have installed:
- Python 3.10 or higher
- FFmpeg
- Tesseract OCR
- Node.js 16.x or higher* *(Optional, if needed in future integrations)

### 📚 **Install Dependencies**

Run:
```bash
pip install -r requirements.txt
```

## 🚀 **How to Run the Project**
You can run the project in two ways:
### 🟢 **1. Using Python Directly**
To execute the script directly via Python:

#### Default Execution (No Parameters):
```python
python main.py
```

```python
python main.py --input input_folder --output output_folder --lang spa --rate 150 --volume 1.0
```
#### Execution with Custom Parameters:
```python
python main.py --input input_folder --output output_folder --lang spa --rate 170 --volume 1.0 --ffmpeg_volume 1.5
```

### 🟢 **2. Using the Batch Script (.bat)**
To simplify the execution, use the pre-configured batch script:
```bat
./run_script.bat
```