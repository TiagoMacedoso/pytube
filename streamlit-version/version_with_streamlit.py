import yt_dlp as youtube_dl
import streamlit as st
import os
import re

download_path = "/app/downloads"

def download_progress_hook(d):
    if d['status'] == 'downloading':
        percent_str = re.sub(r'\x1b\[[0-9;]*m', '', d['_percent_str']).strip()
        try:
            progress_float = float(percent_str.replace('%', '')) / 100
            st.session_state.progress_bar.progress(progress_float)
            st.session_state.progress_text.text(f"Progresso: {percent_str} concluído.")
        except ValueError:
            st.session_state.progress_text.text("Erro ao atualizar o progresso.")
    elif d['status'] == 'finished':
        st.session_state.progress_text.text("Download finalizado, processando...")

def download_media(link_input, selected_format, selected_quality):
    try:
        ydl_opts = {
            'progress_hooks': [download_progress_hook],  # Adiciona o hook de progresso
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        }

        if selected_format in ["mp3", "wav"]:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': selected_format,
                    'preferredquality': '192',
                }],
            })
        elif selected_format == "mp4":
            quality_map = {
                "360p": "bestvideo[height<=360]+bestaudio/best",
                "720p": "bestvideo[height<=720]+bestaudio/best",
                "1080p": "bestvideo[height<=1080]+bestaudio/best",
            }
            selected_quality_format = quality_map.get(selected_quality, "bestvideo+bestaudio/best")

            ydl_opts.update({
                'format': selected_quality_format,
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
            })

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link_input, download=True)
            title = info_dict.get('title', None)

        st.success(f"Mídia: '{title}' baixada com sucesso!")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

def playlist_download(link_input, selected_format, selected_quality):
    try:
        ydl_opts = {
            'progress_hooks': [download_progress_hook],  # Adiciona o hook de progresso
            'outtmpl': os.path.join(download_path, '%(playlist_title)s/%(title)s.%(ext)s'),
        }

        if selected_format in ["mp3", "wav"]:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': selected_format,
                    'preferredquality': '192',
                }],
            })
        else:
            quality_map = {
                "360p": "bestvideo[height<=360]+bestaudio/best",
                "720p": "bestvideo[height<=720]+bestaudio/best",
                "1080p": "bestvideo[height<=1080]+bestaudio/best",
            }
            selected_quality_format = quality_map.get(selected_quality, "bestvideo+bestaudio/best")
            ydl_opts.update({
                'format': selected_quality_format,
                'merge_output_format': 'mp4',
            })

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link_input])

        st.success(f"Playlist baixada completamente!")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

st.title("Downloader de Músicas e Vídeos do YouTube")

link_input = st.text_input("Cole o link do vídeo ou playlist do YouTube:")
selected_format = st.selectbox("Selecione o formato:", ["mp3", "wav", "mp4"])
selected_quality = st.selectbox("Selecione a qualidade do vídeo (apenas para MP4):", ["360p", "720p", "1080p"])

if 'progress_bar' not in st.session_state:
    st.session_state.progress_bar = st.progress(0)
    st.session_state.progress_text = st.empty()

if st.button("Baixar"):
    st.session_state.progress_bar.progress(0)
    st.session_state.progress_text.text("")
    if "playlist" in link_input:
        playlist_download(link_input, selected_format, selected_quality)
    else:
        download_media(link_input, selected_format, selected_quality)