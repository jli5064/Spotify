#!/usr/bin/env python

import sys
import json

sys.path.insert(0, 'src')

# SRC PY FILE IMPORTS
from clean import clean
from kaggle_data import pull_kaggle_data, read_in_csv, create_test_sample
# from test import generate_network


def main(targets):
    '''
        Runs the main project pipeline logic, given the targets.
        targets must contain: 'data', 'model'.
        `main` runs the targets in order of data=>model.
    '''
    
    # model_test = False
    
    if 'clean' in targets:
        clean()

    if ('data' in targets) or ('kaggle' in targets):
        print("This will download kaggle spotify data")
        with open('config/kaggle.json') as fh:
            kaggle_config = json.load(fh)
        pull_kaggle_data(**kaggle_config)
        df = read_in_csv(**kaggle_config)
    
    if ('test-data' in targets):
        print("This will download kaggle spotify data (test)")
        with open('config/kaggle.json') as fh:
            kaggle_config = json.load(fh)
        pull_kaggle_data(**kaggle_config)
        df = read_in_csv(**kaggle_config)
        if df is not None:
            test_df = create_test_sample(df, kaggle_config["test_data_dir"], kaggle_config["test_data_filename"])
            print("test df created!")
        
    if 'model' in targets:
        #G = load in the small spotify sample from pickle
        #genres = pull genres from artist sample
        acc = eval(G, genres)
        
        
if __name__ == '__main__':
    # run via:
    # python main.py data spectral
    targets = sys.argv[1:]
    main(targets)

