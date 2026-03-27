from app.data import FREE_SPACE, QUESTIONS
from app.game_logic import (
    CENTER_INDEX,
    check_bingo,
    generate_board,
    get_winning_square_ids,
    toggle_square,
)
from app.models import BingoLine, BingoSquareData


class TestGenerateBoard:
    def test_board_has_25_squares(self) -> None:
        board = generate_board()
        assert len(board) == 25

    def test_center_is_free_space(self) -> None:
        board = generate_board()
        center = board[CENTER_INDEX]
        assert center.is_free_space is True
        assert center.is_marked is True
        assert center.text == FREE_SPACE

    def test_non_center_squares_are_not_free_space(self) -> None:
        board = generate_board()
        for i, square in enumerate(board):
            if i != CENTER_INDEX:
                assert square.is_free_space is False
                assert square.is_marked is False

    def test_all_questions_from_pool(self) -> None:
        board = generate_board()
        texts = {s.text for s in board if not s.is_free_space}
        assert texts.issubset(set(QUESTIONS))

    def test_squares_have_sequential_ids(self) -> None:
        board = generate_board()
        for i, square in enumerate(board):
            assert square.id == i

    def test_board_is_shuffled(self) -> None:
        """Verify two boards aren't identical (high probability)."""
        board1 = generate_board()
        board2 = generate_board()
        texts1 = [s.text for s in board1]
        texts2 = [s.text for s in board2]
        # Extremely unlikely to be identical
        assert texts1 != texts2


class TestToggleSquare:
    def test_toggle_marks_unmarked_square(self) -> None:
        board = generate_board()
        square_id = 0
        assert board[square_id].is_marked is False
        new_board = toggle_square(board, square_id)
        assert new_board[square_id].is_marked is True

    def test_toggle_unmarks_marked_square(self) -> None:
        board = generate_board()
        board = toggle_square(board, 0)
        assert board[0].is_marked is True
        board = toggle_square(board, 0)
        assert board[0].is_marked is False

    def test_toggle_does_not_affect_free_space(self) -> None:
        board = generate_board()
        new_board = toggle_square(board, CENTER_INDEX)
        assert new_board[CENTER_INDEX].is_marked is True  # Still marked

    def test_toggle_returns_new_list(self) -> None:
        board = generate_board()
        new_board = toggle_square(board, 0)
        assert board is not new_board


class TestCheckBingo:
    def _make_board(self, marked_ids: set[int]) -> list[BingoSquareData]:
        board = generate_board()
        result = []
        for square in board:
            if square.id in marked_ids or square.is_free_space:
                result.append(
                    BingoSquareData(
                        id=square.id,
                        text=square.text,
                        is_marked=True,
                        is_free_space=square.is_free_space,
                    )
                )
            else:
                result.append(square)
        return result

    def test_no_bingo_initially(self) -> None:
        board = generate_board()
        assert check_bingo(board) is None

    def test_row_bingo(self) -> None:
        # Mark first row: indices 0-4
        board = self._make_board({0, 1, 2, 3, 4})
        result = check_bingo(board)
        assert result is not None
        assert result.type == "row"
        assert result.squares == [0, 1, 2, 3, 4]

    def test_column_bingo(self) -> None:
        # Mark first column: indices 0, 5, 10, 15, 20
        board = self._make_board({0, 5, 10, 15, 20})
        result = check_bingo(board)
        assert result is not None
        assert result.type == "column"
        assert result.squares == [0, 5, 10, 15, 20]

    def test_diagonal_bingo(self) -> None:
        # Mark diagonal: 0, 6, 12, 18, 24 (12 is free space)
        board = self._make_board({0, 6, 18, 24})
        result = check_bingo(board)
        assert result is not None
        assert result.type == "diagonal"
        assert result.squares == [0, 6, 12, 18, 24]

    def test_partial_line_no_bingo(self) -> None:
        board = self._make_board({0, 1, 2, 3})  # Only 4 of 5 in first row
        assert check_bingo(board) is None


class TestGetWinningSquareIds:
    def test_none_line_returns_empty_set(self) -> None:
        assert get_winning_square_ids(None) == set()

    def test_returns_square_ids(self) -> None:
        line = BingoLine(type="row", index=0, squares=[0, 1, 2, 3, 4])
        assert get_winning_square_ids(line) == {0, 1, 2, 3, 4}


