from dataclasses import dataclass, field

from app.game_logic import (
    check_bingo,
    check_hunt_complete,
    count_hunt_checked,
    generate_board,
    generate_hunt,
    get_winning_square_ids,
    toggle_hunt_item,
    toggle_square,
)
from app.models import BingoLine, BingoSquareData, GameState, HuntItemData, HuntState


@dataclass
class GameSession:
    """Holds the state for a single game session."""

    game_state: GameState = GameState.START
    board: list[BingoSquareData] = field(default_factory=list)
    winning_line: BingoLine | None = None
    show_bingo_modal: bool = False
    hunt_mode: str | None = None
    hunt_state: HuntState = HuntState.START
    hunt_items: list[HuntItemData] = field(default_factory=list)
    hunt_progress_count: int = 0
    show_hunt_complete_modal: bool = False

    @property
    def winning_square_ids(self) -> set[int]:
        return get_winning_square_ids(self.winning_line)

    @property
    def has_bingo(self) -> bool:
        return self.game_state == GameState.BINGO

    @property
    def hunt_is_playing(self) -> bool:
        return self.hunt_state == HuntState.PLAYING

    def _reset_bingo_modal(self) -> None:
        """Reset bingo modal state."""
        self.show_bingo_modal = False

    def _reset_hunt_modal(self) -> None:
        """Reset hunt modal state."""
        self.show_hunt_complete_modal = False

    def start_game(self) -> None:
        self.board = generate_board()
        self.winning_line = None
        self.game_state = GameState.PLAYING
        self.show_bingo_modal = False

    def handle_square_click(self, square_id: int) -> None:
        if self.game_state != GameState.PLAYING:
            return
        self.board = toggle_square(self.board, square_id)

        if self.winning_line is None:
            bingo = check_bingo(self.board)
            if bingo is not None:
                self.winning_line = bingo
                self.game_state = GameState.BINGO
                self.show_bingo_modal = True

    def reset_game(self) -> None:
        self.game_state = GameState.START
        self.board = []
        self.winning_line = None
        self._reset_bingo_modal()

    def dismiss_modal(self) -> None:
        self._reset_bingo_modal()
        self.game_state = GameState.PLAYING

    def select_mode(self, mode: str) -> None:
        """Select game mode (bingo or hunt)."""
        self.hunt_mode = mode

    def start_hunt(self) -> None:
        """Start a new scavenger hunt."""
        self.hunt_items = generate_hunt()
        self.hunt_state = HuntState.PLAYING
        self.hunt_progress_count = 0
        self._reset_hunt_modal()

    def handle_hunt_item_click(self, item_id: int) -> None:
        """Toggle a hunt item and check for completion."""
        if not self.hunt_is_playing:
            return
        self.hunt_items = toggle_hunt_item(self.hunt_items, item_id)
        self.hunt_progress_count = count_hunt_checked(self.hunt_items)

        if check_hunt_complete(self.hunt_items):
            self.hunt_state = HuntState.COMPLETE
            self.show_hunt_complete_modal = True

    def dismiss_hunt_modal(self) -> None:
        """Dismiss the hunt completion modal."""
        self._reset_hunt_modal()
        self.hunt_state = HuntState.PLAYING

    def reset_hunt(self) -> None:
        """Reset hunt state."""
        self.hunt_mode = None
        self.hunt_state = HuntState.START
        self.hunt_items = []
        self.hunt_progress_count = 0
        self._reset_hunt_modal()


# In-memory session store keyed by session ID
_sessions: dict[str, GameSession] = {}


def get_session(session_id: str) -> GameSession:
    """Get or create a game session for the given session ID."""
    if session_id not in _sessions:
        _sessions[session_id] = GameSession()
    return _sessions[session_id]
