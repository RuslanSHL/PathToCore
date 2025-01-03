import pygame
from build import Wall, Floor, Item, Door
from player import Player
from ui import FollowText


class Phase:
    def __init__(self, game):
        self.game = game
        game.resize(1000, 1000)

        game.player = Player(game, (0, 255, 0), 640, 320, 32, 32)
        # game.player.set_animation(6, 1, 32, 32, 0.5)

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
                Wall(game, (0, 0, 0), 704, 0, 96, 32, True),  # 15
                ]

        self.furniture = {
                'sofa': Item(game, (0, 0, 255), 416, 416, 128, 64, True),
                'tv': Item(game, (0, 0, 255), 416, 256, 128, 32, True),
                'kitchen': Item(game, (0, 0, 255), 768, 256, 192, 64, True),
                'table': Item(game, (0, 0, 255), 704, 448, 160, 96, True),
                'char': Item(game, (0, 0, 255), 874, 488, 32, 32, True),
                'bed': Item(game, (0, 0, 255), 1152, 320, 128, 64, True),
                'armchait': Item(game, (0, 0, 255), 1152, 534, 32, 32, True),
                'work_table': Item(game, (0, 0, 255), 1088, 576, 192, 64, True),
                'toilet': Item(game, (0, 0, 255), 96, 256, 32, 32, True),
                'bath': Item(game, (0, 0, 255), 64, 384, 64, 128, True),
                'sink': Item(game, (0, 0, 255), 192, 480, 64, 32, True)
                }

        game.camera.change(obj=game.player, size=(1000, 1000))

    def event_handling(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if self.game.player.interact:
                    self.game.player.interact.interact()
        return True

    def update(self):
        pass
