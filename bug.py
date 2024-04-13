import pygame

from pygame.sprite import Sprite


class Bug(Sprite):
    """Класс, представляющий одного жука."""

    def __init__(self, ba_game):
        """Инициализирует жука и задает его начальную позицию."""
        super().__init__()
        self.screen = ba_game.screen
        self.settings = ba_game.settings

        # Загрузка изображения жука и назначение атрибута rect.
        self.image = pygame.image.load('images/bug.bmp')
        self.rect = self.image.get_rect()

        # Каждый новый жук появляется в левом верхнем углу экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной горизонтальной позиции жука.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Возвращает True,если жук находится у края экрана."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Перемещает жука в право или в влево."""
        self.x += self.settings.bug_speed * self.settings.fleet_direction
        self.rect.x = self.x
