import networkx as nx
import random
import copy



#强富人俱乐部零模型
def rich_club_create(G0, k=1, nswap=1, max_tries=100, connected=1):
    """
    任选两条边(富节点和非富节点的连边)，若富节点间无连边，非富节点间无连边，则断边重连
    达到最大尝试次数或全部富节点间都有连边，循环结束
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
    keys, degrees = zip(*G.degree())
    cdf = nx.utils.cumulative_distribution(degrees)

    hubs = [e for e in G.nodes() if G.degree()[e] >= k]  # 全部富节点
    hubs_edges = [e for e in G.edges() if G.degree()[e[0]] >= k and G.degree()[e[1]] >= k]  # 网络中已有的富节点和富节点的连边
    len_possible_edges = len(hubs) * (len(hubs) - 1) / 2  # 全部富节点间都有连边的边数

    while swapcount < nswap and len(hubs_edges) < len_possible_edges:
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        u, y = random.sample(hubs, 2)  # 任选两个富节点
        v = random.choice(list(G[u]))
        x = random.choice(list(G[y]))
        if len(set([u, v, x, y])) == 4:
            if G.degree()[v] > k or G.degree()[x] > k:
                continue  # 另一端节点为非富节点
        if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
            G.add_edge(u, y)
            G.add_edge(x, v)
            G.remove_edge(u, v)
            G.remove_edge(x, y)
            hubs_edges.append((u, y))  # 更新已存在富节点和富节点连边
            if nx.number_of_selfloops(G) > 0:#保证生成的图没有自环
                G.add_edge(u, v)
                G.add_edge(x, y)
                G.remove_edge(u, y)
                G.remove_edge(x, v)
                hubs_edges.remove((u, y))
                continue
            if connected == 1 : # 判断是否需要保持联通特性，为1的话则需要保持该特性
                if not nx.is_connected(G):  # 保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                    G.add_edge(u, v)
                    G.add_edge(x, y)
                    G.remove_edge(u, y)
                    G.remove_edge(x, v)
                    hubs_edges.remove((u, y))
                    continue

        if tn >= max_tries:
            print('Maximum number of attempts (%s) exceeded ' % tn)
            break
        swapcount = swapcount + 1
    print(swapcount)
    return G


#弱富人俱乐部零模型
def rich_club_break(G0,k=10,nswap=1,max_tries=100,connected=1):

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
    hubedges = []
    nothubedges = []
    hubs = [e for e in G.nodes() if G.degree()[e]>k]
    for e in G.edges():
        if e[0] in hubs and e[1] in hubs:
            hubedges.append(e)
        elif e[0] not in hubs and e[1] not in hubs:
            nothubedges.append(e)

    swapcount = 0
    while swapcount<nswap and hubedges and nothubedges:
        u,v = random.choice(hubedges)
        x,y = random.choice(nothubedges)
        if len(set([u,v,x,y]))<4:
            continue
        if (y not in G[u]) and (v not in G[x]):
            G.add_edge(u,y)
            G.add_edge(x,v)
            G.remove_edge(u,v)
            G.remove_edge(x,y)
            hubedges.remove((u,v))
            nothubedges.remove((x,y))
            if connected==1:
                if not nx.is_connected(G):
                    G.add_edge(u,v)
                    G.add_edge(x,y)
                    G.remove_edge(x, v)
                    hubedges.append((u, v))
                    nothubedges.append((x, y))
                    continue
        if tn >= max_tries:
            print('Maximum number of attempts (%s) exceeded ' % tn)
            break
        swapcount = swapcount + 1
        print(swapcount)
    return G




fh = open("IEEE162.txt", 'rb')
G = nx.read_edgelist(fh)
fh.close()
G0 = G.to_undirected()

sawpn = 1000
max_tries = 100000
rich_degree=5


G1 = rich_club_create(G0, rich_degree,sawpn, max_tries)
fh=open("IEEE162_rich.txt",'wb')
nx.write_edgelist(G1, fh, data=False)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print(n1)
print(m1)