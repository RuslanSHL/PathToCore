import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__(game.all_sprites)
        self.add(game.life)
        self.game = game
        self.image = pygame.Surface([10, 10])
        self.image.fill((255, 255, 255))
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.direction_x = 0
        self.direction_y = 0
        self.speed_x = 0
        self.speed_y = 0
        self.is_walk = False
        self.walk_speed = 3
        self.interact = None

    def update(self):
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
                    print('press e to interact')
                    self.interact = item
                break
        else:
            self.interact = None
