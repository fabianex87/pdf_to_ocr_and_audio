from pydub import AudioSegment

# Test FFmpeg
audio = AudioSegment.from_file("test_audio.wav")
audio.export("test_audio.aac", format="aac", bitrate="64k")

print("✅ FFmpeg è correttamente configurato!")
