#Youtube video downloader without spam and problem

from flask import Flask
from flask import request, render_template, url_for
from flask_socketio import SocketIO, emit, send

from pytube import YouTube
from threading import Thread

#from selenium import webdriver

import os
import subprocess
import csv
import time

app = Flask(__name__)
app.config['DEBUG'] = True
#socketio = SocketIO(app)
#Rutina descarga video

class Downloader(Thread):
    def __init__(self, name, url):
        Thread.__init__(self)
        self.name = name
        self.url = url

    def run(self):
        ytlove(self.url)
        return('lol')

def ytlove(url):
    try:
        #emit('message', 'holaaaa!!', namespace='/socket')
        yt = YouTube(url)
        
        #driver = webdriver.PhantomJS()
        #driver.get(url)
        #print(driver.find_element_by_class_name('ytp-time-duration').text)

        #Show video config
        print(yt.get_videos())

        #View filename
        print(yt.filename)
        filename = yt.filename

        #Set Filename
        yt.set_filename(filename.replace(" ", "").lower())
        #Print Max quality
        print(yt.filter('mp4')[-1])

        #Select Video
        video = yt.get('mp4', '720p')

        #Download select current directory
        print(os.getcwd())
        video.download(os.getcwd()+'/static/download')

        #log?
        row = [yt.filename.lower(), time.time(), time.ctime()]
        with open('templog.csv', 'a') as f:
            w = csv.writer(f)
            w.writerow(row)

        #socketio.emit('message', 'este es el segundo mensaje',namespace='/socket')
        p = subprocess.Popen(['ffmpeg','-i',os.getcwd()+'/static/download/'+yt.filename+'.mp4', os.getcwd()+'/static/download/'+yt.filename+'.mp3'], stdout=subprocess.PIPE, bufsize=1)
        for line in iter(p.stdout.readline, b''):
            print(line)
        p.stdout.close()
        p.wait()
        os.remove(os.getcwd()+'/static/download/'+yt.filename+'.mp4')
        print('file removed')
        return(url_for('static', filename='download/'+yt.filename+'.mp3'))

    except Exception as e:
        return(e)

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        result = Downloader('hilo',url)
        result.start()
        #result.join()
        return(render_template('base.html', url=url, result=result))
    else:
        return(render_template('base.html'))

if __name__ == '__main__':
    #socketio.run(app, host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=5000)

'''
@socketio.on('connect', namespace='/socket')
def connect():
    print('Iniciando conexion')
    emit('message', 'este es el primer mensaje')

@socketio.on('my_event', namespace='/socket')
def initialize(message):
    print(message)
'''
