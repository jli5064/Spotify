import numpy as np
import networkx as nx
import random
import pandas as pd
import copy
import matplotlib.pyplot as plt

def attribute(sampled_df, G):
    att = sampled_df.groupby('artistname').agg({'playlistname':lambda x: len(np.unique(np.array(list(x)))) >= 10}) * 1
    return np.array([pd.Series([node for node in G.nodes]).apply(lambda x: dict(zip(att.index, att.playlistname))[x])]).T

# bigclam algorithm taken from https://github.com/RobRomijnders/bigclam
def sigm(x):
    return np.divide(np.exp(-1.*x),1.-np.exp(-1.*x))

def log_likelihood(F, A):
    """implements equation 2 of 
    https://cs.stanford.edu/people/jure/pubs/bigclam-wsdm13.pdf"""
    A_soft = F.dot(F.T)

    # Next two lines are multiplied with the adjacency matrix, A
    # A is a {0,1} matrix, so we zero out all elements not contributing to the sum
    FIRST_PART = A*np.log(1.-np.exp(-1.*A_soft))
    sum_edges = np.sum(FIRST_PART)
    SECOND_PART = (1-A)*A_soft
    sum_nedges = np.sum(SECOND_PART)

    log_likeli = sum_edges - sum_nedges
    return -log_likeli

def gradient(F, A, i):
    """Implements equation 3 of
    https://cs.stanford.edu/people/jure/pubs/bigclam-wsdm13.pdf
    
      * i indicates the row under consideration
    
    The many forloops in this function can be optimized, but for
    educational purposes we write them out clearly
    """
    N, C = F.shape

    neighbours = np.where(A[i])
    nneighbours = np.where(1-A[i])

    sum_neigh = np.zeros((C,))
    for nb in neighbours[0]:
        dotproduct = F[nb].dot(F[i])
        sum_neigh += F[nb]*sigm(dotproduct)

    sum_nneigh = np.zeros((C,))
    #Speed up this computation using eq.4
    for nnb in nneighbours[0]:
        sum_nneigh += F[nnb]

    grad = sum_neigh - sum_nneigh
    return grad

def train(A, Att, C, iterations = 1, alpha = .005, lambda_W = .001):
    # initialize an F
    N = A.shape[0]
    F = np.random.rand(N,C)
    F_new = np.zeros((N,C))
    X = Att
    W = np.random.rand(Att.shape[1], C)
    W_new = np.zeros((Att.shape[1], C))
    ll = .01
    ll_new = 0
    Q = np.zeros((F.shape[0], W.shape[0]))
    Sanity = np.zeros((F.shape[0], W.shape[0]))
    for n in range(iterations):
        for u in range(Q.shape[0]):
            for k in range(Q.shape[1]):
                running_sum = 0
                for c in range(F.shape[1]):
                    running_sum += W[k][c] * F[u][c]
                Q[u][k] = 1/(1+np.exp(-running_sum))
        
        for u in range(X.shape[0]):
            grad = gradient(F, A, u)
            for c in range(F.shape[1]):
                running_sum = 0
                for k in range(X.shape[1]):
                    running_sum += (X[u][k] - Q[u][k]) * W[k][c]
                F_new[u][c] = max(.001, F[u][c] + alpha*(running_sum + grad[c]))
        
        for k in range(X.shape[1]):
            for c in range(F.shape[1]):
                running_sum = 0
                for u in range(F.shape[0]):
                    running_sum += (X[u][k] - Q[u][k]) * F[u][c]
                W_new[k][c] = W[k][c] + alpha * running_sum - alpha * lambda_W * np.sign(W[k][c])

        F = copy.deepcopy(F_new)
        W = copy.deepcopy(W_new)
        ll_new = log_likelihood(F, A)
        ll_new += np.sum(np.maximum(.001, X*np.log(np.maximum(.001, Q)) + (1 - X)*np.log(np.maximum(.001, 1 - Q))))
        change = (ll - ll_new) / ll
        if abs(change) < .001:
            break
        else:
            ll = ll_new
    delta = (-np.log(1 - (1/N)))**.5
    
    return F, delta, W


