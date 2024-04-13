import sys
from time import sleep

import pygame

from settings import Settings
from stats import Stats
from score import Score
from button import Button
from plane import Plane
from bullet import Bullet
from bug import Bug


class Bugattack:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Bug attack")

        # Создание экземпляров для хранения статистики,
        # и панель результатов.
        self.stats = Stats(self)
        self.sb = Score(self)

        self.plane = Plane(self)
        self.bullets = pygame.sprite.Group()
        self.bug = pygame.sprite.Group()

        self._create_fleet()

        # Игра атака жуков запускается в неактивном состоянии.
        self.game_active = False

        #Создает кнопку плэй.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()

            if self.game_active:
                self.plane.update()
                self._update_bullets()
                self._update_bug()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Обрабатывает нажатия клавишь и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки ПЛЭЙ."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Сбрасовыет игровые настройки.
            self.settings.initialize_dynamic_settings()

            #Сброс игровой статистики.
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_plane()
            self.game_active = True

            # Очистка списков жуков и снарядов.
            self.bullets.empty()
            self.bug.empty()

            # Создание нового флота .
            self._create_fleet()
            self.plane.center_plane()

            # Прячет указатель мыши.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_RIGHT:
            self.plane.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.plane.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш."""
        if event.key == pygame.K_RIGHT:
            self.plane.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.plane.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и удаляет старые пули."""
        # Обновление позиции пули.
        self.bullets.update()

        # Избавляется от пуль которые исчезли(вышшли за край экрана).
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_bug_collisions()

    def _check_bullet_bug_collisions(self):
        """Обработка коллизий снарядов с жуками."""
        # Удаление снарядов и жуков участвующих коллизии.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.bug, True, True)

        if collisions:
            for bug in collisions.values():
                self.stats.score += self.settings.bug_points * len(bug)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.bug:
            # Уничтожение существующих снарядов и создание нового флота.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Увеличение уровня.
            self.stats.level += 1
            self.sb.prep_level()

    def _plane_hit(self):
        """Обрабатывает столкновение корабля с жуком."""
        if self.stats.plane_left > 0:
            # Уменьшение ships_left, и обновление очков.
            self.stats.plane_left -= 1
            self.sb.prep_plane()

            # Очистка списков жуков и снарядов.
            self.bullets.empty()
            self.bug.empty()

            # Создание нового флота и размещение самолета в центре.
            self._create_fleet()
            self.plane.center_plane()

            # Пауза.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_bug(self):
        """Проверяет, достиг ли флот края экрана, с последующем обновлением всех во флоте."""
        self._check_fleet_edges()
        self.bug.update()

        # Проверка коллизии жук-корабль.
        if pygame.sprite.spritecollideany(self.plane, self.bug):
            self._plane_hit()

        # Проверить добрались ли жуки до нижнего края экрана.
        self._check_bug_bottom()

    def _check_bug_bottom(self):
        """Проверяет, добрались ли жуки до нижнего края экрана."""
        for bug in self.bug.sprites():
            if bug.rect.bottom >= self.settings.screen_height:
                # Происходит то же что и при столкновении с самолетом.
                self._plane_hit()
                break

    def _create_fleet(self):
        """Создание флота вторжения."""
        # Создание жука и вычисление жуков в ряду.
        # Интервал между соседними жуками равен одному жуку.
        bug = Bug(self)
        bug_width, bug_height = bug.rect.size

        current_x, current_y = bug_width, bug_height
        while current_y < (self.settings.screen_height - 3 * bug_height):
            while current_x < (self.settings.screen_width - 2 * bug_width):
                self._create_bug(current_x, current_y)
                current_x += 2 * bug_width

            # Закончив строку сбросили значение x и увеличили значение y.
            current_x = bug_width
            current_y += 2 * bug_height

    def _create_bug(self, x_position, y_position):
        """Создание жука и размещение его в ряду."""
        new_bug = Bug(self)
        new_bug.x = x_position
        new_bug.rect.x = x_position
        new_bug.rect.y = y_position
        self.bug.add(new_bug)

    def _check_fleet_edges(self):
        """Реагирует на достижение жуком экрана."""
        for bug in self.bug.sprites():
            if bug.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление движения."""
        for bug in self.bug.sprites():
            bug.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Обновляет изображение на экране и отображает новый экран."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.plane.blitme()
        self.bug.draw(self.screen)

        # Выводит информацию о счете.
        self.sb.show_score()

        # Кнопка ПЛЭЙ отображается в том случае если игра не активна.
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ba = Bugattack()
    ba.run_game()
