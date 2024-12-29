import pygame


class Build(pygame.sprite.Sprite):
    def __init__(self, game, color, x, y, width, height, collibe):
        super().__init__(game.all_sprites)
        self.game = game
        self.add(game.building_group)
        if collibe:
            self.add(game.collibe_building_group)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = pygame.Rect(x, y, width, height)

    def update(self):
        pass


class Item(Build):
    def __init__(self, *args, radius=10):
        super().__init__(*args)
        self.add(self.game.item)
        self.interact_rect = pygame.Rect(self.rect.x - radius,
                                         self.rect.y - radius,
                                         self.rect.width + 2 * radius,
                                         self.rect.height + 2 * radius
                                        )

    def interact(self):
        print('interact with', self)


class Floor(Build):
    def __init__(self, *args):
        super().__init__(*args)
        self.add(self.game.floor)


class Wall(Build):
    def __init__(self, *args):
        super().__init__(*args)
        self.add(self.game.wall)
