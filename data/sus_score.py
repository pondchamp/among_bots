from enum import Enum

from data.player import Player

# Dumb scores for naive solution
SCORE_SUS = 1.0
SCORE_SAFE = 0.0


class SusScore(Enum):
    SUS = 0
    IDK = 1
    SAFE = 2


class PlayerSus:
    def __init__(self, player: str, sus_score: float):
        self.player = player
        if 0 <= sus_score <= 1:
            self.sus_score = sus_score
        else:
            raise ValueError("sus_score must be between 0 and 1")

    def get_sus(self) -> SusScore:
        if self.sus_score >= SCORE_SUS:
            return SusScore.SUS
        elif self.sus_score <= SCORE_SAFE:
            return SusScore.SAFE
        return SusScore.IDK
