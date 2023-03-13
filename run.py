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
from bigclam import eval
# from test import generate_network


def main(targets):
    '''
        Runs the main project pipeline logic, given the targets.
        targets must contain: 'data', 'model'.
        `main` runs the targets in order of data=>model.
    '''
    # print(os.path.join(kaggle_config["data_dir"], kaggle_config[ "raw_data_filename"]))
    model_test = False

    make_data_dir()
    print(df)

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
        df = read_in_raw_csv()
        if df is not None:
            print("saving sampled data as own file")
            # sample size of 2000 playlists
            df = create_test_sample(2000, df, kaggle_config["data_dir"], kaggle_config["raw_data_filename"])
            print("test df created!")
        else:
            print("sampled data already exists")
        filtered_df = filter_dataset(df)
        G = kaggle_generate_graph(df, os.path.join(kaggle_config["temp_dir"], kaggle_config[ "group_df_filename"]))
        cleaned_G = kaggle_clean_graph_edges(G)
        dump_graph(cleaned_G, os.path.join(kaggle_config["temp_dir"], kaggle_config[ "pickle_graph_filename"]))

    # if ('test-data' in targets):
    #     print("This will download kaggle spotify data (test)")
    #     model_test = True

    #     with open('config/kaggle.json') as fh:
    #         kaggle_config = json.load(fh)
    #     pull_kaggle_data()
    #     df = read_in_raw_csv()
    #     if df is not None:
    #         print("saving sampled data as own file")
    #         df = create_test_sample(df, kaggle_config["test_data_dir"], kaggle_config["test_data_filename"])
    #         print("test df created!")
    #     else:
    #         print("sampled data already exists")
    #     G = kaggle_generate_graph(df, os.path.join(kaggle_config["test_temp_dir"], kaggle_config[ "group_df_filename"]))
    #     print("graph properly generated")
    #     cleaned_G = kaggle_clean_graph_edges(G)
    #     print("graph edges trimmed")
    #     dump_graph(cleaned_G, os.path.join(kaggle_config["test_temp_dir"], kaggle_config[ "test_pickle_graph_filename"]))

    if 'model' in targets:
        if model_test:
            dir = os.path.join(kaggle_config["test_temp_dir"], kaggle_config[ "test_pickle_graph_filename"])   
        else:
            dir = os.path.join(kaggle_config["data_dir"], kaggle_config[ "raw_data_filename"])
        G = load_graph(dir)
        genres = get_artist_genres(G.nodes)

        # to do:
        # - run G through train()
        #     - need to update bigclam.py to make attributes
        # - evaluate results

    #     print("running model, calculating accuracy")
    #     acc, pred = eval(G, genres)
    #     print("Acuracy score of " + str(acc))
    #     print(pred)
        
        
if __name__ == '__main__':
    # run via:
    # python main.py data spectral
    targets = sys.argv[1:]
    main(targets)

