import argparse
import os
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import pyttsx3
from pydub import AudioSegment
import subprocess
import math


# ✅ 1️⃣ **Force FFmpeg Manually**
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffmpeg = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"


# ✅ 2️⃣ **PDF → PDF OCR**
def pdf_to_ocr_pdf(pdf_path, output_pdf_path, lang='spa'):
    try:
        pdf_document = fitz.open(pdf_path)
        output_document = fitz.open()
        
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            pix = page.get_pixmap()
            
            img_path = f"temp_page_{page_number + 1}.png"
            pix.save(img_path)
            
            image = Image.open(img_path)
            ocr_text = pytesseract.image_to_pdf_or_hocr(image, lang=lang, extension='pdf')
            
            temp_pdf = fitz.open("pdf", ocr_text)
            output_document.insert_pdf(temp_pdf)
            
            os.remove(img_path)
            print(f"✅ Page {page_number + 1} OCR completed.")
        
        output_document.save(output_pdf_path)
        output_document.close()
        pdf_document.close()
        
        print(f"✅ PDF OCR saved successfully: {output_pdf_path}")
    
    except Exception as e:
        print(f"❌ PDF OCR Error: {e}")


# ✅ 3️⃣ **Select Correct Voice**
def set_voice_by_language(engine, lang, voice_index=None):
    lang_map = {
        'spa': 'spanish',
        'ita': 'italian',
        'eng': 'english'
    }
    
    voices = engine.getProperty('voices')
    available_voices = [
        voice for voice in voices if lang_map.get(lang, 'english') in voice.name.lower()
    ]
    
    if not available_voices:
        raise ValueError(f"❌ No voices found for language '{lang}'. Check installed voices.")
    
    print("\n🎙️ **Available Voices for Selected Language:**")
    for index, voice in enumerate(available_voices):
        print(f"{index + 1}. {voice.name} ({voice.id})")
    
    # ✅ Selezione tramite indice fornito
    try:
        if voice_index is not None:
            if 1 <= voice_index <= len(available_voices):
                selected_voice = available_voices[voice_index - 1]
            else:
                raise ValueError("Voice index out of range.")
        else:
            selected_voice = available_voices[0]
        
        engine.setProperty('voice', selected_voice.id)
        print(f"✅ Voice selected: {selected_voice.name} ({selected_voice.id})")
    
    except Exception as e:
        print(f"❌ Voice selection error: {e}")
        engine.setProperty('voice', available_voices[0].id)
        print(f"✅ Default voice selected: {available_voices[0].name} ({available_voices[0].id})")


# ✅ 4️⃣ **Adjust Audio Volume (Optional)**
def adjust_audio_volume(input_file, output_file, volume_factor=1.5):
    try:
        print(f"🔊 Increasing volume with FFmpeg (Factor: {volume_factor})...")
        command = [
            r"C:\ffmpeg\bin\ffmpeg.exe",
            '-i', input_file,
            '-filter:a', f"volume={volume_factor}",
            '-y', output_file
        ]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"✅ Volume increased successfully: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg Error:\n{e.stderr}")
    except Exception as e:
        print(f"❌ Error in volume adjustment: {e}")


# ✅ 5️⃣ **Split Audio into 16 MB Parts**
def split_audio_into_parts(input_file, max_mb=16):
    try:
        file_size = os.path.getsize(input_file) / (1024 * 1024)  # In MB
        num_parts = math.ceil(file_size / max_mb)
        print(f"🔄 Splitting the file into {num_parts} parts of up to {max_mb} MB each.")
        
        audio = AudioSegment.from_file(input_file)
        total_duration = len(audio) / 1000  # Total duration in seconds
        
        avg_bitrate_kbps = 64
        max_bytes = max_mb * 1024 * 1024
        max_duration_per_part = (max_bytes * 8) / (avg_bitrate_kbps * 1000)
        
        start_time = 0
        part_counter = 1
        
        while start_time < total_duration:
            end_time = min(start_time + max_duration_per_part, total_duration)
            output_part = f"{os.path.splitext(input_file)[0]}_part{part_counter}.mp3"
            
            audio_part = audio[start_time * 1000:end_time * 1000]
            audio_part.export(output_part, format='mp3', bitrate='64k')
            
            print(f"✅ Part {part_counter} saved as {output_part} ({end_time - start_time} seconds).")
            start_time = end_time
            part_counter += 1
        
        print("🎉 File splitting completed successfully!")
    
    except Exception as e:
        print(f"❌ Error in file splitting: {e}")


