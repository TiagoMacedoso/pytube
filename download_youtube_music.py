from pytube import YouTube
from pytube import Playlist
import os
from tkinter import *
from moviepy.editor import *

def call_download():
    link_input = str(link.get())

    if link_input == "Sair" or link_input == "sair" or link_input == "SAIR" or link_input == "exit" or link_input == "Exit" or link_input == "EXIT":
        window.destroy()

    selected = var_select.get()

    if selected == "m":
        music_download(link_input)
    elif selected == "p":
        playlist_download(link_input)
    else:
        text_end["text"] = "Selecione uma opção entre música ou playlist."
        text_end.config(bg='red')

def playlist_download(link_input):
    link_playlist = Playlist(link_input)

    index = 0

    for url_music in link_playlist.video_urls:
        music_download(url_music)
        index+=1

    if link_playlist.length == index:
        text_end["text"] = "Playlist: " + link_playlist.title + " baixada completamente!"
        text_end.config(bg='green')
    elif link_playlist.length != index:
        text_end["text"] = "Provavelmente alguma música não foi baixada. Ou haviam músicas repetidas."
        text_end.config(bg='red')
    else:
        text_end["text"] = "Ouve um erro, verifique os campos e tente novamente!"
        text_end.config(bg='red')

def music_download(link_input):

    link_music = link_input

    try:
        youtube_var = YouTube(link_music)
        
        old_path = youtube_var.streams.filter(only_audio=True, abr="128kbps", progressive=False, type="audio").get_audio_only().download()
        old_path_split = os.path.splitext(old_path)
        new_path = old_path_split[0]+'.mp3'
        
        convert_mp4_to_mp3(old_path, new_path)

        text_end["text"] = "Música: '" + youtube_var.title + "' baixada"
        text_end.config(bg='green')

        link.delete(0, END)

    except:
        if link_music == "":
            text_end["text"] = "Insira uma URL válida"
            text_end.config(bg='#691212')
        else:
            text_end["text"] = "Ocorreu um erro, verifique os campos e tente novamente!"
            text_end.config(bg='red')
            link.delete(0, END)

def convert_mp4_to_mp3(path_before, path_after):
    file_to_convert = AudioFileClip(path_before)
    file_to_convert.write_audiofile(path_after)
    file_to_convert.close()
    
    os.remove(path_before)

def define_music(e):
    var_select.set("m")

def define_playlist(e):
    var_select.set("p")

def call_download_by_bind(e):
    call_download()

def call_destroy_by_bind(e):
    window.destroy()

window = Tk()
window.title("Baixar músicas do YouTube")
window.maxsize(height=180)
window.minsize(width=630, height=180)

title_window = Label(window, text="Converter do Youtube para MP3", font=("Arial", 15), bg='#9d9d9d')
title_window.grid(column=0, row=0, pady=10, padx=10)

button = Button(window, text="Clique para baixar", command=call_download, font=("Arial", 15), bg='white')
button.grid(column=1, row=0, pady=10, padx=10)

var_select = StringVar()
var_select.set("m")

select_music = Radiobutton(window, text="Música", font=("Arial", 12), variable=var_select, value="m")
select_music.grid(column=0, row=1)

select_playlist = Radiobutton(window, text="Playlist", font=("Arial", 12), variable=var_select, value="p")
select_playlist.grid(column=1, row=1)

title_link = Label(window, text="Insira o link:", font=("Arial", 15))
title_link.grid(column=0, row=2, padx=10, sticky="w")

link = Entry(window, font=("Arial", 15), width=55)
link.grid(column=0, row=3, columnspan=2, padx=10)
link.focus_force()

text_end = Label(window, font=("Arial", 13))
text_end.grid(column=0, row=4, columnspan=2, pady=10)

window.bind('<m>', define_music)
window.bind('<p>', define_playlist)
window.bind('<Return>', call_download_by_bind)
window.bind('<Escape>', call_destroy_by_bind)

window.mainloop()