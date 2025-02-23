import yt_dlp
import tkinter as tk
from tkinter import messagebox
import os
import threading
import webbrowser
import re

def progress_hook(d):
    if d['status'] == 'downloading':
        pass

def download_video(url):
    """ Detecta se a URL é do YouTube ou Twitter e baixa o vídeo corretamente. """
    is_twitter = re.search(r"(x\.com|twitter\.com)", url)
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best' if not is_twitter else 'best',
        'merge_output_format': 'mp4' if not is_twitter else None,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'progress_hooks': [progress_hook]
    }

    if not is_twitter:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
        ydl_opts['postprocessor_args'] = [
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-strict', 'experimental',
        ]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Baixando: {url}")
            ydl.download([url])
            print("Download concluído!")
            loading_label.config(text="✅ Download concluído!", fg=success_color)
            open_folder_button.grid(row=4, column=0, columnspan=2, pady=10)
    except Exception as e:
        print(f"Erro ao baixar o vídeo: {e}")
        loading_label.config(text="❌ Erro no download!", fg=error_color)
    finally:
        download_button.config(state=tk.NORMAL)

def on_download_click():
    url = url_entry.get().strip()
    if url:
        download_button.config(state=tk.DISABLED)
        loading_label.config(text="⏳ Carregando...", fg=loading_color)
        loading_label.grid(row=3, column=0, columnspan=2, pady=10)
        open_folder_button.grid_forget()
        download_thread = threading.Thread(target=download_video, args=(url,))
        download_thread.start()
    else:
        loading_label.config(text="⚠️ Insira uma URL válida!", fg=warning_color)

def on_hover(event):
    download_button.config(bg=hover_color, cursor="hand2")

def on_leave(event):
    download_button.config(bg=button_color)

def on_hover_folder(event):
    open_folder_button.config(bg=folder_hover_color, cursor="hand2")

def on_leave_folder(event):
    open_folder_button.config(bg=highlight_color)

def open_downloads_folder():
    downloads_path = os.path.abspath("downloads")
    webbrowser.open(downloads_path)

if not os.path.exists("downloads"):
    os.makedirs("downloads")

root = tk.Tk()
root.title("Download de Vídeo")
root.geometry("400x280")

bg_color = "#2C3E50"
button_color = "#1ABC9C"
hover_color = "#16A085"
text_color = "#ECF0F1"
highlight_color = "#2980B9"
folder_hover_color = "#1F618D"
input_bg = "#34495E"
loading_color = "#F1C40F"
success_color = "#2ECC71"
error_color = "#E74C3C"
warning_color = "#F39C12"

root.config(bg=bg_color)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

url_label = tk.Label(root, text="Digite a URL do vídeo:", font=("Helvetica", 12), bg=bg_color, fg=text_color)
url_label.grid(row=0, column=0, columnspan=2, pady=10)

url_entry = tk.Entry(root, width=40, font=("Helvetica", 12), bg=input_bg, fg=text_color, insertbackground=text_color)
url_entry.grid(row=1, column=0, columnspan=2, pady=10, padx=20, sticky="ew")

download_button = tk.Button(root, text="Baixar Vídeo", command=on_download_click, font=("Helvetica", 12), bg=button_color, fg=text_color, relief="flat", width=20, height=2)
download_button.grid(row=2, column=0, columnspan=2, pady=10)

download_button.bind("<Enter>", on_hover)
download_button.bind("<Leave>", on_leave)

loading_label = tk.Label(root, text="", font=("Helvetica", 14), fg=loading_color, bg=bg_color)
loading_label.grid(row=3, column=0, columnspan=2, pady=10)

open_folder_button = tk.Button(root, text="📂 Abrir pasta", command=open_downloads_folder, font=("Helvetica", 12), bg=highlight_color, fg=text_color, relief="flat", width=15)
open_folder_button.grid(row=4, column=0, columnspan=2, pady=10)
open_folder_button.grid_forget()

open_folder_button.bind("<Enter>", on_hover_folder)
open_folder_button.bind("<Leave>", on_leave_folder)

root.mainloop()
