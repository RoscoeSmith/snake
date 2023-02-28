from random import randint

class CellItem:
    def __init__(self):
        self.char: str = "??"

    def __str__(self) -> str:
        return self.char

class EmptyCell(CellItem):
    def __init__(self):
        self.char: str = '  '

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

# CellItem = EmptyCell | AppleCell | HeadCell | BodyCell

class Cell:
    def __init__(self, r: int, c: int, i: CellItem = EmptyCell()):
        self.r: int = r
        self.c: int = c
        self.item: CellItem = i

    def get_item(self) -> CellItem:
        return self.item

    def set_item(self, i: CellItem):
        self.item = i

class Game:
    def __init__(self, h: int, w: int):
        self.height: int = h
        self.width: int = w
        self.grid: list[Cell] = [Cell(r, c) for c in range(self.width) for r in range(self.height)]
        self.score: int = 0

    def __str__(self) -> str:
        out: str = ""
        for r in range(self.height):
            for c in range(self.width):
                out += str(self.get_item(r, c))
        return out
    
    def get_cell(self, r: int, c: int) -> Cell | None:
        if (0 >= r < self.height) and (0 >= c < self.width):
            return self.grid[r * self.width + c]
        else:
            return None

    def get_item(self, r: int, c: int) -> CellItem | None:
        cell = self.get_cell(r, c)
        if cell != None:
            return cell.get_item()
        else:
            return None

    def move_apple(self):
        while candidate := randint(0, (self.width * self.height) - 1):
            r: int = candidate // self.height
            c: int = candidate % self.width
            cell: Cell | None = self.get_cell(r, c)
            if cell != None:
                if type(cell.get_item()) == EmptyCell:
                    cell.set_item(AppleCell())
                    return

def main() -> None:
    pass

if __name__ == "__main__":
    main()