from config import db

class LikedSong(db.Model):
    track_id = db.Column(db.String(200), primary_key=True)
    artists = db.Column(db.String(200))
    album_name = db.Column(db.String(200))
    track_name = db.Column(db.String(200))
    popularity = db.Column(db.Integer)
    duration_ms = db.Column(db.Integer)
    explicit = db.Column(db.Boolean)
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    key= db.Column(db.Integer)
    loudness= db.Column(db.Float)
    mode= db.Column(db.Integer)
    speechiness= db.Column(db.Float)
    acousticness= db.Column(db.Float)
    instrumentalness= db.Column(db.Float)
    liveness = db.Column(db.Float)
    valence= db.Column(db.Float)
    tempo= db.Column(db.Float)
    time_signature= db.Column(db.Integer)
    track_genre= db.Column(db.String(200))
    score = db.Column(db.Integer, index=True)
    

    def to_json(self):
        return {
            "trackId": self.track_id,
            "artists": self.artists,
            "albumName": self.album_name,
            "trackName": self.track_name,
            "popularity": self.popularity,
            "durationMs": self.duration_ms,
            "explicit": self.explicit,
            "danceability": self.danceability,
            "energy": self.energy,
            "key": self.key,
            "loudness": self.loudness,
            "mode": self.mode,
            "speechiness": self.speechiness,
            "acousticness": self.acousticness,
            "instrumentalness": self.instrumentalness,
            "liveness": self.liveness,
            "valence": self.valence,
            "tempo": self.tempo,
            "timeSignature": self.time_signature,
            "trackGenre": self.track_genre,
            "score": self.score,
        }