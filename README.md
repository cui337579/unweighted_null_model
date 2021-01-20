无权零模型
================
unweighted_nopath文件下
================
unweighted_null_model.py
------
    该文件包含了基于断边重连的0、1、2、2.5、3阶零模型
    其中需要的包为networkx2.5，环境为python3
tool_inorde.py
-------
     该文件包含了基于断边重连的最强富人俱乐部、最弱富人俱乐部、最强同配、最强异配、最强聚类系数、最弱聚类系数零模型算法
     其中需要的包为networkx2.5，环境为python3
community_class.py
--------
    该文件包含了基于断边重连的1、2、3、2.5阶社团内部零模型,1、2、3、2.5阶社团间零模型以及增强社团、减弱社团零模型算法
    其中需要的包为igraph0.7.1(pycairo-1.18.2)、networkx2.2，环境为python2
说明
-----
    每个py文件里都有调用函数的代码，只需要把函数名、读取文件和生成文件的名字改变一下就可以生成不同的零模型。其中社团零模型部分多了一个node_community_list参数


