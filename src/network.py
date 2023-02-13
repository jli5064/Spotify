import pickle
import networkx as nx
import itertools

def read_edge(gph, n0, n1):
    if gph.has_edge(n0, n1):
        gph[n0][n1]['weight'] +=1
    else:
        gph.add_edge(n0, n1, weight=1)

def kaggle_generate_graph(df, temp_group_dir):
    G = nx.Graph()
    # if not unique, could weight the number of times the artist appears in that playlist
    df_grp = df.groupby('playlistname').agg({'artistname': lambda x: (x).unique()})
    df_grp.to_csv(temp_group_dir)
    for i in range(len(df_grp)):
        
        for a in (df_grp.iloc[i]):
            for a1, a2 in itertools.combinations(a, 2):
                read_edge(G, a1, a2)
    return G

def kaggle_clean_graph_edges(g, wgt_thres = 1):
    # Removes edges based off of weight threshold
    long_edges = list(filter(lambda e: e[2] <= wgt_thres, (e for e in g.edges.data('weight'))))
    g.remove_edges_from(long_edges)
    return g


def dump_graph(graph, path):
    with open(path, 'wb') as f:
        pickle.dump(graph, f)
    print(path + " saved!")
    

def load_graph(path):
    try:
        with open(path, 'rb') as f:  # notice the r instead of w
            G = pickle.load(f)
        print(path + " has been read!")
        return G
    except:
        print("Error loading graph! ")