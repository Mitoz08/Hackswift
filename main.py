import pygame
from sys import exit

window_height = 600
window_width = 1000


class textBox(object):
    status = False
    Colours = [pygame.Color('lightskyblue3'), pygame.Color('grey15')]

    def __init__(self, height, width, x, y, header):
        self.height = height * 32
        self.width = width * 32
        self.x = x
        self.y = y
        self.text = ''
        self.header = header

    # def toggle(self):
    #    self.status = False if self.status else True

    def updateText(self, remove, char):
        if remove:
            self.text = self.text[:-1]
        else:
            self.text += char

    def Draw(self):
        # Drawing Box
        box_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.Colours[0 if self.status else 1], box_rect, 2)

        # Drawing Header
        header_surface = test_font.render(self.header, True, 'white')
        screen.blit(header_surface, (box_rect.x, box_rect.y - 20))

        # Drawing Text
        text_surface = test_font.render(self.text, True, 'white')
        screen.blit(text_surface, (box_rect.x + 5, box_rect.y + 5))


class userInputGUI(object):
    # User GUI Window
    # GUI Size
    BG_Width = 760
    BG_Height = 360

    # (0,0) Position on Background is ( (window_width-BG_Width)/2 , window_height-BG_Height)/2 )
    BG_x = (window_width - BG_Width) / 2
    BG_y = (window_height - BG_Height) / 2

    Background = pygame.Rect(BG_x, BG_y, BG_Width, BG_Height)
    Exit_Rect = pygame.Rect(BG_x + BG_Width - 50, BG_y + 10, 40, 40)
    dict = {}

    def __init__(self):
        # Initialising Empty Input Boxes
        self.category = ['Title', 'Date', 'Time']
        self.dict[self.category[0]] = textBox(1, 20, self.BG_x + 50, self.BG_x + 50, self.category[0])
        self.dict[self.category[1]] = textBox(1, 5, self.BG_x + 50, self.BG_x + 150, self.category[1])
        self.dict[self.category[2]] = textBox(1, 5, self.BG_x + 350, self.BG_x + 150, self.category[2])

    def Draw(self):
        Colours = [pygame.Color('lightskyblue3'), pygame.Color('grey15')]

        # Background
        pygame.draw.rect(screen, 'blue', self.Background)

        # Exit Button
        Exit_Rect = pygame.Rect(self.BG_x + self.BG_Width - 50, self.BG_y + 10, 40, 40)
        pygame.draw.rect(screen, 'red', Exit_Rect)
        Exit_font = pygame.font.Font(None, 80)
        Exit_surface = Exit_font.render('x', True, 'white')
        screen.blit(Exit_surface, (Exit_Rect.x + 5, Exit_Rect.y - 10))

        for item in self.dict.values():
            item.Draw()

    def UserClick(self, MousePos):

        if self.Exit_Rect.collidepoint(MousePos):
            return 1

        for item in self.dict.values():
            # Check Collision
            box_rect = pygame.Rect(item.x, item.y, item.width, item.height)
            if box_rect.collidepoint(MousePos):
                item.status = True
            else:
                item.status = False
        return 0

    def EditText(self, Mode, Char):
        for item in self.dict.values():
            if item.status:
                if Mode == 0:
                    item.text = item.text[:-1]
                else:
                    item.text += Char


pygame.init()

screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()

test_font = pygame.font.Font(None, 32)

input_rect = pygame.Rect(10, 10, 140, 32)
Test = userInputGUI

UserEventGUI = False  # TextBox
DropBoxes = [0, 0, 0]

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # if event.type == pygame.MOUSEBUTTONDOWN:
        #    if input_rect.collidepoint(event.pos) and not UserEventGUI:
        #        Test = userInputGUI()
        #        UserEventGUI = True
        #
        #    if UserEventGUI:
        #        if Test.UserClick(event.pos):
        #            UserEventGUI = False

        # if event.type == pygame.MOUSEMOTION:
        #    if sum(DropBoxes) > 0:
        #       continue
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos) and not UserEventGUI:
                Test = userInputGUI()
                UserEventGUI = True

        if UserEventGUI:  # Only Checks When in User GUI
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Test.UserClick(event.pos):
                    UserEventGUI = False

            if event.type == pygame.MOUSEMOTION:
                if sum(DropBoxes) > 0:
                    continue

        if event.type == pygame.KEYDOWN:
            if UserEventGUI:
                if event.key == pygame.K_BACKSPACE:
                    Test.EditText(0, event.unicode)
                else:
                    Test.EditText(1, event.unicode)

    screen.fill((0, 0, 0))

    if not UserEventGUI:
        pygame.draw.rect(screen, 'white', input_rect)
        Add_Surface = test_font.render('Add Event', True, 'black')
        screen.blit(Add_Surface, input_rect)


    else:
        Test.Draw()

    pygame.display.update()
    clock.tick(60)
