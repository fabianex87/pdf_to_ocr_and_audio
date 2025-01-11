@echo off
:: 🚀 Start the PDF → OCR → Audio process

:: --- Default Execution ---
:: python main.py
:: python main.py --input input_folder --output output_folder --lang spa --rate 150 --volume 1.0

:: --- Custom Execution ---
echo 🚀 Starting PDF → OCR → Audio Process...
python main.py --input input_folder --output output_folder --lang spa --rate 170 --volume 1.0 --ffmpeg_volume 1.5 --voice_index 1
echo ✅ Process Completed Successfully!

pause
