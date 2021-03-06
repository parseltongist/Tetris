class Tetris:

    def __init__(self, m, n):
        self.letter = None
        self.letters_dict = {}
        self.m, self.n = m, n  # 'm' is the board width  'n' is the board height
        self.grid = ["-" for _ in range(self.m * self.n)]
        self.rotation = 0
        self.border_points = {
                              "left": [x for x in range(self.m * self.n) if x % self.m == 0],
                              "right": [x for x in range(self.m * self.n) if x % self.m == 9],
                              "down": [x for x in range((self.m * self.n) - self.m, self.m * self.n)]
        }
        self.static_cells = set()

    def reset_dict(self) -> None:
        self.letters_dict = {
                            "O": [[4, 14, 15, 5]],
                            "I": [[4, 14, 24, 34], [3, 4, 5, 6]],
                            "S": [[5, 4, 14, 13], [4, 14, 15, 25]],
                            "Z": [[4, 5, 15, 16], [5, 15, 14, 24]],
                            "L": [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
                            "J": [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
                            "T": [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]],
        }

    @classmethod
    def from_string(cls) -> 'Tetris':
        try:
            dimensions = [int(x) for x in input().split()]
            assert len(dimensions) == 2
        except (ValueError, AssertionError):
            print("Incorrect values provided")
            return Tetris.from_string()
        return cls(*dimensions)

    @property
    def letter_coordinates(self) -> list:
        return self.letters_dict[self.letter][self.rotation]

    def print_grid(self) -> None:
        for i in range(0, self.n * self.m, self.m):
            print(" ".join(self.grid[i:i + self.m]))
        print()

    def fill_out_grid(self, ) -> None:

        if self.static_cells:
            for cell in self.static_cells:
                self.grid[cell] = "0"

        if self.letter:
            for y in self.letters_dict[self.letter][self.rotation]:
                if 0 < y < self.m * self.n:
                    self.grid[y] = "0"

    def reset_grid(self) -> None:
        self.grid = ["-" for _ in range(self.m * self.n)]

    def rotate(self) -> None:
        # rotate
        self.rotation += 1 if (
                self.rotation + 1 <= len(self.letters_dict[self.letter]) - 1 or self.rotation == -1) else 0
        # validate
        if not all([self.is_valid_move(direction="left"), self.is_valid_move(direction="right")]):
            # undo if validation failed
            self.rotation -= 1

    def move(self, direction) -> None:
        # +1 if moving right, -1 if moving left.
        offset = {"left": -1, "right": +1, "down": self.m}

        if self.is_valid_move(direction=direction):
            new_value = [[int(x) + offset[direction] for x in variant] for variant in self.letters_dict[self.letter]]
            self.letters_dict[self.letter] = new_value

    def is_valid_move(self, direction=None) -> bool:
        border_and_static_cells = set(self.border_points[direction] + list(self.static_cells) + self.border_points["down"])
        return not bool(set(self.letter_coordinates).intersection(border_and_static_cells))

    def make_static(self) -> None:
        # or coodinate is sitting ON a static cell. - make it static
        def in_border_points(cell) -> bool:
            return cell in self.border_points["down"] \
                   or cell in [x - self.m for x in self.static_cells]

        def hits_the_border() -> bool:
            return bool([coordinate for coordinate in self.letter_coordinates if in_border_points(coordinate)])

        if self.letter:
            if hits_the_border():
                # update static_cells list adding current letter coordinates
                self.static_cells = {*self.static_cells, *set(self.letter_coordinates)}
                # reset self.letter value to none to drop self.letter coordinates
                self.letter = None  # need to clear letter coordinates once it became static

    def game_end_check(self):
        # Intersection of two sets returns only elements presented in both sets.
        if self.static_cells.intersection(set((x for x in range(self.m)))):
            exit(print("Game Over!"))

    def drop_row(self):

        def recalculation_required(cell) -> bool:
            # making sure that new value will be within grid borders and cell is not static and can be moved
            return all([cell + self.m <= self.m * self.n - 1,
                        cell + self.m not in self.static_cells])

        self.fill_out_grid()
        original_static_capacity = len(self.static_cells)

        for i in range(0, self.n * self.m, self.m):
            row_indexes = [x for x in range(i, i + self.m)]

            # row == row full of Zeros
            if self.grid[i:i + self.m] == ["0" for _ in range(self.m)]:
                for cell_index in row_indexes:
                    self.static_cells.remove(cell_index)

        if original_static_capacity != len(self.static_cells):
            # iterating over the static cells and recalculate
            # avoiding overwritting of occupied static cells
            # pushing top cells down to be on bottom level of grid or static cells
            self.static_cells = set([cell + self.m if recalculation_required(cell) else cell for cell in self.static_cells])
        self.reset_grid()

    def gameplay(self):
        while True:
            option = input("\n")
            match option:
                case "exit":
                    exit()
                case "rotate":
                    self.rotate()
                    self.move("down")
                case "down":
                    if self.letter:
                        self.move(option)
                case "left" | "right":  # "|" == "or"
                    self.move(option)
                    self.move("down")
                case "break":
                    self.drop_row()
                case "piece":
                    self.reset_dict()
                    self.letter = input().strip().upper()
                    self.rotation = 0
                case _:
                    print("Invalid option.\nPossible options: 'left', 'right', 'down', 'rotate', 'exit': ")
                    return self.gameplay()

            self.fill_out_grid()
            self.make_static()
            self.print_grid()
            if option != "piece":
                self.game_end_check()
            self.reset_grid()


def main():
    game = Tetris.from_string()
    game.print_grid()
    game.gameplay()


if __name__ == "__main__":
    main()
