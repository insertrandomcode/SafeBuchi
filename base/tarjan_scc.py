import sys

if __name__ == '__main__':
    sys.path.insert(0, '.')
else: # annoying python relative import stuff
    sys.path.insert(0, '..')

from typing import Tuple, Set, List
import numpy as np
from base.parity_game import Game
from preprocessing.strategyfinding.strategy_finding import WGraph

def tarjan_scc_wg(WG: WGraph) -> List[Set[int]]:

    info = set([(v, (0,0)) for v in WG.verts])
    edges = set([])

    for v in WG.verts:
        for w, _ in WG.edges[v]:
            edges.add((v,w))

    return tarjan_scc(Game( info, edges ))

def tarjan_scc(G: Game) -> List[Set[int]]:

    # Tarjans Linear Time SCC finding algorithm

    SCCs = []

    # def strongconnect(v: int):
    #     nonlocal i
    #     index[v] = i
    #     lowlink[v] = i
    #     i += 1
    #     stack.append(v)
    #     onstack[v] = True

    #     for w in G[v].edges:

    #         if index[w] < 0:
    #             strongconnect(w)
    #             lowlink[v] = min(lowlink[v], lowlink[w])
    #         elif onstack[w]:
    #             lowlink[v] = min(lowlink[v], index[w])
        
    #     if index[v] == lowlink[v]:
    #         SCC = set([])

    #         while len(stack) != 0:
    #             w = stack.pop()
    #             SCC.add(w)
    #             onstack[w] = False

    #             if w == v:
    #                 break

    #         SCCs.append(SCC)

    i = 0
    stack = []
    index = {v: -1 for v in G.nodes()}
    lowlink = {v: -1 for v in G.nodes()}
    onstack = {v: False for v in G.nodes()}

    for v in G.nodes():
        if index[v] < 0:
            func_stack = [(v, True, set(G[v].edges), None)] # deep copy stuff

            # iterative version of the recursive call made previous to avoid recursion errors
            while len(func_stack) > 0:
                v, set_values, edges_not_visited, w = func_stack.pop()

                new_call = False

                if set_values:
                    index[v] = i
                    lowlink[v] = i
                    i += 1
                    stack.append(v)
                    onstack[v] = True
                else: 
                    lowlink[v] = min(lowlink[v], lowlink[w])

                visited_edges = set([])
                for w in edges_not_visited:
                    visited_edges.add(w)

                    if index[w] < 0:
                        func_stack.append( (v, False, edges_not_visited.difference(visited_edges), w) )
                        func_stack.append( (w, True, set(G[w].edges), None) )
                        new_call = True

                        break
                        
                        # strongconnect(v)
                        # lowlink[v] = min(lowlink[v], lowlink[w])
                    elif onstack[w]:
                        lowlink[v] = min(lowlink[v], index[w])

                if new_call:
                    
                    continue
                
                if index[v] == lowlink[v]:
                    SCC = set([])

                    while len(stack) != 0:
                        w = stack.pop()
                        SCC.add(w)
                        onstack[w] = False

                        if w == v:
                            break

                    SCCs.append(SCC)

    return SCCs
