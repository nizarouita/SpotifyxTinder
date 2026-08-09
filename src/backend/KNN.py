from data import Data
from songs import Song
from taste_rep import Taste
import math

class Knn:
    def __init__(self , slct_songs):
        self.slct_songs = slct_songs
        self.X = Data().scale()
        self.primary = []
        self.secondary = []

    def euclidean_distance(self,p,q):
        total = sum((p_i - q_i) ** 2 for p_i, q_i in zip(p, q))
        return math.sqrt(total)

    def pick_songs(self):
        for song_user in self.slct_songs:
            for song_id in self.X.keys():
                print(';')
                dist = self.euclidean_distance(self.X[song_id], self.X[song_user.id])
                if dist <= 1.8 :
                    song = Song.song_from_id(song_id)
                    if song in self.secondary:
                        if song not in self.primary:
                            self.primary.append(song)
                    else:
                        self.secondary.append(song)
                

