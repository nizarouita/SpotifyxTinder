import pandas as pd
from sklearn.preprocessing import StandardScaler

class Data:
    def __init__(self, path='dataset.csv'):
        self.path = path
        self.df = None
        self.X = None
        self.scaler = None

    def filtre(self):
        df = pd.read_csv(self.path)
        df = df.drop(columns='Unnamed: 0', errors='ignore')
        self.df = df
        return self.df

    def scale(self):
        feature_cols = ['popularity', 'danceability', 'energy', 'loudness',
                         'speechiness', 'acousticness', 'instrumentalness',
                         'liveness', 'valence', 'tempo']

        self.scaler = StandardScaler()
        self.X = self.scaler.fit_transform(self.df[feature_cols])
        return self.X
