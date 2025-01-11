# 🎧 PDF to Audiobook Converter 📚🎙️

This project converts PDF documents into:
- ✅ **PDF OCR** (Readable PDF with extracted text using OCR).
- ✅ **Audiobook** (In AAC format, with the option to split into 15MB chunks).
- ✅ **Customizable Volume** using FFmpeg.

---

## 📦 **Requirements**

Make sure you have installed:
- Python 3.10 or higher
- Flask
- FFmpeg
- Tesseract OCR
- Node.js 16.x or higher *(Optional, for future integrations)*

---

## 📚 **Install Dependencies**

Run the following command to install the required Python packages:
```bash
pip install -r requirements.txt
```

---

## 🚀 **How to Run**

You can execute the script in two ways:

1. **Using Default Parameters:**
   ```bash
   python main.py
   ```
   ```python
    python main.py --input input_folder --output output_folder --lang spa --rate 150 --volume 1.0
    ```

   By default, the script:
   - Reads PDFs from the `input_folder`.
   - Saves outputs to the `output_folder`.
   - Uses Spanish (`spa`) as the language.
   - Sets the speech rate to 150 words per minute.
   - Keeps the volume at 1.0.
   - Does not boost audio volume using FFmpeg.

2. **Using Custom Parameters:**
   You can specify parameters as needed:
   ```bash
   python main.py --input input_folder --output output_folder --lang spa --rate 170 --volume 1.0 --ffmpeg_volume 1.5 --voice_index 2
   ```

   ### Parameter Details:
   - **`--input`**: Specifies the folder containing the PDF files.  
     Default: `input_folder`.
   
   - **`--output`**: Specifies the folder where output files (OCR PDF and audio) will be saved.  
     Default: `output_folder`.

   - **`--lang`**: Sets the language for OCR and text-to-speech.  
     Supported values:  
     - `spa` for Spanish  
     - `ita` for Italian  
     - `eng` for English  
     Default: `spa`.

   - **`--rate`**: Defines the speech rate for audio in words per minute.  
     Example: `--rate 170` (Faster speech), `--rate 120` (Slower speech).  
     Default: `150`.

   - **`--volume`**: Sets the initial speech volume (range: 0.0 to 1.0).  
     Example: `--volume 0.8` (80% of max volume).  
     Default: `1.0`.

   - **`--ffmpeg_volume`**: Boosts the final audio volume using FFmpeg.  
     Example: `--ffmpeg_volume 1.5` (Increases by 50%).  
     If not specified, no additional volume boost is applied.

   - **`--voice_index`**: Allows you to select a specific voice for text-to-speech.  
     Example: `--voice_index 2` selects the second voice for the specified language.  
     Default: The first available voice for the language.

---

## 🖥️ **Using the `.bat` File**

You can automate execution using the provided `.bat` file:

```bat
./run_script.bat
```

```bat
@echo off
:: 🚀 Start the PDF → OCR → Audio process

:: --- Default Execution ---
:: python main.py --input input_folder --output output_folder --lang spa --rate 150 --volume 1.0

:: --- Custom Execution ---
echo 🚀 Starting PDF → OCR → Audio Process...
python main.py --input input_folder --output output_folder --lang spa --rate 170 --volume 1.0 --ffmpeg_volume 1.5 --voice_index 2
echo ✅ Process Completed Successfully!

pause
```

---

## 💡 **Examples**

- **Run with Default Parameters:**
   ```bash
   python main.py
   ```

- **Run with Faster Speech and Custom Voice:**
   ```bash
   python main.py --input input_folder --output output_folder --lang eng --rate 180 --voice_index 1
   ```

- **Run with Boosted Volume and Italian Language:**
   ```bash
   python main.py --input input_folder --output output_folder --lang ita --rate 150 --volume 1.0 --ffmpeg_volume 2.0
   ```

---

## 🛠️ **How it Works**

1. **PDF → OCR PDF**: Extracts text from the PDF using Tesseract OCR and saves a readable PDF.
2. **OCR PDF → Audio**: Converts the extracted text to audio using a TTS engine (pyttsx3).
3. **Audio Processing**:  
   - Compresses the audio into AAC format.  
   - Optionally boosts the volume with FFmpeg.  
   - Splits audio files into chunks of up to 15 MB for easy sharing.

---

## 📝 **Note**

- Ensure the required dependencies are installed and configured correctly.  
- Use `nvm` with `.nvmrc` to manage Node.js versions if needed in future updates.

