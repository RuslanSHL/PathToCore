import pygame


class InteractText:
    def __init__(self, game, x, y, text, color, font, size):
        # TODO обновление кооринат при ходбе
        self.game = game
        self.font = pygame.font.SysFont(font, size)
        self.text = text
        self.x = x
        self.y = y
        self.color = color

    def draw(self, screen):
        lines = self.text.split("\n")
        for i, text in enumerate(lines):
            s = self.font.render(text, False, self.color)
            w, h = s.get_size()
            screen.blit(s, (self.x,
                            self.y - h * (len(lines) - i)))

