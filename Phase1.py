import pygame
from Phase2 import Phase2
from build import Wall, Floor, Item, Door
from player import Player
from ui import FollowText, TaskText, Computer_1


class Phase:
    def __init__(self, game):
        self.game = game
        game.resize(1000, 1000)

        game.player = Player(game, 'player.png', 1216, 384, 64, 64)
        # game.player.set_animation(6, 1, 32, 32, 0.5)
        game.camera.change(obj=game.player, size=(400, 400))

        self.build()

        self._count = 1
        self._task = 0
        self._flag = False
        self._wait = 0
        self._c_step = 20

        self.task_text = TaskText(game, 0, 0, 'Проживайте обычные деньки', 'Умойтесь', (0, 0, 0), (100, 100, 100), (100, 100, 100, 200), 'arial', 20)
        game.ui.append(self.task_text)

    def event_handling(self, event):
        if event.type == pygame.KEYDOWN:
            if self._task == 6 and self._flag and self._count < 10:
                self.computer.handler_key(event.key)
                return False
            else:
                if event.key == pygame.K_e:
                    if self.game.player.interact:
                        self.game.player.interact.interact()
        return True

    def story_event_handling(self, item):
        print(item)
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
                    self.computer = Computer_1(self.game, 10, 10, self.game.width - 20, self.game.height - 20, self._c_step, 11 - self._count)
                    self.game.ui.append(self.computer)
                    self.game.camera.update_size()
                    self._c_step += 11 - self._count
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
        else:
            if self._task == 0:
                if item == self.furniture['sink']:
                    self.game.player.can_walk = False
                    self._wait = 180
                    self._flag = True
                elif item == self.furniture['bath']:
                    print('Впринципе можно и тут')
                    self.game.player.can_walk = False
                    self._wait = 180
                    self._flag = True
                else:
                    phrases = {self.furniture['bed']: 'Не хочу спать'}
                    text = phrases.get(item, 'Нужно сначало умыться')
                    print(text)
            elif self._task == 1:
                if item == self.furniture['kitchen']:
                    print('Почему я готовлю постоянно одно и тоже?')
                    self.game.player.can_walk = False
                    self._wait = 300
                    self._flag = True
                else:
                    phrases = {self.furniture['sofa']: 'Сколько себя помню, я никогда на нём не сидел',
                                self.furniture['tv']: 'Когда я последний раз его включал?'}
                    text = phrases.get(item, 'Для начала позавтракаю')
                    print(text)
            elif self._task == 2:
                if item == self.furniture['table']:
                    self._task = 3
                    self.create_task_text('Проживайте обычные деньки', 'Сядьте за стол')
            elif self._task == 3:
                if item == self.furniture['chair']:
                    self._flag = True
                    self._task = 4
                    self._wait = 300
                    self.game.player.can_walk = False
                    # TODO: игрока делаем невидимым, а у стула меняем текстуру
                    print('Почему я только завтракаю?')
                else:
                    print('У меня остывает завтрак')
            elif self._task == 5:
                if item == self.furniture['kitchen']:
                    self._flag = True
                    self._wait = 180 / self._count
                    self.game.player.can_walk = False
            elif self._task == 6:
                if item == self.furniture['armchair']:
                    print('За этим столом я провожу большую часть времени')
                    self._scale_count = 0
                    self._flag = True
                    self._wait = 300
                    self.game.player.can_walk = False
            elif self._task == 10:
                if item == self.doors[1]:
                    self._task = 11

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
                if self._count >= 10:
                    if self._scale_count < 1000:
                        self._scale_count += 1
                        self.game.camera.scale -= 0.0001
                        self.game.camera.update_size()
                    else:
                        self.create_task_text('Покиньте версию', 'Откройте дверь')
                        self.doors[1].closed = False
                        self._flag = False
                        self.game.player.can_walk = True
                        self._task = 10
                else:
                    if not self.computer.steps:
                        self._task = 7
                        self.game.ui.remove(self.computer)
                        self.create_task_text('Проживайте обычные деньки', 'Умойтесь')
                        self._flag = False
                        self.game.player.can_walk = True
            elif self._task == 7 and self._flag:
                self._task = 8
                self.game.player.can_walk = True
                self._flag = False
                self.create_task_text('Проживайте обычные деньки', 'Ложитесь спать')
            elif self._task == 8 and self._flag:
                self._count += 1
                self._flag = False
                if self._count < 10:
                    self.create_task_text('Проживайте обычные деньки', 'Умойтесь')
                else:
                    self.create_task_text('Проживайте обычные деньки?', 'Умойтесь')
                self._task = 0
                self.game.player.can_walk = True
            elif self._task == 11:
                if self.game.player.rect.bottom < 0:
                    self.game.set_phase(Phase2(self.game))

    def create_task_text(self, title, subtitle, title_color=(0, 0, 0), subtitle_color=(100, 100, 100)):
        self.game.ui.remove(self.task_text)
        self.task_text = TaskText(self.game, 0, 0, title, subtitle, title_color, subtitle_color, (100, 100, 100, 200), 'arial', 20)
        self.game.ui.append(self.task_text)

    def build(self):
        game = self.game
        self.doors = [
                Door(game, 'door.png', 288, 320, 32, 64, True),  # 1
                Door(game, 'door.png', 640, 0, 64, 32, True, horizontal=True, closed=True),  # 2
                Door(game, 'door.png', 960, 384, 32, 64, True)  # 3
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
                'sofa': Item(game, 'sofa.png', 416, 416, 128, 64, True),
                'tv': Item(game, 'tv.png', 416, 256, 128, 32, True),
                'kitchen': Item(game, 'kitchen.png', 768, 256, 192, 64, True),
                'table': Item(game, 'table.png', 704, 448, 160, 96, True),
                'chair': Item(game, 'chair.png', 874, 488, 32, 32, True),
                'bed': Item(game, 'bed.png', 1152, 320, 128, 64, True),
                'armchair': Item(game, 'armchair.png', 1152, 534, 32, 32, True),
                'work_table': Item(game, 'work_table.png', 1088, 576, 192, 64, True),
                'toilet': Item(game, 'toilet.png', 96, 256, 32, 32, True),
                'bath': Item(game, 'bath.png', 64, 384, 64, 128, True),
                'sink': Item(game, 'sink.png', 192, 480, 64, 32, True)
                }
        self.game.camera.update_size()
