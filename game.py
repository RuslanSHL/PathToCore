import pygame
import os
from time import time as now_time


class Game:
    def __init__(self, caption, width, height):
        pygame.init()
        pygame.display.set_caption(caption)
        # Экран
        self.width, self.height = self.size = 1000, 500
        self.game_width, self.game_height = width, height
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.game_surface = pygame.Surface((width, height))
        # Камера
        self.camera = Camera(self, coords=(0, 0))
        self.camera_update_size = False
        # Спрайты
        self.collibe_group = pygame.sprite.Group()
        # Объекты
        self.fone = pygame.sprite.Group()
        self.floor = pygame.sprite.Group()
        self.wall = pygame.sprite.Group()
        self.item = pygame.sprite.Group()
        self.life = pygame.sprite.Group()
        self.ui = []
        # Игровое время
        self.clock = pygame.time.Clock()
        self.fps = 1000
        self.tps = 60
        self.ticks = 0
        self.start_time = None

    def resize(self, width, height):
        self.game_width, self.game_height = width, height
        self.game_surface = pygame.Surface((width, height))

    def end_menu(self, menu):
        running = True
        self.to_menu = False
        menu = menu(self)
        while running:
            if self.to_menu:
                running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    menu.click_handling(event)
            self.screen.fill((0, 0, 0))
            menu.draw(self.screen)
            pygame.display.flip()
        self.restart()

    def main_menu(self, menu):
        running = True
        self.start_game = False
        menu = menu(self)
        while running:
            if self.start_game:
                running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    menu.click_handling(event)
            self.screen.fill((0, 0, 0))
            menu.draw(self.screen)
            pygame.display.flip()


    def run(self):
        """Главный цикл"""
        self.start_time = now_time()
        self.running = True
        _time_fps = 0
        while self.running:
            # TODO: оптимизация
            time = self.clock.tick(max(self.fps, self.tps))
            self.tick = time / 1000 * self.tps
            # обработка событий pygame
            for event in pygame.event.get():
                if self.phase.event_handling(event):
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.VIDEORESIZE:
                        scale = event.h / self.height
                        self.camera.scale *= event.w / self.width
                        self.width = event.w
                        self.height = event.h
                        self.size = self.width, self.height
                        self.camera.update_size()
                        # FIXME: изменение размера ui
                        for i in self.ui:
                            if i.resizable:
                                i.draw_x = i.x * scale
                                i.draw_y = i.y * scale
                                i.draw_width = int(i.draw_width * scale)
                                i.draw_height = int(i.draw_height * scale)
                                i.update()
                        self.game_surface = pygame.Surface((self.width, self.height))
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
                            self.player.direction_x = 0
                        elif event.key in (pygame.K_RIGHT, pygame.K_d):
                            self.player.direction_x = 0
                        elif event.key in (pygame.K_UP, pygame.K_w):
                            self.player.direction_y = 0
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            self.player.direction_y = 0

            self.fone.update()
            self.floor.update()
            self.wall.update()
            self.item.update()
            self.life.update()
            self.phase.update()
            # print(self.clock.get_fps())

            _time_fps += time
            if _time_fps > 1000 / self.fps:
                _time_fps %= 1000 / self.fps
                self.screen.fill((0, 0, 0))
                self.game_surface.fill((0, 0, 0))
                self.camera.update()
                for i in self.fone:
                    i.draw(self.game_surface)
                for i in self.floor:
                    i.draw(self.game_surface)
                for i in self.wall:
                    i.draw(self.game_surface)
                for i in self.item:
                    i.draw(self.game_surface)
                for i in self.life:
                    i.draw(self.game_surface)
                self.screen.blit(self.game_surface, (0, 0))
                for i in self.ui:
                    i.draw(self.screen)
                pygame.display.flip()
        self.quit()

    def set_phase(self, phase):
        self.fone = pygame.sprite.Group()
        self.floor = pygame.sprite.Group()
        self.wall = pygame.sprite.Group()
        self.item = pygame.sprite.Group()
        self.life = pygame.sprite.Group()
        self.collibe_group = pygame.sprite.Group()
        self.ui = []
        self.phase = phase(self)

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

    def load_best_result(self, time: float):
        try:
            with open('result.txt', 'r') as file:
                result = file.read()
                print('result:', result)
                if result:
                    last_result = float(result)
                    if last_result > time:
                        with open('result.txt', 'w') as file:
                            file.write(str(time))
                        print(time)
                        print('best_time')
                else:
                    with open('result.txt', 'w') as file:
                        file.write(str(time))
                    print(time)
                    print('no have last result')
        except Exception as e:
            from icecream import ic
            ic(e)
            return None

    def get_best_result(self):
        try:
            with open('result.txt') as file:
                return float(file.read())
        except Exception as e:
            return None

    def restart(self):
        from Phase1 import Phase
        from ui import MainMenu
        self.set_phase(Phase)
        self.main_menu(MainMenu)
        if self.start_game:
            self.run()

    def end_game(self):
        from ui import EndMenu
        self.load_best_result(now_time() - self.start_time)
        self.end_menu(EndMenu)

    def quit(self):
        """Выход"""
        print("bye!")
        pygame.quit()