def accuracy(G, pred1, sampled_df, main_spotify_dict):
    pred1_dict = dict(zip(G.nodes(), pred1))
    pred1_df = sampled_df.assign(prediction = sampled_df['artistname'].map(pred1_dict))

    community_dicts = {}
    for (i, g) in pred1_df.groupby("prediction"):
        curr_tabular = g.reset_index()
        unique_art = list(g.artistname.unique())
        spotify_info = {a: main_spotify_dict[a] for a in unique_art}
        artist_count = curr_tabular.groupby("artistname").count()["trackname"]
        
        comm_genres = list( main_spotify_dict.values())
        comm_genre_words = pd.Series(comm_genres).apply(lambda x: sum([z.split() for z in x], []))
        
        genre_count = pd.Series(sum(comm_genres, [])).value_counts()
        genre_word_count = pd.Series(sum(comm_genre_words, [])).value_counts()
        
        top_3 = list(genre_count.index[:3])
        top_3_words = list(genre_word_count.index[:3])
        
        top_3_count = sum([any(map(lambda x: x in top_3, a)) for a in comm_genres])
        top_3_word_count = sum([any(map(lambda x: x in top_3_words, a)) for a in comm_genre_words])
        
        top_artists = curr_tabular.groupby("artistname").count()["trackname"].sort_values(ascending=False)[:5]
        
        
        sub = G.subgraph(unique_art)
    
    
    
    community_dicts[i] = {
        "n": len(unique_art),
        "artist_list" : unique_art,
        "top_artists" : top_artists,
        "artist_genres": comm_genres,
        "genre_count": genre_count,
        "top_genre": genre_count.index[0],
        "top_3_genres": top_3,
        "within_top_3": top_3_count,
        
        "artist_genres_words": comm_genre_words,
        "genre_word_count": genre_word_count,
        "top_genre_word": genre_word_count.index[0],
        "top_3_genre_words": top_3_words,
        "within_top_3_words": top_3_word_count,
        
        "playlist_list" : list(g.playlistname.unique()),
        "spotify_info" : spotify_info,
        "graph": sub,
        "tabular": g}



    genre = 0
    words = 0
    n = 0
    for community, info in community_dicts.items():
        print("Community {}'s most popular genre is {} and genre-word is {}'".format(community, info["top_genre"], info["top_genre_word"]))
        curr_n = info["n"]
        print("Community Size: {}".format(curr_n))
        print(info["top_artists"])
        
        curr_genre = info["within_top_3"]
        curr_words = info["within_top_3_words"]
        
                
        print("\nTop 3 Lists:")
        print(info["top_3_genres"])
        print(info["top_3_genre_words"])
        
        n += curr_n
        genre += curr_genre
        words += curr_words
        
        print("\nGenre Accuracy: {}".format(100*curr_genre/curr_n))
        print("Genre-Word Accuracy: {}".format(100*curr_words/curr_n))
        
        
        
        

        
        print("\n\n\n")
    total_accs = {"genre": 100*genre/n, "words": 100*words/n}
    print("\nTotal Genre Accuracy: {}".format(total_accs["genre"]))
    print("Total Genre-Word Accuracy: {}".format(total_accs["words"]))
    return total_accs


def plot_network(
    G,
    node_color='#1f78b4',
    node_border_color = None,
    node_alpha = 0.9,
    edge_alpha = 0.2,
    labels_dict = None,
    labels_size = 16,
    labels_color=None,
    save_dir = None
    ):

    fig = plt.figure(1, figsize=(56, 41), dpi=90)
    position = nx.kamada_kawai_layout(G) # I like this laylout, and gephi doesnt seem to have it, will look into
    nx.draw_networkx_nodes(G, position, node_size=2000, node_color=node_color, linewidths=3, edgecolors=node_border_color, alpha=node_alpha)
    nx.draw_networkx_edges(G, position, width=1.5, alpha=edge_alpha, node_size = 2000)
    nx.draw_networkx_labels(G, position, labels = labels_dict, font_size = labels_size, font_color=labels_color)    
    
    if save_dir:
        plt.savefig(save_dir)



def eval(G, genres, att, c, df):
    A = (nx.to_numpy_array(G) > 0) * 1
    iterations = 5
    F, delta, W = train(A, att, c, iterations)
    pred1 = np.argmax(F, 1)
    z = (zip(G.nodes, pred1))
    for (node, index) in z:
        if index == 0:
            v = {'color': {'r': 255, 'g': 0, 'b': 0, 'a': 1}} # red
        elif index == 1:
            v = {'color': {'r': 255, 'g': 165, 'b': 0, 'a': 1}} # orange
        elif index == 2:
            v = {'color': {'r': 255, 'g': 255, 'b': 0, 'a': 1}} # yellow
        elif index == 3:
            v = {'color': {'r': 0, 'g': 255, 'b': 0, 'a': 1}} # green
        elif index == 4:
            v = {'color': {'r': 0, 'g': 255, 'b': 255, 'a': 1}} # cyan
        elif index == 5:
            v = {'color': {'r': 0, 'g': 0, 'b': 255, 'a': 1}} # blue
        else:
            v = {'color': {'r': 255, 'g': 0, 'b': 255, 'a': 1}} # magenta
    G.nodes[node]['val'] = v
    plot_network(G, node_color = pred1, edge_alpha=0.01, node_border_color = "purple", labels_dict = dict(z), labels_color="red", save_dir = "data/kaggle/out")
    accuracy(G, pred1, df, genres)

    # nodes = list(G.nodes())
    # one = [nodes[i] for i in np.where(pred == 0)[0]]
    # two = [nodes[i] for i in np.where(pred == 1)[0]]
    # three = [nodes[i] for i in np.where(pred == 2)[0]]
    # # need to add correct number of groups
    
    # total = 0
    # for i in [one, two, three]:
    #     total += correct_pred(i, genres, nodes)
        
    ################ 
    #if you want to save the prediction graph to pdf
    ################
    #print("saving prediction graph")
    #plt.figure(num=None, figsize=(50, 50), dpi=100)
    #plt.axis('off')
    #fig = plt.figure(1)

    #pos = nx.spring_layout(G, seed=22)
    #nx.draw(G, pos = pos, node_color=pred)
    #with open(file_name, 'w') as fp:
        #pass
    #plt.savefig(file_name,bbox_inches="tight")
    #del fig
    
    return #(total/len(nodes), pred)
