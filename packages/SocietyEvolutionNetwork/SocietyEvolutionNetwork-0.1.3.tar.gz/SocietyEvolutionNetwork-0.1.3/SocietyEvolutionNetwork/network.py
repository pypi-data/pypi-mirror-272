import redis
import yaml
import sys, os
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
from redisgraph import Node, Edge, Graph

class CRedisGraph:
    def __init__(self, host, port, password, graph_name, direction=0):
        """
        0 无向图 1 有向图
        """
        # seed = 0
        # random.seed(seed)
        # np.random.seed(seed)
        self.nx = nx
        if direction == 0:
            self.nx_graph = nx.Graph()
        else:
            self.nx_graph = nx.DiGraph()

        # 图表操作
        self.graph_name = graph_name
        self.network = redis.Redis(host=host, port=port, db=0, password=password)
        self.network_graph = Graph(self.graph_name, self.network)

    def add_node(self, node_label, kargs) -> None:
        """
        @params: node_label   ->   str 
        @params: kargs      ->  dict
        @desc: 添加节点数据
        """
        node = Node(label=node_label, properties=kargs)
        self.network_graph.merge(node)
        self.network_graph.commit()
        # return node

    def update_node_attr(self, id, kargs) -> None:
        """
        @params: id   ->   str 
        @params: kargs      ->  dict
        @desc: 更新节点数据
        """
        # 查找这个id的是哪个标签的
        try:
            query = f"MATCH (n {{id: '{id}'}}) RETURN n"
            result = self.network_graph.query(query)
            node_label = result.result_set[0][0].label
        except Exception as e:
            print("[update_node_attr] - [update failed] - [node aren't exist!]")
            return

        set_fields = ", ".join([f"{'n.'+key} = '{value}'" for key, value in kargs.items()])
        print("set_fields: ", set_fields)
        query = f"MERGE (n: {node_label} {{id: '{id}'}}) SET {set_fields} RETURN n"
        # MATCH (n:person {id: '1'}) SET n.name = 'zhl', n.id = '1', n.age = '40'
        print("update query: ", query)
        self.network_graph.query(query)
        self.network_graph.commit()

    def remove_node(self, id) -> None:
        """
        @params: node_set   ->  str
        @prams: id
        """
        query = f"MATCH (n {{id: '{id}'}}) DELETE n"
        self.network_graph.query(query)

    def query_node_attr(self, id) -> dict:
        """
        @params: id -> str
        """
        # 查找这个id的是哪个标签的
        query = f"MATCH (n {{id: '{id}'}}) RETURN n"
        result = self.network_graph.query(query)
        node_label = result.result_set[0][0].label

        # 查询节点属性
        query = f"MATCH (n:{node_label} {{id: '{id}'}}) RETURN n"
        result = self.network_graph.query(query)
        return result.result_set[0][0].properties

    def query_all_node(self) -> dict:
        """
        @params: None
        @desc: 查询所有的节点数据
        """
        query = "MATCH (x) RETURN x"
        result = self.network_graph.query(query)
        
        node_list = {}
        for sublist in result.result_set:
            for node in sublist:    
                if node.label not in node_list:
                    node_list[node.label] = []
                node_list[node.label].append(node.properties)

        return node_list

    def add_edge(self, u_of_node, relation, v_of_node, kargs) -> None:
        """
        @params: u_of_node  ->  str
        @params: relation   ->  str
        @params: v_of_node  ->  str
        @prams: kargs   -> dict
        """
        # 查找边的关系, 如果存在就不插入边
        query = f"MATCH (a)-[r]->(b) WHERE a.id = '{u_of_node}' AND b.id = '{v_of_node}' RETURN a, b"
        data = self.network_graph.query(query).result_set
        print("add_edge: ", data)

        if 0 != len(data):
            print("[CMD] - [add_edge] - [add failed] - [edge exist]")
            return


        # 增加边
        query = (
            f"MATCH (a {{id: '{u_of_node}'}}), (b {{id: '{v_of_node}'}})"
            f"CREATE (a)-[:{relation} {{{', '.join(f'{key}: {value}' for key, value in kargs.items())}}}]->(b {{id: '{v_of_node}'}})"
        )
 
        # print("query1: ", query)
        self.network_graph.query(query)
        self.network_graph.commit()
        print(22222)

    def query_edge_attr(self, u_of_node, v_of_node) -> dict:
        """
        @params: u_of_node
        @params: v_of_node
        @params: 查询2个节点直接的关系连线
        @returns: 返回字典, 关于有label和properties
            {
                '1': {'label': 'person', 'properties': {'age': 30, 'id': '1', 'name': 'zhl'}}, 
                'relation': {'label': 'friend', 'properties': {'distance': '80'}},
                '2': {'label': 'person', 'properties': {'age': 30, 'id': '2', 'name': 'ljw'}}
            }
        """
        # query = "MATCH (n1:person {id: '1'})-[r]->(n2:person {id: '2'}) RETURN n1, r, n2"
        query = f"MATCH (n1)-[r]->(n2) WHERE n1.id = '{u_of_node}' AND n2.id = '{v_of_node}' RETURN n1, r, n2"
        # print("query2: ", query)
        try:
            query_data = self.network_graph.query(query).result_set[0]
            print("query_edge_attr: ", query_data[0].label)
            result_dict = {
                str(u_of_node): {
                    "label": query_data[0].label,
                    "properties": query_data[0].properties
                },
                "relation": {
                    "label": query_data[1].relation,
                    "properties": query_data[1].properties
                },
                str(v_of_node): {
                    "label": query_data[2].label,
                    "properties": query_data[2].properties
                },
            }

            return result_dict
        except Exception as e:
            print("[query_edge_attr] - [query failed] - [edge aren't found!]")
            return None

    def remove_edge(self, u_of_node, v_of_node):
        """
        @prams: u_of_node   -> str
        @prams: v_of_node   -> str
        @desc: 移除2个节点直接的关系连线
        """
        query = f"MATCH (n1)-[r]->(n2) WHERE n1.id = '{u_of_node}' AND n2.id = '{v_of_node}' DELETE r"
        self.network_graph.query(query)

    def update_edge_attr(self, u_of_node, v_of_node, kargs):
        """
        @prams: u_of_node   -> str
        @prams: v_of_node   -> str
        @params: kargs  ->  dict
        @desc: 更新边的属性
        """
        # 查找边的关系
        edge_data = self.query_edge_attr(u_of_node, v_of_node)
        if edge_data != None:
            relation = edge_data['relation']['label']
        # print("relation: ", relation)
        set_fields = ", ".join([f"{'r.'+key} = '{value}'" for key, value in kargs.items()])
        query = f"MATCH (a)-[r]->(b) WHERE a.id = '{u_of_node}' AND b.id = '{v_of_node}' SET {set_fields}"
        # query = f"MATCH (a)-[old_rel:{uv_relation}]->(b) WHERE a.id = '{u_of_node}' AND b.id = '{v_of_node}' DELETE old_rel CREATE (a)-[:{relation}]->(b)"

        self.network_graph.query(query)
        self.network_graph.commit()

    def update_edge_relation(self, u_of_node, v_of_node, relation):
        """
        @prams: u_of_node   -> str
        @prams: v_of_node   -> str
        @params: kargs  ->  dict
        @desc: 更新边的关系
        """
        # 先查找关系, 删除旧的关系, 再赋值新的关系[必须做的理由: 节点的度会增加, 所以要禁止插入重复的数据]
        try:
            query = f"MATCH (a)-[r]->(b) RETURN r"
            uv_relation = self.network_graph.query(query).result_set[0][0].relation
        except Exception as e:
            print("[update_edge_relation] - [update failed] - [edge aren't found!]")
        
        # MATCH (a)-[old_rel:friends1]->(b) WHERE a.id = '7' AND b.id = '8' DELETE old_rel CREATE (a)-[:friends1]->(b)  更新语句示例
        query = f"MATCH (a)-[old_rel:{uv_relation}]->(b) WHERE a.id = '{u_of_node}' AND b.id = '{v_of_node}' DELETE old_rel CREATE (a)-[:{relation}]->(b)"
        # print("query3: ", query)
        self.network_graph.query(query)
        self.network_graph.commit()

    def show_graph(self):
        # 使用nx来进行图形展示
        all_edges = self.query_all_edges()
        print("all_edge: ", all_edges)

        for all_edge in all_edges:
            u_of_node, v_of_node = all_edge[0], all_edge[1]
            dict_edge = self.query_edge_attr(u_of_node, v_of_node)
            relation = dict_edge['relation']['label']
            kargs = dict_edge['relation']['properties']
            print("relation: ", relation)
            self.nx_graph.add_node(u_of_node)
            self.nx_graph.add_node(v_of_node)
            self.nx_graph.add_edge(u_of_node, v_of_node, type=relation, **kargs)

        self.nx.draw(self.nx_graph, with_labels=True)
        plt.show()

        # print("Graph cannot be directly visualized showing graph")

    def query_all_edges(self):
        """
        @prams: u_of_node   -> str
        @prams: v_of_node   -> str
        @params: kargs  ->  dict
        @desc: 查找所有的边
        """
        query = "MATCH (a)-[r]->(b) RETURN a.id, b.id"
        try:
            data = self.network_graph.query(query).result_set
            print("query_all_edges: ", data)
            return data
        except Exception as e:
            print("")

    def query_node_degree(self, node):
        """
        @params: node
        @desc: 查找节点的度
        """
        query = f"MATCH (a)-[r]-(b) WHERE a.id = '{node}' RETURN count(r)"
        try:
            data = self.network_graph.query(query).result_set[0][0]
            print("query_node_degree: ", data)
            return data
        except Exception as e:
            print("error")

    def query_node_neighbors(self, node):
        """
        @params: node
        @desc: 查找节点的邻居节点
        """
        query = f"MATCH (a)-[r]-(b) WHERE a.id = '{node}' RETURN collect(b.id)"
        try:
            data = self.network_graph.query(query).result_set[0][0]
            print("query_node_neighbors: ", data)
            return data
        except Exception as e:
            print("error")
    
    def delete_graph(self):
        """
        @params: None
        @desc: 删除图表
        """
        try:
            self.network_graph.delete()
        except Exception as e:
            print('No Graph! ')