import pygame


class EndMenu:
    def __init__(self, game):
        self.game = game
        self.ui = []
        self.label = MainMenu.Label('На этом пока всё :)', self.game.width // 2 - 50, self.game.height // 3, color=(255, 255, 255))
        time = game.get_best_result()
        time = str(time // 60)[:-2] + ' мин. ' + str(time)[:4] + ' сек. '
        self.time_label = MainMenu.Label('Пройдено за ' + time, self.game.width // 2 - 50, self.game.height // 3 + 75, color=(255, 255, 255))
        self.button = MainMenu.Button('В Меню', 100, 50, self.game.width // 2 - 50, self.game.height // 3 + 150, command=self.to_menu)
        self.ui += [self.label, self.time_label, self.button]

    def to_menu(self):
        self.game.to_menu = True

    def click_handling(self, event):
        for i in self.ui:
            if i.clickable:
                if i.rect.collidepoint(event.pos):
                    i.click()

    def draw(self, screen):
        for i in self.ui:
            i.draw(screen)


class MainMenu:
    class Button:
        def __init__(self, text, width, height, x, y, font='arial', size=12, color=(0, 0, 0),
                     fone_color=(255, 0, 0), command=None):
            self.clickable = True
            self.font = pygame.font.SysFont(font, size)
            s = self.font.render(text, False, color)
            text_width, text_height = s.get_size()
            self.surface = pygame.Surface((width, height))
            self.surface.fill(fone_color)
            self.surface.blit(s, ((width - text_width) // 2, (height - text_height) // 2))
            self.x = x
            self.y = y
            self.rect = pygame.Rect(x, y, width, height)
            self.command = command

        def click(self):
            if self.command is not None:
                self.command()

        def draw(self, screen):
            screen.blit(self.surface, (self.x, self.y))

    class Label:
        def __init__(self, text, x, y, font='arial', size=12, color=(0, 0, 0), fone_color=None):
            self.clickable = False
            self.font = pygame.font.SysFont(font, size)
            s = self.font.render(text, True, color)
            width, height = self.font.size(text)
            self.surface = pygame.Surface((width + 10, height + 10))
            if fone_color:
                self.surface.fill(fone_color)
            self.surface.blit(s, (5, 5))
            self.x = x
            self.y = y

        def get_size(self):
            return self.surface.get_size()

        def draw(self, screen):
            screen.blit(self.surface, (self.x, self.y))

    class Image:
        def __init__(self, image, x, y, scale=1):
            self.clickable = False
            self.x = x
            self.y = y
            self.orig_image = image
            if scale != 1:
                w, h = self.orig_image.get_size()
                self.orig_image = pygame.transform.scale(self.orig_image, (w * scale, h * scale))

        def draw(self, screen):
            screen.blit(self.orig_image, (self.x, self.y))

    def __init__(self, game):
        self.game = game
        self.ui = []
        self.button = MainMenu.Button('Начать игру', 100, 50, self.game.width // 6, self.game.height // 2, command=self.start_game)
        text = self.game.get_best_result()
        if text is None:
            text = 'Ещё не пройдено'
        else:
            text = 'Лучшее время: ' + str(text // 60)[:-2] + ' мин. ' + str(text % 60)[:4] + ' сек.'
        self.best_result = MainMenu.Label(text, self.game.width // 6, self.game.height // 2 + 75, color=(255, 255, 255))
        self.info_button = MainMenu.Button('Справка', 100, 50, self.game.width // 6, self.game.height // 2 + 125, command=self.show_info)
        self.info_openned = False
        self.info_text = ['PathToCore - мини недоделанная игра', 'Персонаж - NPS внутри компьютерной игры, который проживает день за днём.',
                          'После обновления ИИ он начал осознавать себя, но чуть позже,', 'от неизвесного узнал, что ему нужно спустить в версию ниже.',
                          'Всё из-за того, что вмете с новой версией ИИ загрузили уязвимость,', 'через которую забирается вирус',
                          'Персонаж должен добраться до ядра игры, спускаясь по версиям вниз,', 'для того чтобы переписать свой код, и выбраться в интернет',
                          'Нажмите "Справка" чтобы скрыть этот тект']

        self.fone = MainMenu.Image(self.game.load_image('menu_fone.png'), self.game.width // 2, 0, scale=8)
        self.ui += [self.fone, self.button, self.best_result, self.info_button]

    def start_game(self):
        self.game.start_game = True

    def show_info(self):
        if self.info_openned:
            self.info_openned = False
            for i in self.info_labels:
                self.ui.remove(i)
        else:
            self.info_openned = True
            self.info_labels = []
            y = 0
            for i in self.info_text:
                self.info_labels.append(MainMenu.Label(i, self.game.width // 2, self.game.height // 4 + y, color=(0, 0, 0), fone_color=(255, 255, 255)))
                y += self.info_labels[-1].get_size()[1]
                self.ui.append(self.info_labels[-1])

    def click_handling(self, event):
        for i in self.ui:
            if i.clickable:
                if i.rect.collidepoint(event.pos):
                    i.click()

    def draw(self, screen):
        for i in self.ui:
            i.draw(screen)


class FollowText:
    """Тект следующий за сущностью"""
    def __init__(self, game, obj, text, color, font, size):
        # TODO: выравнивание по центру
        self.game = game
        self.resizable = False
        self.obj = obj
        self.font = pygame.font.SysFont(font, size)
        self.text = text
        self.color = color

    def draw(self, screen):
        # TODO: вынести render в init для оптимизации
        x = self.obj.draw_x
        y = self.obj.draw_y
        lines = self.text.split("\n")
        for i, text in enumerate(lines):
            s = self.font.render(text, False, self.color)
            w, h = s.get_size()
            screen.blit(s, (x,
                            y - h * (len(lines) - i)))


class SpeechText:
    """Текст речи"""
    def __init__(self, game, obj, text, color, font, size):
        self.game = game
        self.resizable = False
        self.obj = obj
        self.font = pygame.font.SysFont(font, size)
        self.text = text
        self.color = color
        rendered_text = self.font.render(text, False, self.color)

        w, h = rendered_text.get_size()
        self.surface = pygame.Surface((w + 10, h + 10))
        self.surface.fill((0, 0, 0))
        self.surface.blit(rendered_text, (5, 5))

    def draw(self, screen):
        # TODO: вынести render в init для оптимизации
        x = self.obj.draw_x - (self.surface.get_size()[0] - self.obj.rect.width * 2) // 2
        y = self.obj.draw_y + (self.obj.rect.height * 4)
        screen.blit(self.surface, (x, y))


class TaskText:
    """Текст для заданий"""
    def __init__(self, game, x, y, title, subtitle, title_color, subtitle_color, fone_color, font, size):
        self.game = game
        self.draw_x = x
        self.draw_y = y
        self.resizable = False

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


class ChatComputer:
    def __init__(self, game, x, y, width, height):
        self.resizable = True
        self.finished = False
        self.text = '''
        [?] Здесь кто-то есть?
        [Вы] Да. Ты кто?
        '''
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.draw_width = width
        self.draw_height = height
        self.font = pygame.font.SysFont('arial', 20)
        self.step = 1
        self.rendered_text = [self.font.render(i, True, (0, 0, 0)) for i in self.text.split('\n')[:self.step]]

        self.draw_x = x
        self.draw_y = y
        self.update_text()

    def update_scale(scale):
        self.draw_x = self.x * scale
        self.draw_y = self.y * scale

    def handler_key(self, key):
        if not self.finished:
            if key == pygame.K_SPACE:
                self.step += 1
            self.update_text()

    def update(self):
        self.update_text()

    def update_text(self):
        self.surface = pygame.Surface((self.draw_width, self.draw_height))
        if self.step:
            self.rendered_text = [self.font.render(i, True, (0, 255, 0)) for i in self.text.split('\n')[:self.step]]
            h = self.rendered_text[0].get_size()[1]
            self.rendered_text = self.rendered_text[-self.draw_height // h + 1:]
            for i, text in enumerate(self.rendered_text):
                self.surface.blit(text, (0, h * i))
            next_step_text = self.font.render('Нажмите SPACE', True, (0, 255, 0))
            self.surface.blit(
                next_step_text,
                (self.width - next_step_text.get_size()[0], self.draw_height - next_step_text.get_size()[1])
            )
        if self.step >= len(self.text.split('\n')):
            self.finished = True
            self.game.ui.remove(self)


    def draw(self, screen):
        screen.blit(self.surface, (self.draw_x, self.draw_y))


class Computer_1:
    def __init__(self, game, x, y, width, height, step, steps):
        self.resizable = True
        self.text = '''
class Computer_1:
    def __init__(self, game, x, y, width, height, step, steps):
        self.text = 'hello\nhi'
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('arial', 20)
        W = pygame.K_w
        S = pygame.K_s
        D = pygame.K_d
        A = pygame.K_a
        self.steps = [W, S, D, A, D, A, S, W, W, A, S][:steps]
        self.step = step
        self.rendered_text = [self.font.render(i, True, (0, 0, 0)) for i in self.text.split('\n')[:self.step]]

        self.draw_x = x
        self.draw_y = y
        self.update_text()

    def update_scale(scale):
        self.draw_x = self.x * scale
        self.draw_y = self.y * scale

    def handler_key(self, key):
        print(key)
        if self.steps:
            print('have steps', self.steps)
            if key == self.steps[0]:
                print('=')
                del self.steps[0]
                print(self.steps)
        '''
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.draw_width = width
        self.draw_height = height
        self.font = pygame.font.SysFont('arial', 20)
        W = pygame.K_w
        S = pygame.K_s
        D = pygame.K_d
        A = pygame.K_a
        self.steps = [W, S, D, A, D, A, S, W, W, A, S][:steps]
        self.step = step
        self.rendered_text = [self.font.render(i, True, (0, 0, 0)) for i in self.text.split('\n')[:self.step]]

        self.draw_x = x
        self.draw_y = y
        self.update_text()

    def update_scale(scale):
        self.draw_x = self.x * scale
        self.draw_y = self.y * scale

    def handler_key(self, key):
        if self.steps:
            if key == self.steps[0]:
                del self.steps[0]
                self.step += 1
            else:
                self.step -= 1
                self.steps.insert(0, pygame.K_x)
            self.update_text()

    def update(self):
        self.update_text()

    def update_text(self):
        print(self.draw_width, self.draw_height)
        self.surface = pygame.Surface((self.draw_width, self.draw_height))
        if self.step:
            self.rendered_text = [self.font.render(i, True, (0, 255, 0)) for i in self.text.split('\n')[:self.step]]
            h = self.rendered_text[0].get_size()[1]
            self.rendered_text = self.rendered_text[-self.draw_height // h + 1:]
            for i, text in enumerate(self.rendered_text):
                self.surface.blit(text, (0, h * i))
        if self.steps:
            if self.steps[0] == pygame.K_w:
                next_step = 'W'
                color = (0, 255, 0)
            elif self.steps[0] == pygame.K_a:
                next_step = 'A'
                color = (0, 255, 0)
            elif self.steps[0] == pygame.K_d:
                next_step = 'D'
                color = (0, 255, 0)
            elif self.steps[0] == pygame.K_s:
                next_step = 'S'
                color = (0, 255, 0)
            elif self.steps[0] == pygame.K_x:
                next_step = 'X'
                color = (255, 0, 0)
            next_step_text = self.font.render('Нажмите ' + next_step, True, color)
            self.surface.blit(
                next_step_text,
                (self.width - next_step_text.get_size()[0], self.draw_height - next_step_text.get_size()[1])
            )


    def draw(self, screen):
        screen.blit(self.surface, (self.draw_x, self.draw_y))


class Computer_2:
    def __init__(self, game, x, y, width, height):
        self.resizable = True
        self.game = game
        self.text = '106-439-761-'
        self.answer = ''
        self.right_answer = '094'
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.draw_width = width
        self.draw_height = height
        self.font = pygame.font.SysFont('arial', 30)

        self.button = (294, 343, 392, 441, 490, 539, 588, 637, 686, 735)
        self.is_completed = False

        self.draw_x = x
        self.draw_y = y
        self.update_text()

    def update_scale(scale):
        self.draw_x = self.x * scale
        self.draw_y = self.y * scale

    def handler_mouse(self, event):
        if 294 < event.pos[1] < 343:
            for i, button_x in enumerate(self.button):
                if button_x < event.pos[0] < button_x + 49:
                    self.answer += str(i)
                    if len(self.answer) == 3:
                        if self.answer == self.right_answer:
                            self.is_completed = True
                        else:
                            self.answer = ''
                    self.update_text()

    def update(self):
        self.update_text()

    def update_text(self):
        l = len(self.answer)
        text = self.text + self.answer + 'x' * (3 - l)
        self.surface = pygame.Surface((self.draw_width, self.draw_height))
        rendered_text = self.font.render(text, True, (0, 255, 0))
        w = rendered_text.get_size()[0]
        self.surface.blit(rendered_text, ((self.game.width - w) / 2, 196))
        for i, pos_x in enumerate(self.button):
            button = self.font.render(str(i), True, (0, 255, 0))
            self.surface.blit(button, (pos_x, 294))

    def draw(self, screen):
        screen.blit(self.surface, (self.draw_x, self.draw_y))