# ✅ 6️⃣ **PDF OCR → Audio**
def pdf_to_audio(pdf_path, audio_path, lang='spa', rate=150, volume=1.0, ffmpeg_volume=None, voice_index=None):
    try:
        pdf_document = fitz.open(pdf_path)
        text = ''.join(page.get_text() for page in pdf_document)
        pdf_document.close()
        
        text = text.replace('\n', ' ').replace('\r', ' ')
        
        engine = pyttsx3.init()
        set_voice_by_language(engine, lang, voice_index)
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume)
        
        temp_wav = 'temp_audio.wav'
        engine.save_to_file(text, temp_wav)
        engine.runAndWait()
        
        compressed_audio_path = audio_path.replace('.aac', '.aac')
        subprocess.run([
            r"C:\ffmpeg\bin\ffmpeg.exe", '-i', temp_wav, '-b:a', '64k', '-y', compressed_audio_path
        ], check=True)
        
        os.remove(temp_wav)
        print(f"✅ Audiobook saved: {compressed_audio_path}")
        
        if ffmpeg_volume:
            adjusted_audio_path = compressed_audio_path.replace('.aac', '_loud.aac')
            adjust_audio_volume(compressed_audio_path, adjusted_audio_path, ffmpeg_volume)
            compressed_audio_path = adjusted_audio_path
        
        split_audio_into_parts(compressed_audio_path, 15)
    
    except Exception as e:
        print(f"❌ Audio Error: {e}")


# ✅ 7️⃣ **Main Workflow**
def pdf_to_ocr_and_audio(input_folder, output_folder, lang='spa', rate=150, volume=1.0, ffmpeg_volume=None, voice_index=None):
    os.makedirs(output_folder, exist_ok=True)
    
    for file in os.listdir(input_folder):
        if file.endswith('.pdf'):
            pdf_path = os.path.join(input_folder, file)
            base_name = os.path.splitext(file)[0]

            # 🗂️ Create a subfolder for this specific PDF
            book_output_folder = output_folder
            os.makedirs(book_output_folder, exist_ok=True)

            ocr_pdf = os.path.join(book_output_folder, f"{base_name}_ocr.pdf")
            audio_file = os.path.join(book_output_folder, f"{base_name}.aac")

            pdf_to_ocr_pdf(pdf_path, ocr_pdf, lang)
            pdf_to_audio(ocr_pdf, audio_file, lang, rate, volume, ffmpeg_volume, voice_index=voice_index)

# ✅ 8️⃣ **Run from Command Line**
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=False, help="Folder with input PDF files")
    parser.add_argument('--output', required=False, help="Folder for output files")
    parser.add_argument('--lang', default='spa', help="Language for OCR and TTS (default: spa)")
    parser.add_argument('--rate', type=int, default=150, help="Speech rate (default: 150)")
    parser.add_argument('--volume', type=float, default=1.0, help="Speech volume (default: 1.0)")
    parser.add_argument('--ffmpeg_volume', type=float, default=None, help="FFmpeg volume boost (default: None)")
    parser.add_argument('--voice_index', type=int, default=None, help="Voice index (1-based, optional)")
    parser.add_argument('--filename', required=False, help="Specific PDF filename to process (optional)")

    args = parser.parse_args()
    
    if not args.input:
        print("⚠️ '--input' not provided. Using default: 'input_folder'")
        args.input = 'input_folder'
    if not args.output:
        print("⚠️ '--output' not provided. Using default: 'output_folder'")
        args.output = 'output_folder'
    
    pdf_to_ocr_and_audio(
        input_folder=args.input,
        output_folder=args.output,
        filename=args.filename,
        lang=args.lang,
        rate=args.rate,
        volume=args.volume,
        ffmpeg_volume=args.ffmpeg_volume,
        voice_index=args.voice_index
    )
