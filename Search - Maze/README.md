# MAZE - Deep First Search & Breadth-First Search
## Sobre
Resolução de labirinto por Busca em Profundidade (DFS) e Busca em Largura (BFS).

## Requisitos
`$ pip install Pillow`

## Executando 
- Execute o arquivo `maze.py` utilizando Python, e passe `maze.txt` como argumento:
    - `python3 "maze.py" "maze.txt"`.

## Output
- Ao executar, duas imagens serão geradas como saida:
	- `maze_dfs.png`: Resolução do labirinto por Deep-First search	
	- `maze_bfs.png`: Resolução do labirinto por Breadth-First search
    
- Você pode desabilitar/habilitar os caminhos explorados em : `m.output_image("maze.png", show_explored=False)`, alterando o valor de show_explored;

## Labirinto

O labirinto é representado por um arquivo de texto (maze.txt): 

    "A" indica o ponto de partida.
    "B" indica o objetivo.
    Espaços vazios representam caminhos possíveis.
    "#" (ou caracteres não vazios) representam paredes.

```
############
#A  #     B#
#   # ######
# ####     #
#         ##
# ##########
#          #
############
```
