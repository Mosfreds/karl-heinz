#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
#
# Pure random A.I, you may NOT use it to win ;-)
#
########################################################################

import random
from  gamestats import GameStats
from queue import PriorityQueue
from utils import positions

class AI:
    """Pure random A.I, you may NOT use it to win ;-)"""
    def __init__(self):
        pass

    def process(self, game):
        """Do whatever you need with the Game object game"""
        self.game = game

    def decide(self):
        """Must return a tuple containing in that order:
          1 - path_to_goal :
                  A list of coordinates representing the path to your
                 bot's goal for this turn:
                 - i.e: [(y, x) , (y, x), (y, x)]
                 where y is the vertical position from top and x the
                 horizontal position from left.

          2 - action:
                 A string that will be displayed in the 'Action' place.
                 - i.e: "Go to mine"

          3 - decision:
                 A list of tuples containing what would be useful to understand
                 the choice you're bot has made and that will be printed
                 at the 'Decision' place.

          4- hero_move:
                 A string in one of the following: West, East, North,
                 South, Stay

          5 - nearest_enemy_pos:
                 A tuple containing the nearest enenmy position (see above)

          6 - nearest_mine_pos:
                 A tuple containing the nearest enenmy position (see above)

          7 - nearest_tavern_pos:
                 A tuple containing the nearest enenmy position (see above)"""
        gamestats = GameStats(self.game)
        

        decisions = gamestats.motivations
        chosen_action = decisions[0]
        
        #print(decisions)

        actions = ['mine', 'drink', 'attack', 'wait']

        # informational output
        decision = list(map(lambda action: [(d[2], d[0]) for d in decisions if d[2]==action][0], actions))

        # path to the chosen target
        path_tree , path_cost = (self.shortest_path_dist(self.game.hero.pos, chosen_action[3]))
        path = self.get_path(path_tree, chosen_action[3])
        path_to_goal = path

        # next step towards the goal
        hero_move = positions.direction_to_cmd(self.first_step(path))
        action = chosen_action[2] + ":" + hero_move 
        #decision = decisions[action]
        nearest_enemy_pos = random.choice(self.game.heroes).pos
        nearest_mine_pos = random.choice(self.game.mines_locs)
        nearest_tavern_pos = random.choice(self.game.mines_locs)

        return (path_to_goal,
                action,
                decision,
                hero_move,
                nearest_enemy_pos,
                nearest_mine_pos,
                nearest_tavern_pos)


    def get_path(self, tree, goal):
        last = tree[goal]
        
        path = [goal]
        while not last is None:
            path = [last] + path
            last = tree[last]
        return path


    def shortest_path_dist(self, start, goal):
        """A* distance function"""
        frontier = PriorityQueue()
        frontier.put (start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            candidates = self.movable_neighbour_fields(current, goal)
            for candidate in candidates:
                new_cost = cost_so_far[current] + 1
                if (candidate not in cost_so_far) or (new_cost < cost_so_far[candidate]):
                        cost_so_far[candidate] = new_cost
                        priority = new_cost + positions.manhattan_dist(candidate, goal)
                        frontier.put(candidate, priority)
                        came_from[candidate] = current

        return came_from, cost_so_far


    def movable_neighbour_fields(self, pos, goal):
        """get all the positions you can move to from pos"""
        neighbours = [ positions.add(pos, d) for d in positions.directions ]
        return [p for p in neighbours if self.is_movable_position(p) or p == goal]
        

    def is_movable_position(self, p):
        if p is None:
            raise Exception("position p is None")
        return p[0] >= 0 and p[0] < self.game.board_size \
               and p[1] >= 0 and p[1] < self.game.board_size \
               and not (p in self.game.walls_locs or p in self.game.taverns_locs or p in self.game.mines_locs)


    def first_step(self,path):
        return positions.sub(path[1],path[0])


if __name__ == "__main__":
    pass
