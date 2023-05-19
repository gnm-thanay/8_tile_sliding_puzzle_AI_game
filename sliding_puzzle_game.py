# library imports
import random


# custom data structure for nodes
class Node:
    def __init__(self, state, parent, operator, depth, cost):
        self.state = state
        self.parent = parent
        self.operator = operator
        self.depth = depth
        self.cost = cost
        self.heuristic = None


def pretty_print(_input_state):
    """
    Prints the state in a readable format.

    Function ensures the state has a length of 9. If it doesn't, it is most likely trying to print a None type which
    can result from an invalid move for the blank piece (0) in the state.
    """
    if len(_input_state) == 9:
        for i in range(9):
            if i % 3 == 0 and i > 0:
                print("")
            print(str(_input_state[i]) + "", end=" ")
    else:
        return "Length of state too short for pretty print. Check the length of your input!"


def create_node(state, parent, operator, depth, cost):
    return Node(state, parent, operator, depth, cost)


def move_blank_up(state):
    """Moves the blank tile up on the board. Returns a new state as a list."""
    # Create a copy of input state, this will ultimately be returned by the function
    next_state = state.copy()
    # find the index of 0 in the state
    index_of_zero = next_state.index(0)
    # if statement ensures that the 0 is not in the top row. if 0 were in the top row, you couldn't move it UP
    if index_of_zero not in [0, 1, 2]:
        # Swap the values of 0 and the value directly above it
        temp = next_state[index_of_zero - 3]
        next_state[index_of_zero - 3] = next_state[index_of_zero]
        next_state[index_of_zero] = temp
        return next_state
    else:
        # Invalid move
        return None


def move_blank_down(state):
    """Moves the blank tile down on the board. Returns a new state as a list."""
    # Create a copy of input state, this will ultimately be returned by the function
    next_state = state.copy()
    # find the index of 0 in the state
    index_of_zero = next_state.index(0)
    # if statement ensures that the 0 is not in the bottom row. if 0 were in the bottom row, you couldn't move it DOWN
    if index_of_zero not in [6, 7, 8]:
        # Swap the values of 0 and the value directly above it
        temp = next_state[index_of_zero + 3]
        next_state[index_of_zero + 3] = next_state[index_of_zero]
        next_state[index_of_zero] = temp
        return next_state
    else:
        # Invalid move
        return None


def move_blank_right(state):
    """Moves the blank tile right on the board. Returns a new state as a list."""
    # Create a copy of input state, this will ultimately be returned by the function
    next_state = state.copy()
    # find the index of 0 in the state
    index_of_zero = next_state.index(0)
    # if statement makes sure that the 0 is not in the right row. if 0 were in the right row, you couldn't move it RIGHT
    if index_of_zero not in [2, 5, 8]:
        # Swap the values of 0 and the value directly above it
        temp = next_state[index_of_zero + 1]
        next_state[index_of_zero + 1] = next_state[index_of_zero]
        next_state[index_of_zero] = temp
        return next_state
    else:
        # Invalid move
        return None


def move_blank_left(state):
    """Moves the blank tile left on the board. Returns a new state as a list."""
    # Create a copy of input state, this will ultimately be returned by the function
    next_state = state.copy()
    # find the index of 0 in the state
    index_of_zero = next_state.index(0)
    # if statement makes sure that the 0 is not in the left row. if 0 were in the left row, you couldn't move it LEFT
    if index_of_zero not in [0, 3, 6]:
        # Swap the values of 0 and the value directly above it
        temp = next_state[index_of_zero - 1]
        next_state[index_of_zero - 1] = next_state[index_of_zero]
        next_state[index_of_zero] = temp
        return next_state
    else:
        # Invalid move
        return None


