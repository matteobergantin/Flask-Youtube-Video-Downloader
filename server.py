from flask import Flask, render_template, request, Response, send_file, after_this_request
from yt_dlp.utils import ExtractorError, DownloadError
from os.path import sep as DIR_SEPARATOR, exists
from ytplaylist import FindVideoData
from os import remove, listdir
from queue import Queue, Full
from yt_dlp import YoutubeDL
from threading import Thread
from time import sleep
import random

app = Flask(__name__, static_folder='static', static_url_path='/static')
to_remove = Queue()

class RemoveFilesThread(Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
    def run(self):
        global to_remove
        while True:
            sleep(0.1)
            element = to_remove.get(block=True)
            try:
                remove(element)
            except:
                to_remove.put(element, block=True)

@app.route('/')
def index():
    playlist = ""
    if 'playlist' in request.args:
        playlist = request.args.get('playlist')
    video_list = []
    error = False
    if playlist:
        try:
            video_list = FindVideoData(playlist)
        except KeyError:
            video_list = []
            error = "Error: Playlist does not exist or is empty"
    return render_template('index.html', playlist=playlist, video_list=video_list, error=error)

@app.route('/download/<string:videoID>', methods=['GET'])
def download(videoID: str):
    url = f"https://www.youtube.com/watch?v={videoID}"

    def genFilename(audio: bool) -> str:
        out = ""
        for i in range(16):
            out += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        out = f'downloaded{DIR_SEPARATOR}{out}'
        if exists(out + ('.mp3' if onlyAudio else '.mp4')):
            return genFilename(audio)
        return out

    if not isinstance(videoID, str):
        resp = Response()
        resp.status_code = 400
        resp.headers['Content-Type'] = 'text/plain'
        resp.set_data("400 - Invalid data found when processing input")
        return resp

    onlyAudio = True if 'audio' in request.args else False
    tmp_filename = genFilename(onlyAudio)
    opt = {'outtmpl': tmp_filename + '.%(ext)s', 'quiet': True}
    if onlyAudio:
        opt['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3'
        }]
    else:
        opt['format'] = 'mp4'

    with YoutubeDL(opt) as ytdlp:
        try:
            ytdlp.download(url)
        except (ExtractorError, DownloadError):
            resp = Response()
            resp.status_code = 400
            resp.headers['Content-Type'] = 'text/plain'
            resp.set_data("YT-DLP Error: Video ID is invalid")
            return resp

    @after_this_request
    def remove_file(resp):
        global to_remove
        try:
            to_remove.put_nowait(tmp_filename)
        except Full:
            to_remove.put(tmp_filename, block=True)
        return resp

    return send_file(tmp_filename + ('.mp3' if onlyAudio else '.mp4'))


if __name__ == '__main__':
    for f in listdir('downloaded'):
        try:
            remove(f'downloaded{DIR_SEPARATOR}{f}')
        except:
            print(f"Couldn't remove file: {f}")
    RemoveFilesThread().start()
    app.run(debug=False, host="0.0.0.0", port=80)
    for f in listdir('downloaded'):
        try:
            remove(f'downloaded{DIR_SEPARATOR}{f}')
        except:
            print(f"Couldn't remove file: {f}")
