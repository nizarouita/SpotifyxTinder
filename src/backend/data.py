import pandas as pd
from sklearn.preprocessing import StandardScaler

class Data:
    def __init__(self, path='merged_dataset.csv'):
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

        # ids = list(self.df['track_id'])
        self.scaler = StandardScaler()
        self.df[feature_cols] = self.scaler.fit_transform(self.df[feature_cols])
        # if len(ids)==len(scaled_values):
        #     for i in range(len(ids)):
        #         self.X[ids[i]]=scaled_values[i]
        #         self.Y[ids[i]]=self.df[self.df['track_id']==ids[i]]['score'].values[0]
        # else:
        #     raise KeyError("mismatch between ids and scaled values")  
        # return self.X

    # def get_info(self, id):
    #     descr_cols = ['track_id', 'artists', 'album_name', 'track_name']
    #     df = self.df[descr_cols][self.df['track_id']== id]
    #     return df.iloc[0].tolist()

    # def df_to_dic(self):
    #     return self.Y