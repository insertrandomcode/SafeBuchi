import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from base.labelling import Label

from typing import Set
import pydot

class WGraph:

    def __init__(self, verts: Set[int], arcs: Set[int]) -> None:
        self.verts = verts
        self.arcs = arcs

        self.edges = {v: set([]) for v in verts}

        for src, dst, val in arcs:
            self.edges[src].add((dst, val))

    def exclude(self, to_excl: Set[int] ) -> "WGraph":
        assert to_excl.issubset(self.verts), "to_excl not subset of vertices"

        return WGraph(self.verts.difference(to_excl), 
                    [(src,dst,val) for src,dst,val in self.arcs if src not in to_excl and dst not in to_excl])

    def best_paths(self, dst, player) -> int:
        # labelling
        labels = {v: Label(-1, player, v) for v in self.verts}

        inv = WGraph(self.verts, [(dst,src,val) for src,dst,val in self.arcs])

        stack = [dst]
        changes = True

        while len(stack) != 0:
            v = stack.pop()

            for w, val in inv.edges[v]:
                l = Label(max(val, labels[v].value), player, w)
                if labels[w] < l:
                    labels[w] = l
                    stack.append(w)
        
        return labels
    
    def best_path(self, src, dst, player) -> int:
        return self.best_paths(dst, player)[src]

    def reachable(self, src, dest, arc_const: lambda x : True) -> bool:
        # BFS

        stack = [src]
        reached = []

        while len(stack) != 0:
            curr = stack.pop()
            reached.append(curr)

            for dst, val in self.edges[curr]:
                if arc_const((curr, dst, val)) and dst not in reached:
                    stack.append(dst)

        return dest in reached

    def collapse(self) -> None:
        while True:

            to_map = [v for v in self.verts if len(self.edges[v]) <= 1]
            if len(to_map) == 0:
                break
            v = to_map[0]

            if len(self.edges[v]) == 0:

                self.verts.remove(v)
                del self.edges[v]
            
            else:
                
                self.verts.remove(v)
                w, arcval = list(self.edges[v])[0]

                del self.edges[v]
                
                for arc in list(self.arcs):
                    if v in arc[0:2]:
                        self.arcs.remove(arc)
                    if arc[0] != v and arc[1] == v:
                        self.arcs.add((arc[0], w, max(arcval, arc[2])))

                        self.edges[arc[0]].remove((arc[1:]))
                        self.edges[arc[0]].add((w, max(arcval, arc[2])))

        self.__init__(self.verts, self.arcs)

        new_verts = set([v for v in self.verts if len(self.edges[v]) != 1])

        # maps unary vertices to their successors
        mapping = {v : self.edges[v][0] for v in self.verts if len(self.edges[v]) == 1}

        new_arcs = set([
            (arc[0], arc[1], arc[2])
            if arc[1] in new_verts
            else 
                (arc[0], mapping[arc[1]][0], max(arc[2], mapping[arc[1]][1]))
            for arc in self.arcs
            if arc[0] in new_verts
        ])

        self.__init__(new_verts, new_arcs)
    
    def copy(self) -> "WGraph":
        return self.exclude(set([]))

    
    def visualise(self, path='dgraph.png') -> None:
        graph = pydot.Dot(graph_type = 'digraph')

        for vertex in self.verts:
            graph.add_node(pydot.Node( name=str(vertex), shape='circle'))
        
        for src, dst, val in self.arcs:
            graph.add_edge(pydot.Edge(src=str(src), dst=str(dst), label=str(val)))

        graph.write_png(path)