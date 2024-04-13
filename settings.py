class Settings:
    """Класс для хранения всех настроекигры Атака жуков."""

    def __init__(self):
        """Инициализирует настройки игри."""
        # параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Настройки самолета
        self.plane_limit = 3

        # Параметры снаряда
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        # Параметры жуков
        self.fleet_drop_speed = 10

        # Темп ускорения игры
        self.speedup_scale = 1.1
        # Темп роста стоимости пришельцев
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        self.plane_speed = 1.5
        self.bullet_speed = 2.5
        self.bug_speed = 1.0

        # fleet_direction 1 при движении вправо; -1 при движении в лево.
        self.fleet_direction = 1

        # Подсчет очков
        self.bug_points = 50

    def increase_speed(self):
        """Увеличивает настройки скорости."""
        self.plane_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.bug_speed *= self.speedup_scale

        self.bug_points = int(self.bug_points * self.score_scale)
