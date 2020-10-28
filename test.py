import networkx as nx
import random
import copy
import matplotlib.pyplot as plt

fh = open("IEEE118_rich.txt", 'rb')
G = nx.read_edgelist(fh)
fh.close()
G0 = G.to_undirected()

edges = list(G0.edges())
nodes = G0.nodes()
u, v = random.choice(edges)
x, y = random.sample(nodes, 2)

nx.draw(G0,with_labels=True)
plt.show()

# G = copy.deepcopy(G0)
# keys, degrees = zip(*G.degree())
# cdf = nx.utils.cumulative_distribution(degrees)
#
# hubs = [e for e in G.nodes() if G.degree()[e] >= 4]  # 全部富节点
# hubs_edges = [e for e in G.edges() if G.degree()[e[0]] >= 4 and G.degree()[e[1]] >= 4]  # 网络中已有的富节点和富节点的连边
# len_possible_edges = len(hubs) * (len(hubs) - 1) / 2  # 全部富节点间都有连边的边数
# u, y = random.sample(hubs, 2)  # 任选两个富节点
#
# v = random.choice(list(G[u]))
# x = random.choice(list(G[y]))
#
# print(list(G[u]))
