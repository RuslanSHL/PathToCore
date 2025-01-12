import pygame
from ui import FollowText


class Player(pygame.sprite.Sprite):
    def __init__(self, game, texture, x, y, width, height, group=None):
        super().__init__(game.life if group is None else group)

        self.texture = texture
        self.width = width
        self.height = height
        self.game = game

        if type(texture) is tuple:
            self.orig_image = pygame.Surface((width, height))
            self.orig_image.fill(texture)
        else:
            self.orig_image = game.load_image(texture)
            self.orig_image = pygame.transform.scale(self.orig_image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)

        self.direction_x = 0
        self.direction_y = 0
        self._delta_x = 0
        self._delta_y = 0
        self.speed_x = 0
        self.speed_y = 0
        self.walk_speed = 3
        self.interact = None
        self._last_interact = None
        self.animated = False
        self.can_walk = True

        self.draw_x = x
        self.draw_y = y
        self.image = self.orig_image

        self.text = FollowText(
            game,
            self,
            "press e to interact",
            (0, 0, 0), "arial", 20
        )

    def set_animation(self, col, row, width, height, fpt):
        self.fpt = fpt  # Frame per ticks
        self.animated = True
        self.current_frame = 0
        self._ticks = 0
        self.orig_image = []
        image = self.game.load_image(self.texture)
        for r in range(row):
            for c in range(col):
                frame = image.subsurface(pygame.Rect(c * width, r * height, width, height))
                self.orig_image.append(pygame.transform.scale(frame, (self.width, self.height)))
        self.frames = self.orig_image.copy()
        self.image = self.orig_image[0]

    def update(self):
        ticks = self.game.tick
        if self.animated:
            self._ticks += ticks
            if self._ticks > 1 / self.fpt:
                self._ticks %= 1 / self.fpt
                if (self.direction_x or self.direction_y) and self.can_walk:
                    self.current_frame = (self.current_frame + 1) % len(self.frames)
                    self.image = self.frames[self.current_frame]
                else:
                    self.image = self.frames[0]
                    self.current_frame = 0
        # FIXME: персонаж вверх влево идёт медленно
        # перемещение
        if (self.direction_x or self.direction_y) and self.can_walk:
            if self.direction_x and self.direction_y:
                walk_speed_x = self.walk_speed / 2 * self.direction_x
                walk_speed_y = self.walk_speed / 2 * self.direction_y
            else:
                walk_speed_x = self.walk_speed * self.direction_x
                walk_speed_y = self.walk_speed * self.direction_y
            last_x = self.rect.x
            last_y = self.rect.y
            self._delta_x += (self.speed_x + walk_speed_x) * ticks

            # TODO: нужно оптимизировать. Сейчас O(2n)
            # столкновения
            if self._delta_x // 1:
                self.rect.x += self._delta_x // 1
                self._delta_x %= 1

            for build in self.game.collibe_group:
                if self.rect.colliderect(build.rect):
                    if last_x < self.rect.x:
                        self.rect.right = build.rect.left
                    elif last_x > self.rect.x:
                        self.rect.left = build.rect.right

            self._delta_y += (self.speed_y + walk_speed_y) * ticks
            if self._delta_y // 1:
                self.rect.y += self._delta_y // 1
                self._delta_y %= 1

            for build in self.game.collibe_group:
                if self.rect.colliderect(build.rect):
                    if last_y < self.rect.y:
                        self.rect.bottom = build.rect.top
                    elif last_y > self.rect.y:
                        self.rect.top = build.rect.bottom

        # взаимодействия
        for item in self.game.item:
            if self.rect.colliderect(item.interact_rect):
                if self.interact is None:
                    self.interact = item
                    self.game.ui.append(self.text)
                break
        else:
            if self.interact is not None:
                self.interact = None
                if self.text in self.game.ui:
                    self.game.ui.remove(self.text)

    def draw(self, surface):
        surface.blit(self.image, (self.draw_x, self.draw_y))
