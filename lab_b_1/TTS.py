import os
import threading
import queue
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from gtts import gTTS
from playsound import playsound

class HebrewTTSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("המרת טקסט לדיבור - עברית")
        self.root.geometry("800x550")
        self.root.configure(bg="#f0f4f7")
        self.root.resizable(False, False)
        self.dark_mode = False
        self.msg_queue = queue.Queue()
        self.setup_ui()
        self.root.after(100, self.process_queue)

    def setup_ui(self):
        self.style = ttk.Style()
        self.set_theme()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=BOTH, expand=True)

        top_frame = Frame(frame, bg=self.bg_color())
        top_frame.pack(fill=X)

        self.label = ttk.Label(top_frame, text="הכנס טקסט או טען קובץ:")
        self.label.pack(pady=10, anchor=W)

        self.theme_btn = ttk.Button(top_frame, text="🌜 מצב ערכה / בהיר", command=self.toggle_theme)
        self.theme_btn.pack(pady=10, anchor=E)

        self.text_input = Text(frame, wrap=WORD, height=12, font=("Segoe UI", 12), bg="white", fg="black")
        self.text_input.pack(fill=BOTH, expand=True, padx=10, pady=5)

        btn_frame = Frame(frame, bg=self.bg_color())
        btn_frame.pack(pady=10)

        self.load_btn = ttk.Button(btn_frame, text="📂 טען קובץ", command=self.load_file)
        self.load_btn.grid(row=0, column=0, padx=10)

        self.speak_btn = ttk.Button(btn_frame, text="🔊 המר והשמע", command=self.start_speaking)
        self.speak_btn.grid(row=0, column=1, padx=10)

        self.save_btn = ttk.Button(btn_frame, text="🔗 שמור MP3", command=self.save_audio)
        self.save_btn.grid(row=0, column=2, padx=10)

        self.status_label = Label(frame, text="", bg=self.bg_color(), fg="green", font=("Segoe UI", 11))
        self.status_label.pack(pady=5)

        self.playback_bar = ttk.Progressbar(frame, orient=HORIZONTAL, length=400, mode='indeterminate')
        self.playback_bar.pack(pady=10)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.set_theme()

    def set_theme(self):
        bg = self.bg_color()
        fg = self.fg_color()
        self.root.configure(bg=bg)
        self.style.theme_use('clam')
        self.style.configure("TButton", font=("Segoe UI", 12), padding=6)
        self.style.configure("TLabel", font=("Segoe UI", 14), background=bg, foreground=fg)
        self.style.configure("TFrame", background=bg)
        self.style.configure("TProgressbar", troughcolor=bg, background="#2196F3")

    def bg_color(self):
        return "#2e2e2e" if self.dark_mode else "#f0f4f7"

    def fg_color(self):
        return "white" if self.dark_mode else "black"

    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if filepath:
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_input.delete("1.0", END)
                    self.text_input.insert(END, content)
                    self.status_label.config(text="קובץ נטען בהצלחה", fg="green")
            except Exception as e:
                messagebox.showerror("שגיאה", f"שגיאה בטעינת קובץ:\n{e}")

    def start_speaking(self):
        text = self.text_input.get("1.0", "end").strip()
        text = text.replace("\n\n", ". ").replace("\n", " ")

        if not text:
            messagebox.showwarning("שגיאה", "אנא הזן טקסט.")
            return
        threading.Thread(target=self.speak_worker, args=(text,), daemon=True).start()

    def speak_worker(self, text):
        try:
            self.msg_queue.put(("status", "ממיר טקסט...") )
            tts = gTTS(text=text, lang='iw')
            tts.save("temp_output.mp3")
            self.msg_queue.put(("play",))
            self.msg_queue.put(("status", "האזנה הסתיימה."))
        except Exception as e:
            self.msg_queue.put(("error", f"שגיאה בהמרה:\n{e}"))

    def process_queue(self):
        try:
            while True:
                msg = self.msg_queue.get_nowait()
                if msg[0] == "status":
                    self.status_label.config(text=msg[1], fg="blue")
                elif msg[0] == "error":
                    messagebox.showerror("שגיאה", msg[1])
                    self.status_label.config(text="שגיאה", fg="red")
                elif msg[0] == "play":
                    self.playback_bar.start(10)
                    playsound("temp_output.mp3")
                    self.playback_bar.stop()
        except queue.Empty:
            pass
        self.root.after(100, self.process_queue)

    def save_audio(self):
        text = self.text_input.get("1.0", "end").strip()
        text = text.replace("\n\n", ". ").replace("\n", " ")
        if not text:
            messagebox.showwarning("שגיאה", "אנא הזן טקסט.")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if save_path:
            try:
                tts = gTTS(text=text, lang='iw')
                tts.save(save_path)
                self.status_label.config(text=f"שמור נשמר ב־{save_path}", fg="green")
            except Exception as e:
                messagebox.showerror("שגיאה", f"שגיאה בשימור:\n{e}")

if __name__ == "__main__":
    root = Tk()
    app = HebrewTTSApp(root)
    root.mainloop()
