class Menu_Button:
    
    def __init__(self, text, xpo, ypo, height, width, color):
        self.text = text
        self.x_pos = xpo
        self.y_pos = ypo
        self.height = height
        self.width = width
        self.color = color
        
    def draw_button(text, xpo, ypo, height, width, color):
        font=pygame.font.Font(None,30)
        label=font.render(str(text), 1, (color))
        screen.blit(label,(xpo,ypo+8))
        pygame.draw.rect(screen, blue, (xpo-5,ypo-5,width,height),5)