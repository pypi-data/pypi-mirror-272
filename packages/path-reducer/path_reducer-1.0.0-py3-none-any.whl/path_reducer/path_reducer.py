from typing import List


class PathReducer:
    """
    Class to reduce a simplified version of a path plan by removing opposite directions.
    """
    def __init__(self):
        self.stack = []
        self.opposites = {"NORTH": "SOUTH",
                          "SOUTH": "NORTH",
                          "EAST": "WEST",
                          "WEST": "EAST"}

    def reduce_path(self, ls: List[str]) -> List[str]:
        """
        Reduce the given list of directions by removing opposite directions.

        Args:
            ls (List[str]): A list with each item as one of the 4 cardinal paths, all in uppercase.

        Returns:
            List[str]: The optimized set of instructions.
        """
        if not isinstance(ls, list):
            raise ValueError("Input must be a list")

        valid_directions = {"NORTH", "SOUTH", "EAST", "WEST"}
        for direction in ls:
            if direction.upper() not in valid_directions:
                raise ValueError(f"Invalid direction: {direction}")

        stack = []
        for direction in ls:
            if stack and self.opposites[direction] == stack[-1]:
                stack.pop()
            else:
                stack.append(direction)
        return stack