class TestGenerateHunt:
    def test_hunt_has_24_items(self) -> None:
        from app.game_logic import generate_hunt

        hunt = generate_hunt()
        assert len(hunt) == 24

    def test_all_hunt_items_are_questions(self) -> None:
        from app.game_logic import generate_hunt

        hunt = generate_hunt()
        texts = {item.text for item in hunt}
        assert texts.issubset(set(QUESTIONS))

    def test_hunt_items_have_sequential_ids(self) -> None:
        from app.game_logic import generate_hunt

        hunt = generate_hunt()
        for i, item in enumerate(hunt):
            assert item.id == i

    def test_hunt_items_not_checked_initially(self) -> None:
        from app.game_logic import generate_hunt

        hunt = generate_hunt()
        for item in hunt:
            assert item.is_checked is False

    def test_hunt_is_shuffled(self) -> None:
        from app.game_logic import generate_hunt

        hunt1 = generate_hunt()
        hunt2 = generate_hunt()
        texts1 = [item.text for item in hunt1]
        texts2 = [item.text for item in hunt2]
        # Extremely unlikely to be identical
        assert texts1 != texts2


class TestToggleHuntItem:
    def test_toggle_checks_unchecked_item(self) -> None:
        from app.game_logic import generate_hunt, toggle_hunt_item

        hunt = generate_hunt()
        item_id = 0
        assert hunt[item_id].is_checked is False
        new_hunt = toggle_hunt_item(hunt, item_id)
        assert new_hunt[item_id].is_checked is True

    def test_toggle_unchecks_checked_item(self) -> None:
        from app.game_logic import generate_hunt, toggle_hunt_item

        hunt = generate_hunt()
        hunt = toggle_hunt_item(hunt, 0)
        assert hunt[0].is_checked is True
        hunt = toggle_hunt_item(hunt, 0)
        assert hunt[0].is_checked is False

    def test_toggle_returns_new_list(self) -> None:
        from app.game_logic import generate_hunt, toggle_hunt_item

        hunt = generate_hunt()
        new_hunt = toggle_hunt_item(hunt, 0)
        assert hunt is not new_hunt

    def test_toggle_other_items_unchanged(self) -> None:
        from app.game_logic import generate_hunt, toggle_hunt_item

        hunt = generate_hunt()
        hunt = toggle_hunt_item(hunt, 0)
        hunt = toggle_hunt_item(hunt, 0)
        # Toggle item 0 twice, then toggle item 1
        new_hunt = toggle_hunt_item(hunt, 1)
        assert new_hunt[0].is_checked is False
        assert new_hunt[1].is_checked is True


class TestCheckHuntComplete:
    def test_hunt_not_complete_initially(self) -> None:
        from app.game_logic import check_hunt_complete, generate_hunt

        hunt = generate_hunt()
        assert check_hunt_complete(hunt) is False

    def test_hunt_not_complete_with_some_items_checked(self) -> None:
        from app.game_logic import (
            check_hunt_complete,
            generate_hunt,
            toggle_hunt_item,
        )

        hunt = generate_hunt()
        hunt = toggle_hunt_item(hunt, 0)
        hunt = toggle_hunt_item(hunt, 5)
        hunt = toggle_hunt_item(hunt, 10)
        assert check_hunt_complete(hunt) is False

    def test_hunt_complete_when_all_items_checked(self) -> None:
        from app.game_logic import (
            check_hunt_complete,
            generate_hunt,
            toggle_hunt_item,
        )

        hunt = generate_hunt()
        for i in range(len(hunt)):
            hunt = toggle_hunt_item(hunt, i)
        assert check_hunt_complete(hunt) is True


class TestCountHuntChecked:
    def test_count_zero_initially(self) -> None:
        from app.game_logic import count_hunt_checked, generate_hunt

        hunt = generate_hunt()
        assert count_hunt_checked(hunt) == 0

    def test_count_increases_with_toggles(self) -> None:
        from app.game_logic import (
            count_hunt_checked,
            generate_hunt,
            toggle_hunt_item,
        )

        hunt = generate_hunt()
        hunt = toggle_hunt_item(hunt, 0)
        assert count_hunt_checked(hunt) == 1
        hunt = toggle_hunt_item(hunt, 1)
        assert count_hunt_checked(hunt) == 2
        hunt = toggle_hunt_item(hunt, 0)
        assert count_hunt_checked(hunt) == 1

    def test_count_all_checked(self) -> None:
        from app.game_logic import (
            count_hunt_checked,
            generate_hunt,
            toggle_hunt_item,
        )

        hunt = generate_hunt()
        for i in range(len(hunt)):
            hunt = toggle_hunt_item(hunt, i)
        assert count_hunt_checked(hunt) == 24
