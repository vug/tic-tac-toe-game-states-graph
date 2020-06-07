from typing import Iterable, List

#
# Data Structures
#

# Represents one board configuration.
# Other constraints of a State type
#   inner tuple is made of 3 integers, a triplet made of {0, 1, 2}
#   and outer tuple is made of 3 triplets.
State = Iterable[Iterable[int]]
# Constraint on SymmetryGroup type is that
# states it includes has to be symmetric under
# rotation and mirroring.
# Also first state in the list is the
# canonical representation of the group.
SymmetryGroup = List[State]
# Represent the ID of individual Symmetry Groups
GroupId = int


class Node(object):
    def __init__(self, val: GroupId = None, successors: List[GroupId] = None):
        self.val = val
        self.successors = successors or []


if __name__ == "__main__":
    print("Hi!")


#
# Debug utilities
#

# I'd prefer a chain of operations piped sequentially.
# But, here, the processing starts from the inner loop
# I can't join cells in a row, before they are converted to strings
def state_str(st: State) -> str:
    def row_to_str(row: Iterable[int]):
        row = [str(num) for num in row]
        return "".join(row)

    return "\n".join(row_to_str(row) for row in st)


def print_state(st: State) -> None:
    print(state_str(st))


def print_states(states: Iterable[State]):
    for st in states:
        print_state(st)
        print()
