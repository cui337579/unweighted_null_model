
# encoding=utf8

import networkx as nx  # 导入networkx网络分析模块，缩写为nx
import random  # 导入random包
import numpy as np
import igraph as ig
import copy


def edge_in_community(node_community_list, edge):
    # 功能: 判断某条边是不是社团内部连边
    # node_community_list是网络中节点的社团归属信息
    # edge是网络中的一条连边
    # 返回布尔变量：如果是社团内部连边，返回值为1；如果是社团外部连边，返回值为0
    return_value = 0
    for community_i in node_community_list:
        if edge[0] in community_i and edge[1] in community_i:  # 拿出边的两个节点
            return_value += 1
            return 1
    if return_value == 0:
        return 0


def dict_degree_nodes(degree_node_list):
    # 返回的字典为{度：[节点1，节点2，..]}，其中节点1和节点2有相同的度
    D = {}
    for degree_node_i in degree_node_list:
        if degree_node_i[0] not in D:
            D[degree_node_i[0]] = [degree_node_i[1]]
        else:
            D[degree_node_i[0]].append(degree_node_i[1])
    return D

def Q_increase(G0 ,node_community_list ,nswap=1, max_tries=100):
    # 保证度分布不变的情况下，增强社团结构特性
    # G0：待改变结构的网络
    # node_community_list：是网络中节点的社团归属信息
    # nswap：是改变成功的系数，默认值为1
    # max_tries：是尝试改变的次数，默认值为100

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
        if tn >= max_tries:
            e=('尝试次数 (%s)  已超过允许的最大次数'%tn + '有效交换次 数 （%s)'%swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui,xi)=nx.utils .discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u,v,x,y])) == 4: # 保 证是四个独立节点
            if edge_in_community(node_community_list,(u,v))==0 and edge_in_community(node_community_list,(x,y))==0:  # 保证所取的连边为社团间连边
                if edge_in_community(node_community_list,(u,y))==1 and edge_in_community(node_community_list,(v,x))==1:  # 保证新生成的边是内部连边
                    if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络  不存在的边
                        G.add_edge(u,y)  # 增加两条新连边
                        G.add_edge(v,x)
                        G.remove_edge(u,v)  # 删除两条旧连边
                        G.remove_edge(x,y)
                        swapcount+=1  # 改 变成 功次数加1

    return G

def Q_decrease(G0,node_community_list,nswap=1,max_tries=100):
    # 保证度分布不变的情况下，减弱社团结构特性
    # G0：待改变结构的网络
    # node_community_list：是网络中节点的社团归属信息
    # nswap：是改变成功的系数，默认值为1
    # max_tries：是尝试改变的次数，默认值为100

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
    keys,degrees = zip(* G.degree())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < nswap:  # 有效交换次数  数
        if tn >= max_tries:
            e=('尝试次数 (%s) 已超过允许的最大次数'%tn + ',有效交换次数为(% s )'%swapcount)
            print (e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))


        if len(set([u,v,x,y] )) == 4:  # 保  为四个独立节点
            if edge_in_community(node_community_list,(u,v ))==1 and edge_in_community(node_community_list,(x,y))== 1: # 保 证所  的连边是社团内部连边
                if edge_in_community(node_community_list,(u,y)) ==0 and edge_in_community(node_community_list,(v,x))== 0:  #  保证 新生  的边是社团间的连边
                    if (y not in G[u]) and (v not in G[x]):  # 保证新生  的连边是原网络中不存在的边
                        G.add_edge(u,y)  # 增加两条新连边
                        G.add_edge(v,x)
                        G.remove_edge(u,v)  # 删除两条旧连边
                        G.remove_edge(x,y)
                        swapcount+=1							  # 改变成功次数加1

    return G
