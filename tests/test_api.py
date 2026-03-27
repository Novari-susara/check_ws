import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


class TestHomePage:
    def test_home_returns_200(self, client: TestClient) -> None:
        response = client.get("/")
        assert response.status_code == 200

    def test_home_contains_start_screen(self, client: TestClient) -> None:
        response = client.get("/")
        assert "Soc Ops" in response.text
        assert "Start Game" in response.text
        assert "How to play" in response.text

    def test_home_sets_session_cookie(self, client: TestClient) -> None:
        response = client.get("/")
        assert "session" in response.cookies


class TestStartGame:
    def test_start_returns_game_board(self, client: TestClient) -> None:
        # First visit to get session
        client.get("/")
        response = client.post("/start")
        assert response.status_code == 200
        assert "FREE SPACE" in response.text
        assert "← Back" in response.text

    def test_board_has_25_squares(self, client: TestClient) -> None:
        client.get("/")
        response = client.post("/start")
        # Count the toggle buttons (squares with hx-post="/toggle/")
        assert response.text.count('hx-post="/toggle/') == 24  # 24 + 1 free space


class TestToggleSquare:
    def test_toggle_marks_square(self, client: TestClient) -> None:
        client.get("/")
        client.post("/start")
        response = client.post("/toggle/0")
        assert response.status_code == 200
        # The response should contain the game screen with a marked square
        assert "FREE SPACE" in response.text


class TestResetGame:
    def test_reset_returns_start_screen(self, client: TestClient) -> None:
        client.get("/")
        client.post("/start")
        response = client.post("/reset")
        assert response.status_code == 200
        assert "Start Game" in response.text
        assert "How to play" in response.text


class TestDismissModal:
    def test_dismiss_returns_game_screen(self, client: TestClient) -> None:
        client.get("/")
        client.post("/start")
        response = client.post("/dismiss-modal")
        assert response.status_code == 200
        assert "FREE SPACE" in response.text


class TestSelectMode:
    def test_select_bingo_mode(self, client: TestClient) -> None:
        client.get("/")
        response = client.post("/select-mode?mode=bingo")
        assert response.status_code == 200

    def test_select_hunt_mode(self, client: TestClient) -> None:
        client.get("/")
        response = client.post("/select-mode?mode=hunt")
        assert response.status_code == 200


class TestStartHunt:
    def test_start_hunt_returns_hunt_screen(self, client: TestClient) -> None:
        client.get("/")
        client.post("/select-mode?mode=hunt")
        response = client.post("/start-hunt")
        assert response.status_code == 200
        assert "Scavenger Hunt" in response.text

    def test_hunt_has_24_items(self, client: TestClient) -> None:
        client.get("/")
        client.post("/select-mode?mode=hunt")
        response = client.post("/start-hunt")
        # Count the check buttons (items with hx-post="/check/")
        assert response.text.count('hx-post="/check/') == 24

    def test_hunt_displays_progress_counter(self, client: TestClient) -> None:
        client.get("/")
        client.post("/select-mode?mode=hunt")
        response = client.post("/start-hunt")
        assert "0/24" in response.text


class TestCheckHuntItem:
    def test_check_item_marks_it(self, client: TestClient) -> None:
        client.get("/")
        client.post("/select-mode?mode=hunt")
        client.post("/start-hunt")
        response = client.post("/check/0")
        assert response.status_code == 200
        # Response should show updated counter
        assert "1/24" in response.text

    def test_check_multiple_items_updates_progress(self, client: TestClient) -> None:
        client.get("/")
        client.post("/select-mode?mode=hunt")
        client.post("/start-hunt")
        client.post("/check/0")
        client.post("/check/1")
        response = client.post("/check/5")
        assert response.status_code == 200
        assert "3/24" in response.text

    def test_uncheck_item_decreases_progress(self, client: TestClient) -> None:
        client.get("/")
        client.post("/select-mode?mode=hunt")
        client.post("/start-hunt")
        client.post("/check/0")
        response = client.post("/check/0")  # Toggle back
        assert response.status_code == 200
        assert "0/24" in response.text


class TestHuntCompletion:
    def test_hunt_complete_shows_modal(self, client: TestClient) -> None:
        client.get("/")
        client.post("/select-mode?mode=hunt")
        client.post("/start-hunt")
        # Check all 24 items
        for i in range(24):
            response = client.post(f"/check/{i}")
        # Last response should show completion modal
        assert (
            "Hunt Complete" in response.text or "hunt-complete-modal" in response.text
        )

    def test_hunt_complete_final_counter(self, client: TestClient) -> None:
        client.get("/")
        client.post("/select-mode?mode=hunt")
        client.post("/start-hunt")
        # Check all 24 items
        for i in range(24):
            response = client.post(f"/check/{i}")
        # Final counter should show 24/24
        assert "24/24" in response.text


class TestDismissHuntModal:
    def test_dismiss_hunt_modal_returns_hunt_screen(self, client: TestClient) -> None:
        client.get("/")
        client.post("/select-mode?mode=hunt")
        client.post("/start-hunt")
        response = client.post("/dismiss-hunt-modal")
        assert response.status_code == 200
        assert "Scavenger Hunt" in response.text
