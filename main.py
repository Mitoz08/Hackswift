import pygame
from sys import exit
from math import * #floor function of ScrollSen

window_height = 900
window_width = 1600


class TextBox(object):
    ObjectType = 0
    status = False
    Colours = [pygame.Color('lightskyblue3'), pygame.Color('grey15')]

    def __init__(self, height, width, x, y, header, DefText):
        self.height = height * 32
        self.width = width * 24
        self.x = x
        self.y = y
        self.text = ''
        self.header = header
        self.box_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.DefText = DefText

    def checkStatus(self,MousePos):
        # Check Collision
        if self.box_rect.collidepoint(MousePos):
            self.status = True
        else:
            self.status = False

    def updateText(self, Mode, char):
        if Mode == 0:
            self.text = self.text[:-1]
        elif Mode == 1:
            self.text += char

    def Draw(self):
        # Drawing Box
        pygame.draw.rect(screen, 'white', self.box_rect)
        pygame.draw.rect(screen, self.Colours[0 if self.status else 1], self.box_rect,2)

        # Drawing Header
        header_surface = test_font.render(self.header, True, 'black')
        screen.blit(header_surface, (self.box_rect.x, self.box_rect.y - 20))

        # Drawing Default Text
        #DefText_surface = test_font.render(self.BoxText, True, 'black')
        #screen.blit(DefText_surface, ((self.box_rect.x + 5, self.box_rect.y + 5)))

        # Drawing Text
        #text_surface = test_font.render(self.text, True, 'black')
        #screen.blit(text_surface, (self.box_rect.x + 5, self.box_rect.y + 5))

        # Merged Commented Code

        # Drawing Text/ Default Text
        if len(self.text) == 0:
            text_surface = test_font.render(self.DefText, True, 'grey')
        else:
            text_surface = test_font.render(self.text, True, 'black')
        screen.blit(text_surface, (self.box_rect.x + 5, self.box_rect.y + 5))


class DropBox(TextBox):
    ObjectType = 1
    Cycle = 0
    ScrollSen = 2
    def __init__(self, height, width, x, y, header,DefText,Content,MaxCycle):
        super().__init__(height, width, x, y, header,DefText)
        self.DDBox_Rect = pygame.Rect(self.x,self.y-self.height, self.width,self.height*3)
        self.Content = Content
        self.MaxCycle = MaxCycle


    def DrawDDBox(self):
        self.Draw()
        if self.status and self.MaxCycle:
            pygame.draw.rect(screen, 'purple', self.DDBox_Rect)
            for i in range(3):
                text_surface = test_font.render(f"{self.Content[(floor(self.Cycle/self.ScrollSen)+(i-1))%self.MaxCycle]:02d}", True, 'black')
                screen.blit(text_surface, (self.DDBox_Rect.x + 5, self.box_rect.y + 5 + (i-1)*self.height))

            #Update the TextBox
            self.text = f"{self.Content[floor(self.Cycle/self.ScrollSen)]:02d}"



        elif self.status and not self.MaxCycle:
            small_font = pygame.font.Font(None, 16)
            text_surface = small_font.render('Enter Month and Year first!', True, 'red')
            screen.blit(text_surface, (self.DDBox_Rect.x + 5, self.box_rect.y + self.height+5))

    def CheckDayMon(self):
        if self.header == 'Date' or self.header == 'Month':
            if len(self.Content) == 0:
                return 1

        return 0

class TickBox(object):
    ObjectType = 2
    status = False
    Tick_Status = False

    Colours = ['white','red']

    def __init__(self,x,y,header):
        self.x = x
        self.y = y
        self.header = header
        self.box_rect = pygame.Rect(self.x,self.y,30,30)

    def checkStatus(self,MousePos):
        # Check Collision
        if self.box_rect.collidepoint(MousePos):
            self.status = True
            if self.Tick_Status:
                self.Tick_Status = False
            else:
                self.Tick_Status = True
        else:
            self.status = False

    def Draw(self):
        # Drawing Box
        pygame.draw.rect(screen, self.Colours[1 if self.Tick_Status else 0], self.box_rect)
        pygame.draw.rect(screen, 'black', self.box_rect, 2)

        # Drawing Header
        header_surface = test_font.render(self.header, True, 'black')
        screen.blit(header_surface, (self.x + 35, self.y))


