from pytube import YouTube
from pytube import Playlist
from tkinter import *
import os
from moviepy.editor import *

def call_download():
    link_input = str(link.get())

    if link_input == "Sair" or link_input == "sair" or link_input == "SAIR" or link_input == "exit" or link_input == "Exit" or link_input == "EXIT":
        window.destroy()

    selected = var_select_music_or_playlist.get()

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

        selected = var_select_mp3_or_mp4.get()

        if selected == "mp3":
            old_path = youtube_var.streams.filter(only_audio=True, abr="128kbps", progressive=False, type="audio").get_audio_only().download()
            old_path_split = os.path.splitext(old_path)
            new_path = old_path_split[0]+'.mp3'
            
            convert_mp4_to_mp3(old_path, new_path)

        elif selected == "mp4":

            quality = var_select_quality.get()

            match quality:

                case "360p":
                    youtube_var.streams.filter(file_extension='mp4').get_by_itag(18).download()

                case "720p":
                    youtube_var.streams.filter(file_extension='mp4').get_by_itag(22).download()
                
                case "1080p":
                    youtube_var.streams.filter(file_extension='mp4').get_by_itag(137).download()

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
    var_select_music_or_playlist.set("m")

def define_playlist(e):
    var_select_music_or_playlist.set("p")

def call_download_by_bind(e):
    call_download()

def call_destroy_by_bind(e):
    window.destroy()

window = Tk()
window.title("Baixar músicas do YouTube")
window.maxsize(height=180)
window.minsize(width=630, height=180)

title_window = Label(window, text="Converter do Youtube para MP3 ou MP4", font=("Arial", 15), bg='#9d9d9d')
title_window.grid(column=0, row=0, columnspan=2, pady=10, padx=10)

button = Button(window, text="Clique para baixar", command=call_download, font=("Arial", 15), bg='white')
button.grid(column=2, row=0, pady=10, padx=10)

var_select_music_or_playlist = StringVar()
var_select_music_or_playlist.set("m")

select_music = Radiobutton(window, text="Música", font=("Arial", 12), variable=var_select_music_or_playlist, value="m")
select_music.grid(column=0, row=1)

select_playlist = Radiobutton(window, text="Playlist", font=("Arial", 12), variable=var_select_music_or_playlist, value="p")
select_playlist.grid(column=0, row=2)

var_select_mp3_or_mp4 = StringVar()
var_select_mp3_or_mp4.set("mp3")

select_mp3 = Radiobutton(window, text="Somente áudio (.mp3)", font=("Arial", 12), variable=var_select_mp3_or_mp4, value="mp3")
select_mp3.grid(column=2, row=1)

select_mp4 = Radiobutton(window, text="Áudio e Vídeo (.mp4)", font=("Arial", 12), variable=var_select_mp3_or_mp4, value="mp4")
select_mp4.grid(column=2, row=2)

title_quality = Label(window, text="Selecione a qualidade do vídeo (somente para .mp4)", font=("Arial", 15), bg='#b8b8b8')
title_quality.grid(column=0, row=3, columnspan=3, pady=10, padx=10)

var_select_quality = StringVar()
var_select_quality.set("720p")

select_360p = Radiobutton(window, text="360p (leve/ruim)", font=("Arial", 12), variable=var_select_quality, value="360p")
select_360p.grid(column=0, row=4)

select_720p = Radiobutton(window, text="720p (médio/bom)", font=("Arial", 12), variable=var_select_quality, value="720p")
select_720p.grid(column=1, row=4)

select_1080p = Radiobutton(window, text="1080p (pesado/ótimo)", font=("Arial", 12), variable=var_select_quality, value="1080p")
select_1080p.grid(column=2, row=4)

title_link = Label(window, text="Insira o link:", font=("Arial", 15))
title_link.grid(column=0, row=5, padx=10, sticky="w")

link = Entry(window, font=("Arial", 15), width=55)
link.grid(column=0, row=6, columnspan=3, padx=10)
link.focus_force()

text_end = Label(window, font=("Arial", 13))
text_end.grid(column=0, row=7, columnspan=2, pady=10)

window.bind('<m>', define_music)
window.bind('<p>', define_playlist)
window.bind('<Return>', call_download_by_bind)
window.bind('<Escape>', call_destroy_by_bind)

window.mainloop()