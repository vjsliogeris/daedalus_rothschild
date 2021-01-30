# Playlist engine :)

from youtubesearchpython import VideosSearch
import youtube_dl
import pickle
import os
from random import randrange

MAX_DURATION = 900

class playlist_engine():
    def __init__(self):
        print("Playlist engine reporting in!")

        self.asset_folder_name = 'assets'

        self.authors = [f.path[len(self.asset_folder_name)+1:]  for f in os.scandir(self.asset_folder_name) if f.is_dir()]
        self.lads = []
      
    def delete(self, author, operand):
        response = "Jei sita matai - vytenis nemok programuot."
        if not str(author.id) in self.authors:
            response = "You have no songs saved. Jau daug istrynes XD"
            return response
        directory = "assets/"+str(author.id)+"/"
        songs = os.listdir(directory)
        if operand < 0 or operand > len(songs):
            response = "Neturi tiek dainu (tu turi {0}, o paprasei istrinti {1})".format(len(songs), operand)
        else:
            song_to_die = songs[operand]
            deldir = directory + song_to_die
            response = "Istriname {0}".format(song_to_die)
            os.remove(deldir)
        return response


    def get_playlist_author(self, author):
        response = "Jei sita matai - something went wrong."
        if not str(author.id) in self.authors:
            response = "You have no songs saved. Save some using #!p"
        else:
            directory = "assets/"+str(author.id)+"/"
            songs = os.listdir(directory)
            response = ""
            index = 0
            for song in songs:
                response += "{0}: {1}\n".format(index, song)
                index += 1
        return response

    def download_song(self, query, author):
        print(query)
        print(author.id)
        if not str(author.id) in self.authors:
            os.mkdir(self.asset_folder_name+"/"+str(author.id))
            self.authors += str(author.id)
            print("Creating folder for {0}".format(author))
        ydl_opts = {'outtmpl': self.asset_folder_name+"/"+str(author.id)+"/%(title)s.%(ext)s",
                'postprocessors':[{'key': 'FFmpegExtractAudio'}]}
        ydl = youtube_dl.YoutubeDL(ydl_opts)

        response = "Uh oh code broke sakyk vyteniui kad jis susipiso siso neturetum matyt."


        if query[:5] =="https":
            dictMeta = ydl.extract_info(query,download=False)
            duration = dictMeta['duration']
            name = dictMeta['title']
            if duration < MAX_DURATION:
                ydl.download([query])
                response = "Daina \"{0}\" sekmingai downloadinta".format(name)
            else:
                response = "Daina \"{0}\" yra ilgesne nei 15 minuciu ({1} seconds), tad pisk nx".format(name, duration)
        else:
            query = "ytsearch:" + query
            dictMeta = ydl.extract_info(query,download=False)['entries'][0]
            duration = dictMeta['duration']
            name = dictMeta['title']
            if duration < MAX_DURATION:
                ydl.download([query])
                response = "Daina \"{0}\" sekmingai downloadinta".format(name)
            else:
                response = "Daina \"{0}\" yra ilgesne nei 15 minuciu ({1} seconds), tad pisk nx".format(name, duration)

        return response


    def sample(self):
        authored_lads = [lad for lad in self.lads if str(lad.id) in self.authors]
        author_ID = randrange(len(authored_lads))
        winning_lad = authored_lads[author_ID]
        directory = "assets/"+str(winning_lad.id)+"/"
        songs = os.listdir(directory)
        song_ID = randrange(len(songs))
        song = songs[song_ID]

        return "assets/"+str(winning_lad.id) + "/"+song

    def connect_lads(self, lads):
        self.lads = lads