class Camera:
    def __init__(self, game, obj=None, coords=None, delta_coords=None,
                 size=None):
        self.game = game
        self.obj = obj
        self.delta_coords = delta_coords
        self.coords = coords
        self.scale = 1
        if size:
            width, height = size
            if width > height:
                self.scale = game.width / width
            else:
                self.scale = game.height / height
            self.update_size()
        else:
            self.scale = 1

    def change(self, obj=None, coords=None, delta_coords=None, size=None):
        self.obj = obj
        self.delta_coords = delta_coords
        self.coords = coords
        if size:
            width, height = size
            if width > height:
                self.scale = self.game.width / width
            else:
                self.scale = self.game.height / height
            self.update_size()

    def transform(self, obj):
        if obj.animated:
            frames = []
            for frame in obj.orig_image:
                frames.append(
                    pygame.transform.scale(
                        frame,
                        (int(obj.image_width * self.scale), int(obj.image_height * self.scale))
                    )
                )
            obj.frames = frames
            obj.image = pygame.transform.scale(
                obj.image,
                (int(obj.image_width * self.scale) + 1, int(obj.image_height * self.scale) + 1)
            )
        else:
            obj.image = pygame.transform.scale(
                obj.orig_image,
                (int(obj.image_width * self.scale) + 1, int(obj.image_height * self.scale) + 1)
            )

    def update_size(self):
        if self.scale != 1:
            for i in self.game.floor:
                self.transform(i)
            for i in self.game.wall:
                self.transform(i)
            for i in self.game.item:
                self.transform(i)
            for i in self.game.life:
                self.transform(i)

    def update(self):
        # TODO: оптимизация, округлять scale
        if self.delta_coords is not None:
            d_x, d_y = self.delta_coords
        else:
            d_x = 0
            d_y = 0
        c_x = self.game.width / 2
        c_y = self.game.height / 2
        if self.obj is None:
            d_x += c_x - self.coords[0]
            d_y += c_y - self.coords[1]
        else:
            d_x += c_x - self.obj.rect.centerx
            d_y += c_y - self.obj.rect.centery

        for i in self.game.fone:
            i.draw_x = int(c_x - (c_x - i.rect.x - d_x * i.k) * self.scale) - 1
            i.draw_y = int(c_y - (c_y - i.rect.y - d_y * i.k) * self.scale) - 1
        for i in self.game.floor:
            i.draw_x = int(c_x - (c_x - i.rect.x + i.d_x_image - d_x) * self.scale) - 1
            i.draw_y = int(c_y - (c_y - i.rect.y + i.d_y_image - d_y) * self.scale) - 1
        for i in self.game.wall:
            i.draw_x = int(c_x - (c_x - i.rect.x + i.d_x_image - d_x) * self.scale) - 1
            i.draw_y = int(c_y - (c_y - i.rect.y + i.d_y_image - d_y) * self.scale) - 1
        for i in self.game.item:
            i.draw_x = int(c_x - (c_x - i.rect.x + i.d_x_image - d_x) * self.scale) - 1
            i.draw_y = int(c_y - (c_y - i.rect.y + i.d_y_image - d_y) * self.scale) - 1
        for i in self.game.life:
            i.draw_x = int(c_x - (c_x - i.rect.x + i.d_x_image - d_x) * self.scale) - 1
            i.draw_y = int(c_y - (c_y - i.rect.y + i.d_y_image - d_y) * self.scale) - 1


if __name__ == "__main__":
    core = Game("PathToCore", 1000, 500)
    from Phase1 import Phase
    from Phase2 import Phase2
    from ui import MainMenu

    core.set_phase(Phase)
    core.main_menu(MainMenu)
    if core.start_game:
        core.run()
