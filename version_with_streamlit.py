import yt_dlp as youtube_dl
import streamlit as st
import os

# Defina o caminho para o diretório de download
download_path = "./../../../run/user/1000/gvfs/smb-share:server=server.local,share=pasta-compartilhada/Tiago/downloads_pytube"

def download_media(link_input, selected_format, selected_quality):
    try:
        # Configurações para download de áudio ou vídeo
        ydl_opts = {}

        if selected_format in ["mp3", "wav"]:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': selected_format,
                    'preferredquality': '192',
                }],
            }
        elif selected_format == "mp4":
            # Mapear qualidade para a expressão correta para o yt-dlp
            quality_map = {
                "360p": "bestvideo[height<=360]+bestaudio/best",
                "720p": "bestvideo[height<=720]+bestaudio/best",
                "1080p": "bestvideo[height<=1080]+bestaudio/best",
            }
            selected_quality_format = quality_map.get(selected_quality, "bestvideo+bestaudio/best")

            ydl_opts = {
                'format': selected_quality_format,
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
                'postprocessors': [
                    {
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }
                ],
            }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link_input, download=True)
            title = info_dict.get('title', None)

        st.success(f"Mídia: '{title}' baixada com sucesso!")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

def playlist_download(link_input, selected_format, selected_quality):
    try:
        quality_map = {
            "360p": "bestvideo[height<=360]+bestaudio/best",
            "720p": "bestvideo[height<=720]+bestaudio/best",
            "1080p": "bestvideo[height<=1080]+bestaudio/best",
        }
        selected_quality_format = quality_map.get(selected_quality, "bestvideo+bestaudio/best")

        ydl_opts = {
            'format': 'bestaudio/best' if selected_format in ["mp3", "wav"] else selected_quality_format,
            'outtmpl': os.path.join(download_path, '%(playlist_title)s/%(title)s.%(ext)s'),
            'merge_output_format': 'mp4' if selected_format == 'mp4' else None,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': selected_format,
                'preferredquality': '192',
            }] if selected_format in ["mp3", "wav"] else None,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link_input])

        st.success(f"Playlist baixada completamente!")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

# Streamlit UI
st.title("Downloader de Músicas e Vídeos do YouTube")

link_input = st.text_input("Cole o link do vídeo ou playlist do YouTube:")
selected_format = st.selectbox("Selecione o formato:", ["mp3", "wav", "mp4"])
selected_quality = st.selectbox("Selecione a qualidade do vídeo (apenas para MP4):", ["360p", "720p", "1080p"])

if st.button("Baixar"):
    if "playlist" in link_input:
        playlist_download(link_input, selected_format, selected_quality)
    else:
        download_media(link_input, selected_format, selected_quality)