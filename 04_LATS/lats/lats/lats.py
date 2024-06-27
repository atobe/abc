from math import log
import random
from prettyprinter import pprint
from pathlib import Path
import pickle

from .apps._base import App, get_app_by_name
from .model import Node
from .cache import cache

w = 1.0

class LATS:
    def __init__(self, app: App):
        self.app = app
        self.root = app.get_root_node()

    def select(self) -> Node:
        node = self.root
        while not node.is_leaf:
            node2score = {child: self._ucb(child) for child in node.children}
            node = max(node2score, key=node2score.get)
        return node

    def _ucb(self, node: Node) -> float:
        # print all the input values
        print(f'score: {node.score}, N: {node.N}, parent.N: {node.parent.N} w: {w}')
        if node.N == 0: return float("inf")
        return node.score / node.N + w * (2 * log(node.parent.N) / node.N) ** 0.5

    def expand(self, node: Node):
        new_nodes = []
        for n in range(3):
            new_node = getattr(self.app, f'expand_{node.__class__.__name__}')(node)
            node.children.append(new_node)
            new_nodes.append(new_node)
        return random.choice(new_nodes)

    def evaluate(self, node: Node):
        # ignore for now and use the observation/score directly
        return self.app.evaluate(node)

    def simulate(self, node: Node):
        # not used for humaneval in the paper
        return self.app.simulate(node)

    def backprop(self, node: Node):
        current_node = node
        score = node.observation
        while current_node is not None:
            current_node.N += 1
            current_node.score += score
            if current_node.score / current_node.N >= 1.0:
            # if current_node.score >= 1.0:
                current_node.is_terminal = True
            # print(f'updated node {str(current_node)[:100]}')
            current_node = current_node.parent

    def reflection(self, node: Node):
        return self.app.reflect(node)
    
    # utils
    def show(self):
        pprint(self.root)
    
    # bigger stuff
    def step(self):
        node = self.select()
        node = self.expand(node)
        self.simulate(node)
        self.evaluate(node)
        if node:
            self.backprop(node)
        # self.reflection(node)
        
        self.show_compact()
        print(f'node terminal: {node.is_terminal}')
        if node.state:
            print(node.state.chunks[-1])

        # return True if done
        return node.is_terminal
        
    def run(self, k=None):
        if k is None:
            while True:
                if self.step():
                    break
        else:
            for _ in range(k):
                if self.step():
                    break


    def show_compact(self, node=None, depth=0):
        if node is None:
            node = self.root
        indent = '  ' * depth
        excl_s = '!' if node.is_terminal and node.observation >= 1.0 else ''
        print(f'{indent}o:{node.observation} s:{node.score} N:{node.N} sc:{node.subcount}{excl_s}')
        for child in node.children:
            self.show_compact(child, depth + 1)

def run(app_name, case=None):
    case_s = f" with case {case}" if case else ""
    print(f"running {app_name}{case_s}")

    app_cls = get_app_by_name(app_name)
    app = app_cls(case)

    if app.REQUIRES_CASE and case is None:
        raise ValueError(f"{app_name} requires a case")
    
    lats = LATS(app)
    lats.run(k=50)

    print(f'cache hits: {cache.hits}')
    app.show_end_state()
    
    
    name = f'case-{case}'
    name = name.replace(' ', '_')
    name = name.replace('?','')
    root_rp = Path(__file__).parents[2] / f'{name}.pickle'
    with root_rp.open('wb') as f:
        pickle.dump(lats.root, f)
        