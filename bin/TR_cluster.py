# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 15:39:17 CST 2025

@author: zhengshang@frasergen.com zhengshang-zn@qq.com
"""
import sys
import networkx as nx
pair_file=sys.argv[1]
output_file=sys.argv[2]
#pair_file='FILTERED_tandem_repeats.blast.filter'
#output_file='after_clusterin_summary.xls'
pair_list=[]
with open(pair_file,'r') as obj:
    for line in obj:
        tmp=tuple(line.split())
        pair_list.append(tmp)

g = nx.Graph()
g.clear() #将图上元素清空
g.add_edges_from(pair_list)
connected_components = list(nx.connected_components(g))

TR_group=[]
count=0
for component in connected_components:
    count+=1
    subgraph = g.subgraph(component)
    degrees = dict(subgraph.degree())
    max_degree_node = max(degrees, key=degrees.get)
    TR_group.append(["CL{}".format(count),max_degree_node,list(set(component))])


tmp_list=[]
Copy_num=0
raw_result=[]
for group_id , Monomer_id , group_list in TR_group:
    Monomer_len=int(Monomer_id.split("_")[1])
    for i in group_list:
        tmp=i.split("_")
        Copy_num+=(int(tmp[1])*float(tmp[2])/Monomer_len)
        tmp_list.append(i)
    raw_result.append([group_id , Monomer_id,Monomer_len,Copy_num,','.join(tmp_list)])
    tmp_list=[]
    Copy_num=0

#去掉总大小小于10,000bp的图
fin_result=[i for i in raw_result if i[2]*i[3]>10000]

f=open(output_file,'w')
f.write("Cluster ID\tSignificant monomer id\tMonomer length\tCopy num\tTR group\n")
for i in fin_result:
    f.write("{}\t{}\t{}\t{}\t{}\n".format(i[0],i[1],i[2],i[3],i[4]))
    
f.close()
  

  

