import os
import sys
import tkinter as tk
from tkinter import messagebox

# Latin to Cyrillic and Cyrillic to Latin mappings for Serbian
latin_to_cyrillic = {
    "nj": "њ", "dž": "џ", "lj": "љ",
    "a": "а", "b": "б", "v": "в", "g": "г", "d": "д", "đ": "ђ", "e": "е",
    "ž": "ж", "z": "з", "i": "и", "j": "ј", "k": "к", "l": "л", "m": "м",
    "n": "н", "o": "о", "p": "п", "r": "р", "s": "с", "t": "т", "ć": "ћ",
    "u": "у", "f": "ф", "h": "х", "c": "ц", "č": "ч", "š": "ш"
}

# Add uppercase versions
latin_to_cyrillic.update({k.upper(): v.upper() for k, v in latin_to_cyrillic.items()})
# Preserve digraphs like Nj, Dž, Lj
latin_to_cyrillic.update({"Nj": "Њ", "Dž": "Џ", "Lj": "Љ"})

# Cyrillic to Latin mapping (reverse)
cyrillic_to_latin = {v: k for k, v in latin_to_cyrillic.items()}

# Sort digraphs first to avoid partial replacements
digraphs = ["dž", "lj", "nj", "Dž", "Lj", "Nj"]


def latin_to_cyr(text):
    result = ""
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i:i+2] in latin_to_cyrillic:
            result += latin_to_cyrillic[text[i:i+2]]
            i += 2
        else:
            result += latin_to_cyrillic.get(text[i], text[i])
            i += 1
    return result


def cyr_to_latin(text):
    result = ""
    for ch in text:
        result += cyrillic_to_latin.get(ch, ch)
    return result


# For disabling events
def disable_typing(event):
    return "break"


# Get absolute path to resource (for PyInstaller and development)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# GUI
def create_gui():
    # First option
    # window = tk.Tk()
    # window.title("Serbian Latin ↔ Cyrillic Translator")
    # window.geometry("600x400")
    # window.resizable(False, False)

    # Second option
    window = tk.Tk()
    window.title("LATCRY Serbian Latin ↔ Cyrillic Translator")
    # Set window icon
    icon_path = resource_path("icon.ico")
    window.iconbitmap(icon_path)
    # Center the window
    window_width = 600
    window_height = 400
    # Not full working
    # screen_width = window.winfo_screenwidth()
    # screen_height = window.winfo_screenheight()
    # x = int((screen_width / 2) - (window_width / 2))
    # y = int((screen_height / 2) - (window_height / 2))
    # window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    window.geometry(f"{window_width}x{window_height}")
    window.resizable(False, False)

    # Input Text
    tk.Label(window, text="Input Text:", font=("Arial", 12)).pack(pady=15)
    # input_text = tk.Text(window, height=6, width=70)
    # input_text.pack()

    # With Frame
    input_frame = tk.Frame(window)
    input_frame.pack()
    input_text = tk.Text(input_frame, height=6, width=70, wrap="word")
    input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    input_scrollbar = tk.Scrollbar(input_frame, command=input_text.yview)
    input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    input_text.config(yscrollcommand=input_scrollbar.set)


    # Output Text
    tk.Label(window, text="Translated Text:", font=("Arial", 12)).pack(pady=15)
    # output_text = tk.Text(window, wrap="word",height=6, width=70) # wrap
    # output_text.pack()

    # Frame for Output Text and Scrollbar
    output_frame = tk.Frame(window)
    output_frame.pack()
    output_text = tk.Text(output_frame, height=6, width=70, wrap="word")
    output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    output_scrollbar = tk.Scrollbar(output_frame, command=output_text.yview)
    output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    output_text.config(yscrollcommand=output_scrollbar.set)

    # Prevent key presses and mouse pastes
    output_text.bind("<Key>", disable_typing)
    output_text.bind("<<Paste>>", disable_typing)
    output_text.bind("<Control-v>", disable_typing)
    output_text.bind("<Command-v>", disable_typing)
    output_text.bind("<Button-3>", disable_typing)

    # Translate Functions
    def translate_to_cyr():
        input_str = input_text.get("1.0", tk.END).strip()
        if not input_str:
            messagebox.showwarning("Warning", "Please enter text.")
            return
        output_str = latin_to_cyr(input_str)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, output_str)

    def translate_to_latin():
        input_str = input_text.get("1.0", tk.END).strip()
        if not input_str:
            messagebox.showwarning("Warning", "Please enter text.")
            return
        output_str = cyr_to_latin(input_str)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, output_str)

    def clear_texts():
        input_text.delete("1.0", tk.END)
        output_text.delete("1.0", tk.END)

    # Buttons
    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Latin → Cyrillic", width=20, command=translate_to_cyr).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Cyrillic → Latin", width=20, command=translate_to_latin).grid(row=0, column=1, padx=10)
    tk.Button(btn_frame, text="Clear", width=10, command=clear_texts).grid(row=0, column=2, padx=10)

    window.mainloop()


if __name__ == "__main__":
    create_gui()
