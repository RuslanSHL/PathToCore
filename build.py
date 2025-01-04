import pygame


class Build(pygame.sprite.Sprite):
    def __init__(self, game, texture, x, y, width, height, is_collibe):
        super().__init__()
        self.game = game
        self.animated = False
        self.is_collibe = is_collibe
        if is_collibe:
            self.add(game.collibe_group)
        if type(texture) is str:
            self.orig_image = game.load_image(texture)
            self.orig_image = pygame.transform.scale(self.orig_image, (width, height))
        else:
            self.orig_image = pygame.Surface((width, height))
            self.orig_image.fill(texture)
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height

        self.image = self.orig_image
        self.draw_x = x
        self.draw_y = y

    def draw(self, surface):
        surface.blit(self.image, (self.draw_x, self.draw_y))

    def update(self):
        pass


class Item(Build):
    def __init__(self, *args, radius=10):
        super().__init__(*args)
        self.add(self.game.item)
        self.interact_rect = pygame.Rect(
            self.rect.x - radius,
            self.rect.y - radius,
            self.rect.width + 2 * radius,
            self.rect.height + 2 * radius,
        )

    def interact(self):
        self.game.phase.story_event_handling(self)


class Floor(Build):
    def __init__(self, *args):
        super().__init__(*args)
        self.add(self.game.floor)


class Wall(Build):
    def __init__(self, *args):
        super().__init__(*args)
        self.add(self.game.wall)


class Door(Build):
    def __init__(self, *args, radius=10):
        super().__init__(*args)
        self.add(self.game.item)
        self.interact_rect = pygame.Rect(
            self.rect.x - radius,
            self.rect.y - radius,
            self.rect.width + 2 * radius,
            self.rect.height + 2 * radius,
        )

    def toggle(self):
        if self.is_collibe:
            self.remove(self.game.collibe_group)
            self.is_collibe = False
        else:
            self.add(self.game.collibe_group)
            self.is_collibe = True

    def interact(self):
        self.toggle()
