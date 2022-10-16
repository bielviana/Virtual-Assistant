import speech_recognition as sr
import playsound
import pyttsx3
from gtts import gTTS
import random
import os

class VirtualAssist():
    def __init__(self, assist_name, person):
        self.assist_name = assist_name
        self.person = person

        self.r = sr.Recognizer()
        self.engine = pyttsx3.init()

        self.voice_data = ''

    def engine_speak(self, text):
        # Fala da assistente virtual
        text = str(text)

        self.engine.say(text)
        self.engine.runAndWait()

    def recordAudio(self, ask=''):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)

            if ask:
                print(ask)
                # self.engineSpeak(ask)
            
            audio = self.r.listen(source, 5, 5)

            try:
                self.voice_data = self.r.recognize_google(audio)
            except sr.UnknownValueError:
                print('{}: Não consegui te ouvir, {}, pode repetir por favor?'.format(self.assist_name.capitalize(), self.person.capitalize()))
            except sr.RequestError:
                self.engineSpeak('Desculpe chefe! Tive um erro de conexão.')
            
            print('>> {}'.format(self.voice_data.lower()))
            self.voice_data = self.voice_data.lower()

        return self.voice_data.lower()

    def engineSpeak(self, audio_string):
        audio_string = str(audio_string)
        tts = gTTS(text=audio_string, lang='pt-br')
        r = random.randint(1, 20000)
        audio_file = 'audio{}.mp3'.format(str(r))
        tts.save(audio_file)
        playsound.playsound(audio_file)
        print('{}: {}'.format(self.assist_name, audio_string))
        os.remove(audio_file)
    
    def termExist(self, terms):
        for term in terms:
            if term in self.voice_data:
                return True

    def respond(self, voice_data):
        #if self.assist_name in voice_data:
        if self.termExist(['hey', 'oi', 'olá', 'ola']):
            response = [
                f'Olá {self.person}! Em que posso ajudar?',
                'Oi chefe! Precisa de alguma coisa?',
            ]
            resp = response[random.randint(0, len(response)-1)]
            self.engineSpeak(resp)

        if self.termExist(['qual seu nome?']):
            self.engineSpeak(f'Meu nome é {self.assist_name}')

        # Google
        if self.termExist(['procurar por']):
            pass

assistent = VirtualAssist('siri', 'gabriel')

while True:
    voice_data = assistent.recordAudio('Ouvindo...')
    assistent.respond(voice_data)

    if assistent.termExist(['tchau', 'bye']):
        assistent.engineSpeak('Até logo chefe!')
        break
