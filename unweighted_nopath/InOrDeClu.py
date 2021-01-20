import networkx as nx
import random
import copy

def  enhanceClu(G0,nswap=1,max_tries=100,connected=1):
# 保证度分度特性不变的情况下随机交换连边

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 4:
        raise nx.NetworkXError("节点数太少，至少要含四个节点")

    tn = 0 #尝试次数
    swapcount = 0 #有效交换次数

    G = copy.deepcopy(G0)
    # keys,deges =zip(*G.degree().items())
    keys,edges =zip(*dict(G.degree()).items())
    cdf = nx.utils.cumulative_distribution(edges)# 计算度的累积分布
    while swapcount < nswap:
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数'%tn + '有效交换次数（%s)'%swapcount)
            print(e)
            break
        tn += 1
        oldG = copy.deepcopy(G)
        avcOldG = nx.average_clustering(oldG)
        #保证度分布不变的情况下，随机选取两条边u-v,x-y
        (ui,xi) = nx.utils.discrete_sequence(2,cdistribution=cdf) #返回长度为2的采样序列
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u,v,x,y])) == 4:
            if(y not in G[u]) and (v not in G[x]):
                G.add_edge(u,y)
                G.add_edge(v,x)
                G.remove_edge(u,v)
                G.remove_edge(x,y)
                avcNewG = nx.average_clustering(G)
                if avcOldG >= avcNewG:
                    G.add_edge(u, v)
                    G.add_edge(x, y)
                    G.remove_edge(u, y)
                    G.remove_edge(x, v)
                    continue
        if connected==1:
            if not nx.is_connected(G):
                G.add_edge(u,v)
                G.add_edge(x,y)
                G.remove_edge(u,y)
                G.remove_edge(x,v)
                continue
        swapcount=swapcount+1
    return G


def  weakenClu(G0,nswap=1,max_tries=100,connected=1):
# 保证度分度特性不变的情况下随机交换连边

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 4:
        raise nx.NetworkXError("节点数太少，至少要含四个节点")

    tn = 0 #尝试次数
    swapcount = 0 #有效交换次数

    G = copy.deepcopy(G0)
    # keys,deges =zip(*G.degree().items())
    keys,edges =zip(*dict(G.degree()).items())
    cdf = nx.utils.cumulative_distribution(edges)# 计算度的累积分布

    while swapcount < nswap:
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数'%tn + '有效交换次数（%s)'%swapcount)
            print(e)
            break
        tn += 1
        oldG = copy.deepcopy(G)
        avcOldG = nx.average_clustering(oldG)
        #保证度分布不变的情况下，随机选取两条边u-v,x-y
        (ui,xi) = nx.utils.discrete_sequence(2,cdistribution=cdf) #返回长度为2的采样序列
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u,v,x,y])) == 4:
            if(y not in G[u]) and (v not in G[x]):
                G.add_edge(u,y)
                G.add_edge(v,x)
                G.remove_edge(u,v)
                G.remove_edge(x,y)
                avcNewG = nx.average_clustering(G)
                if avcOldG < avcNewG:
                    G.add_edge(u, v)
                    G.add_edge(x, y)
                    G.remove_edge(u, y)
                    G.remove_edge(x, v)
                    continue
        if connected==1:
            if not nx.is_connected(G):
                G.add_edge(u,v)
                G.add_edge(x,y)
                G.remove_edge(u,y)
                G.remove_edge(x,v)
                continue
        swapcount=swapcount+1
    return G















