class Menu_Button:

    BORDER_PADDING = 5
    RECT_FRAME_WIDTH = 5
    
    def __init__(self, text, xpo, ypo, height, width, color, action, action_text, padding=BORDER_PADDING, argv=None):
        self.text = text
        self.x_pos = xpo - padding
        self.y_pos = ypo - padding
        self.height = height
        self.width = width
        self.color = color
        self.action = action
        self.action_text = action_text
        self.padding = padding
        self.args = argv
        
    def call_action(self):
        if self.args:
            self.action(*self.args)
        else:
            self.action()
            
    def matches_touch(touch_pos):
        touch_x = touch_pos[0]
        touch_y = touch_pos[1]
        if self.x_pos <= touch_x <= (self.x_pos + self.width) and self.y_pos <= touch_y <= (self.y_pos + self.height):
            return True
        else:
            return False