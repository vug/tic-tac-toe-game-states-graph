from collections import deque
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


#
# Algorithms
#
def get_symmetries(st: State) -> SymmetryGroup:
    """Compute Symmetry Group of a board state.

    There are 8 symmetries of a state. Identity + 3 90 degree
    rotations. And the same for it's mirror (either horizontal
    or vertical.)

    Also remove duplicate states in a group.

    Keeps the original state to be used to compute the group
    at the first index, so that it can be used as the
    "canonical state" that represents the group.
    """

    def get_vertical_mirror(st: State) -> State:
        return tuple(reversed(st))

    def get_rotations(st: State) -> List[State]:
        # fmt: off
        ((a, b, c),
         (d, e, f),
         (g, h, i)) = st
        rot1 = ((g, d, a),
                (h, e, b),
                (i, f, c))
        rot2 = ((i, h, g),
                (f, e, d),
                (c, b, a))
        rot3 = ((c, f, i),
                (b, e, h),
                (a, d, g))
        # fmt: on
        return [st, rot1, rot2, rot3]

    def apply_all_symmetry_operations(st: State) -> List[State]:
        mir = get_vertical_mirror(st)
        return get_rotations(st) + get_rotations(mir)

    all_symmetries = apply_all_symmetry_operations(st)
    duplicates_removed = list(dict.fromkeys(all_symmetries))
    return duplicates_removed


def is_end(st: State) -> bool:
    """Tell whether given state is a game-ending state.

    Go over every column, row and diagonals (lines) and
    check whether they are made of all-Xs or all-Os.
    """

    def are_same(triplet):
        a, b, c = triplet
        return a == b == c != 0

    horizontals = [[st[ix][0], st[ix][1], st[ix][2]] for ix in range(3)]
    verticals = [[st[0][ix], st[1][ix], st[2][ix]] for ix in range(3)]
    diag1 = [st[0][0], st[1][1], st[2][2]]
    diag2 = [st[2][0], st[1][1], st[0][2]]
    lines = horizontals + verticals + [diag1, diag2]

    return any(are_same(line) for line in lines)


def make_move(st: State, row: int, col: int, val: int) -> State:
    """Take a state and a move and creates resulting state.

    Do not check the legality of the move."""
    mutable_st = [list(r) for r in st]
    mutable_st[row][col] = val
    new_st = tuple(tuple(r) for r in mutable_st)
    return new_st


def get_next_states_raw(st: State, step: int) -> List[State]:
    """Compute states that can be reach via legal moves.

    Given a state and the number of current step.
    Assuming empty board is step=0, X's are placed in even
    steps and O's in odd steps.

    If given state is an ending state, there no next states.
    """
    next_states = []
    if is_end(st):
        return []
    new_val = step % 2 + 1
    for row in range(3):
        for col in range(3):
            val = st[row][col]
            if val == 0:
                new_st = make_move(st, row, col, new_val)
                next_states.append(new_st)
    return next_states
