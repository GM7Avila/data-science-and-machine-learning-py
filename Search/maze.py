import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

# Fronteira - implementada por stack (DFS)     
class StackFrontier():
    def __init__(self):
        self.frontier = []
        
    def add(self, node):
        self.frontier.append(node)
        
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0 
    
    # remove e retorna o último nó da stack - LIFO
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

# Fronteira - implementação por fila (BFS)     
class QueueFrontier(StackFrontier):
    
    # remove e retorna o primeiro nó - FIFO
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            
class Maze():

    # mepeamento do labirinto
    def __init__(self, filename):
        # lê o arquivo
        with open(filename) as f:
            contents = f.read()

        # verifica se possui início e fim no labirinto (validação)
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # determina a altura e largura do labirinto
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # lista bidimensional para manter o rastreamento das paredes
        self.walls = []
        
        # itera sobre as linhas do labirinto (height)
        for i in range(self.height):
            row = []
            # itera sobre as colunas x linha
            for j in range(self.width):
                try:
                    # verifica se é o ponto de partida
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    # verifica se é o objetivo
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    # se for vazio, adiciona False na posição / sem parede
                    elif contents[i][j] == " ":
                        row.append(False)
                    # parede
                    else:
                        row.append(True)        
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        # armazena a solução do labirinto - a ser preenchido
        self.solution = None

        
    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()        

    # Encontrar os vizinhos dentro de um state (posição)
    def neighbors(self, state):
        row, col = state
        
        # lista que contem tuplas dos vizinhos
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        # resultado de vizinhos válidos encontrados
        result = []
        
        # itera sobre cada tupla em candidates
            # desempacota a action (direção) e as coordenadas do vizinho atual
        for action, (r, c) in candidates:
            # verifica se o vizinho é considerado valido 
                # se esta dentro do limite do labirinto e não é ma parade
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                # se o vizinho for valido adiciona a direção (action) e as coordenadas (r,c) à lista result
                result.append((action, (r, c)))
        return result