import tkinter as tk
import speech_recognition as sr
from difflib import SequenceMatcher
from gtts import gTTS
import os
import pyttsx3

def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        output_text.delete('1.0', tk.END)
        output_text.insert(tk.END, text)
    except sr.UnknownValueError:
        output_text.delete('1.0', tk.END)
        output_text.insert(tk.END, "Could not understand audio")
    except sr.RequestError:
        output_text.delete('1.0', tk.END)
        output_text.insert(tk.END, "Could not request results; check your internet connection")

def text_to_audio():
    text_to_speak = input_entry.get().strip()
    tts = gTTS(text=text_to_speak, lang='en')
    tts.save("output.mp3")
    os.system("start output.mp3")  # Mở file audio để phát

def speak_text():
    text_to_speak = input_entry.get().strip()
    if text_to_speak:
        engine = pyttsx3.init()

        # Thay đổi tốc độ đọc (mặc định là 200)
        engine.setProperty('rate', 100)  # Tốc độ: 150 words per minute

        # Thay đổi giọng đọc (mặc định là 'en')
        engine.setProperty('voice', 'english+f3')  # Giọng Anh - Anh (Nữ)

        engine.say(text_to_speak)
        engine.runAndWait()
    else:
        print("No text to speak")

def compare_text():
    input_text = input_entry.get().lower().split()
    recorded_text = output_text.get('1.0', tk.END).lower().split()

    compared_text.delete('1.0', tk.END)

    common_words = []
    unique_to_input = []
    unique_to_recorded = []

    for word in input_text:
        if word in recorded_text and word not in common_words:
            common_words.append(word)
        elif word not in unique_to_input:
            unique_to_input.append(word)

    for word in recorded_text:
        if word not in common_words and word not in unique_to_recorded:
            unique_to_recorded.append(word)

    for word in input_text:
        if word in common_words:
            compared_text.insert(tk.END, word, 'common ')
            compared_text.insert(tk.END, ' ')
        elif word in unique_to_input:
            compared_text.insert(tk.END, word, 'unique_input ')
            compared_text.insert(tk.END, ' ')

    compared_text.tag_config('common', foreground='green')
    compared_text.tag_config('unique_input', foreground='red')


def reset():
    input_entry.delete(0, tk.END)
    output_text.delete('1.0', tk.END)
    compared_text.delete('1.0', tk.END)
    # Xóa file ghi âm cũ ở đây (để được thực hiện)
    if os.path.exists("output.mp3"):
        os.remove("output.mp3")
    if os.path.exists("output_speak.mp3"):
        os.remove("output_speak.mp3")

root = tk.Tk()
root.title("Pronunciation Checker")

input_label = tk.Label(root, text="Enter text:")
input_label.grid(row=0, column=0)

input_entry = tk.Entry(root, width=100)
input_entry.grid(row=0, column=1)

speak_button = tk.Button(root, text="Speak", command=speak_text)
speak_button.grid(row=0, column=2)

output_text = tk.Text(root, height=5, width=50)
output_text.grid(row=1, column=0, columnspan=3)

record_button = tk.Button(root, text="Record", command=record_audio)
record_button.grid(row=2, column=0)

compare_button = tk.Button(root, text="Compare", command=compare_text)
compare_button.grid(row=2, column=1)

compared_text = tk.Text(root, height=5, width=50)
compared_text.grid(row=3, column=0, columnspan=3)

reset_button = tk.Button(root, text="Reset", command=reset)
reset_button.grid(row=4, column=0, columnspan=3)

root.mainloop()


