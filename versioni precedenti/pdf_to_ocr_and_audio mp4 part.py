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
    
    voice_selected = False
    voices = engine.getProperty('voices')
    
    for voice in voices:
        if lang_map.get(lang, 'english') in voice.name.lower():
            engine.setProperty('voice', voice.id)
            voice_selected = True
            print(f"✅ Voce selezionata: {voice.name} ({voice.id})")
            break
    
    if not voice_selected:
        raise ValueError(f"❌ Nessuna voce trovata per la lingua '{lang}'. Verifica le voci installate.")


# ✅ 4️⃣ **PDF OCR → Audio (Audiolibro con Partizionamento)**
def pdf_to_audio(pdf_path, audio_path, lang='spa'):
    try:
        pdf_document = fitz.open(pdf_path)
        text = ''
        for page in pdf_document:
            text += page.get_text()
        pdf_document.close()
        
        if not text.strip():
            raise ValueError("❌ Nessun testo trovato nel PDF OCR.")
        
        engine = pyttsx3.init()
        set_voice_by_language(engine, lang)
        engine.setProperty('rate', 150)
        
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
        
        # ✅ Dividi il file AAC in parti da 16 MB
        split_audio_into_parts(compressed_audio_path, 16)
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Errore FFmpeg:\n{e.stderr}")
    except Exception as e:
        print(f"❌ Errore nell'audiolibro: {e}")


# ✅ 5️⃣ **Dividere il File AAC in Parti da 16 MB**
def split_audio_into_parts(input_file, max_mb):
    try:
        # Calcola la dimensione totale del file
        file_size = os.path.getsize(input_file) / (1024 * 1024)  # In MB
        
        # Calcola il numero di parti
        num_parts = math.ceil(file_size / max_mb)
        print(f"🔄 Divisione del file in {num_parts} parti da massimo {max_mb} MB ciascuna.")
        
        # Ottieni la durata totale usando pydub
        audio = AudioSegment.from_file(input_file)
        duration = len(audio) / 1000  # Durata in secondi
        
        # Durata per ciascuna parte
        part_duration = duration / num_parts
        
        for i in range(num_parts):
            start_time = i * part_duration * 1000  # in millisecondi
            end_time = (i + 1) * part_duration * 1000
            
            output_part = f"{os.path.splitext(input_file)[0]}_part{i+1}.mp4"
            audio_part = audio[start_time:end_time]
            audio_part.export(output_part, format='mp4', codec='aac', bitrate='64k')
            
            print(f"✅ Parte {i+1} salvata come {output_part}")
        
        print("🎉 Divisione completata con successo!")
    
    except Exception as e:
        print(f"❌ Errore nella divisione del file: {e}")


# ✅ 6️⃣ **Workflow Completo**
def pdf_to_ocr_and_audio(input_pdf, ocr_pdf, audio_file, lang='spa'):
    print("🔄 Avvio processo PDF → PDF OCR → Audiolibro...")
    pdf_to_ocr_pdf(input_pdf, ocr_pdf, lang=lang)
    lang_audio = {'spa': 'spa', 'ita': 'ita', 'eng': 'eng'}.get(lang, 'eng')
    pdf_to_audio(ocr_pdf, audio_file, lang=lang_audio)
    print("🎉 Processo completato con successo!")


# ✅ 7️⃣ **Esempio di utilizzo**
pdf_to_ocr_and_audio('documento.pdf', 'documento_ocr.pdf', 'audiolibro.aac', lang='spa')
