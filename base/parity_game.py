import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from typing import Set, Tuple
import pydot

class Game:
    class Node:
        def __init__(self, owner: int, priority: int, edges: Set[int]):
            self.owner = owner
            self.priority = priority
            self.edges = edges
        
        def add_edge(self, edge: int):

            self.edges.add(edge)
        
        def __repr__(self) -> str:
            return f'i = {self.owner}, p = {self.priority}, {self.edges}'


    def __init__(self, vertices: Set[Tuple[int, Tuple[int, int]]], edges: Set[Tuple[int, int]] ) -> None:

        self.dict = {}
        self.edges = edges

        for vert, info in vertices:
            self.dict[vert] = Game.Node(*info, set([]))
        
        for edge in edges:
            self.dict[edge[0]].add_edge(edge[1])

    def max_priority(self) -> int:
        # returns the max priority
        if len(self) == 0:
            return 0

        return max([node.priority for node in self.dict.values()])

    def exclude(self, to_excl: Set[int]) -> "Game":
        # not particularly efficient but this isn't the important bit
        # if len(to_excl) == 0:
        #     return self
        assert self.nodes().issuperset(to_excl)

        remaining = self.nodes().difference(to_excl)
        info = [(self[key].owner, self[key].priority) for key in remaining]

        edges = [ (key, edge) for key in remaining for edge in self[key].edges if edge in remaining  ]

        return Game(zip(remaining, info), edges)

    def copy(self) -> "Game":
        return self.exclude(set([]))

    def nodes(self, func = lambda _ : True) -> Set[int]:
        # returns a list of all nodes that pass the given filter
        return set([key for key in self.dict.keys() if func(self[key])])
    
    def invert_edges(self) -> "Game":
        vertices = self.nodes()
        edges = [(edge, key) for key in vertices for edge in self[key].edges]
        info = [(self[key].owner, self[key].priority) for key in vertices]

        return Game(zip(vertices, info), edges)

    def __getitem__(self, key):
        return self.dict[key]
    
    def __len__(self):
        return len(self.dict)

    def __repr__(self) -> str:
        string = ['|']
        for node in self.dict.keys():
            string += [f'{node}: ', self.dict[node].__repr__(), '\n']
        
        string[-1] = '|'
        return ''.join(string)
    
    def visualise(self, path='game.png', subset=set([])) -> None:

        assert(self.nodes().issuperset(subset))

        graph = pydot.Dot(graph_type = 'digraph')

        # add vertices
        for vertex in self.dict.keys():
            graph.add_node(pydot.Node( name=f'[{self[vertex].priority}] {vertex}', shape='box' if self[vertex].owner != 0 else 'circle',
                            color='red' if vertex in subset else 'black'))

        # add edges
        for vertex in self.dict.keys():
            for dest in self[vertex].edges:
                graph.add_edge(pydot.Edge(src=f'[{self[vertex].priority}] {vertex}', dst=f'[{self[dest].priority}] {dest}'))

        graph.write_png(path)

    def export(self, path='game.gm') -> None:

        f = open(path, 'w')

        f.write(f'game size {len(self)}\n')

        for vertex in self.nodes():

            f.write( f'{ vertex } {self[vertex].priority} {self[vertex].owner} {", ".join(map(str,sorted(list(self[vertex].edges))))};\n' )

        f.close()
    
    def remove_uncreachable(self) -> "Game":

        G = self.copy()

        while True:

            G_inv = G.invert_edges()
            to_rmv = G_inv.nodes(lambda x: len(x.edges) == 0)

            if len(to_rmv) == 0:
                break

            G = G.exclude(to_rmv)

        return G
    
    def modify_vertices(self, mod_f = lambda x : x, sel_f = lambda _: True):

        G = self.copy()

        for v in self.nodes(sel_f):
            G.dict[v] = mod_f(G[v])

        return G

    def redo_edges(self):

        new_edges = set([])

        for v in self.nodes():
            for e in self[v].edges:
                new_edges.add( (v,e) )
        
        self.edges = new_edges

if __name__ == '__main__':
    # Wikipedia Graph
    verts = 8
    info = [(1,0), (1,1), (1,2), (0,3), (0,4), (0,5), (0,6), (1,8)]
    edges = [(0,3), (0,1), (1,4), (1,6), (2,0), (2,5), (3,2), (4,0), (4,1),
             (5,7), (6,1), (6,7), (7,2), (7, 5)]

    game = Game(zip(range(verts), info), edges)
    game.visualise()
