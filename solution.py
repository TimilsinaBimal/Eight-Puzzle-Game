from graphviz import Digraph
import random


class EightPuzzleSolver():
    def __init__(self, initial_state, final_state):
        self.initial_state = initial_state
        self.final_state = final_state
        self.state_dict = {}
        self.to_visit = [self.initial_state]
        self.visited_state = []
        self.OUTPUT_LOCATION = 'output/state_space.gv'
        self.dot = Digraph(name="State Space Tree")
        self.dot.attr('node', shape='plaintext',
                      fillcolor='lightblue2', style="filled")
        self.dot.attr(size='200,200')
        self.dot.attr(overlap='false')
        self.dot.attr(label=r'State Space Tree of Eight Puzzle game')
        self.dot.attr(fontsize='50')

    @staticmethod
    def _index(state):
        for idx_row, row in enumerate(state):
            for idx_col, col in enumerate(row):
                if col == 0:
                    return (idx_row, idx_col)

    @staticmethod
    def _move(initial_pos, final_pos, present_state):
        current_state = [[j for j in i] for i in present_state]
        temp_val = current_state[final_pos[0]][final_pos[1]]
        current_state[final_pos[0]][final_pos[1]] = 0
        current_state[initial_pos[0]][initial_pos[1]] = temp_val
        return current_state

    def _up(self, current_state):
        position = self._index(current_state)
        if position[0] == 0:
            return current_state
        else:
            final_position = (position[0]-1, position[1])
            next_state = self._move(position, final_position, current_state)
            return next_state

    def _down(self, current_state):
        position = self._index(current_state)
        if position[0] == 2:
            return current_state
        final_position = (position[0]+1, position[1])
        next_state = self._move(position, final_position, current_state)
        return next_state

    def _left(self, current_state):
        position = self._index(current_state)
        if position[1] == 0:
            return current_state
        final_position = (position[0], position[1]-1)
        next_state = self._move(position, final_position, current_state)
        return next_state

    def _right(self, current_state):
        position = self._index(current_state)
        if position[1] == 2:
            return current_state
        final_position = (position[0], position[1]+1)
        next_state = self._move(position, final_position, current_state)

        return next_state

    def _generate_nodes(self, current_state):
        L = self._left(list(current_state))
        R = self._right(current_state)
        U = self._up(current_state)
        D = self._down(current_state)

        return [L, R, U, D]

    def solve(self):
        while True:
            parent_state = self.to_visit.pop(0)
            self.visited_state.append(parent_state)
            states = self._generate_nodes(parent_state)
            self.state_dict[f"{parent_state}"] = []
            for state in states:
                self.state_dict[f"{parent_state}"].append(state)
                if state not in self.visited_state:
                    self.to_visit.append(state)

                if state == self.final_state:
                    return

    @staticmethod
    def _print_table(state):
        return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                        <TR>
                        <TD> {state[0][0]} </TD>
                        <TD> {state[0][1]} </TD>
                        <TD> {state[0][2]} </TD>
                        </TR>
                        <TR>
                        <TD> {state[1][0]} </TD>
                        <TD> {state[1][1]} </TD>
                        <TD> {state[1][2]} </TD>
                        </TR>
                        <TR>
                        <TD> {state[2][0]} </TD>
                        <TD> {state[2][1]} </TD>
                        <TD> {state[2][2]} </TD>
                        </TR>
                        </TABLE>>'''

    def _replace_zero(self, state):
        pos = self._index(state)
        try:
            state[pos[0]][pos[1]] = ""
        except:
            pass
        return state

    def draw_graph(self):
        self.initial_state = self._replace_zero(self.initial_state)
        self.dot.node(f"0", self._print_table(self.initial_state))
        a = 1
        added = [self.initial_state]
        for idx, key in enumerate(self.state_dict):
            states = self.state_dict[key]
            for state in states:
                state = self._replace_zero(state)
                if state in added:
                    temp = random.random()
                    self.dot.node(f"{temp}", self._print_table(state))
                    self.dot.edge(f"{idx}", f"{temp}")
                else:
                    added.append(state)
                    if state == self._replace_zero(self.final_state):
                        self.dot.attr('node', shape='plaintext',
                                      fillcolor='pink', style="filled")
                    self.dot.node(f"{a}", self._print_table(state))
                    self.dot.edge(f"{idx}", f"{a}")
                    a += 1
        self.dot.render(self.OUTPUT_LOCATION, view=True, format="pdf")


def main():
    initial_state = [[2, 8, 3], [1, 6, 4], [7, 0, 5]]
    final_state = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
    solver = EightPuzzleSolver(initial_state, final_state)
    solver.solve()
    solver.draw_graph()


if __name__ == '__main__':
    main()
