import tkinter as tk
from tkinter import filedialog, messagebox
import speech_recognition as sr
import threading
from deep_translator import GoogleTranslator   # ✅ FIXED

def new_file():
    text.delete(1.0, tk.END)

def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text Files","*.txt")])
    if file_path:
        with open(file_path, 'r', encoding="utf-8") as file:
            text.delete(1.0, tk.END)
            text.insert(tk.END, file.read())

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",  # ✅ FIXED
                                             filetypes=[("Text Files","*.txt")])
    if file_path:
        with open(file_path, 'w', encoding="utf-8") as file:
            file.write(text.get(1.0, tk.END))
            messagebox.showinfo("Info", "File saved successfully!")

def cut():
    text.event_generate("<<Cut>>")

def copy():
    text.event_generate("<<Copy>>")

def paste():
    text.event_generate("<<Paste>>")  # ✅ FIXED

recognizer = sr.Recognizer()
mic = sr.Microphone()
listening = False
input_language = "en-IN"
output_language = "en"

def voice_typing():
    global listening
    listening = True

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        text.insert(tk.END, f"Voice typing started... (Input: {input_language}, Output: {output_language})\n")

    while listening:
        try:
            with mic as source:
                audio = recognizer.listen(source)
                result = recognizer.recognize_google(audio, language=input_language)

            if output_language:
                translated = GoogleTranslator(source='auto', target=output_language).translate(result)  # ✅ FIXED
                display_text = f"{result} → {translated}"
            else:
                display_text = result

            text.insert(tk.END, display_text + "\n")
            text.see(tk.END)

        except sr.UnknownValueError:
            text.insert(tk.END, "[Speech not recognized]\n")
        except sr.RequestError:
            text.insert(tk.END, "[API Error]\n")

def start_voice_typing():
    threading.Thread(target=voice_typing, daemon=True).start()

def stop_voice_typing():
    global listening
    listening = False
    text.insert(tk.END, "\nVoice typing stopped.\n")  # ✅ FIXED

# --- Language selection ---
def set_input_language(lang_code):
    global input_language
    input_language = lang_code
    text.insert(tk.END, f"\n[Input Language changed to {lang_code}]\n")

def set_output_language(lang_code):
    global output_language
    output_language = lang_code
    text.insert(tk.END, f"\n[Output Language changed to {lang_code}]\n")

# GUI
root = tk.Tk()
root.title("Voice Text Editor")
root.geometry("900x650")

text = tk.Text(root, wrap=tk.WORD, font=("Helvetica", 12), fg="black")
text.pack(expand=tk.YES, fill=tk.BOTH)

menu = tk.Menu(root)

# File Menu
file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu.add_cascade(label="File", menu=file_menu)

# Edit Menu
edit_menu = tk.Menu(menu, tearoff=0)
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)
menu.add_cascade(label="Edit", menu=edit_menu)

# Voice Menu
voice_menu = tk.Menu(menu, tearoff=0)
voice_menu.add_command(label="Start Voice Typing", command=start_voice_typing)
voice_menu.add_command(label="Stop Voice Typing", command=stop_voice_typing)
menu.add_cascade(label="Voice", menu=voice_menu)

# Input Language Menu
input_lang_menu = tk.Menu(menu, tearoff=0)
input_lang_menu.add_command(label="English", command=lambda: set_input_language("en-IN"))
input_lang_menu.add_command(label="Hindi", command=lambda: set_input_language("hi-IN"))
input_lang_menu.add_command(label="French", command=lambda: set_input_language("fr-FR"))
input_lang_menu.add_command(label="Spanish", command=lambda: set_input_language("es-ES"))
menu.add_cascade(label="Input Language", menu=input_lang_menu)

# Output Language Menu
output_lang_menu = tk.Menu(menu, tearoff=0)
output_lang_menu.add_command(label="English", command=lambda: set_output_language("en"))
output_lang_menu.add_command(label="Hindi", command=lambda: set_output_language("hi"))
output_lang_menu.add_command(label="French", command=lambda: set_output_language("fr"))
output_lang_menu.add_command(label="Spanish", command=lambda: set_output_language("es"))
menu.add_cascade(label="Output Language", menu=output_lang_menu)

root.config(menu=menu)
root.mainloop()