def expand_node(node):
    """
    Expands the current node to all possible (and valid) next moves

    Returns a list of expanded nodes with invalid moves filtered out
    """
    # Set up an empty list to keep the expanded nodes
    expanded_nodes = list()
    # the following 4 lines iterate through all moves for the current state, including invalid moves
    expanded_nodes.append(create_node(move_blank_up(node.state), node, "up", node.depth + 1, 0))
    expanded_nodes.append(create_node(move_blank_down(node.state), node, "down", node.depth + 1, 0))
    expanded_nodes.append(create_node(move_blank_left(node.state), node, "left", node.depth + 1, 0))
    expanded_nodes.append(create_node(move_blank_right(node.state), node, "right", node.depth + 1, 0))
    # Remove all invalid moves from the list
    expanded_nodes = [node for node in expanded_nodes if node.state is not None]

    return expanded_nodes


def bfs(start, goal):
    """
    Performs a breadth first search from the start state to the goal using a FIFO queue

    Note that breadth first search is a special case of uniform cost search where the cost is the same for each
    move (1)
    """
    goal = goal
    # the start node is the initial state
    start_node = create_node(start, None, None, 0, 0)
    fringe = list()
    fringe.append(start_node)
    # pop(0) ensure first-in-first-out
    current = fringe.pop(0)
    # list that contains all the moves (up, down, left, right) that led to the solution
    path = []
    # track the total number of nodes generated
    total_nodes_generated = 1
    # while loop continues searching until a goal state is found
    while current.state != goal:
        # generate all possible moves from the current state
        expanded_nodes = expand_node(current)
        # add all possible moves to the fringe
        fringe.extend(expanded_nodes)
        # add the number of nodes created to the total count of nodes created
        total_nodes_generated += len(expanded_nodes)
        # FIFO to get the current node
        current = fringe.pop(0)
    # after a goal state is found, work backwards from the current (goal) state until you reach the parent (initial)
    # state
    while current.parent is not None:
        path.insert(0, current.operator)
        current = current.parent
    # cost of the solution, in this case it is the same as the depth of the solution found and the length of the path
    # to the solution
    total_cost = len(path)
    return path, total_nodes_generated, total_cost


def heuristic(state, goal):
    number_mismatched_tiles = 0
    for i in range(0, 9):
        if state.state[i] != goal[i]:
            number_mismatched_tiles += 1
    state.heuristic = number_mismatched_tiles


def greedy(start, goal):
    """
    Search that only uses the heuristic, making the evaluation function f(x) = h(x) where h(x) is the heuristic
    """
    # the start node is the initial state
    start_node = create_node(start, None, None, 0, 0)
    fringe = list()
    # add the initial state/root node to the fringe
    fringe.append(start_node)
    path = list()
    # track the total number of nodes generated
    total_nodes_generated = 1
    # make the root node the current node
    current = fringe.pop(0)
    while current.state != goal:
        # generate all possible moves from the current state
        expanded_nodes = expand_node(current)
        # add the expanded nodes to the fringe
        fringe.extend(expanded_nodes)
        # add the number of nodes created to the total count of nodes created
        total_nodes_generated += len(expanded_nodes)
        # calculate the heuristic for all the nodes/states in the fringe
        for state in fringe:
            heuristic(state, goal)
        # priority queue, sort the fringe by the heuristic. put the node with the lowest heuristic at the front of the
        # queue
        fringe.sort(key=lambda x: x.heuristic)
        # get the node at the front of the queue, which has the lowest heuristic
        current = fringe.pop(0)
    # when current.parent is None, you've reached the initial state/root node
    while current.parent is not None:
        # keep track of the path of moves and the heuristic value for each move, consists of
        # tuples containing (operator, heuristic)
        path.insert(0, (current.operator, current.heuristic))
        current = current.parent
    path.insert(0, ("operator", "heuristic"))
    total_cost = "See heuristic values in path"
    return path, total_nodes_generated, total_cost


def a_star(start, goal):
    """
    Search that uses both path cost and heuristic in the evaluation function f(x), meaning f(x) = g(x) + h(x) where g(x)
    is the path cost and h(x) is the heuristic
    """
    # the start node is the initial state
    start_node = create_node(start, None, None, 0, 0)
    fringe = list()
    # add the initial state/root node to the fringe
    fringe.append(start_node)
    path = list()
    # track the total number of nodes generated
    total_nodes_generated = 1
    # make the root node the current node
    current = fringe.pop(0)
    while current.state != goal:
        # generate all possible moves from the current state
        expanded_nodes = expand_node(current)
        # add the expanded nodes to the fringe
        fringe.extend(expanded_nodes)
        # add the number of nodes created to the total count of nodes created
        total_nodes_generated += len(expanded_nodes)
        # calculate the heuristic for all the nodes/states in the fringe
        for state in fringe:
            heuristic(state, goal)
            # update the heuristic to be the heuristic h(x) plus the path cost g(x)
            state.heuristic += state.depth
        # priority queue, sort the fringe by the heuristic. put the node with the lowest heuristic at the front of the
        # queue
        fringe.sort(key=lambda x: x.heuristic)
        # get the node at the front of the queue, which has the lowest heuristic/evaluation output
        current = fringe.pop(0)
    # when current.parent is None, you've reached the initial state/root node
    while current.parent is not None:
        # keep track of the path of moves and the heuristic value for each move, consists of
        # tuples containing (operator, path_cost)
        path.insert(0, (current.operator, current.heuristic))
        current = current.parent
    path.insert(0, ("operator", "path cost"))
    total_cost = "See path cost values in path"
    return path, total_nodes_generated, total_cost


def user_choose_algorithm():
    algo = input("Choose one of the following algorithms (bfs, greedy, a_star): ")
    while algo not in ['bfs', 'greedy', 'a_star']:
        print("Please choose one of the options")
        algo = input("Choose one of the following algorithms (bfs, greedy, a_star): ")
    return algo


def user_choose_random_initial_state():
    answer = input("Choose one of the following options...\n"
                   "1 to use random initial state\n"
                   "2 to write your own initial state\n"
                   "Enter your choice here: \n")
    while answer not in ["1", "2"]:
        print("Please choose one of the options")
        answer = input("Choose one of the following options...\n"
                       "1 to use random initial state\n"
                       "2 to write your own initial state\n"
                       "Enter your choice here: \n")

    return answer


def create_random_initial_state(_goal_state):
    '''
    this function generate an initial state by randomly shuffling the goal state
    '''
    output_state = _goal_state.copy()
    random.shuffle(output_state)
    return output_state


def custom_initial_state():
    input_string = input("Enter 0 through 8 in any order you'd like,\n"
                         "separating each value with a comma (no spaces): \n")
    user_list = input_string.split(',')
    user_list = [int(x) for x in user_list]

    assert len(user_list) == 9, "There should only be 9 values (0 through 8)"
    assert max(user_list) <= 8, "No number should be larger than 8"
    assert min(user_list) >= 0, "No number should be smaller than 0"
    return user_list


def main():
    # declare the goal state
    goal_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]
    #goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    # ask user if they want to choose a random initial state or create their own
    user_initial_state_choice = user_choose_random_initial_state()
    if user_initial_state_choice == "1":
        initial_state = create_random_initial_state(goal_state)
        print(f"Initial state = {initial_state}")
    elif user_initial_state_choice == "2":
        initial_state = custom_initial_state()
        print(f"Initial state = {initial_state}")
    # ask the user which algorithm they would like to choose
    user_algo_choice = user_choose_algorithm()
    if user_algo_choice == 'bfs':
        result, total_nodes_generated, total_cost = bfs(initial_state, goal_state)
    elif user_algo_choice == 'greedy':
        result, total_nodes_generated, total_cost = greedy(initial_state, goal_state)
    elif user_algo_choice == 'a_star':
        result, total_nodes_generated, total_cost = a_star(initial_state, goal_state)

    # print the outputs from the chosen algorithm
    if result is None:
        print("No solution found")
    elif result == []:
        print("Start node was the goal!")
    else:
        print(f"Solution: {result}")
        print(f"{len(result)} moves to get to goal state")
        print(f"Total number of nodes generated: {total_nodes_generated}")
        print(f"Path cost for solution: {total_cost}")


if __name__ == "__main__":
    main()