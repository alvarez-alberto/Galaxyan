class ScoreService:
    def __init__(self) -> None:
        self._high_score = 500
        self._current_score = 0

    def update_score_player(self, value:int) -> bool:
        self._current_score += value
        if self._current_score > self._high_score:
            self._high_score = self._current_score
            return True
        return False

    def get_high_score_player(self) -> int:
        return self._high_score       

    def get_current_score_player(self) -> int:
        return self._current_score
    
    def reset_current_score(self) -> None:
        self._current_score = 0
        