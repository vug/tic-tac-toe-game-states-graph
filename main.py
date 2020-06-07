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
