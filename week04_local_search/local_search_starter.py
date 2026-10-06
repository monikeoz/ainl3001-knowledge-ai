"""
AINL3001 — Knowledge-Driven AI
Week 4 — Local Search and Optimisation
BSP 2026

This week introduces local search.

In previous weeks, search algorithms explored paths through
a state space in order to reach a goal.

Local search takes a different approach:

    1. Start with a state.
    2. Evaluate how good that state is.
    3. Generate neighbouring states.
    4. Move to a better neighbour.
    5. Repeat.

We will explore this using the N-Queens problem.

Tasks
-----

1. Understand the problem representation.
2. Implement conflict counting.
3. Explore neighbouring states.
4. Implement Hill Climbing.
5. Implement Simulated Annealing.
"""

import math
import random

from queens_problem import QueensProblem

N = 8


# --------------------------------------------------
# TASK 0 — UNDERSTANDING THE STATE
# --------------------------------------------------

example_board = [0, 1, 2, 3]

print("Manual Exploration Board:")
print(example_board)

print(
    "\nEach list position represents a column."
)

print(
    "Each value represents the row containing the queen."
)

print(
    "\nQuestion: How many conflicts exist on this board?"
)


# --------------------------------------------------
# TASK 1 — EVALUATE A STATE
# --------------------------------------------------

def count_conflicts(board):
    """
    Return the number of pairs of queens
    that attack each other.

    Lower values are better.

    A solution has:

        conflict count = 0
    """

    # TODO:
    # Compare each queen with every queen
    # that comes after it.
    #
    # Queens conflict when they are:
    #
    #   1. in the same row
    #   2. on the same diagonal

    conflicts = 0 

    for i in range(len(board)):
        for j in range(i + 1, len(board)):

            # same row
            if board[i] == board[j]:
                conflicts += 1

            # same diagonal
            elif abs(i - j) == abs(board[i] - board[j]):
                conflicts += 1

    return conflicts


# --------------------------------------------------
# TASK 2 — EXPLORE THE PROBLEM
# --------------------------------------------------

def generate_neighbours(problem, board):
    """
    Generate all neighbouring boards.

    Use the Problem interface introduced this week:

        problem.actions(state)
        problem.result(state, action)
    """

    neighbours = []

    # TODO:
    #
    # 1. Ask the problem for the available actions.
    # 2. Apply each action.
    # 3. Add the resulting state to neighbours.

    actions = problem.actions(board)

    for action in actions:
        neighbour = problem.result(board, action)
        neighbours.append(neighbour)

    return neighbours


# --------------------------------------------------
# TASK 3 — HILL CLIMBING
# --------------------------------------------------

def hill_climbing(problem, start_board):
    """
    Use Hill Climbing to reduce the number
    of conflicts.

    Algorithm:

        current = start state

        repeat:

            generate neighbours

            find the neighbour with the
            lowest conflict count

            if the neighbour is not better:
                stop

            otherwise:
                move to the neighbour

        return current
    """

    current = start_board

    # TODO

    while True:

        neighbours = generate_neighbours(problem, current) # gets all possible next states

        best_neighbour = min(neighbours, key=count_conflicts) # finds the neighb our w lowest conflict count

        # checks whether the best neighbour is actually better
        if count_conflicts(best_neighbour) >= count_conflicts(current):
            break 

        current = best_neighbour

    return current




# --------------------------------------------------
# TASK 4 — SIMULATED ANNEALING
# --------------------------------------------------

def simulated_annealing(problem, start_board):
    """
    Use Simulated Annealing to search for
    a solution.

    Unlike Hill Climbing, Simulated Annealing
    can sometimes accept a worse state.

    This can help escape local minima.
    """

    current = start_board

    temperature = 10.0
    cooling_rate = 0.95

    # TODO

    while temperature > 0.1:

        neighbours = generate_neighbours(problem, current)

        neighbour = random.choice(neighbours)

        current_cost = count_conflicts(current)
        neighbour_cost = count_conflicts(neighbour)

        delta = neighbour_cost - current_cost

        if delta < 0:
            current = neighbour

        else:
            probability = math.exp(-delta / temperature)

            if random.random() < probability:
                current = neighbour

        temperature *= cooling_rate

    return current


# --------------------------------------------------
# TESTING AREA
# --------------------------------------------------

if __name__ == "__main__":

    board = [
        random.randint(0, N - 1)
        for _ in range(N)
    ]

    problem = QueensProblem(board)

    print("\nRandom Board")
    print(board)

    print("\nConflicts")
    print(
        count_conflicts(board)
    )

    print("\nPossible Actions")

    actions = problem.actions(board)

    print(
        f"{len(actions)} actions available"
    )

    print("\nNeighbours")

    neighbours = generate_neighbours(
        problem,
        board
    )

    print(
        f"{len(neighbours)} neighbours generated"
    )

    print("\nHill Climbing")

    result = hill_climbing(
        problem,
        board
    )

    print("Starting conflicts:", count_conflicts(board))
    print("Final board:", result)
    print("Final conflicts:", count_conflicts(result))

    print("\nHill Climbing Experiments")

    for i in range(10):

        start_board = [
            random.randint(0, N - 1)
            for _ in range(N)
        ]

        problem = QueensProblem(start_board)

        result = hill_climbing(
            problem,
            start_board
        )

        print(
            f"Run {i + 1}: "
            f"{count_conflicts(start_board)} -> "
            f"{count_conflicts(result)}"
        )

    print("\nSimulated Annealing")

    sa_result = simulated_annealing(
        problem,
        board
    )

    print(
        "Starting conflicts:",
        count_conflicts(board)
    )

    print(
        "Final board:",
        sa_result
    )

    print(
        "Final conflicts:",
        count_conflicts(sa_result)
    )

    print("\nSimulated Annealing Experiments")

    for i in range(10):

        start_board = [
            random.randint(0, N - 1)
            for _ in range(N)
        ]

        problem = QueensProblem(start_board)

        result = simulated_annealing(
            problem,
            start_board
        )

        print(
            f"Run {i + 1}: "
            f"{count_conflicts(start_board)} -> "
            f"{count_conflicts(result)}"
        )