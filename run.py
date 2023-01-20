#!/usr/bin/env python

import sys
import json
import networkx as nx

sys.path.insert(0, 'src')
from spotify_etl import pull_kaggle_data, read_raw_sql

# from clean import clean
# from test_etl import create_rand_graphs, create_combined, create_combined_edges
# from nips_etl import pull_kaggle_data, read_raw_sql
# from political_etl import pull_political_data, fix_political_gml, prepare_political
# from spectral_analysis import graph_stats, return_sub_graphs, spectral_cluster, spectral_evaluation, create_original_data, save_ground_truth_graph, save_prediction_graph



def main(targets):
    '''
        Runs the main project pipeline logic, given the targets.
        targets must contain: 'data', 'model'.
        `main` runs the targets in order of data=>model.
    '''
    
    # model_test = False
    
    # if 'clean' in targets:
    #     clean()
    
    # if 'test' in targets:
    #     targets.extend(["test-data", "spectral"])
    #     model_test = True
    #     print("extended test-data & spectral!")

    # if 'all' in targets:
    #     targets.extend(["data", "spectral"])
    #     model_test = False
    #     print("extended data & spectral!")
    
    # if 'test-data' in targets:
    #     model_test = True
    #     with open('config/test_etl.json') as fh:
    #         test_etl_config = json.load(fh)
    #     create_rand_graphs(**test_etl_config)
    #     create_combined(**test_etl_config)
    #     create_combined_edges(**test_etl_config)

    if ('data' in targets) or ('spotify' in targets):
        print("This will download kaggle data")
        with open('config/spotify_etl.json') as fh:
            nips_etl_config = json.load(fh)
        pull_kaggle_data(**nips_etl_config)
        read_raw_sql(**nips_etl_config)
        
        
    # if 'spectral' in targets:
    #     print("This will check which dataset to load (if REAL data exists, that. otherwise check if test data exists, uest that) and run model")
    #     print(model_test)
    #     if model_test:
    #         # plitical/temp
    #         print("using test data to make model!")

    #         GR = nx.read_gpickle('data/test/temp/combined.pickle')
    #         g0, g1 = return_sub_graphs(GR)[0], return_sub_graphs(GR)[1]
    #         g_dict = {'main_graph':GR, 'subgraph1':g0, 'subgraph2':g1}

    #         with open("data/test/out/graphstats.txt", "w") as fh:
    #             for i in ['main_graph', 'subgraph1', 'subgraph2']:
    #                 fh.write(i)
    #                 fh.write(str(graph_stats(g_dict[i])))
    #                 fh.write("\n")
            
    #         print("saving unlabeled graph")
    #         create_original_data(GR, "data/test/out/unlabeled_graph.pdf")
    #         print("saving ground truth graph")
    #         save_ground_truth_graph(GR, "data/test/temp/ground_truth.json", "data/political/out/ground_truth.pdf")
    #         print("spectral clustering")
    #         evals = spectral_evaluation(GR)

    #         print("saving prediction graph")
    #         save_prediction_graph(GR, evals["predictions"], "data/test/out/prediction_graph.pdf")
            
    #     else:
    #         # test/temp
    #         print("using real data to make model!")

    #         GR = nx.read_gpickle("data/political/temp/political_graph.pickle") 
    #         g0, g1 = return_sub_graphs(GR)[0], return_sub_graphs(GR)[1]
    #         g_dict = {'main_graph':GR, 'subgraph1':g0, 'subgraph2':g1}

    #         with open("data/political/out/graphstats.txt", "w") as fh:
    #             for i in ['main_graph', 'subgraph1', 'subgraph2']:
    #                 fh.write(i)
    #                 fh.write(str(graph_stats(g_dict[i])))
    #                 fh.write("\n")
    #         print("saving unlabeled graph")
    #         create_original_data(GR, "data/political/out/unlabeled_graph.pdf")
    #         print("saving ground truth graph")
    #         save_ground_truth_graph(GR, "data/political/temp/ground_truth.json", "data/political/out/ground_truth.pdf")
    #         print("spectral clustering")
    #         evals = spectral_evaluation(GR)

    #         print("saving prediction graph")
    #         save_prediction_graph(GR, evals["predictions"], "data/political/out/prediction_graph.pdf")

        
if __name__ == '__main__':
    # run via:
    # python main.py data spectral
    targets = sys.argv[1:]
    main(targets)

