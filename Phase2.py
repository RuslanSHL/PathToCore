import pygame
from build import Wall, Floor, Item, Door
from player import Player
from ui import FollowText, TaskText, Computer_2


class Phase2:
    def __init__(self, game):
        self.game = game
        game.resize(1000, 1000)

        game.player = Player(game, (0, 255, 0), 1216, 384, 32, 32)
        # game.player.set_animation(6, 1, 32, 32, 0.5)
        game.camera.change(obj=game.player, size=(1000, 1000))

        game.player.rect.x = 336
        game.player.rect.y = 704
        game.floor = pygame.sprite.Group()
        game.wall = pygame.sprite.Group()
        game.item = pygame.sprite.Group()
        game.collibe_group = pygame.sprite.Group()
        game.ui = []

        self.build()

        self._count = 10
        self._task = 5
        self._flag = False
        self._flag1 = False
        self._flag2 = False
        self._flag3 = False
        self._wait = 0

        self.task_text = TaskText(game, 0, 0, 'Попадите в предыдущую версию', '', (0, 0, 0), (100, 100, 100), (100, 100, 100, 200), 'arial', 20)
        game.ui.append(self.task_text)

    def event_handling(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if self.game.player.interact:
                    self.game.player.interact.interact()
        elif event.type == pygame.MOUSEBUTTONUP:
            if self._flag3:
                self.computer.handler_mouse(event)
                return False
        return True

    def story_event_handling(self, item):
        if item == self.items['level_1']:
            self._flag1 = True
        if item == self.items['level_2']:
            self._flag2 = True
        elif item == self.items['computer']:
            if self._flag1 and self._flag2:
                self.computer = Computer_2(self.game, 10, 10, self.game.width - 20, self.game.height - 20)
                self.game.ui.append(self.computer)
                self._flag3 = True

    def update(self):
        if self._flag:
            if self._wait > 0:
                self._wait -= 1
            else:
                self.bridge.delete()
                self._flag = False
        elif self._flag3:
            if self.computer.is_completed:
                self.game.ui.remove(self.computer)
                self.bridge = Floor(self.game, (10, 10, 10), 320, 128, 64, 384, False)
                self.game.camera.update_size()
                self._flag = True
                self._wait = 3000
                self._flag3 = False

    def create_task_text(self, title, subtitle, title_color=(0, 0, 0), subtitle_color=(100, 100, 100)):
        self.game.ui.remove(self.task_text)
        self.task_text = TaskText(self.game, 0, 0, title, subtitle, title_color, subtitle_color, (100, 100, 100, 200), 'arial', 20)
        self.game.ui.append(self.task_text)

    def build(self):
        game = self.game
        self.floor = [
                Floor(game, (0, 0, 0), 64, 0, 576, 64, False),
                Floor(game, (0, 0, 0), 128, 576, 448, 192, False),
                Floor(game, (0, 0, 0), 320, 64, 64, 64, False),
                Floor(game, (0, 0, 0), 320, 512, 64, 64, False),
                ]

        self.items = {
                'level_1': Item(game, (0, 0, 255), 128, 640, 64, 64, True),
                'level_2': Item(game, (0, 0, 255), 512, 640, 64, 64, True),
                'computer': Item(game, (0, 0, 255), 256, 576, 64, 64, True),
                'door': Door(game, (255, 0, 0), 320, -32, 64, 32, True)
                }
        self.game.camera.update_size()
