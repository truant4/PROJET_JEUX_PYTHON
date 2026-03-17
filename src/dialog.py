import pygame

class DialogBox:
    BOX_WIDTH = 700
    BOX_HEIGHT = 100
    PORTRAIT_SIZE = 64  # scaled up from 8x8

    def __init__(self, screen_width=1980, screen_height=1080):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.box = pygame.image.load('dialogs/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (self.BOX_WIDTH, self.BOX_HEIGHT))

        self.npc_sheet = pygame.image.load('assets/sprites/NPCS_Faces.png')

        self.x = (screen_width - self.BOX_WIDTH) // 2
        self.y = screen_height - self.BOX_HEIGHT - 20  # 20px padding from bottom

        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font("dialogs/dialog_font.ttf", 18)
        self.reading = False
        self.portrait = None

    def get_portrait(self, npc_index=0, expression=0, facing="right"):
        frame_size = 8

        # Convert facing to row offset
        direction = 0 if facing == "right" else 1

        # Compute row
        row = npc_index * 2 + direction

        # Compute position
        x = expression * frame_size
        y = row * frame_size

        portrait = pygame.Surface((frame_size, frame_size), pygame.SRCALPHA)
        portrait.blit(self.npc_sheet, (0, 0), (x, y, frame_size, frame_size))

        return pygame.transform.scale(
            portrait,
            (self.PORTRAIT_SIZE, self.PORTRAIT_SIZE)
        )

    def execute(self, dialog=[], npc_index=0, expression=0, facing="right"):
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.letter_index = 0
            self.texts = dialog
            self.portrait = self.get_portrait(npc_index, expression, facing)

    def render(self, screen):
        if not self.reading:
            return

        # Typewriter effect
        self.letter_index += 1
        if self.letter_index >= len(self.texts[self.text_index]):
            self.letter_index = len(self.texts[self.text_index])

        # Draw box centered at bottom
        screen.blit(self.box, (self.x, self.y))

        # Draw portrait on the left of the box
        if self.portrait:
            portrait_x = self.x - self.PORTRAIT_SIZE - 10  # just left of box
            portrait_y = self.y + (self.BOX_HEIGHT - self.PORTRAIT_SIZE) // 2
            screen.blit(self.portrait, (portrait_x, portrait_y))

        # Draw text with offset to leave room on the left
        text_surface = self.font.render(
            self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0)
        )
        screen.blit(text_surface, (self.x + 20, self.y + 30))

    def next_text(self):
        self.text_index += 1
        self.letter_index = 0
        if self.text_index >= len(self.texts):
            self.reading = False
