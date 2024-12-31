import pygame
from build import Wall, Floor, Item
from player import Player


class Phase:
    def __init__(self, game):
        self.game = game
        print('start phase 1')

        game.player = Player(game, 'player.png', 0, 0, 50, 50)
        game.player.set_animation(6, 1, 32, 32, 0.5)

        wall = Wall(game, 'wall.png', 100, 100, 50, 50, True)
        floor = Floor(game, (255, 0, 0), 100, 200, 25, 50, False)
        item = Item(game, (255, 0, 0), 200, 200, 25, 50, True)

    def event_handling(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if self.game.player.interact:
                    self.game.player.interact.interact()
        return True
