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


def dump_graph(graph, filename):
    pickle.dump(graph, open(filename, 'wb'))
    print(filename + " has been saved!")

def load_graph(filename):
    try:
        G = pickle.load(open(filename, 'rb'))
        print(filename + " has been read!")
        return G
    except:
        print("Error loading graph! ")