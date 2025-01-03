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
                Door(game, (255, 0, 0), 288, 320, 32, 64, True),
                Door(game, (255, 0, 0), 640, 0, 64, 32, True),
                Door(game, (255, 0, 0), 960, 384, 32, 64, True)
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

        game.camera.change(obj=game.player, size=(1000, 1000))



    def event_handling(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if self.game.player.interact:
                    self.game.player.interact.interact()
        return True

    def update(self):
        pass
