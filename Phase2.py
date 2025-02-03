import pygame
from build import Wall, Floor, Item, Door, Fone
from player import Player
from ui import FollowText, TaskText, Computer_2
from time import time


class Phase2:
    def __init__(self, game):
        self.game = game
        game.resize(1000, 1000)

        game.player = Player(game, 'player.png', 1216, 384, 32, 32, d_y=32, d_x = 16, scale=2)
        game.player.set_animation('walk_animation.png', 4, 1, 32, 32, 0.08)
        game.camera.change(obj=game.player, size=(1000, 1000))

        game.player.rect.x = 336
        game.player.rect.y = 704

        self.build()

        self._count = 1
        self._task = 1
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
            self.items['level_1'].change_texture('switch_on.png')
            self.game.camera.update_size()
        if item == self.items['level_2']:
            self._flag2 = True
            self.items['level_2'].change_texture('switch_on.png')
            self.game.camera.update_size()
        elif item == self.items['computer']:
            if self._flag1 and self._flag2:
                self.computer = Computer_2(self.game, 10, 10, self.game.width - 20, self.game.height - 20)
                self.game.ui.append(self.computer)
                self._flag3 = True
                self._flag1 = False

    def update(self):
        if self.game.player.rect.y <= -32 and 320 < self.game.player.rect.x < 384:
            self.game.end_game()

        if not self.game.player.on_floor():
            self.game.set_phase(Phase2)
        if self._flag:
            if self._wait > 0:
                self._wait -= 1
            else:
                self.bridge.delete()
                self._flag = False
        elif self._flag3:
            if self.computer.is_completed:
                self.game.ui.remove(self.computer)
                self.bridge = Floor(self.game, 'floor3.png', 320, 128, 64, 384, False)
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
                Floor(game, 'floor2.png', 64, 0, 576, 64, False),
                Floor(game, 'floor1.png', 128, 576, 448, 192, False),
                Floor(game, 'floor2.1.png', 320, 64, 64, 64, False),
                Floor(game, 'floor1.1.png', 320, 512, 64, 64, False),
                ]

        self.items = {
                'level_1': Item(game, 'switch_off.png', 128, 576, 64, 64, True),
                'level_2': Item(game, 'switch_off.png', 512, 576, 64, 64, True),
                'computer': Item(game, 'computer.png', 256, 576, 64, 64, True),
                'door': Door(game, 'door.png' , 320, -32, 64, 32, True, horizontal=True)
                }

        self.fone2 = Fone(game, -1000, -1000, 'fone2.png', k=0.2, scale=10)
        self.fone1 = Fone(game, -1000, -1000, 'fone1.png', k=0.5, scale=10)
        self.game.camera.update_size()
