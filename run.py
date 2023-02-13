#!/usr/bin/env python

import sys
import json
import os

sys.path.insert(0, 'src')

# SRC PY FILE IMPORTS
from clean import clean, make_data_dir
from kaggle_data import pull_kaggle_data, read_in_raw_csv, read_in_temp_csv, create_test_sample, filter_dataset, get_artist_list
from network import kaggle_generate_graph, kaggle_clean_graph_edges, dump_graph, load_graph
from spotify_api import get_access_token, get_spotify_genres
from bigclam import eval
# from test import generate_network


def main(targets):
    '''
        Runs the main project pipeline logic, given the targets.
        targets must contain: 'data', 'model'.
        `main` runs the targets in order of data=>model.
    '''
    
    model_test = False
    
    make_data_dir()

    if 'clean' in targets:
        clean()

    if 'test' in targets:
        print('Adding "test-data" and "model"') 
        targets.extend(["test-data", "model"])
        model_test = True
        
    if 'all' in targets:
        print('Adding "data" and "model"') 
        targets.extend(["data", "model"])

    if ('data' in targets) or ('kaggle' in targets):
        print("This will download kaggle spotify data")
        with open('config/kaggle.json') as fh:
            kaggle_config = json.load(fh)
        pull_kaggle_data()
        df = read_in_raw_csv()
        filtered_df = filter_dataset(df)

        print("dataframe filtered")
        G = kaggle_generate_graph(filtered_df, os.path.join(kaggle_config["temp_dir"], kaggle_config[ "group_df_filename"]))
        print("graph properly generated")
        cleaned_G = kaggle_clean_graph_edges(G)
        print("graph edges trimmed")
        dump_graph(cleaned_G, os.path.join(kaggle_config["temp_dir"], kaggle_config[ "temp_pickle_graph_filename"]))
    
    if ('test-data' in targets):
        print("This will download kaggle spotify data (test)")
        model_test = True

        with open('config/kaggle.json') as fh:
            kaggle_config = json.load(fh)
        pull_kaggle_data()
        df = read_in_raw_csv()
        if df is not None:
            print("saving sampled data as own file")
            df = create_test_sample(df, kaggle_config["test_data_dir"], kaggle_config["test_data_filename"])
            print("test df created!")
        else:
            print("sampled data already exists")
        filtered_df = filter_dataset(df)
        print("test dataframe filtered")
        G = kaggle_generate_graph(filtered_df, os.path.join(kaggle_config["test_temp_dir"], kaggle_config[ "group_df_filename"]))
        print("graph properly generated")
        cleaned_G = kaggle_clean_graph_edges(G)
        print("graph edges trimmed")
        dump_graph(cleaned_G, os.path.join(kaggle_config["test_temp_dir"], kaggle_config[ "test_pickle_graph_filename"]))

    if 'model' in targets:
        #G = load in the small spotify sample from pickle
        #genres = pull genres from artist sample
        with open('config/spotify_api.json') as fh:
            spotify_config = json.load(fh)
        if model_test:
            grouped_df = read_in_temp_csv(os.path.join(kaggle_config["test_temp_dir"], kaggle_config[ "group_df_filename"]))
        else:
            grouped_df = read_in_temp_csv(os.path.join(kaggle_config["temp_dir"], kaggle_config[ "group_df_filename"]))
        
        artists = get_artist_list(grouped_df)
        print(artists)
        print("collected unique artist list! Using Spotify Web API to collect genre information")
        access_token = get_access_token()
        genres = get_spotify_genres(access_token, artists)
        print("genre information loaded! Loading pickle graph")

        if model_test:
            dir = os.path.join(kaggle_config["test_temp_dir"], kaggle_config[ "test_pickle_graph_filename"])
            
        else:
            dir = os.path.join(kaggle_config["temp_dir"], kaggle_config[ "temp_pickle_graph_filename"])
        
        G = load_graph(dir)
        print(dir + "loaded!")

        print("running model, calculating accuracy")
        acc = eval(G, genres)
        print("Acuracy score of " + acc)
        
        
if __name__ == '__main__':
    # run via:
    # python main.py data spectral
    targets = sys.argv[1:]
    main(targets)

