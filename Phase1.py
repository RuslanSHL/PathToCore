import pygame
from build import Wall, Floor, Item
from player import Player


class Phase:
    def __init__(self, game):
        self.game = game
        game.resize(1000, 1000)

        game.player = Player(game, 'player.png', 0, 0, 64, 64)
        game.player.set_animation(6, 1, 32, 32, 0.5)

        self.wall = Wall(game, 'wall.png', 150, 150, 30, 30, True)


        game.camera.change(obj=game.player, size=(200, 200))



    def event_handling(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if self.game.player.interact:
                    self.game.player.interact.interact()
        return True

    def update(self):
        pass
