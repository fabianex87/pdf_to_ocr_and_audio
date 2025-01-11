from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from main import pdf_to_ocr_and_audio

app = Flask(__name__)
UPLOAD_FOLDER = 'input_folder'
OUTPUT_FOLDER = 'output_folder'
DOWNLOAD_FOLDER = 'output_folder'

# Configura le cartelle
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# 🏠 Home Page
@app.route('/')
def index():
    return render_template('index.html')

# 🚀 Upload File
@app.route('/upload', methods=['POST'])
def upload():
    if 'pdf' not in request.files:
        return "No file uploaded!", 400
    pdf = request.files['pdf']
    if pdf.filename == '':
        return "No selected file!", 400
    
    # Save uploaded PDF
    upload_folder = os.path.join('input_folder', pdf.filename)
    os.makedirs('input_folder', exist_ok=True)
    pdf.save(upload_folder)
    
    # Process the uploaded file
    output_path = os.path.join('output_folder', os.path.splitext(pdf.filename)[0])
    os.makedirs(output_path, exist_ok=True)
    pdf_to_ocr_and_audio(
        input_folder='input_folder',
        output_folder=output_path,
        lang=request.form.get('lang', 'spa'),
        rate=int(request.form.get('rate', 150)),
        volume=float(request.form.get('volume', 1.0)),
        ffmpeg_volume=float(request.form.get('ffmpeg_volume', 1.0))
    )
    
    # Redirect to download page for this specific file
    return redirect(url_for('download_file_page', folder=os.path.splitext(pdf.filename)[0]))

# Rotta per il processo dei file
@app.route('/process/<filename>')
def process_file(filename):
    input_path = os.path.join('input_folder', filename)
    output_path = os.path.join('output_folder', os.path.splitext(filename)[0])

    # Esegui l'elaborazione del file
    pdf_to_ocr_and_audio(
        input_folder='input_folder',
        output_folder=output_path,
        lang=request.form.get('lang', 'spa'),
        rate=int(request.form.get('rate', 150)),
        volume=float(request.form.get('volume', 1.0)),
        ffmpeg_volume=float(request.form.get('ffmpeg_volume', 1.0))
    )

    # Lista dei file elaborati nella cartella di output
    files = os.listdir(output_path)
    if not files:
        return "Error: No output files generated.", 500
    
    return render_template('download.html', files=files, folder=os.path.splitext(filename)[0])

# 📥 Download Page for a Specific File
@app.route('/download/<folder>')
def download_file_page(folder):
    folder_path = os.path.join('output_folder', folder)
    if not os.path.exists(folder_path):
        return "Folder not found!", 404
    files = os.listdir(folder_path)
    return render_template('download.html', files=files, folder=folder)

# 📂 Download All Files (if needed)
@app.route('/download/all')
def download_all():
    folder_path = 'output_folder'
    if not os.path.exists(folder_path):
        return "No output files found!", 404
    folders = os.listdir(folder_path)
    return render_template('all_downloads.html', folders=folders)

# 📂 Serve File
@app.route('/download/<folder>/<filename>')
def download_file(folder, filename):
    folder_path = os.path.join('output_folder', folder)
    return send_from_directory(folder_path, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
