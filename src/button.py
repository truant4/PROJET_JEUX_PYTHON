import pygame

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect= pygame.Rect(x,y,width, height)
        self.text = text
        self.survol = False
    
    def draw(self, surface, font):
        if self.hovered :
            color = (80, 140, 80)
        else :
            color = (50, 100, 50)
        
        pygame.draw.rect(surface, color, self.rect, border_radius = 10)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, width=2, border_radius=10)
        rendered = font.render(self.text, True, (255, 255, 255))
        surface.blit(rendered, rendered.get_rect(center = self.rect.center))

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return(
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )