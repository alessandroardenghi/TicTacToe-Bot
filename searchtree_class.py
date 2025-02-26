import numpy as np
import random
import pandas as pd
from tqdm import tqdm


class SearchTree:
    def __init__(self, node):
        self.node = node
        self.children = []
        self.value = 0

    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children

    def get_node(self):
        return self.node

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def __str__(self):
        return str(self.node) + " " + str(self.value)

    def __repr__(self):
        return str(self.node) + " " + str(self.value)