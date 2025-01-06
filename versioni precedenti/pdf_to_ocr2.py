import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import os


# Percorso Tesseract (se necessario)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# def pdf_to_ocr_pdf(pdf_path, output_pdf_path, lang='ita'):
def pdf_to_ocr_pdf(pdf_path, output_pdf_path, lang='spa'):
    try:
        pdf_document = fitz.open(pdf_path)
        output_document = fitz.open()
        
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            pix = page.get_pixmap()
            
            # Salva la pagina come immagine
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
            
            print(f"Pagina {page_number + 1} elaborata con successo.")
        
        # Salva il PDF OCR finale
        output_document.save(output_pdf_path)
        output_document.close()
        pdf_document.close()
        
        print(f"PDF OCR creato con successo: {output_pdf_path}")
    
    except Exception as e:
        print(f"Errore: {e}")


# Esempio di utilizzo
pdf_to_ocr_pdf('documento.pdf', 'documento_ocr.pdf', lang='spa')
