import pyttsx3
from threading import Thread


class Speaker(Thread):
    def __init__(self, text: str):
        self.text = text
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        tts_engine = pyttsx3.init()
        tts_engine.say(self.text)
        tts_engine.runAndWait()
