from gtts import gTTS
from google.cloud import texttospeech
from tempfile import TemporaryDirectory
from playsound import playsound
from threading import Thread

from data.context import context


class Speaker(Thread):
    def __init__(self, text: str, emphasis: bool = False):
        self.text = _string_cleanup(text)
        self.emphasis = emphasis
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        if len(self.text) == 0:
            return
        d = TemporaryDirectory()
        f = d.name + '\\au.mp3'
        try:
            if context.use_gcp:
                self.gcp_run(f)
            else:
                self.gtts_run(f)
            playsound(f)
        finally:
            d.cleanup()

    def gcp_run(self, f: str):
        client = texttospeech.TextToSpeechClient()
        if self.emphasis:
            self.text = '<prosody volume="x-loud" range="10st" pitch="+2st">' + self.text + "</prosody>"
        else:
            self.text = '<prosody pitch="-2st">' + self.text + "</prosody>"
        self.text = f'<speak>{self.text}</speak>'
        synthesis_input = texttospeech.SynthesisInput({'ssml': self.text})
        voice = texttospeech.VoiceSelectionParams(
            {'language_code': "en-US", 'ssml_gender': texttospeech.SsmlVoiceGender.MALE}
        )
        audio_config = texttospeech.AudioConfig(
            {'audio_encoding': texttospeech.AudioEncoding.MP3}
        )
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        with open(f, "wb") as out:
            out.write(response.audio_content)

    def gtts_run(self, f: str):
        tts = gTTS(self.text)
        tts.save(f)


def _string_cleanup(text: str) -> str:
    text = text \
        .replace('sus', 'suss') \
        .replace('caf', 'caff')
    return text
