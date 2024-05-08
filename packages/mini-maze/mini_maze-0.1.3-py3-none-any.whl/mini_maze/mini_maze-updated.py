from __future__ import annotations

import random
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Goal, Wall
from minigrid.minigrid_env import MiniGridEnv

from .maze_generator import find_next_state
from .maze import Maze


class MiniMazeEnv(MiniGridEnv):
    def __init__(
            self,
            maze: Maze,
            max_steps: int | None = None,
            **kwargs,
    ):
        self.start_pos = maze.start
        self.target_pos = maze.goal
        self.maze = maze

        mission_space = MissionSpace(mission_func=self._gen_mission)
        size = max( maze.height, maze.width) # max(len(maze), len(maze[0]))

        if max_steps is None:
            max_steps = 4 * size ** 2

        super().__init__(
            mission_space=mission_space,
            grid_size=size,
            # Set this to True for maximum speed
            see_through_walls=True,
            max_steps=max_steps,
            **kwargs,
        )

    @staticmethod
    def _gen_mission():
        return "get to the green goal square"

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Populate the grid based on the input matrix
        for i, row in enumerate(self.maze.maze):
            for j, item in enumerate(row):
                if item == 1:  # Wall
                    self.grid.set(j, i, Wall())

        i, j = self.target_pos
        self.put_obj(Goal(), j, i)

        # Place the agent
        if self.start_pos is not None:
            i, j = self.start_pos
            self.agent_pos = (j, i)
            self.agent_dir = 0
        else:
            self.place_agent()

        self.mission = "get to the green goal square"

    def get_optimal_action(self):
        # Evaluate the next state.
        i, j = self.target_pos
        next_state = find_next_state(self.maze, self.agent_pos, (j,i))
        assert next_state is not None
        move = {0: (1, 0), 1: (0, 1), 2: (-1, 0), 3: (0, -1)}
        left_dir = self.agent_dir - 1
        if left_dir < 0:
            left_dir += 4
        left_pos = (self.agent_pos[0] + move[left_dir][0], self.agent_pos[1] + move[left_dir][1])
        right_dir = (self.agent_dir + 1) % 4
        right_pos = (self.agent_pos[0] + move[right_dir][0], self.agent_pos[1] + move[right_dir][1])

        # Discuss what the next action to take.
        if next_state[0] == self.front_pos[0] and next_state[1] == self.front_pos[1]:
            return 2  # move forward
        elif next_state[0] == left_pos[0] and next_state[1] == left_pos[1]:
            return 0  # turn left
        elif next_state[0] == right_pos[0] and next_state[1] == right_pos[1]:
            return 1  # turn right
        else:
            return random.choice([0, 1])

