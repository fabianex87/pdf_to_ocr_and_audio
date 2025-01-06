import pyttsx3

# Inizializza il motore TTS
engine = pyttsx3.init()

# Elenco delle voci
voices = engine.getProperty('voices')

# Mostra le voci disponibili
for voice in voices:
    print(f"ID: {voice.id}")
    print(f"Nome: {voice.name}")
    print(f"Lingua: {voice.languages if hasattr(voice, 'languages') else 'Non disponibile'}\n")
