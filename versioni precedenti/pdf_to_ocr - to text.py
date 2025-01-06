import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import os

# Imposta il percorso di Tesseract (su Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def pdf_to_ocr(pdf_path, output_folder):
    try:
        os.makedirs(output_folder, exist_ok=True)
        pdf_document = fitz.open(pdf_path)
        
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            pix = page.get_pixmap()
            
            # Salva la pagina come immagine temporanea
            img_path = os.path.join(output_folder, f"page_{page_number + 1}.png")
            pix.save(img_path)
            
            # Esegui OCR sull'immagine
            # text = pytesseract.image_to_string(Image.open(img_path), lang='ita')
            
            # OCR in spagnolo
            text = pytesseract.image_to_string(Image.open(img_path), lang='spa')
            
            # Salva il testo estratto
            text_path = os.path.join(output_folder, f"page_{page_number + 1}.txt")
            with open(text_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text)
                
            print(f"Pagina {page_number + 1} elaborata con successo.")
        
        pdf_document.close()
        print("Conversione OCR completata con successo!")
    
    except Exception as e:
        print(f"Errore: {e}")

# Esempio di utilizzo
pdf_to_ocr('documento.pdf', 'output_ocr')
