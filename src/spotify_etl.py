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


# kaggle datasets download -d andrewmvd/spotify-playlists


# "kaggle_dir": "andrewmvd/spotify-playlists",
# "temp_dir": "data/spotify/temp/",
# "data_dir": "data/spotify/raw/"

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
        print("Kaggle data already prepared for analysis! Moving on to next step")
    else:
        n = 4
        df = pd.read_csv(os.path.join(data_dir, raw_data_filename),
                        usecols=range(n),
                        lineterminator='\n',
                        header=0)
        df.columns = [x.replace('"', '').lstrip() for x in df.columns]