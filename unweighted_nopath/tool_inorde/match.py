import networkx as nx
import random
import copy


#强同配零模型
def assort_mixing(G0,nswap=1,max_tries=100,connected=1):
    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")

    tn = 0
    swapcount = 0

    G = copy.deepcopy(G0)
    keys,degress = zip(*G.degree())
    cdf = nx.utils.cumulative_distribution(degress)

    while swapcount < nswap:
        tn = tn+1

        (ui,xi) = nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u,v,x,y]))<4:
            continue
        sortednodes = list(zip(*sorted(G.degree([u,v,x,y]),key=lambda d:d[1],reverse=True)))[0]
        if (sortednodes[0] not in G[sortednodes[2]]) and (sortednodes[2] not in G[sortednodes[3]]):
            G.add_edge(sortednodes[0],sortednodes[1])
            G.add_edge(sortednodes[2],sortednodes[3])
            G.remove_edge(x,y)
            G.remove_edge(u,v)

            if connected==1:
                if not nx.is_connected(G):
                    G.remove_edge(sortednodes[0],sortednodes[1])
                    G.remove_edge(sortednodes[2],sortednodes[3])
                    G.add_edge(x,y)
                    G.add_edge(u,v)
                    continue
        if tn >= max_tries:
            print('Maximum number of swap attempts '+str(tn)+' exceeded , before desired swaps achieved '+str(nswap))
            break
        swapcount = swapcount+1

    return G

#强异配零模型
def disassort_mixing(G0,nswap=1, max_tries=100, connected=1):
    """
    随机选取两条边，四个节点，将这四个节点的度值从大到小排序，
    将度值差异较大的两个节点进行连接，第一和第四两个节点相连，
    将度值差异较小的两个节点进行连接，第二和第三两个节点相连
    最终形成了异配网络
    """
    # G0：待改变结构的网络
    # k 为富节点度值的门限值
    # nswap：是改变成功的系数，默认值为1
    # max_tries：是尝试改变的次数，默认值为100
    # connected：是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys ,degrees = zip(*G.degree())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < nswap:  # 有效交换次数小于规定交换次数
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui ,xi ) =nx.utils.discrete_sequence(2 ,cdistribution=cdf)
        if ui==xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u ,v ,x ,y]) ) <4:
            continue
        sortednodes = list(zip(*sorted(G.degree([u ,v ,x ,y]) ,key=lambda d :d[1] ,reverse=True)))[0]
        if (sortednodes[0] not in G[sortednodes[3]]) and (sortednodes[1] not in G[sortednodes[2]]):
            # 保证新生成的连边是原网络中不存在的边

            G.add_edge(sortednodes[0] ,sortednodes[3])  # 连新边
            G.add_edge(sortednodes[1] ,sortednodes[2])
            G.remove_edge(x ,y)  # 断旧边
            G.remove_edge(u ,v)

            if connected==1:
                if not nx.is_connected(G):
                    G.remove_edge(sortednodes[0] ,sortednodes[3])
                    G.remove_edge(sortednodes[1] ,sortednodes[2])
                    G.add_edge(x ,y)
                    G.add_edge(u ,v)
                    continue
        if tn >= max_tries:
            print('Maximum number of swap attempts '+str(tn)+' exceeded , before desired swaps achieved '+str(nswap))
            break
        swapcount+=1
    return G





fh = open("IEEE118.txt",'rb')
G = nx.read_edgelist(fh)
fh.close()
G0 = G.to_undirected()

n = len(G0.edges())
nswap = 6*n
max_tries = 100*n

G1 = assort_mixing(G0,nswap,max_tries)
fh = open("IEEE118_assort.txt",'wb')
nx.write_edgelist(G1,fh,data=False)
fh.close()
n1 = len(G1.nodes())
m1 = len(G1.edges())
print(n1)
print(m1)
