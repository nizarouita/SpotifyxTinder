from flask import request, jsonify
from config import app,db
from models import LikedSong
from recommender import Knn
from data import Data
import pandas as pd
import requests
import time


def get_artwork_url(track_name, artist_name):
    try:
        
        response = requests.get(
            "https://itunes.apple.com/search",
            params={
                "term": f"{track_name} {artist_name}",
                "media": "music",
                "limit": 1,
            },
            timeout=3,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("resultCount", 0) > 0:
            artwork_url = data["results"][0].get("artworkUrl100")
            if artwork_url:
                
                return artwork_url.replace("100x100", "600x600")
        
        
        return None
    except requests.RequestException:
        return None



with app.app_context():
        t0 = time.time()
        data = Data()
        data.scale()
        df = data.df

        
        df.to_sql('liked_song', db.engine, if_exists='replace', index=False)
        db.session.execute(db.text('CREATE INDEX IF NOT EXISTS ix_liked_song_score ON liked_song (score)'))
        db.session.commit()
        Algo = Knn(df)
        print(f"Load from DB: {time.time() - t0:.2f}s")

@app.route("/get_songs", methods=["GET"])
def get_liked_songs():
    songs = LikedSong.query.all()
    json_songs = list(map(lambda x: x.to_json(), songs))
    return jsonify(json_songs)

@app.route("/search_songs", methods=["GET"])
def search_songs():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify([])

    results = LikedSong.query.filter(
        db.or_(
            LikedSong.track_name.ilike(f"%{query}%"),
            LikedSong.artists.ilike(f"%{query}%"),
        )
    ).limit(10).all()

    return jsonify([r.to_json() for r in results])


@app.route('/get_one_song/<track_id>', methods=['GET'])
def get_liked_song(track_id):
    song = LikedSong.query.filter_by(track_id=track_id).first()
    if song is None:
        return jsonify({"error": "Song not found"}), 404
    return jsonify(song.to_json())


@app.route("/add_liked_song/<track_id>", methods=["PATCH"])
def add_song(track_id):
    song = db.session.get(LikedSong, track_id)

    if not song:
        return (jsonify({"message": "no id found"}), 404)
    
    data = request.json
    song.score = data.get("score", song.score)

    db.session.commit()
    return jsonify({"message": "Score updated"}), 201

@app.route("/get_next_song", methods=["GET"])
def get_next_song():
    
    Algo.pick_song()
    
    next_song_id = Algo.next_song
    next_song = LikedSong.query.filter_by(track_id=next_song_id).first()
    
    if next_song is None:
        return jsonify({"error": "Song not found"}), 404
    song_data = next_song.to_json()
    t1=time.time()
    song_data["artworkUrl"] = get_artwork_url(next_song.track_name, next_song.artists)
    t2=time.time()
    #print(f"apple music artwork response: {t2-t1:.3f}s")
    return jsonify(song_data)
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)


