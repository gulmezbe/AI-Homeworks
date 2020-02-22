import time
import random
from copy import deepcopy
from agent import Agent


#  use whichever data structure you like, or create a custom one
import queue
import heapq
from collections import deque


"""
  you may use the following Node class
  modify it if needed, or create your own
"""
class Node():
    
    def __init__(self, parent_node, level_matrix, player_row, player_column, depth, chosen_dir):
        self.parent_node = parent_node
        self.level_matrix = level_matrix
        self.player_row = player_row
        self.player_col = player_column
        self.depth = depth
        self.chosen_dir = chosen_dir

        self.seq = []
        if (self.chosen_dir == "X"):
            pass
        else:
            self.seq.extend(self.parent_node.seq)
            self.seq.append(self.chosen_dir)



class DFSAgent(Agent):

    def __init__(self):
        super().__init__()

    def solve(self, level_matrix, player_row, player_column):
        super().solve(level_matrix, player_row, player_column)
        move_sequence = []

        initial_level_matrix = [list(row) for row in level_matrix] #deepcopy(level_matrix)

        node_list = []
        new_node = Node(None, initial_level_matrix, player_row, player_column, 0, "X")
        node_list.append(new_node)
        visited = []
        apple_nodes = []

        while len(node_list) != 0:
            node = node_list.pop(0)
            visited.append((node.player_row, node.player_col))

            if level_matrix[node.player_row + 1][node.player_col] != "W" and (
            node.player_row + 1, node.player_col) not in visited:
                new_node = Node(node, initial_level_matrix, node.player_row + 1, node.player_col, node.depth + 1, "U")
                node_list.insert(0, new_node)
            if level_matrix[node.player_row][node.player_col + 1] != "W" and (
            node.player_row, node.player_col + 1) not in visited:
                new_node = Node(node, initial_level_matrix, node.player_row, node.player_col + 1, node.depth + 1, "R")
                node_list.insert(0, new_node)
            if level_matrix[node.player_row - 1][node.player_col] != "W" and (
            node.player_row - 1, node.player_col) not in visited:
                new_node = Node(node, initial_level_matrix, node.player_row - 1, node.player_col, node.depth + 1, "D")
                node_list.insert(0, new_node)
            if level_matrix[node.player_row][node.player_col - 1] != "W" and (
            node.player_row, node.player_col - 1) not in visited:
                new_node = Node(node, initial_level_matrix, node.player_row, node.player_col - 1, node.depth + 1, "L")
                node_list.insert(0, new_node)

            if level_matrix[node.player_row][node.player_col] == "A":
                level_matrix[node.player_row][node.player_col] = "F"
                apple_nodes.append((node.player_row, node.player_col))
                move_sequence.extend(node.seq)
                node_list.clear()
                visited.clear()
                new_node = Node(None, initial_level_matrix, node.player_row, node.player_col, 0, "X")
                node_list.append(new_node)

        for (i, j) in apple_nodes:
            level_matrix[i][j] = "A"

        return move_sequence