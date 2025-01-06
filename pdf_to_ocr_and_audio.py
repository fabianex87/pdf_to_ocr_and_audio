import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import pyttsx3
from pydub import AudioSegment
import subprocess
import os
import math


# ✅ 1️⃣ **Forza FFmpeg Manualmente**
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
            print(f"✅ Pagina {page_number + 1} OCR completata.")
        
        output_document.save(output_pdf_path)
        output_document.close()
        pdf_document.close()
        
        print(f"✅ PDF OCR salvato con successo: {output_pdf_path}")
    
    except Exception as e:
        print(f"❌ Errore PDF OCR: {e}")


# ✅ 3️⃣ **Seleziona la Voce Corretta**
def set_voice_by_language(engine, lang):
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
        raise ValueError(f"❌ Nessuna voce trovata per la lingua '{lang}'. Verifica le voci installate.")
    
    print("\n🎙️ **Voci Disponibili per la Lingua Selezionata:**")
    for index, voice in enumerate(available_voices):
        print(f"{index + 1}. {voice.name} ({voice.id})")
    
    # 🔄 Richiesta di input all'utente per selezionare la voce
    try:
        choice = input("\n👉 Seleziona il numero della voce desiderata (Premi INVIO per usare la prima disponibile): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(available_voices):
            selected_voice = available_voices[int(choice) - 1]
        else:
            selected_voice = available_voices[0]  # Default alla prima voce se non viene selezionato nulla
        
        engine.setProperty('voice', selected_voice.id)
        print(f"✅ Voce selezionata: {selected_voice.name} ({selected_voice.id})")
    
    except Exception as e:
        print(f"❌ Errore nella selezione della voce: {e}")
        engine.setProperty('voice', available_voices[0].id)
        print(f"✅ Voce di default selezionata: {available_voices[0].name} ({available_voices[0].id})")


# ✅ 4️⃣ **Aumentare il Volume con FFmpeg (Opzionale)**
def adjust_audio_volume(input_file, output_file, volume_factor=1.5):
    try:
        print(f"🔊 Aumento del volume con FFmpeg (Fattore: {volume_factor})...")
        command = [
            r"C:\ffmpeg\bin\ffmpeg.exe",
            '-i', input_file,
            '-filter:a', f"volume={volume_factor}",
            '-y', output_file
        ]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"✅ Volume aumentato con successo: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Errore FFmpeg durante l'aumento del volume:\n{e.stderr}")
    except Exception as e:
        print(f"❌ Errore nell'aumento del volume: {e}")


# ✅ 5️⃣ **PDF OCR → Audio (Audiolibro con Partizionamento)**
def pdf_to_audio(pdf_path, audio_path, lang='spa', rate=150, volume=1.0, ffmpeg_volume=None):
    try:
        pdf_document = fitz.open(pdf_path)
        text = ''
        for page in pdf_document:
            text += page.get_text()
        pdf_document.close()
        
        if not text.strip():
            raise ValueError("❌ Nessun testo trovato nel PDF OCR.")
        
        # ✅ Rimuovi le interruzioni di riga per evitare pause indesiderate
        text = text.replace('\n', ' ').replace('\r', ' ')
        
        engine = pyttsx3.init()
        set_voice_by_language(engine, lang)
        engine.setProperty('rate', rate)  # Velocità dell'audio
        engine.setProperty('volume', volume)  # Volume dell'audio (0.0 - 1.0)
        
        # Salva temporaneamente come WAV
        temp_wav = 'temp_audio.wav'
        engine.save_to_file(text, temp_wav)
        engine.runAndWait()
        
        print("✅ Audio temporaneo salvato come WAV.")
        
        # Comprime e salva come AAC con subprocess
        compressed_audio_path = audio_path.replace('.aac', '.aac')
        command = [
            r"C:\ffmpeg\bin\ffmpeg.exe",
            '-i', temp_wav,
            '-b:a', '64k',
            '-y',
            compressed_audio_path
        ]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        os.remove(temp_wav)
        print(f"✅ Audiolibro compresso salvato con successo: {compressed_audio_path}")
        
        # ✅ Opzionale: Aumenta il volume con FFmpeg
        if ffmpeg_volume:
            adjusted_audio_path = compressed_audio_path.replace('.aac', '_loud.aac')
            adjust_audio_volume(compressed_audio_path, adjusted_audio_path, ffmpeg_volume)
            compressed_audio_path = adjusted_audio_path
        
        # ✅ Dividi il file AAC in parti da 15 MB
        split_audio_into_parts(compressed_audio_path, 15)
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Errore FFmpeg:\n{e.stderr}")
    except Exception as e:
        print(f"❌ Errore nell'audiolibro: {e}")

# ✅ 5️⃣ **Dividere il File MP3 in Parti da 15 MB**
def split_audio_into_parts(input_file, max_mb=16):
    try:
        # Calcola la dimensione totale del file
        file_size = os.path.getsize(input_file) / (1024 * 1024)  # In MB
        
        # Calcola il numero di parti
        num_parts = math.ceil(file_size / max_mb)
        print(f"🔄 Divisione del file in {num_parts} parti da massimo {max_mb} MB ciascuna.")
        
        # Ottieni la durata totale usando pydub
        audio = AudioSegment.from_file(input_file)
        total_duration = len(audio) / 1000  # Durata totale in secondi
        
        # Calcola la durata per ciascuna parte basata sulla dimensione reale
        avg_bitrate_kbps = 64  # Bitrate specificato in kbps
        max_bytes = max_mb * 1024 * 1024  # Dimensione massima in byte
        max_duration_per_part = (max_bytes * 8) / (avg_bitrate_kbps * 1000)  # Durata in secondi
        
        print(f"🔢 Durata massima per parte: {int(max_duration_per_part)} secondi.")
        
        start_time = 0
        part_counter = 1
        
        while start_time < total_duration:
            end_time = min(start_time + max_duration_per_part, total_duration)
            output_part = f"{os.path.splitext(input_file)[0]}_part{part_counter}.mp3"
            
            # Estrai la parte audio
            audio_part = audio[start_time * 1000:end_time * 1000]
            audio_part.export(output_part, format='mp3', bitrate='64k')
            
            print(f"✅ Parte {part_counter} salvata come {output_part} ({end_time - start_time} secondi).")
            
            start_time = end_time
            part_counter += 1
        
        print("🎉 Divisione completata con successo!")
    
    except Exception as e:
        print(f"❌ Errore nella divisione del file: {e}")


# ✅ 6️⃣ **Workflow Completo**
def pdf_to_ocr_and_audio(input_folder, output_folder, lang='spa', rate=150, volume=1.0, ffmpeg_volume=None):
    os.makedirs(output_folder, exist_ok=True)
    for file in os.listdir(input_folder):
        if file.endswith('.pdf'):
            pdf_path = os.path.join(input_folder, file)
            base_name = os.path.splitext(file)[0]
            book_output_folder = os.path.join(output_folder, base_name)
            os.makedirs(book_output_folder, exist_ok=True)
            ocr_pdf = os.path.join(book_output_folder, f"{base_name}_ocr.pdf")
            audio_file = os.path.join(book_output_folder, f"{base_name}.aac")
            pdf_to_ocr_pdf(pdf_path, ocr_pdf, lang)
            pdf_to_audio(ocr_pdf, audio_file, lang, rate, volume, ffmpeg_volume)


# ✅ 7️⃣ **Esempio di utilizzo**
pdf_to_ocr_and_audio('input_folder', 'output_folder', lang='spa', rate=180, volume=1.0, ffmpeg_volume=1.5)
