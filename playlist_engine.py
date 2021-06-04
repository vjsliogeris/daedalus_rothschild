# Playlist engine :)

from youtubesearchpython import VideosSearch
import youtube_dl
import pickle
import os
from random import randrange
import numpy as np
import random

MAX_DURATION = 900

class playlist_engine():
    def __init__(self):
        """Load mdata
        """
        print("Playlist engine reporting in!")

        self.asset_folder_name = 'assets'
        self.metadata_file_name = 'queue.pkl'
        #load song names from folder
        self.songs = [f.path[len(self.asset_folder_name)+1:]  for f in os.scandir(self.asset_folder_name)]
        self.songs.sort()
        random.shuffle(self.songs)


    def download_song(self, query):
        """Download queried song
        """
        print(query)
        ydl_opts = {'outtmpl': self.asset_folder_name+"/%(title)s.%(ext)s",
                'postprocessors':[{'key': 'FFmpegExtractAudio'}]}
        ydl = youtube_dl.YoutubeDL(ydl_opts)


        if query[:5] =="https":
            dictMeta = ydl.extract_info(query,download=False)
            duration = dictMeta['duration']
            name = dictMeta['title']
            audio_codec = dictMeta['acodec']
        else:
            query = "ytsearch:" + query
            dictMeta = ydl.extract_info(query,download=False)['entries'][0]
            duration = dictMeta['duration']
            name = dictMeta['title']
            audio_codec = dictMeta['acodec']
        #Check if we first already have the song
        new_song_fname = name
        print(new_song_fname)
        already_in = False
        for s in self.songs:
            s_eless = ''.join([x + "." for x in s.split(".")[:-1]])[:-1]
            #s_eless = s.split(".")[:-1][0]
            if s_eless == new_song_fname.replace("?",""):
                already_in = True
        print(already_in)
        #If not - download
        if not already_in:
            if duration > MAX_DURATION:
                print("%(title)s.%(ext)s")
                return "The song is too long."
            ydl.download([query])


        #Add it to play next
        songlist_new = [f.path[len(self.asset_folder_name)+1:]  for f in os.scandir(self.asset_folder_name)]
        for s in songlist_new:
            s_eless = ''.join([x + "." for x in s.split(".")[:-1]])[:-1]
            if s_eless == name.replace("?",""):
                new_song_fname = s
                break
        print(new_song_fname)
        self.songs = [new_song_fname] + self.songs
        return "Done."

    def shuffle(self):
        random.shuffle(self.songs)

    def get_playlist(self, n):
        next_songs = self.songs[:n]
        output = "is now playing: {0}\nQueue:".format(self.song)
        i = 1
        for song in next_songs:
            output += "\n {1}: {0}".format(song, i)
            i += 1
        return output



    def sample(self):
        """Return next song to play
        """
        self.song = self.songs[0]
        self.songs.remove(self.song)
        self.songs.append(self.song)

        return "assets/"+self.song
