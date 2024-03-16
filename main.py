import pygame
from sys import exit


class textBox(object):

    def __init__(self, height, width, x, y, header):
        self.height = height * 32
        self.width = width * 32
        self.x = x
        self.y = y
        self.text = ''
        self.header = header
        self.status = False

    def toggle(self):
        self.status = False if self.status else True

    def updateText(self, remove, char):
        if remove:
            self.text = self.text[:-1]
        else:
            self.text += char


class userInputGUI(object):

    def __init__(self):
        self.dict = {}
        self.category = ['Date', 'Event', 'Time']
        self.dict[self.category[0]] = textBox(1, 5, 50, 50, self.category[0])
        self.dict[self.category[1]] = textBox(1, 20, 50, 150, self.category[1])
        self.dict[self.category[2]] = textBox(1, 5, 350, 50, self.category[2])
        self.currentBox = -1

    def Draw(self):
        Colours = [pygame.Color('lightskyblue3'), pygame.Color('grey15')]

        #Backgbround
        Background = pygame.Rect(20,20,760,360)
        pygame.draw.rect(screen, 'blue', Background)

        #Exit Button
        Exit_Rect = pygame.Rect(720,30,40,40)
        pygame.draw.rect(screen, 'red', Exit_Rect)
        Exit_font = pygame.font.Font(None, 80)
        Exit_surface = Exit_font.render('x', True, 'white')
        screen.blit(Exit_surface, (Exit_Rect.x +5, Exit_Rect.y-10))



        for item in self.dict.values():
            # Drawing Box
            box_rect = pygame.Rect(item.x, item.y, item.width, item.height)
            pygame.draw.rect(screen, Colours[0 if item.status else 1], box_rect, 2)

            #Drawing Header
            header_surface = test_font.render(item.header, True, 'white')
            screen.blit(header_surface, (box_rect.x, box_rect.y - 20))

            # Drawing Text
            text_surface = test_font.render(item.text, True, 'white')
            screen.blit(text_surface, (box_rect.x + 5, box_rect.y + 5))

    def UserClick(self, MousePos):

        Exit_Rect = pygame.Rect(720,30,40,40)
        if Exit_Rect.collidepoint(MousePos):
            return 1

        for item in self.dict.values():
            # Check Collision
            box_rect = pygame.Rect(item.x, item.y, item.width, item.height)
            if box_rect.collidepoint(MousePos):
                item.status = True
            else:
                item.status = False
        return 0

    def EditText(self,Mode,Char):
        for item in self.dict.values():
            if item.status:
                if Mode == 0:
                    item.text = item.text[:-1]
                else:
                    item.text += Char




pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

test_font = pygame.font.Font(None, 32)


input_rect = pygame.Rect(10, 10, 140, 32)
Test = userInputGUI

UserEventGUI = False #TextBox

while True:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos) and not UserEventGUI:
                Test = userInputGUI()
                UserEventGUI = True

            if UserEventGUI:
                if Test.UserClick(event.pos):
                    UserEventGUI = False


        if event.type == pygame.KEYDOWN:
            if UserEventGUI:
                if event.key == pygame.K_BACKSPACE:
                    Test.EditText(0,event.unicode)
                else:
                    Test.EditText(1,event.unicode)


    screen.fill((0, 0, 0))

    if not UserEventGUI:
        pygame.draw.rect(screen,'white',input_rect)
        Add_Surface = test_font.render('Add Event',True,'black')
        screen.blit(Add_Surface,input_rect)


    else:
        Test.Draw()

    '''if active:
        color1 = color
    else:
        color1 = color_passive
    pygame.draw.rect(screen, color1, input_rect, 2)

    text_surface = test_font.render(user_text, True, (255, 255, 255))
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

    input_rect.w = max(text_surface.get_width() + 10, 200)'''

    pygame.display.update()
    clock.tick(60)
