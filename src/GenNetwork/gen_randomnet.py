import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import powerlaw

def nodeSetting (G,layer=1):
    """ Generate (x,y,z) coordinates, Node ID and Attribute Setting for cascade methods

    (x,y) coordinates follow the networkx spring layout.
    z coordinates(Layer) is given as a parameter 'layer'
    Save (x,y,z) coordinates as an attribute of node named '3D_pos'
    This information is used for drawing interdependent graph

    Parameters
    ----------
    G : Network Graph
    layer : Layer of this graph
    
    """    
    # Node Attribute '3D_pos' added
    pos = nx.spring_layout(G)
    for node in pos.keys():
        pos[node] = np.append(pos[node],layer)
    nx.set_node_attributes(G,pos,name='3D_pos')

    # Node Attribute 'Num' added
    for e in G.edges():
        G.edges[e]['num'] = layer
    for node in G.nodes():
        G.nodes[node]['num'] = layer

    # Node Renaming
    mapping = {}
    for node in G.nodes():
        mapping[node] = str(layer) + '-' + str(node)
    
    H = nx.relabel_nodes(G, mapping)

    return H

def SF_powerlaw_exp (G):
    """ Calculate gamma value of power-law degree distribution

    Parameters
    ----------
    G : Network Graph

    Returns
    -------
    alpha : gamma value of power-law degree distribution
    
    """
    d = [G.degree()[i] for i in G.nodes()]

    fit = powerlaw.Fit(d, discrete=True, verbose=False)
    alpha = fit.power_law.alpha

    return alpha

def networkER_w_3Dpos(N, avgdegree, layer=1):
    """ Create Erdos-Renyi Network with 3D position attribute

    Parameters
    ----------
    N : Number of nodes
    avgdegree : Expected average degree
    layer : Layer of this graph (refer to the method 'nodeSetting')

    Returns
    -------
    H : ER Networkx Graph

    """    

    G = nx.erdos_renyi_graph(N, avgdegree/N)
    H = nodeSetting(G,layer)

    return H

def networkSF_w_3Dpos_BA(N,m,layer=1):
    """ Create Scale-Free Network following Barabasi Albert Model with 3D position attribute

    Parameters
    ----------
    N : Number of nodes
    m : Number of edges to attach from a new node to existing nodes
    layer : Layer of this graph (refer to the method 'nodeSetting')

    Returns
    -------
    H : Scale Free Barabasi Albert Networkx Graph

    """    
    G = nx.barabasi_albert_graph(N,m)
    H = nodeSetting(G,layer)

    return H

def networkSF_w_3Dpos_PowerL(N,gamma,layer=1):
    """ Create Scale-Free Network following PowerLaw Degree Distribution with 3D position attribute

    Parameters
    ----------
    N : Number of nodes
    gamma : Expected gamma value of powerlaw degree distribution 
    layer : Layer of this graph (refer to the method 'add_3Dpos_attributes')

    Returns
    -------
    H : Scale Free Powerlaw Degree Distribution Networkx Graph

    """ 

    T = 1000
    i = 0
    while i<T: 
        s=[]

        while len(s)<N: # N nodes, power-law gamma without zero degree
            nextval = int(nx.utils.powerlaw_sequence(1, gamma)[0])
            if nextval!=0:
                s.append(nextval)
                
        if (sum(s)%2 == 0): #  As each edge contains two vertices, the degree seq sum has to be even.

            G = nx.configuration_model(s)
            G = nx.Graph(G) # remove parallel edges
            G.remove_edges_from(nx.selfloop_edges(G)) # remove selfloop edges

            gamma_real = SF_powerlaw_exp(G)
            r_gamma_real = round(gamma_real,1) # check the powerlaw gamma value (rounded at decimal place 1)

            if (r_gamma_real==gamma):
                break

        i += 1
    
    H = nodeSetting(G,layer)

    if (i == 1000):
        print("Couldn't generate Scale-Free Network based on given powerLaw parameters. Last gamma:", gamma_real)
    else:
        print("Generate Scale-Free Network based on given powerLaw parameters. Last gamma:", gamma_real)

    return H

def intd_random_net (G_a,G_b):
    """ Create an interdependent network from two Random Network

    Link two Random Network based on each Node ID
    Each ER Network should have same node size

    Parameters
    ----------
    G_a : First Network Graph
    G_a : Second Network Graph

    Returns
    -------
    intd_G : Networkx Graph

    """    
    _ = list(G_a.nodes())[0]
    a_layer = _.split('-')[0]
    _ = list(G_b.nodes())[0]
    b_layer = _.split('-')[0]

    intd_G = nx.union(G_a,G_b)

    if len(G_a.nodes()) == len(G_b.nodes()):
        for i in range(len(G_a.nodes())):
            intd_G.add_edge(a_layer+'-'+str(i),b_layer+'-'+str(i)) # Link between two nodes which has same node id.
    else:
        print("ERROR : Given two networks has different network size")

    return intd_G

def intdNetworkDraw(intd_G):
    """ Draw Interdependent Network

    Refer to each node's 3D coordinates.

    Parameters
    ----------
    intd_G : Interdependent Network Graph from the method 'intd_RAND_networks'

    """    
    fig = plt.figure(figsize=(10,10))
    ax = plt.axes(projection='3d')
    color = ['b','g','r','c','m','y','k','w']

    n_attr = nx.get_node_attributes(intd_G,'3D_pos')

    for node in n_attr.keys():
        pos = n_attr[node]
        x,y,z = [ i for i in pos]
        layer = int(node.split('-')[0])
        ax.scatter(x,y,z,c=color[layer])

    for edge in list(intd_G.edges):

        pos_a, pos_b = [n_attr[i] for i in edge]
        x_a,y_a,z_a = [i for i in pos_a]
        x_b,y_b,z_b = [i for i in pos_b]

        if z_a != z_b:
            alpha = 0.5 # If the edge connect two nodes in different layer, the edge transparency set differently.
        else:
            alpha = 1
        ax.plot([x_a,x_b],[y_a,y_b],[z_a,z_b],color="tab:gray",alpha=alpha)

    
    ax.set_axis_off()
    plt.show()
    return