from pytube import YouTube
import os
from tkinter import *

def call_music_download(e):
    music_download()

def music_download():

    link_music = str(link.get())

    if link_music == "Sair" or link_music == "sair" or link_music == "SAIR" or link_music == "exit" or link_music == "Exit" or link_music == "EXIT":
        window.destroy()

    else:
        try:
            youtube_var = YouTube(link_music)
            
            out_path = youtube_var.streams.filter(only_audio=True, file_extension='mp4').first().download()
            new_path = os.path.splitext(out_path)
            os.rename(out_path, new_path[0]+'.mp3')
            
            text_end["text"] = "Música: '" + youtube_var.title + "' baixada"
            text_end.config(bg='green')

            link.delete(0, END)

        except:
            if link_music == "":
                text_end["text"] = "Insira uma URL válida"
                text_end.config(bg='#691212')
            else:
                text_end["text"] = "Ocorreu um erro, tente novamente!"
                text_end.config(bg='red')
                link.delete(0, END)

def destroy(e):
    window.destroy()

window = Tk()
window.title("Baixar músicas do YouTube")
window.maxsize(width=675, height=175)
window.minsize(width=600, height=125)

title_window = Label(window, text="Converter do Youtube para MP3", font=("Arial", 15), bg='#9d9d9d')
title_window.grid(column=0, row=0, pady=10, padx=10)

button = Button(window, text="Clique para baixar", command=music_download, font=("Arial", 15), bg='white')
button.grid(column=1, row=0, pady=10, padx=10)

window.bind('<Return>', call_music_download)

title_link = Label(window, text="Insira o link:", font=("Arial", 15))
title_link.grid(column=0, row=1, padx=10, sticky="w")

link = Entry(window, font=("Arial", 15), width=55)
link.grid(column=0, row=2, columnspan=2, padx=10)

text_end = Label(window, font=("Arial", 15))
text_end.grid(column=0, row=4, columnspan=2, pady=10)

window.bind('<Escape>', destroy)
window.mainloop()