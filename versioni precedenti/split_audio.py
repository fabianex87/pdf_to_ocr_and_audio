from pydub import AudioSegment
import os
import math

# ✅ **Configurazione Generale**
FILE_INPUT = "audiolibro.aac"
MAX_MB = 16  # Dimensione massima per ogni parte in MB


# ✅ **Funzione di Divisione**
def split_audio_into_parts(input_file, max_mb):
    try:
        # Controlla se il file esiste
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"❌ Il file '{input_file}' non esiste.")

        # Calcola la dimensione totale del file
        file_size = os.path.getsize(input_file) / (1024 * 1024)  # Dimensione in MB
        
        # Calcola il numero di parti
        num_parts = math.ceil(file_size / max_mb)
        print(f"🔄 Divisione del file in {num_parts} parti da massimo {max_mb} MB ciascuna.")
        
        # Ottieni la durata totale usando pydub
        audio = AudioSegment.from_file(input_file)
        total_duration = len(audio) / 1000  # Durata in secondi
        
        # Calcola la durata massima di ciascuna parte
        avg_bitrate_kbps = 64  # Bitrate specificato in kbps
        max_bytes = max_mb * 1024 * 1024  # Dimensione massima in byte
        max_duration_per_part = (max_bytes * 8) / (avg_bitrate_kbps * 1000)  # Durata in secondi
        
        print(f"🔢 Durata massima per parte: {int(max_duration_per_part)} secondi.")
        
        start_time = 0
        part_counter = 1
        
        while start_time < total_duration:
            end_time = min(start_time + max_duration_per_part, total_duration)
            output_part = f"{os.path.splitext(input_file)[0]}_part{part_counter}.aac"
            
            # Estrai la parte audio
            audio_part = audio[start_time * 1000:end_time * 1000]
            audio_part.export(output_part, format='aac', bitrate='64k')
            
            print(f"✅ Parte {part_counter} salvata come {output_part} ({int(end_time - start_time)} secondi).")
            
            start_time = end_time
            part_counter += 1
        
        print("🎉 Divisione completata con successo!")
    
    except Exception as e:
        print(f"❌ Errore nella divisione del file: {e}")


# ✅ **Esegui la Divisione**
if __name__ == "__main__":
    split_audio_into_parts(FILE_INPUT, MAX_MB)
