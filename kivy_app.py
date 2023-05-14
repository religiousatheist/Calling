#!/usr/bin/env python
# coding: utf-8

# In[2]:


from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
import openai
import pyttsx3
from gtts import gTTS
import speech_recognition as sr
import pygame
import os



class ChatBot(App):
    def build(self):
        self.window=GridLayout()
        self.window.cols=1
        self.window.size_hint=(0.6,0.7)
        self.window.pos_hint={'center_x':0.5,'center_y':0.5}
        self.window.add_widget(Image(source=('App_logo.png')))
        
        self.button= Button(text='Press to Talk',size_hint=(0.3,0.3),bold=True,
                            font_size=30)
        self.button.bind(on_press=self.getCode)
        self.window.add_widget(self.button)

        self.button2= Button(text='Quit',size_hint=(0.2,0.2),bold=True,
                            font_size=30)
        self.button2.bind(on_press=self.Close_app)
        self.window.add_widget(self.button2)
        
        return self.window

    def Close_app(self):
        App.get_running_app().stop()
        Window.close()
    
    def getCode(self,instance):

        
        openai.api_key='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'
        
        
        r=sr.Recognizer()
        engine=pyttsx3.init()
        engine.setProperty('rate',135)
        engine.setProperty('volume',1)

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            engine.say('Say something')
            engine.runAndWait()
            
            while True:
                audio= r.listen(source)
                try:
                    text=r.recognize_google(audio)
                    
                    response=openai.ChatCompletion.create(model='gpt-3.5-turbo',messages=[{'role':'system','content':'You are AI assistant named Hemi'},
                              {'role':'user','content':text}],temperature=0.8,max_tokens=500)
                    my_obj=gTTS(text=response['choices'][0]['message']['content'])
                    my_obj.save('speech.mp3')
                    pygame.mixer.init()
                    sound=pygame.mixer.Sound('speech.mp3')
                    sound.play()
                    pygame.time.wait(int(sound.get_length()*1000))
                    pygame.mixer.quit()
                    
                except sr.UnknownValueError:
                    text='Can not understand'
                    engine.say(text)
                    engine.runAndWait()
                except sr.RequestError as e:
                    print(f'the error is {e}')
if __name__=='__main__':
    ChatBot().run()


# In[ ]:




