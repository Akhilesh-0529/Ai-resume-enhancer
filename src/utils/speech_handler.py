import os
from gtts import gTTS
import speech_recognition as sr
import tempfile

class SpeechHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def text_to_speech(self, text, lang='en'):
        try:
            tts = gTTS(text=text, lang=lang)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                tts.save(fp.name)
                return fp.name
        except Exception as e:
            raise Exception(f"Error in text to speech conversion: {str(e)}")

    def speech_to_text(self, audio_file):
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                return text
        except Exception as e:
            raise Exception(f"Error in speech to text conversion: {str(e)}")

    def cleanup_audio_file(self, file_path):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up audio file: {str(e)}")