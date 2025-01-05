import pygame
from build import Wall, Floor, Item, Door
from player import Player
from ui import FollowText, TaskText


class Phase:
    def __init__(self, game):
        self.game = game
        game.resize(1000, 1000)

        game.player = Player(game, (0, 255, 0), 1216, 384, 32, 32)
        # game.player.set_animation(6, 1, 32, 32, 0.5)
        game.camera.change(obj=game.player, size=(1000, 1000))

        self.build()

        self._count = 1
        self._task = 0
        self._flag = False
        self._wait = 0

        self.task_text = TaskText(game, 0, 0, 'Проживайте обычные деньки', 'Умойтесь', (0, 0, 0), (100, 100, 100), (100, 100, 100, 200), 'arial', 20)
        game.ui.append(self.task_text)

    def event_handling(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if self.game.player.interact:
                    self.game.player.interact.interact()
        return True

    def story_event_handling(self, item):
        if self._count < 10:
            if self._task == 0:
                if item == self.furniture['sink']:
                    self.game.player.can_walk = False
                    self._wait = int(180 / self._count)
                    self._flag = True
            elif self._task == 1:
                if item == self.furniture['kitchen']:
                    self.game.player.can_walk = False
                    self._wait = int(300 / self._count)
                    self._flag = True
            elif self._task == 2:
                if item == self.furniture['table']:
                    self._task = 3
                    self.create_task_text('Проживайте обычные деньки', 'Сядьте за стол')
            elif self._task == 3:
                if item == self.furniture['chair']:
                    self._flag = True
                    self._task = 4
                    self._wait = int(300 / self._count)
                    self.game.player.can_walk = False
                    # TODO: игрока делаем невидимым, а у стула меняем текстуру
            elif self._task == 5:
                if item == self.furniture['kitchen']:
                    self._flag = True
                    self._wait = int(180 / self._count)
                    self.game.player.can_walk = False
            elif self._task == 6:
                if item == self.furniture['armchair']:
                    self._flag = True
                    self._wait = int(300 / self._count)
                    self.game.player.can_walk = False
            elif self._task == 7:
                if item == self.furniture['sink']:
                    self._flag = True
                    self._wait = int(180 / self._count)
                    self.game.player.can_walk = False
            elif self._task == 8:
                if item == self.furniture['bed']:
                    self._flag = True
                    self._wait = int(500 / self._count)
                    self.game.player.can_walk = False

    def update(self):
        if self._wait > 0:
            self._wait -= self.game.tick
        else:
            if self._task == 0 and self._flag:
                self.game.player.can_walk = True
                self.create_task_text('Проживайте обычные деньки', 'Приготовте завтрак')
                self._task = 1
                self._flag = False
            elif self._task == 1 and self._flag:
                self.game.player.can_walk = True
                self.create_task_text('Проживайте обычные деньки', 'Поставте тарелку на стол')
                self._task = 2
                self._flag = False
            elif self._task == 4 and self._flag:
                self.game.player.can_walk = True
                self.create_task_text('Проживайте обычные деньки', 'Помойте тарелку')
                self._task = 5
                self._flag = False
            elif self._task == 5 and self._flag:
                self._task = 6
                self.game.player.can_walk = True
                self.create_task_text('Проживайте обычные деньки', 'Сядьте за компьютер')
                self._flag = False
            elif self._task == 6 and self._flag:
                self._task = 7
                self.game.player.can_walk = True
                self.create_task_text('Проживайте обычные деньки', 'Умойтесь')
                self._flag = False
            elif self._task == 7 and self._flag:
                self._task = 8
                self.game.player.can_walk = True
                self._flag = False
                self.create_task_text('Проживайте обычные деньки', 'Ложитесь спать')
            elif self._task == 8 and self._flag:
                self._count += 1
                self._flag = False
                self.create_task_text('Проживайте обычные деньки', 'Умойтесь')
                self._task = 0
                self.game.player.can_walk = True


    def create_task_text(self, title, subtitle, title_color=(0, 0, 0), subtitle_color=(100, 100, 100)):
        self.game.ui.remove(self.task_text)
        self.task_text = TaskText(self.game, 0, 0, title, subtitle, title_color, subtitle_color, (100, 100, 100, 200), 'arial', 20)
        self.game.ui.append(self.task_text)


    def build(self):
        game = self.game
        self.doors = [
                Door(game, (255, 0, 0), 288, 320, 32, 64, True),  # 1
                Door(game, (255, 0, 0), 640, 0, 64, 32, True),  # 2
                Door(game, (255, 0, 0), 960, 384, 32, 64, True)  # 3
                ]

        self.walls = [
                Wall(game, (0, 0, 0), 544, 0, 32, 256, True),  # 1
                Wall(game, (0, 0, 0), 768, 0, 32, 256, True),  # 2
                Wall(game, (0, 0, 0), 32, 224, 512, 32, True),  # 3
                Wall(game, (0, 0, 0), 32, 256, 32, 288, True),  # 4
                Wall(game, (0, 0, 0), 64, 512, 224, 32, True),  # 5
                Wall(game, (0, 0, 0), 288, 256, 32, 64, True),  # 6
                Wall(game, (0, 0, 0), 288, 384, 32, 256, True),  # 7
                Wall(game, (0, 0, 0), 288, 640, 1024, 32, True),  # 8
                Wall(game, (0, 0, 0), 960, 448, 32, 192, True),  # 9
                Wall(game, (0, 0, 0), 960, 256, 32, 128, True),  # 10
                Wall(game, (0, 0, 0), 992, 288, 320, 32, True),  # 11
                Wall(game, (0, 0, 0), 1280, 320, 32, 320, True),  # 12
                Wall(game, (0, 0, 0), 800, 224, 192, 32, True),  # 13
                Wall(game, (0, 0, 0), 544, 0, 96, 32, True),  # 14
                Wall(game, (0, 0, 0), 704, 0, 96, 32, True)  # 15
                ]

        self.furniture = {
                'sofa': Item(game, (0, 0, 255), 416, 416, 128, 64, True),
                'tv': Item(game, (0, 0, 255), 416, 256, 128, 32, True),
                'kitchen': Item(game, (0, 0, 255), 768, 256, 192, 64, True),
                'table': Item(game, (0, 0, 255), 704, 448, 160, 96, True),
                'chair': Item(game, (0, 0, 255), 874, 488, 32, 32, True),
                'bed': Item(game, (0, 0, 255), 1152, 320, 128, 64, True),
                'armchair': Item(game, (0, 0, 255), 1152, 534, 32, 32, True),
                'work_table': Item(game, (0, 0, 255), 1088, 576, 192, 64, True),
                'toilet': Item(game, (0, 0, 255), 96, 256, 32, 32, True),
                'bath': Item(game, (0, 0, 255), 64, 384, 64, 128, True),
                'sink': Item(game, (0, 0, 255), 192, 480, 64, 32, True)
                }
        self.game.camera.update_size()
