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
            self.frontier = self.frontier[1:]
            return node
            
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
    
    def solve_dfs(self):
        print("Solving with Deep-First Search...")
        # numero de estados explorados
        self.num_explored = 0

        # cria o node inicial
        start = Node(state=self.start, parent=None, action=None)
        
        # inicializa a fronteira stack e adiciona o node 
        frontier = StackFrontier()
        frontier.add(start)

        # cria um set de explorados
        self.explored = set()

        # loop - buscando por solução
        while True:

            # se não há nada na fronteira então não a solução
            if frontier.empty():
                raise Exception("no solution")

            # pega um node da fronteira e incrementa o contador de explorados
            node = frontier.remove()
            self.num_explored += 1

            # armazenando a solução se o nó atual é o goal (i,j)
            if node.state == self.goal:
                
                actions = []
                cells = []
                
                # backtracking do goal ao inicial
                    # cada nó armazena o nó pai que o levou até certo ponto
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # move o nó para o set de explorados
            self.explored.add(node.state)

            # adiciona os vizinhos a fronteira
            for action, state in self.neighbors(node.state):
                
                # se o nó não foi explorado e não esta na fronteira
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
                                   
    def solve_bfs(self):
        print("Solving with Breadth-First Search...")
        
        # numero de estados explorados
        self.num_explored = 0

        # cria o node inicial
        start = Node(state=self.start, parent=None, action=None)
        
        # inicializa a fronteira (fila) e adiciona o node 
        frontier = QueueFrontier()
        frontier.add(start)

        # cria um set de explorados
        self.explored = set()
        

        # loop - buscando por solução
        while True:

            # se não há nada na fronteira então não a solução
            if frontier.empty():
                raise Exception("no solution")

            # pega um node da fronteira e incrementa o contador de explorados
            node = frontier.remove()
            self.num_explored += 1

            # armazenando a solução se o nó atual é o goal (i,j)
            if node.state == self.goal:
                
                actions = []
                cells = []
                
                # backtracking do goal ao inicial
                    # cada nó armazena o nó pai que o levou até certo ponto
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # move o nó para o set de explorados
            self.explored.add(node.state)

            # adiciona os vizinhos a fronteira
            for action, state in self.neighbors(node.state):
                
                # se o nó não foi explorado e não esta na fronteira
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

# Executando DFS
m = Maze(sys.argv[1])
print("Maze:")
m.print()
m.solve_dfs()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze_dfs.png", show_explored=True)

# Executando BFS
m.solve_bfs()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze_bfs.png", show_explored=True)