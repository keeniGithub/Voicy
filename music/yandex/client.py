import yandex_music
from yandex_music import Client
import yandex_music.exceptions
import config
import os

client = Client(config.YA_TOKEN).init()

def play(url: str, guild):
    if "https://music.yandex.ru/" in url:
        try:
            spl = url.split("/")
            arg1 = spl[len(spl) - 1]
            arg2 = spl[len(spl) - 3]
            name = f"{arg1}:{arg2}"
            track = client.tracks([name])
            track = track[0]
        except yandex_music.exceptions.BadRequestError:
            return None
    else:
        search_result = client.search(url, type_="track", playlist_in_best=False)
        track = search_result.tracks["results"][0]
        url = "https://music.yandex.ru/album/" + str(track["albums"][0]["id"]) + "/track/" + str(track["id"])

    track.download(f"music/songs/{guild}.mp3")

def remove(guild):
    try:
        os.remove(f"music/songs/{guild}.mp3")
    except FileNotFoundError:
        return None