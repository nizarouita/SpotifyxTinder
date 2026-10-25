import pandas as pd
from sklearn.preprocessing import StandardScaler

class Data:
    def __init__(self, path='dataset_merged_raw.csv'):
        self.path = path
        self.df = pd.read_csv(self.path, low_memory=False)
        self.df = self.df.drop(columns='Unnamed: 0', errors='ignore')
        self.df['score'] = 0
        self.df = self.df.drop_duplicates(subset='track_id', keep='first')
        self.df = self.df.drop_duplicates(subset=['track_name', 'artists'], keep='first')
        self.scaler = None

    def scale(self):
        feature_cols = ['danceability', 'energy', 'loudness',
                         'speechiness', 'acousticness', 'instrumentalness',
                         'liveness', 'valence', 'tempo']

        self.scaler = StandardScaler()
        self.df[feature_cols] = self.scaler.fit_transform(self.df[feature_cols])
        