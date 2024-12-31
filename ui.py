import pygame


class InteractText:
    def __init__(self, x, y, text, color, font, size, obj):
        self.font = pygame.font.SysFont(font, size)
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.obj = obj

    def draw(self, screen):
        self.x, self.y = self.obj.rect.x, self.obj.rect.y
        for i, text in enumerate(self.text.split('\n')):
            s = self.font.render(text, False, self.color)
            w, h = s.get_size()
            screen.blit(s, (self.x - (w - self.obj.rect.width) / 2, self.y + h * i - h))

