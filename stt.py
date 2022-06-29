from tkinter import *
import pyttsx3
from googletrans import Translator
from gtts import *
import playsound
import requests
from threading import *
import os
import speech_recognition as sr
from speech_recognition import UnknownValueError
from PIL import Image, ImageTk

#-------------- Variable Declaration --------------#
application_background_color = '#262339'
frame_background_color = '#262339'
title_label_background_color = '#FC7462'

root = Tk()
root.title('Language Translator')

app_width = 800
app_height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (app_width / 2)
y = ((screen_height / 2) - (app_height / 2)) * 0.65

root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
root.minsize(width=710, height=600)
root.config(bg=application_background_color)
try:
	root.iconbitmap('.ico\\microphone.ico')
except Exception as e:
	print(e)

titleLabel = Label(root, text='Language Translator', font=('Cambria', 20, "bold"), padx=20, pady=20, bg=title_label_background_color, fg="#fff")
titleLabel.pack(pady=(0, 50))

frame1 = LabelFrame(root, text="System", padx=155, pady=10, font="arial 16 bold", bg=frame_background_color, fg="#fff")
frame1.pack()

frame2 = LabelFrame(root, text="Your Speech", padx=155, pady=10, font="arial 16 bold", bg=frame_background_color, fg="#fff")
frame2.pack(pady=10)

frame3 = LabelFrame(root, text="Translated Speech", padx=155, pady=10, font="arial 16 bold", bg=frame_background_color, fg="#fff")
frame3.pack()

count = 0
text_listen = Label(root, text='System Listening Your Speech...', bg=application_background_color, fg='#fff', font="Cambria 16 normal", pady=50)

def on_closing():
	try:
		os.system('wmic process where name="stt.exe" delete')
	except Exception as e:
		print(e)
	root.destroy()

def on_enter(e):
	e.widget['cursor'] = 'hand2'

def on_leave(e):
	e.widget['cursor'] = 'hand2'

def system_speech(system_text):
	text = system_text
	Message(frame1, text=text, bg=application_background_color, fg="#fff", width=400, justify='center').pack(fill=BOTH)

def user_speech(user_text):
	text = user_text
	Message(frame2, text=text, bg=application_background_color, fg="#fff", width=400, justify='center').pack(fill=BOTH)

def translated_speech(translated_text):
	text = translated_text
	Message(frame3, text=text, bg=application_background_color, fg="#fff", width=400, justify='center').pack(fill=BOTH)

def clear_frame():
	for widget in frame1.winfo_children():
		widget.destroy()
	for widget in frame2.winfo_children():
		widget.destroy()
	for widget in frame3.winfo_children():
		widget.destroy()
	frame1.pack_forget()
	frame2.pack_forget()
	frame3.pack_forget()

def threading_speech():
	thread_contiue = Thread(target=speech_translate)
	thread_contiue.start()

def clicked():
	global count
	count = count + 1
	if count > 1:
		clear_frame()

def speak(audio):
	engine = pyttsx3.init('sapi5')
	rate = engine.getProperty('rate')
	engine.setProperty('rate', rate-29)

	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[0].id)
	print('System: ' + audio)
	engine.say(audio)
	engine.runAndWait()

