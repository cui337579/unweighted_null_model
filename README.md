无权零模型
================
unweighted_nopath文件下
================
tool_inorde/richclub.py
----------
    该文件实现的是富人俱乐部零模型算法
    其中函数rich_club_create实现的是生成最强富人俱乐部零模型，该函数的系数中，G0是图文件，rich_degree是设置的富边系数（默认为5），swapn为有效交换次数，max_tries为最大尝试次数。
    函数rich_club_break实现的是生成最弱富人俱乐部零模型，其中系数和上面一样。
    两个函数的调用代码是通用的，只需要改函数名即可，拿最强富人俱乐部零模型算法为例：
    ===================================
    fh = open("IEEE118.txt", 'rb')   //打开图文件
    G = nx.read_edgelist(fh)   //将图赋值给G
    fh.close()
    G0 = G.to_undirected()    //将有向图转化为无向图（确保图为无向图）

    swapn = 1000             //有效交换次数
    max_tries = 100000      //最大尝试次数
    rich_degree=5          //定义富边系数

    G1 = rich_club_create(G0, rich_degree,swapn, max_tries)   //函数调用
    fh=open("IEEE162_rich.txt",'wb')
    nx.write_edgelist(G1, fh, data=False)  //将结果保存为txt图文件
    fh.close()
    ===================================
    其中需要的包为networkx2.5，环境为python3。
tool_inorde/match.py
----------
    该文件实现的是同配/异配零模型算法
    其中函数assort_mixing实现的是生成最强同配零模型，该函数的系数中，G0是图文件，nswap为有效交换次数，max_tries为最大尝试次数。
    函数disassort_mixing实现的是生成最强异配零模型，其中系数和上面一样。
    两个函数的调用代码是通用的，只需要改函数名即可，拿最强同配零模型算法为例：
    ===================================
    fh = open("IEEE118.txt",'rb') //打开图文件
    G = nx.read_edgelist(fh)    //将图赋值给G
    fh.close()
    G0 = G.to_undirected()  //将有向图转化为无向图（确保图为无向图）

    nswap = 1000            
    max_tries = 100000          

    G1 = assort_mixing(G0,nswap,max_tries)
    fh = open("IEEE118_assort.txt",'wb')
    nx.write_edgelist(G1,fh,data=False) //将结果保存为txt图文件
    fh.close() 
    ===================================
    其中需要的包为networkx2.5，环境为python3。
tool_inorde/Clustering coefficient.py
--------
    该文件实现的是聚类系数零模型算法
    其中函数enhanceClu实现的是生成最强聚类系数零模型，该函数的系数中，G0是图文件，nswap为有效交换次数，max_tries为最大尝试次数。
    函数weakenClu实现的是生成最弱聚类系数零模型，其中系数和上面一样。
    两个函数的调用代码是通用的，只需要改函数名即可，以最强聚类系数模型算法为例：
    ===================================
    fh = open("IEEE118.txt",'rb') //打开图文件
    G = nx.read_edgelist(fh)    //将图赋值给G
    fh.close()
    G0 = G.to_undirected()  //将有向图转化为无向图（确保图为无向图）

    nswap = 1000            
    max_tries = 100000          

    G1 = enhanceClu(G0,nswap,max_tries,connected=1)
    fh = open("IEEE118_enhanceCluenhanceClu.txt",'wb')
    nx.write_edgelist(G1,fh,data=False)     //将结果保存为txt图文件
    fh.close() 
    ===================================
    其中需要的包为networkx2.5，环境为python3。
unweighted_null_model.py
------
    该文件包含了基于断边重连的0、1、2、2.5、3阶零模型
    调用代码是通用的，只需要改函数名即可，以1阶零模型算法为例：
    ===================================
    fh = open("IEEE118.txt",'rb') //打开图文件
    G = nx.read_edgelist(fh)    //将图赋值给G
    fh.close()
    G0 = G.to_undirected()  //将有向图转化为无向图（确保图为无向图）

    nswap = 1000            
    max_tries = 100000          

    G1 = random_1k(G0,nswap,max_tries,connected=1)
    fh = open("IEEE118_1K.txt",'wb')
    nx.write_edgelist(G1,fh,data=False)     //将结果保存为txt图文件
    fh.close() 
    ===================================
    其中需要的包为networkx2.5，环境为python3
community_class.py
--------
    该文件包含了基于断边重连的1、2、3、2.5阶社团内部零模型,1、2、3、2.5阶社团间零模型以及增强社团、减弱社团零模型算法
    其中需要的包为igraph0.7.1(pycairo-1.18.2)、networkx2.2，环境为python2.7,在python3环境下，程序会报错运行不了。
    调用代码是通用的，只需改函数名即可，以增强社团零模型算法为例：
    ===================================
    G0=nx.read_edgelist('IEEE300.txt')  //读取图文件
    M=nx.number_of_edges(G0)
    Gi = ig.Graph.Read_Edgelist("IEEE300.txt")  # 基于这些连边使用igraph创建一个新网络
    Gi = Gi.as_undirected()
    community_list0 = Gi.community_multilevel(weights=None,return_levels=False) //得到图的社团列表
    community_list1 = []
    for item in community_list0:
        community_list1.append(item)
    del community_list1[0] // 去掉列表头部的无效元素
    community_list_s=community_list1
    for i in range(0,len(community_list1)):
        community_list_s[i]=map(str, community_list1[i])  //转换成字符串列表
    G=Q_increase(G0,community_list_s,nswap=200, max_tries=100000)  //调用算法
    nx.write_edgelist(G,'IEEE300_decrease.txt',data=False) //将新生成的图保存到图文件中

    Gi=ig.Graph.Read_Edgelist("IEEE300_increase.txt") 
    Gii=Gi.as_undirected()   
    communities = Gii.community_multilevel(weights=None, return_levels=False)
    Q=Gii.modularity(communities,weights=None)
    print Q   //计算新生成网络的Q值
    ===================================
说明
-----
    每个py文件里都有调用函数的代码，只需要把函数名、读取文件和生成文件的名字改变一下就可以生成不同的零模型。其中社团零模型部分多了一个node_community_list参数、富人俱乐部零模型部分多了rich_degree参数。
    其中有效交换次数和最大尝试次数是需要在多次尝试之后得到的一个趋于稳定的结果，有效交换次数必须小于最大尝试次数。


