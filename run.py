#!/usr/bin/env python

import sys
import json

sys.path.insert(0, 'src')

from clean import clean
from kaggle_data import pull_kaggle_data, read_in_csv
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
        print("This will download kaggle spotify data (test)")
        with open('config/kaggle.json') as fh:
            kaggle_config = json.load(fh)
        pull_kaggle_data(**kaggle_config)
        read_in_csv(**kaggle_config)
        

        
if __name__ == '__main__':
    # run via:
    # python main.py data spectral
    targets = sys.argv[1:]
    main(targets)

