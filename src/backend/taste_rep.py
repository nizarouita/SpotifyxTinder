from data import Data

class Taste:
    def __init__(self, user_pref):
        self.user_choice = user_pref
        self.data = Data().X
        self.av_songs = None

    def available_songs(self):
        for s in self.user_choice:
            if s.id in self.data.keys():
                self.av_songs.append(s)
