from graph import Graph

class SudokuConnections(): 
    def __init__(self): #constructor

        self.graph = Graph()

        self.rows = 9
        self.cols = 9
        self.total_blocks = self.rows*self.cols

        self.generate_graph() #generate all nodes
        self.connect_edges() #connect all nodes according to sudoku restrictions

        self.all_ids = self.graph.get_all_nodes_ids() #store all ids in a list

    def generate_graph(self):
        for idx in range(1, self.total_blocks+1): 
            _ = self.graph.add_node(idx)

    def connect_edges(self):
        matrix = self.get_grid_matrix(); head_connections = dict()

        for row in range(9):
            for col in range(9): 
                head = matrix[row][col]
                connections = self.what_to_connect(matrix, row, col)
                head_connections[head] = connections

        self.connect_those(head_connections=head_connections)
        
    def connect_those(self, head_connections): 
        for head in head_connections.keys():
            connections = head_connections[head]

            for key in connections:  #get the list of all connections
                for v in connections[key]: 
                    self.graph.add_edge(src=head, dst=v)
 
    def what_to_connect(self, matrix, rows, cols):
        connections = dict(); row = []; col = []; block = []

        #linhas
        for c in range(cols+1, 9): 
            row.append(matrix[rows][c])
        
        #colunas
        for r in range(rows+1, 9):
            col.append(matrix[r][cols])

        #blocos
        if rows%3 == 0:
            if cols%3 == 0:
                block.append(matrix[rows+1][cols+1])
                block.append(matrix[rows+1][cols+2])
                block.append(matrix[rows+2][cols+1])
                block.append(matrix[rows+2][cols+2])

            elif cols%3 == 1:
                block.append(matrix[rows+1][cols-1])
                block.append(matrix[rows+1][cols+1])
                block.append(matrix[rows+2][cols-1])
                block.append(matrix[rows+2][cols+1])
                
            elif cols%3 == 2:
                block.append(matrix[rows+1][cols-2])
                block.append(matrix[rows+1][cols-1])
                block.append(matrix[rows+2][cols-2])
                block.append(matrix[rows+2][cols-1])

        elif rows%3 == 1:
            if cols%3 == 0:
                block.append(matrix[rows-1][cols+1])
                block.append(matrix[rows-1][cols+2])
                block.append(matrix[rows+1][cols+1])
                block.append(matrix[rows+1][cols+2])

            elif cols%3 == 1:
                block.append(matrix[rows-1][cols-1])
                block.append(matrix[rows-1][cols+1])
                block.append(matrix[rows+1][cols-1])
                block.append(matrix[rows+1][cols+1])
                
            elif cols%3 == 2:
                block.append(matrix[rows-1][cols-2])
                block.append(matrix[rows-1][cols-1])
                block.append(matrix[rows+1][cols-2])
                block.append(matrix[rows+1][cols-1])

        elif rows%3 == 2:
            if cols%3 == 0:
                block.append(matrix[rows-2][cols+1])
                block.append(matrix[rows-2][cols+2])
                block.append(matrix[rows-1][cols+1])
                block.append(matrix[rows-1][cols+2])

            elif cols%3 == 1:
                block.append(matrix[rows-2][cols-1])
                block.append(matrix[rows-2][cols+1])
                block.append(matrix[rows-1][cols-1])
                block.append(matrix[rows-1][cols+1])
                
            elif cols%3 == 2:
                block.append(matrix[rows-2][cols-2])
                block.append(matrix[rows-2][cols-1])
                block.append(matrix[rows-1][cols-2])
                block.append(matrix[rows-1][cols-1])
        
        connections["rows"] = row; connections["cols"] = col; connections["blocks"] = block

        return connections

    def get_grid_matrix(self): 
        matrix = [[0 for cols in range(self.cols)] for rows in range(self.rows)]; count = 1
        
        for rows in range(9):
            for cols in range(9):
                matrix[rows][cols] = count; count+=1

        return matrix

