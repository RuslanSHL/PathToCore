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
        self.image_width = width
        self.image_height = height
        self.image_x = x
        self.image_y = y

    def draw(self, surface):
        surface.blit(self.image, (self.draw_x, self.draw_y))

    def set_animation(self, animation, row, col, width, height, fpt, one=True, next_image=None):
        self.fpt = fpt  # Frame per ticks
        self.one = one
        self.animated = True
        self.current_frame = 0
        self._ticks = 0
        self.next_image = next_image if next_image is not None else self.orig_image
        self.orig_image = []
        image = self.game.load_image(animation)
        for r in range(row):
            for c in range(col):
                frame = image.subsurface(pygame.Rect(c * width, r * height, width, height))
                self.orig_image.append(frame)
        self.frames = self.orig_image.copy()
        self.image = self.orig_image[0]

    def update(self):
        ticks = self.game.tick
        if self.animated:
            self._ticks += ticks
            if self._ticks > 1 / self.fpt:
                self._ticks %= 1 / self.fpt
                if self.one:
                    self.current_frame += 1
                    if self.current_frame < len(self.frames):
                        self.animated = False
                        self.orig_image = self.next_image
                        self.game.camera.update_size()
                    else:
                        self.image = self.frames[self.current_frame]
                else:
                    self.current_frame = (self.current_frame + 1) % len(self.frames)
                    self.image = self.frames[self.current_frame]


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

    def delete(self):
        self.remove(self.game.floor)


class Wall(Build):
    def __init__(self, *args):
        super().__init__(*args)
        self.add(self.game.wall)


class Door(Item):
    def __init__(self, *args, radius=10, horizontal=False, closed=False):
        self.horizontal = horizontal
        self.closed = closed
        super().__init__(*args, radius=radius)
        if horizontal:
            self.orig_image = pygame.transform.rotate(self.orig_image, -90)

    def toggle(self):
        if self.is_collibe:
            self.remove(self.game.collibe_group)
            self.is_collibe = False
        else:
            self.add(self.game.collibe_group)
            self.is_collibe = True

    def interact(self):
        if not self.closed:
            # FIXME: Ужастные костыли, и нужно добавить анимации
            # if self.is_collibe:
            #     self.set_animation('door_open.png', 1, one=True, next_image='opened_door.png')
            # else:
            #     self.set_animation('door_close.png', 1, one=True, next_image='closed_door.png')
            if self.is_collibe:
                if self.horizontal:
                    self.orig_image = pygame.transform.rotate(self.game.load_image('opened_door.png'), -90)
                    self.image_y -= 64
                    self.height = 96
                else:
                    self.orig_image = self.game.load_image('opened_door.png')
                    self.image_x -= 64
                    self.width = 96
                self.game.camera.update_size()
            else:
                if self.horizontal:
                    self.orig_image = pygame.transform.rotate(self.game.load_image('door.png'), -90)
                    self.image_y += 64
                    self.height = 32
                else:
                    self.orig_image = self.game.load_image('door.png')
                    self.image_x += 64
                    self.width = 32
                self.game.camera.update_size()
            self.toggle()
        super().interact()
