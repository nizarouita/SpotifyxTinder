import pandas as pd
from sklearn.preprocessing import StandardScaler

class Data:
    def __init__(self, path='dataset.csv'):
        self.path = path
        self.df = pd.read_csv(self.path)
        self.X = {}
        self.scaler = None

    def filtre(self):
        self.df = self.df.drop(columns='Unnamed: 0', errors='ignore')


    def scale(self):
        feature_cols = ['popularity', 'danceability', 'energy', 'loudness',
                         'speechiness', 'acousticness', 'instrumentalness',
                         'liveness', 'valence', 'tempo']

        self.filtre()
        ids = list(self.df['track_id'])
        self.scaler = StandardScaler()
        scaled_values = self.scaler.fit_transform(self.df[feature_cols]).tolist()
        if len(ids)==len(scaled_values):
            for i in range(len(ids)):
                self.X[ids[i]]=scaled_values[i]
        else:
            KeyError
        return self.X

    def get_info(self, id):
        descr_cols = ['track_id', 'artists', 'album_name', 'track_name']
        df = self.df[descr_cols][self.df['track_id']== id]
        return df.iloc[0].tolist()

