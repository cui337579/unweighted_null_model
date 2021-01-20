无权零模型
================
unweighted_null_model.py
------
    该文件包含了基于断边重连的0、1、2、2.5、3阶零模型，以及强富人俱乐部、弱富人俱乐部、强同配、强异配零模型的算法
    其中需要的包为networkx2.5，环境为python3
InOrDeClu.py
-------
     该文件包含了基于断边重连的增强和减弱聚类系数零模型的算法
     其中需要的包为networkx2.5，环境为python3
inner_random.py
--------
    该文件包含了基于断边重连的1、2、3、2.5阶社团内部零模型的算法
    其中需要的包为igraph0.7.1(pycairo-1.18.2)、networkx2.2，环境为python2
inter_random.py
---------
    该文件包含了基于断边重连的额1、2、3、2.5阶社团间零模型的算法
    其中需要的包为igraph0.7.1(pycairo-1.18.2)、networkx2.2，环境为python2
InOrDeComm.py
------
    该文件包含了增强社团和减弱社团零模型的算法
    其中需要的包为igraph0.7.1(pycairo-1.18.2)、networkx2.2，环境为python2
说明
-----
    每个py文件里都有调用函数的代码，只需要把函数名、读取文件和生成文件的名字改变一下就可以生成不同的零模型。其中社团零模型部分多了一个node_community_list参数


