import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import pyttsx3
from pydub import AudioSegment
import os


# ✅ 1️⃣ **PDF → PDF OCR**
def pdf_to_ocr_pdf(pdf_path, output_pdf_path, lang='spa'):
    try:
        pdf_document = fitz.open(pdf_path)
        output_document = fitz.open()
        
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            pix = page.get_pixmap()
            
            # Salva la pagina come immagine temporanea
            img_path = f"temp_page_{page_number + 1}.png"
            pix.save(img_path)
            
            # OCR per ottenere il testo e la posizione
            image = Image.open(img_path)
            ocr_text = pytesseract.image_to_pdf_or_hocr(image, lang=lang, extension='pdf')
            
            # Carica il PDF OCR generato da pytesseract
            temp_pdf = fitz.open("pdf", ocr_text)
            
            # Aggiungi il contenuto OCR al PDF di output
            output_document.insert_pdf(temp_pdf)
            
            # Rimuovi il file immagine temporaneo
            os.remove(img_path)
            
            print(f"✅ Pagina {page_number + 1} OCR completata.")
        
        # Salva il PDF OCR finale
        output_document.save(output_pdf_path)
        output_document.close()
        pdf_document.close()
        
        print(f"✅ PDF OCR salvato con successo: {output_pdf_path}")
    
    except Exception as e:
        print(f"❌ Errore PDF OCR: {e}")


# ✅ 2️⃣ **Seleziona la Voce Corretta**
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


# ✅ 3️⃣ **PDF OCR → Audio (Audiolibro)**
def pdf_to_audio(pdf_path, audio_path, lang='spa'):
    try:
        # Apri il PDF OCR
        pdf_document = fitz.open(pdf_path)
        text = ''

        for page in pdf_document:
            text += page.get_text()

        pdf_document.close()
        
        if not text.strip():
            raise ValueError("❌ Nessun testo trovato nel PDF OCR.")
        
        # Imposta il motore text-to-speech
        engine = pyttsx3.init()
        set_voice_by_language(engine, lang)
        engine.setProperty('rate', 150)
        
        # Salva temporaneamente come WAV
        temp_wav = 'temp_audio.wav'
        engine.save_to_file(text, temp_wav)
        engine.runAndWait()
        
        print("✅ Audio temporaneo salvato come WAV.")

        # Imposta manualmente il percorso di FFmpeg
        AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
        AudioSegment.ffmpeg = r"C:\ffmpeg\bin\ffmpeg.exe"
        AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"
        
        # Comprime e salva come MP3
        audio = AudioSegment.from_wav(temp_wav)
        compressed_audio_path = audio_path.replace('.aac', '.mp3')
        audio.export(compressed_audio_path, format='mp3', bitrate='64k')
        
        # Rimuovi il file temporaneo WAV
        os.remove(temp_wav)
        print(f"✅ Audiolibro compresso salvato con successo: {compressed_audio_path}")
    
    except Exception as e:
        print(f"❌ Errore nell'audiolibro: {e}")

# ✅ 4️⃣ **Workflow Completo: PDF → PDF OCR → Audiolibro**
def pdf_to_ocr_and_audio(input_pdf, ocr_pdf, audio_file, lang='spa'):
    """
    Esegue l'intero workflow:
    1. Converte il PDF in un PDF OCR.
    2. Genera un audiolibro nella lingua corretta.
    """
    print("🔄 Avvio processo PDF → PDF OCR → Audiolibro...")
    
    # Step 1: Crea PDF OCR
    pdf_to_ocr_pdf(input_pdf, ocr_pdf, lang=lang)
    
    # Step 2: Crea Audiolibro dal PDF OCR
    lang_audio = {'spa': 'spa', 'ita': 'ita', 'eng': 'eng'}.get(lang, 'eng')
    pdf_to_audio(ocr_pdf, audio_file, lang=lang_audio)
    
    print("🎉 Processo completato con successo!")


# ✅ 5️⃣ **Esempio di utilizzo**
# Cambia 'lang' in 'spa' (spagnolo), 'ita' (italiano), 'eng' (inglese)
pdf_to_ocr_and_audio('documento.pdf', 'documento_ocr.pdf', 'audiolibro.aac', lang='spa')
