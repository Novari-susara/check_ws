import functools
import random
from typing import TypeVar

from app.data import FREE_SPACE, QUESTIONS
from app.models import BingoLine, BingoSquareData, HuntItemData

BOARD_SIZE = 5
CENTER_INDEX = 12  # 5x5 grid, center is index 12 (row 2, col 2)

# Generic type for model instances with id and toggleable state
T = TypeVar("T")


def _toggle_by_id(items: list[T], item_id: int, state_field: str) -> list[T]:
    """Generic toggle helper: flip state_field for item matching item_id."""
    return [
        item.model_copy(update={state_field: not getattr(item, state_field)})
        if item.id == item_id
        else item
        for item in items
    ]


def generate_board() -> list[BingoSquareData]:
    """Generate a new 5x5 bingo board."""
    questions = iter(random.sample(QUESTIONS, 24))
    return [
        BingoSquareData(id=i, text=FREE_SPACE, is_marked=True, is_free_space=True)
        if i == CENTER_INDEX
        else BingoSquareData(id=i, text=next(questions))
        for i in range(BOARD_SIZE * BOARD_SIZE)
    ]


def toggle_square(
    board: list[BingoSquareData], square_id: int
) -> list[BingoSquareData]:
    """Toggle a square's marked state. Returns a new board list."""
    return [
        sq.model_copy(update={"is_marked": not sq.is_marked})
        if sq.id == square_id and not sq.is_free_space
        else sq
        for sq in board
    ]


@functools.cache
def _get_winning_lines() -> tuple[BingoLine, ...]:
    """Get all possible winning lines (cached)."""
    lines: list[BingoLine] = []

    for row in range(BOARD_SIZE):
        squares = [row * BOARD_SIZE + col for col in range(BOARD_SIZE)]
        lines.append(BingoLine(type="row", index=row, squares=squares))

    for col in range(BOARD_SIZE):
        squares = [row * BOARD_SIZE + col for row in range(BOARD_SIZE)]
        lines.append(BingoLine(type="column", index=col, squares=squares))

    lines.append(BingoLine(type="diagonal", index=0, squares=[0, 6, 12, 18, 24]))
    lines.append(BingoLine(type="diagonal", index=1, squares=[4, 8, 12, 16, 20]))

    return tuple(lines)


def check_bingo(board: list[BingoSquareData]) -> BingoLine | None:
    """Check if there's a bingo and return the winning line."""
    if len(board) < BOARD_SIZE * BOARD_SIZE:
        return None
    return next(
        (
            line
            for line in _get_winning_lines()
            if all(board[idx].is_marked for idx in line.squares)
        ),
        None,
    )


def get_winning_square_ids(line: BingoLine | None) -> set[int]:
    """Get the square IDs that are part of a winning line."""
    return set(line.squares) if line else set()


def generate_hunt() -> list[HuntItemData]:
    """Generate a new scavenger hunt with 24 items."""
    questions = random.sample(QUESTIONS, 24)
    return [HuntItemData(id=i, text=text) for i, text in enumerate(questions)]


def toggle_hunt_item(items: list[HuntItemData], item_id: int) -> list[HuntItemData]:
    """Toggle a hunt item's checked state. Returns a new list."""
    return _toggle_by_id(items, item_id, "is_checked")  # type: ignore


def check_hunt_complete(items: list[HuntItemData]) -> bool:
    """Check if all hunt items are checked."""
    return all(item.is_checked for item in items)


def count_hunt_checked(items: list[HuntItemData]) -> int:
    """Count how many hunt items are checked."""
    return sum(1 for item in items if item.is_checked)
