import pygame
from ui import InteractText


class Player(pygame.sprite.Sprite):
    def __init__(self, game, texture, x, y, width, height):
        super().__init__(game.all_sprites)
        self.add(game.life)
        self.texture = texture
        self.width = width
        self.height = height
        self.game = game
        self.image = game.load_image(texture)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)

        self.direction_x = 0
        self.direction_y = 0
        self.speed_x = 0
        self.speed_y = 0
        self.is_walk = False
        self.walk_speed = 3
        self.interact = None
        self._last_interact = None
        self.animated = False

        self.text = InteractText(x, y, 'press e to interact', (0, 0, 0), 'arial', 20, self)

    def set_animation(self, col, row,  width, height, fpf):
        self.fpf = fpf
        self.animated = True
        self.current_frame = 0
        self.current_f = 0
        self.frames = []
        image = self.game.load_image(self.texture)
        for r in range(row):
            for c in range(col):
                frame = pygame.Rect(c * width, r * height, width, height)
                self.frames.append(image.subsurface(frame))
        self.image = self.frames[0]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def update(self):
        if self.animated:
            self.current_f += 1
            if self.game.fps / self.fpf == self.current_f:
                self.current_f = 0
                if self.direction_x or self.direction_y:
                    self.current_frame  = (self.current_frame + 1) % len(self.frames)
                    self.image = self.frames[self.current_frame]
                    self.image = pygame.transform.scale(self.image, (self.width, self.height))
                else:
                    self.image = self.frames[0]
                    self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # FIXME: персонаж вверх влево идёт медленно
        # перемещение
        if self.direction_x and self.direction_y:
            walk_speed_x = self.walk_speed / 2 * self.direction_x
            walk_speed_y = self.walk_speed / 2 * self.direction_y
        else:
            walk_speed_x = self.walk_speed * self.direction_x
            walk_speed_y = self.walk_speed * self.direction_y
        last_x = self.rect.x
        last_y = self.rect.y
        self.rect.x += self.speed_x + walk_speed_x

        # TODO: нужно оптимизировать. Сейчас O(2n)
        # столкновения
        for build in self.game.collibe_building_group:
            if self.rect.colliderect(build.rect):
                if last_x < self.rect.x:
                    self.rect.right = build.rect.left
                elif last_x > self.rect.x:
                    self.rect.left = build.rect.right

        self.rect.y += self.speed_y + walk_speed_y

        for build in self.game.collibe_building_group:
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
                    print(self.game.ui)
                break
        else:
            if self.interact is not None:
                self.interact = None
                self.game.ui.remove(self.text)
