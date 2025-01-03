import pygame


class FollowText:
    """Тект следующий за сущностью"""
    def __init__(self, game, obj, text, color, font, size):
        # TODO: выравнивание по центру
        self.game = game
        self.obj = obj
        self.font = pygame.font.SysFont(font, size)
        self.text = text
        self.color = color

    def draw(self, screen):
        x = self.obj.draw_x
        y = self.obj.draw_y
        lines = self.text.split("\n")
        for i, text in enumerate(lines):
            s = self.font.render(text, False, self.color)
            w, h = s.get_size()
            screen.blit(s, (x,
                            y - h * (len(lines) - i)))
