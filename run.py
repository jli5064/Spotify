#!/usr/bin/env python

import sys
import json
import os

sys.path.insert(0, 'src')

# SRC PY FILE IMPORTS
from clean import clean, make_data_dir
from kaggle_data import pull_kaggle_data, read_in_csv, create_test_sample, filter_dataset
from network import kaggle_generate_graph, kaggle_clean_graph_edges, dump_graph, load_graph
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
        print('Adding "test-data", "augment", and "cesna"') 
        targets.extend(["test-data", "augment", "cesna"])
        model_test = True
        
    if 'all' in targets:
        print('Adding "data", "augment", and "cesna"') 
        targets.extend(["data", "augment", "cesna"])

    if ('data' in targets) or ('kaggle' in targets):
        print("This will download kaggle spotify data")
        with open('config/kaggle.json') as fh:
            kaggle_config = json.load(fh)
        pull_kaggle_data()
        df = read_in_csv()
        filtered_df = filter_dataset(df)
    
    if ('test-data' in targets):
        print("This will download kaggle spotify data (test)")
        model_test = True

        with open('config/kaggle.json') as fh:
            kaggle_config = json.load(fh)
        pull_kaggle_data()
        df = read_in_csv()
        if df is not None:
            df = create_test_sample(df, kaggle_config["test_data_dir"], kaggle_config["test_data_filename"])
            print("test df created!")
        filtered_df = filter_dataset(df)
        print("test dataframe filtered")
        G = kaggle_generate_graph(filtered_df)
        print("graph properly generated")
        cleaned_G = kaggle_clean_graph_edges(G)
        print("graph edges trimmed")
        dump_graph(cleaned_G, os.path.join(kaggle_config["test_temp_dir"], kaggle_config[ "test_pickle_graph_filename"]))


    if 'augment' in targets:
        print("Pulling necessary information from Spotify! (WIP)")
        with open('config/spotify_api.json') as fh:
            spotify_api_config = json.load(fh)
    # TODO spotifyapifunc(**spotify_api_config) 
       
        
    if 'model' in targets:
        #G = load in the small spotify sample from pickle
        #genres = pull genres from artist sample
        acc = eval(G, genres)
        
        
if __name__ == '__main__':
    # run via:
    # python main.py data spectral
    targets = sys.argv[1:]
    main(targets)

