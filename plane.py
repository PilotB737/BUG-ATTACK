import pygame
from pygame.sprite import Sprite


class Plane(Sprite):
    """Класс для управления самолетом."""

    def __init__(self, ba_game):
        """Инициализирует самолет и задает его начальную позицию."""
        super().__init__()
        self.screen = ba_game.screen
        self.settings = ba_game.settings
        self.screen_rect = ba_game.screen.get_rect()

        # Загружает изображение самолета и получает прямоугольник.
        self.image = pygame.image.load('images/plane.bmp')
        self.rect = self.image.get_rect()

        # Каждый новый самолет появляется у нижнего края экрана.
        self.rect.midbottom = self.screen_rect.midbottom

        # Сохранение вещественной координаты центра корабля.
        self.x = float(self.rect.x)

        # Флаги перемещения.
        self.moving_right = False
        self.moving_left = False

    def center_plane(self):
        """Центрирование самолета на экране."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        """Обновление позиции самолета с учетом флагов."""
        # Обновляется атрибут x, не rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.plane_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.plane_speed
            
        # Обновление атрибута rect на основании self.x.
        self.rect.x = self.x

    def blitme(self):
        """Рисует самолет в текущей позиции."""
        self.screen.blit(self.image, self.rect)
