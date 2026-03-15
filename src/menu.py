import pygame
from button import Button

class Menu:
    def __init__(self, screen, title, background_image=None):
        self.screen = screen
        self.title = title
        self.width, self.height = screen.get_size()

        self.title_font  = pygame.font.SysFont("impact", 80)
        self.button_font = pygame.font.SysFont("arial", 36, bold=True)

        if background_image:
            self.background = pygame.transform.scale(
                pygame.image.load(background_image).convert(),
                (self.width, self.height)
            )
        else:
            self.background = None

        cx = self.width // 2 - 150
        self.btn_play = Button(cx, 500, 300, 65, "Play")
        self.btn_quit = Button(cx, 600, 300, 65, "Quit")

    def run(self):
        clock = pygame.time.Clock()

        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if self.btn_play.is_clicked(event):
                    return "play"
                if self.btn_quit.is_clicked(event):
                    return "quit"

            self.btn_play.update(mouse_pos)
            self.btn_quit.update(mouse_pos)
            self._draw()
            pygame.display.flip()
            clock.tick(60)

    def _draw(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((20, 20, 40))

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))

        cx = self.width // 2
        shadow = self.title_font.render(self.title, True, (0, 0, 0))
        title  = self.title_font.render(self.title, True, (255, 210, 60))
        self.screen.blit(shadow, shadow.get_rect(center=(cx + 3, 253)))
        self.screen.blit(title,  title.get_rect(center=(cx, 250)))

        pygame.draw.line(self.screen, (255, 210, 60),
                         (cx - 200, 320), (cx + 200, 320), 2)

        self.btn_play.draw(self.screen, self.button_font)
        self.btn_quit.draw(self.screen, self.button_font)