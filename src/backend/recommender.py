from data import Data
from models import LikedSong
from config import db
import math
from scipy.spatial.distance import cdist
import numpy as np
import time

class Knn:
    def __init__(self, df):
        self.feature_cols = ['danceability', 'energy', 'loudness',
                 'speechiness', 'acousticness', 'instrumentalness',
                 'liveness', 'valence', 'tempo']

        self.track_ids = df['track_id'].values
        self.feature_matrix = df[self.feature_cols].values
        self.id_to_idx = {tid: i for i, tid in enumerate(self.track_ids)}
        self.next_song = None
        self.next_song_after = None

    def pick_song(self):
        t0 = time.time()
        slct_ids = [row[0] for row in db.session.query(LikedSong.track_id).filter_by(score=1).all()]
        used_ids = [row[0] for row in db.session.query(LikedSong.track_id).filter_by(score=-1).all()]
        t1 = time.time()

        selected_idx = [self.id_to_idx[t] for t in slct_ids if t in self.id_to_idx]
        exclude_idx = set(selected_idx) | {self.id_to_idx[t] for t in used_ids if t in self.id_to_idx}
        t2 = time.time()

        mask = np.ones(len(self.track_ids), dtype=bool)
        if exclude_idx:
            mask[list(exclude_idx)] = False
        t3 = time.time()

        candidates = self.feature_matrix[mask]
        candidate_ids = self.track_ids[mask]
        selected = self.feature_matrix[selected_idx]
        t4 = time.time()

        dist_matrix = cdist(candidates, selected, metric='euclidean')
        t5 = time.time()

        min_idx = np.unravel_index(dist_matrix.argmin(), dist_matrix.shape)
        self.next_song = candidate_ids[min_idx[0]]
        t6 = time.time()

        # print(f"db queries: {t1-t0:.3f}s | idx lookup: {t2-t1:.3f}s | mask build: {t3-t2:.3f}s | array slicing: {t4-t3:.3f}s | cdist: {t5-t4:.3f}s | argmin: {t6-t5:.3f}s")