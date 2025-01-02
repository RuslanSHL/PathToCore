import pygame
import os


class Game:
    def __init__(self, caption, width, height):
        pygame.init()
        pygame.display.set_caption(caption)
        # Экран
        self.width, self.height = self.size = width, height
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.game_surface = pygame.Surface(self.size)
        # Камера
        self.camera_size_x = width / 2
        self.camera_size_y = height / 2
        if self.camera_size_x < self.camera_size_y:
            self.camera_scale = width / self.camera_size_x
        elif self.camera_size_x > self.camera_size_y:
            self.camera_scale = height / self.camera_size_y
        self.camera_x = 0
        self.camera_y = 0
        # Спрайты
        self.all_sprites = pygame.sprite.Group()
        self.building_group = pygame.sprite.Group()
        self.collibe_building_group = pygame.sprite.Group()
        # Объекты
        self.floor = pygame.sprite.Group()
        self.wall = pygame.sprite.Group()
        self.item = pygame.sprite.Group()
        self.life = pygame.sprite.Group()
        self.ui = []
        # Игровое время
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.tps = 60
        self.ticks = 0


    def run(self):
        """Главный цикл"""
        self.running = True
        _time_fps = 0
        while self.running:
            time = self.clock.tick(max(self.fps, self.tps))
            self.tick = time / 1000 * self.tps
            # обработка событий pygame
            for event in pygame.event.get():
                if self.phase.event_handling(event):
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.VIDEORESIZE:
                        if event.w < event.h:
                            self.camera_scale *= event.w / self.width
                        else:
                            self.camera_scale *= event.h / self.height
                        self.width, self.height = event.w, event.h
                        self.phase.update_size()
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
            self.phase.update()

            _time_fps += time
            if _time_fps > 1000 / self.fps:
                _time_fps %= 1000 / self.fps
                self.screen.fill((255, 255, 255))
                self.game_surface.fill((255, 255, 255))
                self.floor.draw(self.game_surface)
                self.wall.draw(self.game_surface)
                self.item.draw(self.game_surface)
                self.life.draw(self.game_surface)
                if self.camera_scale != 1:
                    game_surface = pygame.transform.scale(
                            self.game_surface,
                            (self.game_surface.get_rect().width * self.camera_scale,
                             self.game_surface.get_rect().height * self.camera_scale))
                    self.screen.blit(game_surface, (self.camera_x, self.camera_y))
                else:
                    self.screen.blit(self.game_surface, (self.camera_x, self.camera_y))
                for i in self.ui:
                    i.draw(self.screen)
                pygame.display.flip()
        self.quit()

    def set_phase(self, phase):
        self.phase = phase

    def load_image(self, name, colorkey=None):
        fullname = os.path.join("data", name)
        if not os.path.isfile(fullname):
            print("Unknown image:", name)
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
        print("bye!")
        pygame.quit()


if __name__ == "__main__":
    core = Game("PathToCore", 1000, 500)
    from Phase1 import Phase

    core.set_phase(Phase(core))
    core.run()