class UserInputGUI(object):
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

    DD_Mins = [00,15,30,45]
    DD_Hours = [x for x in range(24)]
    DD_Year = [x + 2020 for x in range(50)]
    DD_Month = [x + 1 for x in range(12)]
    DD_Days = [x+1 for x in range(31)]
    DD_MthDay = [31,28,31,30,31,30,31,31,30,31,30,31]

    def __init__(self):
        # Initialising Empty Input Boxes
        self.category = ['Title', 'Date', 'Hour', 'Min', 'Year', 'Month', 'Day']

        #TextBoxes
        self.dict[self.category[0]] = TextBox(1, 20, self.BG_x + 50, self.BG_y + 50, self.category[0],'Enter the Title')
        self.dict[self.category[1]] = TextBox(1, 5, self.BG_x + 50, self.BG_y + 150, self.category[1],'Date')

        #DropBoxes
        self.dict[self.category[2]] = DropBox(1, 2, self.BG_x + 250, self.BG_y + 150, self.category[2], 'Hr',self.DD_Hours, 24)
        self.dict[self.category[3]] = DropBox(1, 2, self.BG_x + 350, self.BG_y + 150, self.category[3],'Min', self.DD_Mins, 4)
        #Date including Leap year
        self.dict[self.category[4]] = DropBox(1, 4, self.BG_x + 210, self.BG_y + 250, self.category[4], 'YYYY', self.DD_Year, 50)
        self.dict[self.category[5]] = DropBox(1, 2, self.BG_x + 130, self.BG_y + 250, self.category[5], 'MM', self.DD_Month, 12)
        self.dict[self.category[6]] = DropBox(1, 2, self.BG_x + 50, self.BG_y + 250, self.category[6], 'DD', self.DD_Days, 0)

        #TickBoxes
        self.dict['Recurring'] = TickBox(self.BG_x + 50,self.BG_y + 300,'Recurring')


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
            if item.ObjectType == 0:
                item.Draw()
            elif item.ObjectType == 1:
                item.DrawDDBox()
            elif item.ObjectType == 2:
                item.Draw()

    def UserClick(self, MousePos):
        if self.Exit_Rect.collidepoint(MousePos):
            return 1
        for item in self.dict.values():
            item.checkStatus(MousePos)
        return 0

    def EditText(self, Mode, Char):
        for item in self.dict.values():
            if item.status and item.ObjectType == 0:
                item.updateText(Mode,Char)

    def ScrollDD(self, Mode, MousePos):
        for item in self.dict.values():
            if item.status and item.ObjectType == 1:
                if item.CheckDayMon():
                    return
                if Mode == 4:   # Scroll Up
                    item.Cycle -= 1
                else:           # Scroll Down
                    item.Cycle += 1
                if item.Cycle == item.ScrollSen*item.MaxCycle:  # Cycle from last to first
                    item.Cycle = 0
                if item.Cycle == -1:                            # Cycle from first to last
                    item.Cycle = item.ScrollSen*item.MaxCycle-1
        self.Update()
    def Update(self):
        Year = self.dict.get('Year')
        Month = self.dict.get('Month')
        Day = self.dict.get('Day')
        if Year.status or Month.status:
            if Year.text != '' and Month.text != '':
                if(int(Year.text)-2024)&4 == 0:
                    Leap = 1
                else:
                    Leap = 0
                MthDay = int(Month.text) - 1
                MaxDays = self.DD_MthDay[MthDay] + Leap
                #Day.Content = [x+1 for x in range(MaxDays)]
                Day.MaxCycle = MaxDays
                Day.Cycle = 0
            else:
                Day.MaxCycle = 0
                Day.Cycle = 0


    def DeactiveAll(self):
        for item in self.dict.values():
            item.status = False

pygame.init()

screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()

test_font = pygame.font.Font(None, 32)

input_rect = pygame.Rect(10, 10, 140, 32)
Test = UserInputGUI

UserEventGUI = False  # TextBox


"""Testing Area"""
#TimeDBox = DropBox(1,12,100,100,"Time")


"""Testing Area"""

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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if input_rect.collidepoint(event.pos) and not UserEventGUI:
                Test = UserInputGUI()
                UserEventGUI = True

        if UserEventGUI:  # Only Checks When in User GUI

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    Test.DeactiveAll()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if Test.UserClick(event.pos):
                        UserEventGUI = False

                if event.button in [4,5]:
                    print(event.button)
                    Test.ScrollDD(event.button, event.pos)

            #if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #    if Test.UserClick(event.pos):
            #        UserEventGUI = False

            #if event.type == pygame.MOUSEMOTION and (event.buttons in [4,5]):
            #    Test.ScrollDD(event.button,event.pos)



        if event.type == pygame.KEYDOWN:
            if UserEventGUI:
                if event.key == pygame.K_BACKSPACE:
                    Test.EditText(0, event.unicode)
                else:
                    Test.EditText(1, event.unicode)

    screen.fill('white')

    if not UserEventGUI:
        pygame.draw.rect(screen, 'blue', input_rect)
        Add_Surface = test_font.render('Add Event', True, 'white')
        screen.blit(Add_Surface, (input_rect.x+10,input_rect.y+5))


    else:
        Test.Update()
        Test.Draw()

    #TimeDBox.DrawDDBox()

    pygame.display.update()
    clock.tick(60)
