@echo off
:: 🚀 Start the PDF → OCR → Audio process

:: --- Default Execution (Commented) ---
:: python main.py --input input_folder --output output_folder --lang spa --rate 150 --volume 1.0

:: --- Direct Execution ---
echo 🚀 Starting PDF → OCR → Audio Process...
python main.py --input input_folder --output output_folder --lang spa --rate 170 --volume 1.0 --ffmpeg_volume 1.5
echo ✅ Process Completed Successfully!

:: --- Run with Default Command (if uncommented) ---
:: To use default parameters, uncomment the first python command above.

pause
