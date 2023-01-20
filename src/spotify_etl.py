import sqlite3
import os
import os.path
import pickle
import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib import pylab
import itertools


# TODO: ADD HEADER
# TODO: ADD json option for multiply vs add?
# kaggle datasets download -d andrewmvd/spotify-playlists


# "kaggle_dir": "andrewmvd/spotify-playlists",
# "temp_dir": "data/spotify/temp/",
# "data_dir": "data/spotify/raw/"



# TODO: get json file read in and remove key
os.environ['KAGGLE_USERNAME']="andrewmokhta"
os.environ['KAGGLE_KEY']="eb7de261bcf48ef0ca684c07e28bb309"

from kaggle.api.kaggle_api_extended import KaggleApi


def pull_kaggle_data(kaggle_dir, temp_dir, data_dir, raw_data_filename, temp_pickle_graph_filename):

    if os.path.exists(data_dir + raw_data_filename):
        print("Raw data already downloaded from Kaggle! Moving on to next step")
    else:
        kapi = KaggleApi()
        kapi.authenticate()

        print(kapi.dataset_list_files(kaggle_dir).files)
        kapi.dataset_download_files(kaggle_dir, path=data_dir, quiet=False, unzip=True)


def read_raw_sql(kaggle_dir, temp_dir, data_dir, raw_data_filename, temp_pickle_graph_filename):
    if os.path.exists(temp_dir + temp_pickle_graph_filename):
        print("Pickle data already prepared for analysis! Moving on to next step")
    else:
        n = 4
        df_spotify = pd.read_csv(data_dir + raw_data_filename, skiprows=1,
                         names=['user_id', 'artistname', 'trackname', 'playlistname'],
                         on_bad_lines='skip')

        # G = nx.Graph()

        # for p, a in df_nips.groupby('paper_id')['author_name']: 
        #     for a1, a2 in itertools.combinations(a, 2):
        #     # creates an edge
        #         read_edge(G, a1, a2)

        # pickle.dump(G, open(temp_dir + temp_pickle_graph_filename, 'wb'))
        # print(temp_dir + temp_pickle_graph_filename + ' saved!')