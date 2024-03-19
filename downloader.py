from pytube import YouTube
import instaloader
import os
import shutil
import requests

def remove(nome):
    os.remove(nome)

def download_reel(reel_url):
    L = instaloader.Instaloader()
    nome_arquivo = ""
    post = instaloader.Post.from_shortcode(L.context, reel_url.split("/")[-2])
    temp_folder = "temp_reel"
    os.makedirs(temp_folder, exist_ok=True)
    L.download_post(post, target=temp_folder)
    for filename in os.listdir(temp_folder):
        if filename.endswith(".mp4"):
            description = post.caption
            valid_chars = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            description_cleaned = ''.join(c for c in description if c in valid_chars)
            new_filename = description_cleaned[:30] + ".mp4"
            nome_arquivo = new_filename
            shutil.move(os.path.join(temp_folder, filename), os.path.join(os.getcwd(), new_filename))
    shutil.rmtree(temp_folder)
    return nome_arquivo

def download_story(story_url):
    L = instaloader.Instaloader()
    try:
        story_id = story_url.split("/")[-1]
        story = instaloader.Post.from_shortcode(L.context, story_id)
        video_url = story.video_url or story.url
        response = requests.get(video_url)
        with open(f"story_{story_id}.mp4", "wb") as f:
            f.write(response.content)
        print("Story baixado com sucesso.")
        escolha = input("Deseja continuar? (N) Não, (S) Sim: ").upper()
        if escolha == "S":
            print("Redirecionando.")
            return main()
        if escolha == "N":
            print("Até a proxima.")
            return 
    except instaloader.exceptions.InstaloaderException as e:
        print("Ocorreu um erro:", str(e))

def download_video(url):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        arquivo = video.download()
        return arquivo
    except Exception as e:
        return "Ocorreu um erro"

def download_audio(url):
    try:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        arquivo = audio.download()
        return arquivo
    except Exception as e:
        return "Ocorreu um Erro"

def main():
    print("Bem-vindo ao programa de download do DuXis!")
    escolha = input("Você gostaria de baixar algo do Youtube ou do Instagram? (Y) YouTube, (I) Instagram: ").upper()
    
    if escolha == "Y":
        modo = input("Você gostaria de baixar um video ou um audio? (V) Videos, (A) audio").upper()
        if modo == "V":
            try:
                url = input("Por favor, insira o URL do vídeo: ")
                download_video(url)
            except Exception as e:
                print("Ocorreu um erro:", str(e))
        elif modo == "A":
            try:
                url = input("Por favor, insira o URL do vídeo: ")
                download_audio(url)
            except Exception as e:
                print("Ocorreu um erro:", str(e))
        else:
            print("Escolha inválida. Por favor, selecione 'V' para vídeo ou 'A' para áudio.")
    elif escolha == "I":
        modo = input("Você gostaria de baixar um reels ou um storys? (R) Reels, (S) Storys: ")
        if modo == "R":
            try:
                reel_url = input("Digite a URL do Reels a ser baixado: ")
                download_reel(reel_url)
            except Exception as e:
                print("Ocorreu um erro:", str(e))
        elif modo == "S":
            try:
                story_url = input("Digite a URL do Reels a ser baixado: ")
                download_story(story_url)
            except Exception as e:
                print("Ocorreu um erro:", str(e))

if __name__ == "__main__":
    main()