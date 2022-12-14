import os
import random
import webbrowser
from re import search
from unittest.case import _AssertRaisesContext

import playsound
import pyttsx3
import speech_recognition as sr
from gtts import gTTS


# criação da classe
class Virtual_assit():

    def __init__(self, assist_name, person):  # metodo construtor
        self.person = person  # pessoa que estara utilizando o sistema
        self.assist_name = assist_name  # Nome da assistente virtual

        self.engine = pyttsx3.init()  # identificação do audio
        self.r = sr.Recognizer()  # Reconhecimento da voz

        self.voice_data = ''  # vai armazenar o texto do nosso audio

    def voz_assist(self, text):
        """Fala da assistente virtual"""
        text = str(text)
        self.engine.say(text)  # vai fazer o play do audio
        self.engine.runAndWait()  # exculta e aguarda um tempo

    def record_audio(self, frase=""):

        with sr.Microphone() as source:  # utilizando o microfone microfone
            if frase:
                print("Gravando...")  # informando que esta gravando
                self.voz_assist(frase)  # dizendo que esta ouvindo

            audio = self.r.listen(source, 5, 5)
            print("olhando o banco de dados")

            try:
                self.voice_data = self.r.recognize_google(
                    audio, language='pt-BR')  # Reconhecendo a frase em portugues
            except sr.UnknownValueError:
                # tratamento para quando não entender o que foi falado pesso para repetir
                self.voz_assist(
                    f"Olá {self.person} , Não consegui entender o que você disse por favor repita? ")
            except sr.RequestError:
                # Tratamento para caso não consiga acessar a internet
                self.voz_assist("Olá servidor indisponivel")

            print(">>", self.voice_data.lower())
            self.voice_data = self.voice_data.lower()  # deixar tudo minusculo

            return self.voice_data.lower()

    def voz_assist(self, audio_strig):
        # convertendo para string caso não venha
        audio_strig = str(audio_strig)
        # alteração do idioma do assistente virtual
        tts = gTTS(text=audio_strig,  lang='pt-BR')
        # aqui serve para ele ir gravando o mp3 para não se repetir
        r = random.randint(1, 20000)
        audio_file = 'audio' + str(r) + '.mp3'  # aqui onde salvo o arquivo
        tts.save(audio_file)
        playsound.playsound(audio_file)  # aqui vai execultar o arquivo mp3
        print(self.assist_name + ':', audio_strig)
        # apos a fala ele vai remover o aquivo para não encher a pasta
        os.remove(audio_file)

    def existe(self, terms):
        """Função para identificar se o termo existe"""
        for term in terms:
            if term in self.voice_data:
                return True

    def resposta_assist(self, voice_data):
        # checagem para verificar se esta na nossa lista
        if self.existe(['Olá', 'oi', 'ola', 'vamos começar']):
            # Lista de saudação cadastrada
            greetings = [f'Oi {self.person} em que posso ajudar hoje?',
                         'Oi o que deseja fazer?',
                         'Oi vamos trabalhar?']

            greet = greetings[random.randint(0, len(greetings) - 1)]
            self.voz_assist(greet)

        # aqui que colocamos a função para abrir programa ou outras coisas
        # google
        if self.existe(['procurar por ']) and 'youtube' not in voice_data:
            search_term = voice_data.split("por")[-1]
            url = 'http://google.com/search?q=' + search_term
            webbrowser.get().open(url)
            self.voz_assist('aqui está o que eu encontrei para' +
                            search_term + 'no google')
        # youtube
        if self.existe(['abrir youtube']):
            search_term = voice_data.split("por")[-1]
            url = 'http://www.youtube.com/results?search_query=' + search_term
            webbrowser.get().open(url)
            self.voz_assist('abrindo' +
                            search_term + 'no youtube')


assistent = Virtual_assit('Lucia', 'Jonathan')

while True:

    voice_data = assistent.record_audio('ouvindo...')
    assistent.resposta_assist(voice_data)

    if assistent.existe(['até logo', 'tchau', 'fui', 'ate mais']):
        assistent.voz_assist("Até logo tenha um otimo dia!")
        break
