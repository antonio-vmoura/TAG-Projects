"""
name: Antonio Vinicius de Moura Rodrigues

sources:
- https://medium.com/code-science/sudoku-solver-graph-coloring-8f1b4df47072 
- https://medium.com/codex/building-a-sudoku-solver-and-generator-in-python-1-3-f29d3ede6b23

"""

import random
from sudoku_connections import SudokuConnections

class sodukuSolver():

    def mapped_matrix(): #generates a matrix 9x9 of ids
        matrix = [[0 for cols in range(9)] for rows in range(9)]; count = 1

        for rows in range(9): 
            for cols in range(9):
                matrix[rows][cols] = count; count+=1
        return matrix

    def assemble_board(board): #assemble the sudoku so it can be shown

        draw_board = "\n"; parallel = " * - - - - - - - - - - - - - - * \n"
        
        for i in range(len(board)): 
            if i%3 == 0: draw_board += parallel

            for j in range(len(board[i])): 
                if j %3 == 0:
                    draw_board += " |  "
                if j == 8:
                    draw_board += f"{board[i][j]}  |    \n"
                else: 
                    draw_board += f"{board[i][j]} "

        draw_board += parallel

        return draw_board 

    def safe_color(sudoku_graph, v, color, c, given): #check if it is safe to put the color
        
        if v in given and color[v] == c: 
            return True
        elif v in given: 
            return False

        for i in range(1, sudoku_graph.graph.total_vertices+1):
            if color[i] == c and sudoku_graph.graph.is_neighbour(v, i):
                return False
            
        return True #returns True in case the color can be placed.

    def graph_color_utility(sudoku_graph, m, color, v, given):
        
        if v == sudoku_graph.graph.total_vertices+1: #if already checked all vertices returns True
            return True
        
        for c in range(1, m+1): 
            if sodukuSolver.safe_color(sudoku_graph, v, color, c, given) == True: 
                color[v] = c
                
                #if it's safe to put the color, it calls the function again to check the next vertex
                if sodukuSolver.graph_color_utility(sudoku_graph, m, color, v+1, given):
                    return True

            if v not in given: 
                color[v] = 0

    def graph_coloring_initialize_color(board, sudoku_graph, mapped_grid): #initialize the colors
        color = [0]*(sudoku_graph.graph.total_vertices+1)
        given = [] #list of numbers that have already been provided in sudoku

        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] != 0: #check if the position number has already been provided or not
                    idx = mapped_grid[row][col] #get the id of the position
                    color[idx] = board[row][col] #update the color
                    given.append(idx) #save the index of the given value

        return color, given

    def solve_graph_coloring(board, sudoku_graph, mapped_grid, m=9): #solves sudoku using graph coloring algorithm
        color, given = sodukuSolver.graph_coloring_initialize_color(board, sudoku_graph, mapped_grid)

        if sodukuSolver.graph_color_utility(sudoku_graph, m=m, color=color, v=1, given=given) is None:
            return False

        count = 1
        for row in range(9): 
            for col in range(9):
                board[row][col] = color[count]
                count += 1
        return color

    def check_sudoku(unsolved_board): #check and solve the sudoku solution
        sudoku_graph = SudokuConnections()
        mapped_grid = sodukuSolver.mapped_matrix()
        
        solved_board = [x[:] for x in unsolved_board] #copy the past board

        result = sodukuSolver.solve_graph_coloring(solved_board, sudoku_graph, mapped_grid, m=9)

        if result != False:
            return unsolved_board, solved_board
        else:
            return unsolved_board, False

    def generate_sudoku(difficulty="normal"): #generates a sudoku and its solution
        sudoku_graph = SudokuConnections()
        mapped_grid = sodukuSolver.mapped_matrix()
        init = []; solved_board = []

        #initializes the diagonal values with random numbers
        init.extend(random.sample(range(1, 9), 3))
        init.extend(random.sample(range(1, 9), 3))
        init.extend(random.sample(range(1, 9), 3))
        
        for x in range(0,9): #mounts to matrix with diagonal filled
            aux_list = [0,0,0,0,0,0,0,0,0]
            aux_list[x] = init[x]
            solved_board.append(aux_list)

        sodukuSolver.solve_graph_coloring(solved_board, sudoku_graph, mapped_grid, m=9)

        #check the difficulty to change the number of initialized fields
        if difficulty == "easy":
            chosen_ids = random.sample(range(1, 81), 40) #get random ids to make the game dynamic
        elif difficulty == "normal":
            chosen_ids = random.sample(range(1, 81), 30)
        elif difficulty == "hard":
            chosen_ids = random.sample(range(1, 81), 20)

        unsolved_board = [x[:] for x in solved_board] #copy the solved board

        for row in range(len(unsolved_board)):
            for col in range(len(unsolved_board[row])):
                if mapped_grid[row][col] not in chosen_ids:
                    unsolved_board[row][col] = 0

        return unsolved_board, solved_board

    def main():
        #keeping matrix that represents sudoku, 0's are empty fields
        unsolved_board = [
            [8,0,0,1,5,0,6,0,0],
            [0,0,0,3,0,0,0,4,1],
            [5,0,0,0,0,0,7,0,0],
            [0,0,0,0,0,9,0,6,2],
            [0,0,0,0,3,0,0,0,0],
            [1,4,0,8,0,0,0,0,0],
            [0,0,8,0,0,0,0,0,9],
            [2,9,0,0,0,1,0,0,0],
            [0,0,5,0,9,7,0,0,6]
        ]

        print("\n- - - - - - - - - - - - - - CHECKING SUDOKU - - - - - - - - - - - - - -\n")

        unsolved_board, solved_board = sodukuSolver.check_sudoku(unsolved_board) #calls the function that checks if the sudoku is valid

        if solved_board != False:
            print(f"- SUDOKU PAST:\n{sodukuSolver.assemble_board(unsolved_board)}\n- RESOLUTION OF THE PAST SUDOKU:\n{sodukuSolver.assemble_board(solved_board)}")
        else:
            print("O Sudoku não pode ser resolvido!\n")
        
        print("- - - - - - - - - - - - - - GENERATING SUDOKU - - - - - - - - - - - - - - -\n")

        difficulty = "normal"
        unsolved_board, solved_board = sodukuSolver.generate_sudoku(difficulty) #calls the function that generates the sudoku

        print(f"- SUDOKU GENERATED:\n- DIFFICULTY: {difficulty}\n{sodukuSolver.assemble_board(unsolved_board)}\n- RESOLUTION OF SUDOKU GENERATED:\n{sodukuSolver.assemble_board(solved_board)}") #printa o sudoku gerado e sua resolucao

if __name__ == "__main__": 
    sodukuSolver.main()
