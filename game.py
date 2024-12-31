import pygame
import os
from build import Build
from player import Player


class Game:
    def __init__(self, caption, width, height):
        self.width, self.height = self.size = width, height
        pygame.init()
        pygame.display.set_caption(caption)
        # Экран
        self.screen = pygame.display.set_mode(self.size)
        # Спрайты
        self.all_sprites = pygame.sprite.Group()
        self.building_group = pygame.sprite.Group()
        self.collibe_building_group = pygame.sprite.Group()

        self.life = pygame.sprite.Group()
        self.wall = pygame.sprite.Group()
        self.floor = pygame.sprite.Group()
        self.item = pygame.sprite.Group()
        self.ui = []
        # Игровое время
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.tps = 60  # Тики не могут быть медленее fps
        self.ticks = 0

        self.time_events = {}

        self.building = []

    def run(self):
        """Главный цикл"""
        self.running = True
        time_fps = 0
        while self.running:
            time = self.clock.tick(self.tps)
            self.ticks += 1
            # обработка time events
            for t, c in self.time_events.copy().items():
                if t == self.ticks:
                    c()
                    del self.time_events[t]
            # обработка событий pygame
            for event in pygame.event.get():
                if self.phase.event_handling(event):
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key in (pygame.K_LEFT, pygame.K_a):
                            self.player.direction_x += -1
                        elif event.key in (pygame.K_RIGHT, pygame.K_d):
                            self.player.direction_x += 1
                        elif event.key in (pygame.K_UP, pygame.K_w):
                            self.player.direction_y += -1
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            self.player.direction_y += 1
                    elif event.type == pygame.KEYUP:
                        if event.key in (pygame.K_LEFT, pygame.K_a):
                            self.player.direction_x -= -1
                        elif event.key in (pygame.K_RIGHT, pygame.K_d):
                            self.player.direction_x -= 1
                        elif event.key in (pygame.K_UP, pygame.K_w):
                            self.player.direction_y -= -1
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            self.player.direction_y -= 1
            self.all_sprites.update()

            time_fps += time
            if time_fps > 1000 / self.fps:
                time_fps %= 1000 / self.fps
                self.screen.fill((255, 255, 255))
                self.floor.draw(self.screen)
                self.wall.draw(self.screen)
                self.item.draw(self.screen)
                self.life.draw(self.screen)
                for i in self.ui:
                    i.draw(self.screen)
                pygame.display.flip()
        self.quit()

    def wait(self, ticks, command):
        self.time_events[self.ticks + ticks] = command

    def set_phase(self, phase):
        self.phase = phase

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print('Unknown image:', name)
            self.quit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def quit(self):
        """Выход"""
        print('bye!')
        pygame.quit()



if __name__ == '__main__':
    core = Game('PathToCore', 500, 500)
    from Phase1 import Phase
    core.set_phase(Phase(core))
    core.run()
