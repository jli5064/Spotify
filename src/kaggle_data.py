import os
import os.path
import json
import pandas as pd
import networkx as nx
import numpy as np

with open('config/kaggle.json') as fh:
    kaggle_config = json.load(fh)
os.environ['KAGGLE_USERNAME']=kaggle_config["username"]
os.environ['KAGGLE_KEY']=kaggle_config["key"]
from kaggle.api.kaggle_api_extended import KaggleApi


# import matplotlib.pyplot as plt
#from matplotlib import pylab


# kaggle datasets download -d andrewmvd/spotify-playlists


# "kaggle_dir": "andrewmvd/spotify-playlists",
# "temp_dir": "data/spotify/temp/",
# "data_dir": "data/spotify/raw/"



def pull_kaggle_data():
        # username, key, kaggle_dir, temp_dir, data_dir, test_data_dir, test_data_filename, raw_data_filename, temp_pickle_graph_filename

    if os.path.exists(kaggle_config["data_dir"] + kaggle_config["raw_data_filename"]):
        print("Raw data already downloaded from Kaggle! Moving on to next step")
    else:
        kapi = KaggleApi()
        kapi.authenticate()

        print(kapi.dataset_list_files(kaggle_config["kaggle_dir"]).files)
        kapi.dataset_download_files(kaggle_config["kaggle_dir"], path=kaggle_config["data_dir"], quiet=False, unzip=True)
        print("kaggle data downloaded")


def read_in_raw_csv():
    if os.path.exists(kaggle_config["temp_dir"] + kaggle_config["temp_pickle_graph_filename"]):
        print("Kaggle data already made into networkX data! Moving on to next step")
    else:
        n = 4
        df = pd.read_csv(os.path.join(kaggle_config["data_dir"], kaggle_config["raw_data_filename"]),
                        usecols=range(n),
                        lineterminator='\n',
                        header=0)
        print("kaggle data loaded")
        df.columns = [x.replace('"', '').lstrip() for x in df.columns]


        print("kaggle data cleaned")
        return df
    
def read_in_temp_csv(fn):
    df = pd.read_csv(fn)
    print("grouped data loaded")
    return df

def filter_dataset(df):
    appearances = df.groupby('artistname').agg({'trackname':'count', 'playlistname':lambda x: len(x.unique())})
    print(appearances.sort_values(by=['trackname', 'playlistname']))

    artists = appearances[appearances['playlistname']>=10].index
    print('# of artists on >= 10 playlists (sample):', len(artists))

    df1 = df[df['artistname'].isin(artists)]

    df1_grped = df1.groupby('playlistname').agg({'artistname':lambda x: len(x.unique())})
    playlists = df1_grped[df1_grped['artistname'] > 1].index
    df2 = df1[df1['playlistname'].isin(playlists)]
    print("dataframe filtered")
    return df2
    
def create_test_sample(df, test_data_dir, test_data_filename):
    if os.path.exists(test_data_dir + test_data_filename):
        print("Sample data already created! Moving on to next step")
    else:
        np.random.seed(0)
        playlists = df['playlistname'].unique()
        print("picking sample playlists")
        sample_playlists = np.random.choice(playlists, 1000, replace=False)
        sampled_df = df[df['playlistname'].isin(sample_playlists)]
        filtered_df = filter_dataset(sampled_df)
        print("saving sample to " + os.path.join(test_data_dir, test_data_filename))
        filtered_df.to_csv(os.path.join(test_data_dir, test_data_filename))
        return filtered_df


# don't think we need this
# def get_artist_list(df_dir):
#     df = pd.read_csv(df_dir)
#     return list(df['artistname'].apply(lambda x: str(x).lower()).unique())
    

def get_artist_weight(artist, g):
    weight_dict = {}
    node_weights = nx.get_edge_attributes(g, "weight")
    for i in node_weights:
        if artist in i:
            weight_dict[i] = node_weights[i]
    return sorted(weight_dict.items(), key=lambda x:x[1], reverse=True)


