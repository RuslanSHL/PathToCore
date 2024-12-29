import pygame
from build import Wall, Floor, Item


class Phase:
    def __init__(self, game):
        self.game = game
        print('start phase 1')
        game.building.append(Wall(game, (255, 0, 0), 100, 100, 50, 50, True))
        game.building.append(Floor(game, (255, 0, 0), 200, 200, 25, 50, False))
        game.building.append(Item(game, (255, 0, 0), 200, 200, 25, 50, True))

    def event_handling(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if self.game.player.interact:
                    self.game.player.interact.interact()
        return True
