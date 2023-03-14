#!/usr/bin/env python
# TODO ADD SPOTIFY API TO DOCKER

import sys
import json
import os

sys.path.insert(0, 'src')

# SRC PY FILE IMPORTS
from clean import clean, make_data_dir
from kaggle_data import pull_kaggle_data, read_in_raw_csv, create_test_sample, filter_dataset
from network import kaggle_generate_graph, kaggle_clean_graph_edges, dump_graph, load_graph
from spotify_api import get_artist_genres
from cesna_model import attribute, train, eval
# from test import generate_network


def main(targets):
    '''
        Runs the main project pipeline logic, given the targets.
        targets must contain: 'data', 'model'.
        `main` runs the targets in order of data=>model.
    '''
    model_test = False

    make_data_dir()

    if 'clean' in targets: # works
        clean()

    if 'test' in targets:
        print('Adding "test-data" and "model"') 
        targets.extend(["test-data", "model"])
        model_test = True
        
    if 'all' in targets:
        print('Adding "data" and "model"') 
        targets.extend(["data", "model"])

    if ('data' in targets) or ('kaggle' in targets):
        model_test = False
        print("This will download kaggle spotify data")
        with open('config/kaggle.json') as fh:
            kaggle_config = json.load(fh)
        pull_kaggle_data()

        if os.path.exists(kaggle_config["data_dir"] + kaggle_config["sample_data_filename"]):
            # if sample csv already exists just read in that
            df = read_in_raw_csv(os.path.join(kaggle_config["data_dir"], kaggle_config["sample_data_filename"]))
        else:
            # otherwise read in full dataset and sample
            df = read_in_raw_csv(os.path.join(kaggle_config["data_dir"], kaggle_config["raw_data_filename"]))
            print("saving sampled data as own file")
            # sample size of 2000 playlists
            df = create_test_sample(2000, df, kaggle_config["data_dir"], kaggle_config["sample_data_filename"])

        filtered_df = filter_dataset(df)
        G = kaggle_generate_graph(df, os.path.join(kaggle_config["temp_dir"], kaggle_config[ "group_df_filename"]))
        
        cleaned_G = kaggle_clean_graph_edges(G)
        dump_graph(cleaned_G, os.path.join(kaggle_config["temp_dir"], kaggle_config[ "temp_pickle_graph_filename"]))

    if 'model' in targets:
        dir = os.path.join(kaggle_config["temp_dir"], kaggle_config[ "temp_pickle_graph_filename"])
        G = load_graph(dir)
        
        genres = get_artist_genres(G.nodes)
        att = attribute(df, G)
        
        print("running model, calculating accuracy")
        eval(G, genres, att, 7, df)
        
        
if __name__ == '__main__':
    # run via:
    # python main.py data spectral
    targets = sys.argv[1:]
    main(targets)