def speech_translate():
	clicked()
	r = sr.Recognizer()
	br = sr.Recognizer()
	er = sr.Recognizer()

	info_label.config(text='Application is running')
	trans_btn.config(state='disabled')

	try:
		requests.get("https://www.google.com", timeout=5)
		try:
			requests.get("https://translate.google.com/", timeout=5)
			with sr.Microphone() as source:
				try:
					r.adjust_for_ambient_noise(source, duration=0.5)
					speak("Please select a language for translation! For selection say Bangla or English.")
					print('Listening...')
					text_listen.pack()
					audio = r.listen(source, phrase_time_limit=5)
					try:
						text_listen.pack_forget()
						if 'bangla' in r.recognize_google(audio) or 'Bangla' in r.recognize_google(audio):
							br = sr.Recognizer()
							with sr.Microphone() as source:
								br.adjust_for_ambient_noise(source, duration=3)
								speak("Your speech will be translated in English language. Say now.")
								text_listen.pack()
								print('Listening...')
								audio = br.listen(source)
								try:
									text_listen.pack_forget()
									text = br.recognize_google(audio, language='bn-BD')
									if count > 1:
										frame2.pack()
									user_speech("You said : {}".format(text))
									bangla_text = "You said : {}".format(text)
									tts = gTTS(bangla_text, lang='bn')
									tts.save('speak.mp3')
									playsound.playsound('speak.mp3', True)
									os.remove('speak.mp3')
									destination_languages = {
										'English': 'en'
									}

									translator = Translator()

									for key, value in destination_languages.items():
										if count > 1:
											frame3.pack()
										translated_speech("Translated Speech: " + translator.translate(text, dest=value).text)
										speak("Translated Speech: " + translator.translate(text, dest=value).text)
								except gTTSError:
									text_listen.pack_forget()
									if count > 1:
										frame1.pack()
									system_speech("Failed to connect to the server.")
									speak("Failed to connect to the server.")
								except:
									text_listen.pack_forget()
									if count > 1:
										frame1.pack()
									system_speech("Sorry could not recognize what you said. Try again.")
									speak("Sorry could not recognize what you said. Try again.")
						elif 'english' in er.recognize_google(audio) or 'English' in er.recognize_google(audio):
							er = sr.Recognizer()
							with sr.Microphone() as source:
								er.adjust_for_ambient_noise(source, duration=3)
								speak("Your speech will be translated in Bangla language. Say now.")
								print('Listening...')
								text_listen.pack()
								audio = er.listen(source)
								try:
									text_listen.pack_forget()
									text = er.recognize_google(audio, language='en')
									if count > 1:
										frame2.pack()
									user_speech("You said : {}".format(text))
									destination_languages = {
										'Bangla': 'bn'
									}

									translator = Translator()

									for key, value in destination_languages.items():
										if count > 1:
											frame3.pack()
										translated_speech("Translated Speech: " + translator.translate(text, dest=value).text)
										bangla_text = "Translated Speech: " + translator.translate(text, dest=value).text
										tts = gTTS(bangla_text, lang='bn')
										tts.save('speak.mp3')
										playsound.playsound('speak.mp3', True)
										os.remove('speak.mp3')
								except gTTSError:
									text_listen.pack_forget()
									if count > 1:
										frame1.pack()
									system_speech("Failed to connect to the server.")
									speak("Failed to connect to the server.")
								except:
									text_listen.pack_forget()
									if count > 1:
										frame1.pack()
									system_speech("Sorry could not recognize what you said. Try again.")
									speak("Sorry could not recognize what you said. Try again.")
						else:
							text_listen.pack_forget()
							if count > 1:
								frame1.pack()
							system_speech('Language is not registered yet. Development is in progress.')
							speak('Language is not registered yet. Development is in progress.')
					except UnknownValueError:
						text_listen.pack_forget()
						if count > 1:
							frame1.pack()
						system_speech('Sorry! Recognization Failed. Try again.')
						speak("Sorry! Recognization Failed. Try again.")
				except sr.RequestError:
					text_listen.pack_forget()
					if count > 1:
						frame1.pack()
					system_speech('You are not connected to the internet.\nThe program requires an active internet connection.')
					speak('You are not connected to the internet. The program requires an active internet connection.')
		except (requests.ConnectionError, requests.Timeout):
			text_listen.pack_forget()
			if count > 1:
				frame1.pack()
			system_speech('Server Connection Failed. Use VPN to connect the server.')
			speak('Server Connection Failed. Use VPN to connect the server.')
	except (requests.ConnectionError, requests.Timeout):
		text_listen.pack_forget()
		if count > 1:
			frame1.pack()
		system_speech('You are not connected to the internet.\nThe program requires an active internet connection.')
		speak('You are not connected to the internet. The program requires an active internet connection.')
	info_label.config(text='Press on icon to start the application')
	trans_btn.config(state='normal')

try:
	img_file = Image.open(".ico\\mc.png")
except:
	img_file = Image.open("mc.png")
img_file = img_file.resize((50, 50) )
img_con = ImageTk.PhotoImage(img_file )

image_label = Label(image=img_con)
info_label = Label(root, text='Press on icon to start the application', font='arial 10 italic', bg=application_background_color, fg='white')
info_label.pack(pady=(0, 100), side=BOTTOM)

trans_btn = Button(root, image=img_con, bg=application_background_color, borderwidth=0, pady=5, activebackground= application_background_color, command=threading_speech)
trans_btn.pack(pady=(0, 10), side=BOTTOM)

trans_btn.bind("<Enter>", on_enter)
trans_btn.bind("<Leave>", on_leave)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()