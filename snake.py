from random import randint
from time import sleep

class CellItem:
    def __init__(self):
        self.char: str = "??"

    def __str__(self) -> str:
        return self.char

    def get_decay(self) -> int:
        # Dummy function, should never be called
        assert False
        return 0

    def dec_decay(self):
        # Dummy function, should never be called
        assert False

class EmptyCell(CellItem):
    def __init__(self):
        self.char: str = '. '

class AppleCell(CellItem):
    def __init__(self):
        self.char: str = '＠'

class HeadCell(CellItem):
    def __init__(self):
        self.char: str = '％'

class BodyCell(CellItem):
    def __init__(self, d: int):
        self.char: str = '＃'
        self.decay: int = d
    
    def get_decay(self) -> int:
        return self.decay

    def set_decay(self, n: int):
        self.decay = n

    def dec_decay(self):
        self.decay -= 1

# CellItem = EmptyCell | AppleCell | HeadCell | BodyCell

class Cell:
    def __init__(self, r: int, c: int, i: CellItem = EmptyCell()):
        self.r: int = r
        self.c: int = c
        self.item: CellItem = i
        self.cost = 0

    def __lt__(self, rhs: "Cell") -> bool:
        return self.cost < rhs.cost

    def get_r(self) -> int:
        return self.r

    def get_c(self) -> int:
        return self.c
    
    def get_rc(self) -> tuple[int, int]:
        return (self.r, self.c)

    def get_item(self) -> CellItem:
        return self.item

    def set_item(self, i: CellItem):
        self.item = i

    def get_cost(self) -> int:
        return self.cost

class Game:
    def __init__(self, h: int, w: int):
        self.height: int = h
        self.width: int = w
        self.grid: list[Cell] = [Cell(r, c) for r in range(self.width) for c in range(self.height)]
        # self.bodies: set[Cell] = set()
        self.bodies: list[Cell] = []

    def __str__(self) -> str:
        out: str = ""
        for r in range(self.height):
            for c in range(self.width):
                out += str(self.get_item(r, c))
            out += '\n'
        return out

    def setup_game(self, hr, hc, ar, ac):
        self.score: int = 0
        self.head: Cell = self.get_cell(hr, hc)
        self.head.set_item(HeadCell())
        self.apple: Cell = self.get_cell(ar, ac)
        self.apple.set_item(AppleCell())
    
    def get_cell(self, r: int, c: int) -> Cell:
        assert (0 <= r < self.height) and (0 <= c < self.width)
        return self.grid[(r * self.width) + c]

    def get_item(self, r: int, c: int) -> CellItem | None:
        return self.get_cell(r, c).get_item()

    def get_neighbors(self) -> list[Cell]:
        # neighbors: set[Cell] = set()
        neighbors: list[Cell] = []
        r, c = self.head.get_rc()
        for vec in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            try: cell: Cell = self.get_cell(*vec)
            except AssertionError: continue
            else: neighbors.append(cell)
        return neighbors

    def check_legal_move(self, source: Cell, target: Cell) -> bool:
        item: CellItem = target.get_item()
        if type(item) == EmptyCell or AppleCell:
            return True
        elif type(item) == BodyCell:
            if item.get_decay() >= source.get_cost():
                return False
            else:
                return True
        return False

    def do_move(self, target: Cell) -> bool:
        apple_hook: bool = False
        try: assert self.check_legal_move(self.head, target)
        except AssertionError: return False
        item: CellItem = target.get_item()
        if type(item) == EmptyCell or (type(item) == BodyCell and item.get_decay() == 0):
            for body in self.bodies:
                body.get_item().dec_decay()
                if body.get_item().get_decay() <= 0:
                    body.set_item(EmptyCell())
                    self.bodies.remove(body)
        elif type(item) == AppleCell:
            self.score += 1
            apple_hook = True
        self.head.set_item(BodyCell(self.score))
        self.bodies.append(self.head)
        target.set_item(HeadCell())
        self.head = target
        if apple_hook:
            self.move_apple()
        return True

    def move_apple(self):
        while candidate := randint(0, (self.width * self.height) - 1):
            r: int = candidate // self.height
            c: int = candidate % self.width
            cell = self.get_cell(r, c)
            if type(cell.get_item()) == EmptyCell:
                cell.set_item(AppleCell())
                self.apple = cell
                return

    def manhattan(self, s: Cell, g: Cell | None = None) -> int:
        if g == None:
            g = self.apple
        return abs(g.get_c() - s.get_c()) + abs(g.get_r() - s.get_r())

def main() -> None:
    g = Game(10, 10)
    g.setup_game(4, 1, 4, 8)
    print(g)
    input()
    while True:
        n = g.get_neighbors()
        best_h = 99
        best_cell = Cell(-1, -1)
        for m in n:
            h = g.manhattan(m)
            if h < best_h:
                best_cell = m
                best_h = h
        g.do_move(best_cell)
        print(g)
        input()

if __name__ == "__main__":
    main()