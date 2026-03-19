import pygame

class DialogBox:
    BOX_WIDTH = 1400
    BOX_HEIGHT = 200
    PORTRAIT_SIZE = 112  

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.box = pygame.image.load('dialogs/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (self.BOX_WIDTH, self.BOX_HEIGHT))
        self.npc_sheet = pygame.image.load('assets/sprites/NPCS_Faces.png')
        self.x = (screen_width - self.BOX_WIDTH) // 2
        self.y = screen_height - self.BOX_HEIGHT - 20
        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font("dialogs/dialog_font.ttf", 24)  
        self.reading = False
        self.portrait = None

        
        self.frame_w = 96
        self.frame_h = 112

    def get_portrait(self, npc_index=0, expression=0, facing="right"):
        direction = 0 if facing == "right" else 1
        row = npc_index * 2 + direction
        x = expression * self.frame_w
        y = row * self.frame_h

        portrait = pygame.Surface((self.frame_w, self.frame_h), pygame.SRCALPHA)
        portrait.blit(self.npc_sheet, (0, 0), (x, y, self.frame_w, self.frame_h))

        
        return pygame.transform.scale(portrait, (self.PORTRAIT_SIZE * 2, self.PORTRAIT_SIZE * 2))

    def execute(self, dialog=[], npc_index=0, expressions=[], facing="right"):
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.letter_index = 0
            self.texts = dialog
            self.npc_index = npc_index
            self.facing = facing
            
            self.expressions = expressions if expressions else [0] * len(dialog)
            self.portrait = self.get_portrait(npc_index, self.expressions[0], facing)

    def next_text(self):
        self.text_index += 1
        self.letter_index = 0
        if self.text_index >= len(self.texts):
            self.reading = False
        else:
            
            expression = self.expressions[self.text_index] if self.text_index < len(self.expressions) else 0
            self.portrait = self.get_portrait(self.npc_index, expression, self.facing)

    def render(self, screen):
        if not self.reading:
            return

        
        self.letter_index += 1
        current_text = self.texts[self.text_index]
        if self.letter_index >= len(current_text):
            self.letter_index = len(current_text)

        
        screen.blit(self.box, (self.x, self.y))

        
        if self.portrait:
            portrait_w = self.portrait.get_width()
            portrait_h = self.portrait.get_height()
            portrait_x = self.x + 50  
            portrait_y = self.y - portrait_h  
            screen.blit(self.portrait, (portrait_x, portrait_y))

        
        text_surface = self.font.render(
            current_text[0:self.letter_index], False, (0, 0, 0)
        )
        portrait_w = self.portrait.get_width() if self.portrait else 0
        text_x = self.x + portrait_w + 10  
        text_y = self.y + (self.BOX_HEIGHT - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))
