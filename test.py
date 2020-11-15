import networkx as nx
import random
import copy
import matplotlib.pyplot as plt
import inter_random as inter
import inner_random as inner
import InOrDeClu as idclu
import InOrDeCreaseComm as idcom
import igraph as ig


#调用无权各阶零模型以及聚类系数零模型
fh = open("IEEE300.txt", 'rb')
G = nx.read_edgelist(fh)
fh.close()
G0 = G.to_undirected()

sawpn = 2000
max_tries = 50000

G1 = idclu.weakenClu(G0,sawpn,max_tries)
fh = open("IEEE300_weakenClu.txt", 'wb')
nx.write_edgelist(G1, fh, data=False)
fh.close()
n1 = len(G1.nodes())
m1 = len(G1.edges())

print(n1)
print(m1)


#调用社团各阶零模型以及增强减弱社团零模型

G0=nx.read_edgelist('IEEE118.txt')
M=nx.number_of_edges(G0)
Gi = ig.Graph.Read_Edgelist("IEEE118.txt")  # 基于这些连边使用igraph创建一个新网络
Gi = Gi.as_undirected()
# h1 = Gi.community_edge_betweenness(clusters=None, directed=False, weights=None)
# community_list = list(h1.as_clustering())

community_list0 = Gi.community_multilevel(weights=None,return_levels=False)
community_list1 = []
for item in community_list0:
    community_list1.append(item)

del community_list1[0]
community_list_s=community_list1
for i in range(0,len(community_list1)):
    community_list_s[i]=map(str, community_list1[i])

G=inner.inner_random_25k(G0,community_list_s,nswap=100, max_tries=20*M)
n1 = len(G.nodes())
m1 = len(G.edges())

print(n1)
print(m1)
nx.write_edgelist(G,'IEEE118_inner_25K.txt',data=False)













