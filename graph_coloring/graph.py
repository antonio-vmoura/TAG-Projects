class Node(): 

    def __init__(self, idx, data = 0): #constructor
        self.id = idx
        self.data = data
        self.connected_to = dict()

    def add_neighbour(self, neighbour , weight = 0):
        if neighbour.id not in self.connected_to.keys():  
            self.connected_to[neighbour.id] = weight

    def set_data(self, data): 
        self.data = data 

    def get_connections(self): 
        return self.connected_to.keys()

    def get_id(self): 
        return self.id
    
    def get_data(self): 
        return self.data

    def get_weight(self, neighbour): 
        return self.connected_to[neighbour.id]

    def __str__(self): 
        return str(self.data) + " connected with: " + str([x.data for x in self.connected_to])

class Graph():

    total_vertices = 0
    
    def __init__(self): #constructor
        self.allNodes = dict()

    def add_node(self, idx):
        if idx in self.allNodes: 
            return None
        
        Graph.total_vertices += 1
        node = Node(idx=idx)
        self.allNodes[idx] = node
        return node

    def add_node_data(self, idx, data):
        if idx in self.allNodes: 
            node = self.allNodes[idx]
            node.set_data(data)
        else: 
            print("invalid idx")

    def add_edge(self, src, dst, wt = 0): 
        self.allNodes[src].add_neighbour(self.allNodes[dst], wt)
        self.allNodes[dst].add_neighbour(self.allNodes[src], wt)
    
    def is_neighbour(self, u, v):
        if u >=1 and u <= 81 and v >=1 and v<= 81 and u !=v: 
            if v in self.allNodes[u].get_connections(): 
                return True
        return False

    def print_edges(self):
        for idx in self.allNodes:
            node =  self.allNodes[idx]
            for con in node.get_connections(): 
                print(node.get_id(), " --> ", self.allNodes[con].get_id())
    
    def get_node(self, idx): 
        if idx in self.allNodes: 
            return self.allNodes[idx]
        return None

    def get_all_nodes_ids(self): 
        return self.allNodes.keys()
