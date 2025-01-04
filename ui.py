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


class TaskText:
    """Текст для заданий"""
    def __init__(self, game, x, y, title, subtitle, title_color, subtitle_color, fone_color, font, size):
        self.game = game
        self.draw_x = x
        self.draw_y = y

        title_font = pygame.font.SysFont(font, size)
        subtitle_font = pygame.font.SysFont(font, size - 2)

        title_rendered_text = [title_font.render(i, True, title_color) for i in title.split('\n')]
        subtitle_rendered_text = [subtitle_font.render(i, True, subtitle_color) for i in subtitle.split('\n')]
        _, title_h = title_rendered_text[0].get_size()
        _, subtitle_h = subtitle_rendered_text[0].get_size()

        rect_w = max([i.get_size()[0] for i in title_rendered_text + subtitle_rendered_text])
        rect_h = title_h * len(title_rendered_text) + subtitle_h * len(subtitle_rendered_text)

        self.surface = pygame.Surface((rect_w, rect_h), pygame.SRCALPHA)
        self.surface.fill(fone_color)

        for i, text in enumerate(title_rendered_text):
            self.surface.blit(text, (x, y + title_h * i))
        _title_h = title_h * (i + 1)
        for i, text in enumerate(subtitle_rendered_text):
            self.surface.blit(text, (x, y + subtitle_h * i + _title_h))

    def update_scale(scale):
        self.draw_x = self.x * scale
        self.draw_y = self.y * scale

    def draw(self, screen):
        screen.blit(self.surface, (self.draw_x, self.draw_y))
