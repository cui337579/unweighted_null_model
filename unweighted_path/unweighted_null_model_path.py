import networkx as nx
import random
import copy



#在基本保持平均路径长度不变情况下
#最强富人零网络
def rich_club_create_path(G0, k=1, nswap=1, max_tries=100, connected=1):
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
    path = nx.average_shortest_path_length(G)
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
            new_path = nx.average_shortest_path_length(G)
            ret = abs(path - new_path)
            if ret > 0.1:
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
    return G


#在基本保持平均路径长度不变情况下
#最弱富人零网络

def rich_club_break_path(G0,k=10,nswap=1,max_tries=100,connected=1):

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
    print(hubedges)
    print(nothubedges)
    path = nx.average_shortest_path_length(G)
    print(path)
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
                    G.remove_edge(u,y)
                    hubedges.append((u, v))
                    nothubedges.append((x, y))
                    continue
            new_path = nx.average_shortest_path_length(G)
            ret = abs(path - new_path)
            if ret > 0.1:
                G.add_edge(u, v)
                G.add_edge(x, y)
                G.remove_edge(x, v)
                G.remove_edge(u, y)
                hubedges.append((u, v))
                nothubedges.append((x, y))
                continue
        if tn >= max_tries:
            print('Maximum number of attempts (%s) exceeded ' % tn)
            break
        swapcount = swapcount + 1
    print(swapcount)
    return G


#在基本保持平均路径长度不变情况下
#最强同配零网络
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
    path = nx.average_shortest_path_length(G)
    print(path)
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
            new_path = nx.average_shortest_path_length(G)
            ret = abs(path - new_path)
            if ret > 0.1:
                G.remove_edge(sortednodes[0], sortednodes[1])
                G.remove_edge(sortednodes[2], sortednodes[3])
                G.add_edge(x, y)
                G.add_edge(u, v)
                continue
        if tn >= max_tries:
            print('Maximum number of swap attempts '+str(tn)+' exceeded , before desired swaps achieved '+str(nswap))
            break
        swapcount = swapcount+1
    print(swapcount)
    newpath = nx.average_shortest_path_length(G)
    print(newpath)
    return G


#在基本保持平均路径长度不变情况下
#最弱同配零网络

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
    path = nx.average_shortest_path_length(G)
    print(path)
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
            new_path = nx.average_shortest_path_length(G)
            ret = abs(path - new_path)
            if ret > 0.1:
                G.remove_edge(sortednodes[0], sortednodes[3])
                G.remove_edge(sortednodes[1], sortednodes[2])
                G.add_edge(x, y)
                G.add_edge(u, v)
                continue
        if tn >= max_tries:
            print('Maximum number of swap attempts '+str(tn)+' exceeded , before desired swaps achieved '+str(nswap))
            break
        swapcount+=1
    print(swapcount)
    return G

#在基本保持平均路径长度不变情况下
#最强聚类系数零网络

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
    path = nx.average_shortest_path_length(G)
    print(path)
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
        new_path = nx.average_shortest_path_length(G)
        ret = abs(path - new_path)
        if ret > 0.1:
            G.add_edge(u, v)
            G.add_edge(x, y)
            G.remove_edge(u, y)
            G.remove_edge(x, v)
            continue
        swapcount=swapcount+1
    print(swapcount)
    return G

#在基本保持平均路径长度不变情况下
#最弱聚类系数零网络

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
    path = nx.average_shortest_path_length(G)
    print(path)
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
        new_path = nx.average_shortest_path_length(G)
        ret = abs(path - new_path)
        if ret > 0.1:
            G.add_edge(u, v)
            G.add_edge(x, y)
            G.remove_edge(u, y)
            G.remove_edge(x, v)
            continue
        swapcount=swapcount+1
    return G
