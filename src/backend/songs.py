from data import Data

class Song:
    def __init__(self, id, artist, album, name):
        self.id = id
        self.name = name
        self.artist = artist
        self.album = album

    def __eq__(self, s):
        return self.id == s.id

    def song_from_id(id):
        l = Data().get_info(id)
        return Song(l[0],l[1],l[2],l[3])