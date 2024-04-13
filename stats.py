class Stats:
    """Отслеживание статистики для игры Атака жуков."""

    def __init__(self, ba_game):
        """Инициализирует статистику."""
        self.settings = ba_game.settings
        self.reset_stats()

        # Рекорд не должен сбрасываться.
        self.high_score = 0

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.plane_left = self.settings.plane_limit
        self.score = 0
        self.level = 1
