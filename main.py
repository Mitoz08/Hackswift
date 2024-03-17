import pygame
from sys import exit
from math import * #floor function of ScrollSen
from Event import *
import datetime

pygame.init()

window_height = 600
window_width = 1000


font_size = int(0.02* sqrt(window_width**2 + window_height**2))


class TextBox(object):
    ObjectType = 0
    status = False
    Colours = [pygame.Color('lightskyblue3'), pygame.Color('grey15')]


    def __init__(self, height, width, x, y, header, DefText, TextMode = 0,textMax = 30):
        self.height = height * font_size
        self.width = width * font_size
        self.x = x
        self.y = y
        self.text = ''
        self.textMax = textMax
        self.header = header
        self.box_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.DefText = DefText
        self.TextMode = TextMode

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
            if self.TextMode:
                try:
                    int(char)
                except ValueError:
                    return 1
                except:
                    return 2
            if (len(self.text) >= self.textMax):
                return 0
            self.text += char

    def Draw(self):
        # Drawing Box
        pygame.draw.rect(screen, 'white', self.box_rect)
        pygame.draw.rect(screen, self.Colours[0 if self.status else 1], self.box_rect,2)

        # Drawing Header
        header_surface = test_font.render(self.header, True, 'black')
        screen.blit(header_surface, (self.box_rect.x, self.box_rect.y - 0.8*font_size))

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

    def checkStatus(self,MousePos):
        # Check Collision
        if self.box_rect.collidepoint(MousePos):
            if self.status:
                self.status = False
            else:
                self.status = True
        else:
            self.status = False

    def DrawDDBox(self):
        self.Draw()
        if self.status and self.MaxCycle:
            pygame.draw.rect(screen, 'purple', self.DDBox_Rect)
            for i in range(3):
                if i == 1:
                    pygame.draw.rect(screen, 'purple', self.box_rect)
                    pygame.draw.rect(screen, self.Colours[0 if self.status else 1], self.box_rect, 2)
                text_surface = test_font.render(f"{self.Content[(floor(self.Cycle/self.ScrollSen)+(i-1))%self.MaxCycle]:02d}", True, 'black')
                screen.blit(text_surface, (self.DDBox_Rect.x + 5, self.box_rect.y + 5 + (i-1)*self.height))

            #Update the TextBox
            self.text = f"{self.Content[floor(self.Cycle/self.ScrollSen)]:02d}"

        elif self.status and not self.MaxCycle: # ONLY FOR DD MM YYYY
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
    BG_Width = 0.8*window_width
    BG_Height = 0.8*window_height

    # (0,0) Position on Background is ( (window_width-BG_Width)/2 , window_height-BG_Height)/2 )
    BG_x = (window_width - BG_Width) / 2
    BG_y = (window_height - BG_Height) / 2

    Background = pygame.Rect(BG_x, BG_y, BG_Width, BG_Height)
    Exit_Rect = pygame.Rect(BG_x + BG_Width - 50, BG_y + 10, font_size, font_size)
    Save_Rect = pygame.Rect(BG_x + font_size, BG_y + font_size, 2 * font_size, font_size)

    DefDict = {}
    RecurDict = {}
    FixDict = {}
    DymDict = {}

    DD_Mins = [00,15,30,45]
    DD_Hours = [x for x in range(24)]
    DD_Year = [x + 2020 for x in range(50)]
    DD_Month = [x + 1 for x in range(12)]
    DD_Days = [x + 1 for x in range(31)]
    DD_MthDay = [31,28,31,30,31,30,31,31,30,31,30,31]

    """ Start of Merging"""
    Mode = 0 # 0 for Fixed 1 for Dynamic

    DefParaStr = ['Event','Location','Description']
    DefParaDB = ['Priority',['Day','Month','Year']]
    DefParaTB = ['Dynamic Event']

    FixParaStr = ['Period','Cycle']
    FixParaDB = [['StartHr','StartMin'],['EndHr','EndMin']]
    FixParaTB = ['Recurrent']

    DymParaDB = [['DurHr','DurMin']]



    """ End of Merging"""


    def __init__(self):
        # Initialising Empty Input Boxes
        #self.category = ['Title', 'Date', 'Hour', 'Min', 'Year', 'Month', 'Day']

        #TextBoxes
        #self.dict[self.category[0]] = TextBox(1, 20, self.BG_x + 50, self.BG_y + 50, self.category[0],'Enter the Title')
        #self.dict[self.category[1]] = TextBox(1, 5, self.BG_x + 50, self.BG_y + 150, self.category[1],'Date')

        #DropBoxes
        #self.dict[self.category[2]] = DropBox(1, 2, self.BG_x + 250, self.BG_y + 150, self.category[2], 'Hr',self.DD_Hours, 24)
        #self.dict[self.category[3]] = DropBox(1, 2, self.BG_x + 350, self.BG_y + 150, self.category[3],'Min', self.DD_Mins, 4)
        #Date including Leap year
        #self.dict[self.category[4]] = DropBox(1, 4, self.BG_x + 210, self.BG_y + 250, self.category[4], 'YYYY', self.DD_Year, 50)
        #self.dict[self.category[5]] = DropBox(1, 2, self.BG_x + 130, self.BG_y + 250, self.category[5], 'MM', self.DD_Month, 12)
        #self.dict[self.category[6]] = DropBox(1, 2, self.BG_x + 50, self.BG_y + 250, self.category[6], 'DD', self.DD_Days, 0)

        #TickBoxes
        #self.dict['Recurring'] = TickBox(self.BG_x + 50,self.BG_y + 300,'Recurring')

        """ Start of Merging"""
        # Default parameters
        # Strings: name,location,description
        # DropBoxes: priority

        # Fixed parameters
        # Strings: recurring (add textbox if true)
        # DropBoxes: start time,end time,date,
        # TickBoxes: recurring

        # Dynamic parameters
        # Strings
        # DropBoxes: expiry date,duration (datetime.time format)

        # Default Boxes
        # Event Type
        self.DefDict[self.DefParaTB[0]] = TickBox(self.BG_x + 6 * font_size, self.BG_y + font_size, self.DefParaTB[0])

        # Event Name
        self.DefDict[self.DefParaStr[0]] = TextBox(1, 20, self.BG_x + font_size, self.BG_y + 4 * font_size, self.DefParaStr[0],
                                              'Enter the Event')

        # Event Location
        self.DefDict[self.DefParaStr[1]] = TextBox(1, 20, self.BG_x + font_size, self.BG_y + 6 * font_size, self.DefParaStr[1],
                                                'Enter the Location')

        # Event Description
        self.DefDict[self.DefParaStr[2]] = TextBox(3, 20, self.BG_x + font_size, self.BG_y + 8 * font_size, self.DefParaStr[2],
                                                'Enter the Description',textMax=30)

        # Priority Dropbox
        self.DefDict[self.DefParaDB[0]] = DropBox(1, 2, self.BG_x + 22 * font_size, self.BG_y + 4 * font_size, self.DefParaDB[0],
                                               '0', [1,2,3,4], 4)
        # Date
        self.DefDict[self.DefParaDB[1][0]] = DropBox(1, 2, self.BG_x + 4.5 * font_size, self.BG_y + 12 * font_size,
                                                     self.DefParaDB[1][0],
                                                  'DD', self.DD_Days, 0)
        self.DefDict[self.DefParaDB[1][1]] = DropBox(1, 2, self.BG_x + 7 * font_size, self.BG_y + 12 * font_size,
                                                     self.DefParaDB[1][1],
                                                  'MM', self.DD_Month, 12)
        self.DefDict[self.DefParaDB[1][2]] = DropBox(1, 2, self.BG_x + 9.5 * font_size, self.BG_y + 12 * font_size,
                                                     self.DefParaDB[1][2],
                                                  'YYYY', self.DD_Year, 50)



        # Fixed Boxes
        # Recurrent Start
        self.RecurDict[self.FixParaStr[0]] = TextBox(1, 2, self.BG_x + 29 * font_size, self.BG_y + 6 * font_size, self.FixParaStr[0],
                                                '00',1,2)
        self.RecurDict[self.FixParaStr[1]] = TextBox(1, 2, self.BG_x + 26 * font_size, self.BG_y + 6 * font_size, self.FixParaStr[1],
                                                '00',1,2)
        self.FixDict[self.FixParaTB[0]] = TickBox(self.BG_x + 14 * font_size, self.BG_y + font_size, self.FixParaTB[0])
        # Recurrent End

        # Time
        # Start Time
        self.FixDict[self.FixParaDB[0][0]] = DropBox(1, 2, self.BG_x + 4.5 * font_size, self.BG_y + 16 * font_size, 'Hour',
                                                  'Hrs', self.DD_Hours, 24)
        self.FixDict[self.FixParaDB[0][1]] = DropBox(1, 2, self.BG_x + 7 * font_size, self.BG_y + 16 * font_size, 'Min',
                                                  'Mins', self.DD_Mins, 4)
        # End Time
        self.FixDict[self.FixParaDB[1][0]] = DropBox(1, 2, self.BG_x + 15 * font_size, self.BG_y + 16 * font_size, 'Hour',
                                                  'Hrs', self.DD_Hours, 24)
        self.FixDict[self.FixParaDB[1][1]] = DropBox(1, 2, self.BG_x + 17.5 * font_size, self.BG_y + 16 * font_size, 'Min',
                                                  'Mins', self.DD_Mins, 4)

        # Dynamic Boxes
        self.DymDict[self.DymParaDB[0][0]] = DropBox(1, 2, self.BG_x + 4.5 * font_size, self.BG_y + 16 * font_size, 'Hour',
                                                  'Hrs', self.DD_Hours, 24)
        self.DymDict[self.DymParaDB[0][1]] = DropBox(1, 2, self.BG_x + 7 * font_size, self.BG_y + 16 * font_size, 'Min',
                                                  'Mins', self.DD_Mins, 4)

        """ End of Merging"""

    def Draw(self):
        Colours = [pygame.Color('lightskyblue3'), pygame.Color('grey15')]

        # Background
        pygame.draw.rect(screen, 'blue', self.Background)

        # Exit Button
        pygame.draw.rect(screen, 'red', self.Exit_Rect)
        Exit_font = pygame.font.Font(None, self.Exit_Rect.width)
        Exit_surface = Exit_font.render('x', True, 'white')
        screen.blit(Exit_surface, (self.Exit_Rect.x + 0.25*font_size, self.Exit_Rect.y))

        # Save Button
        pygame.draw.rect(screen, 'red', self.Save_Rect)
        Save_Surface = test_font.render('Save', True, 'white')
        screen.blit(Save_Surface, (self.Save_Rect.x,self.Save_Rect.y))

        # Priority Text
        Priority = ['Low','Medium','High','Urgent']
        Priority_Class = self.DefDict['Priority']

        for i in range(4):
            Priority_Surface = Small_font.render(f'{i} - {Priority[i]}', True, 'White')
            screen.blit(Priority_Surface, (Priority_Class.x + 3 * font_size, Priority_Class.y - font_size + i*0.5*font_size))

        # Date Text
        Date_Class = self.DefDict['Day']
        DateTitle_Surface = test_font.render('Date:', True, 'white')
        screen.blit(DateTitle_Surface, (Date_Class.x - 3 * font_size, Date_Class.y))

        # Default Drawing
        for item in self.DefDict.values():
            if item.ObjectType == 1:
                item.DrawDDBox()
            else:
                item.Draw()

        # Dynamic Drawing
        if self.Mode:
            Time_Class = self.DymDict['DurHr']
            TimeTitle_Surface = test_font.render('Duration:', True, 'white')
            screen.blit(TimeTitle_Surface, (Time_Class.x - 3 * font_size, Time_Class.y))

            for item in self.DymDict.values():
                if item.ObjectType == 1:
                    item.DrawDDBox()
                else:
                    item.Draw()

        else:
            Time_Class = self.FixDict['StartHr']
            TimeTitle_Surface = test_font.render('Start:', True, 'white')
            screen.blit(TimeTitle_Surface, (Time_Class.x - 3 * font_size, Time_Class.y))

            Time_Class = self.FixDict['EndHr']
            TimeTitle_Surface = test_font.render('End:', True, 'white')
            screen.blit(TimeTitle_Surface, (Time_Class.x - 3 * font_size, Time_Class.y))

            if self.FixDict['Recurrent'].Tick_Status:
                Recurrent_Class = self.RecurDict['Cycle']
                RecurTitle_Surface = test_font.render('Recurrent:', True, 'white')
                screen.blit(RecurTitle_Surface, (Recurrent_Class.x - 4 * font_size, Recurrent_Class.y))
                RecurText_Surface = Small_font.render(f'Cycle: 0 - Forver '
                                                      f'          N - N Times', True, 'White')
                screen.blit(RecurText_Surface,
                            (Recurrent_Class.x - 4 * font_size, Recurrent_Class.y + 1.1 * font_size))
                RecurText_Surface = Small_font.render(f'Perid: 1 - Every Day'
                                                      f'       7 - Every Week', True, 'White')
                screen.blit(RecurText_Surface,
                            (Recurrent_Class.x - 4 * font_size, Recurrent_Class.y + 1.6 * font_size))

                for item in self.RecurDict.values():
                    if item.ObjectType == 1:
                        item.DrawDDBox()
                    else:
                        item.Draw()


            for item in self.FixDict.values():
                if item.ObjectType == 1:
                    item.DrawDDBox()
                else:
                    item.Draw()

    def UserClick(self, MousePos):
        if self.Exit_Rect.collidepoint(MousePos):
            return 1

        if self.Save_Rect.collidepoint(MousePos):
            print("Hi")
            if self.CheckFilled():
                return 0
            else:
                self.DeactiveAll()
                return 2

        for item in self.DefDict.values():
            item.checkStatus(MousePos)

        TempDict = self.DymDict if self.Mode else self.FixDict
        for item in TempDict.values():
            item.checkStatus(MousePos)
        if not self.Mode and self.FixDict['Recurrent'].Tick_Status:
            for item in self.RecurDict.values():
                item.checkStatus(MousePos)

        return 0

    def EditText(self, Mode, Char):
        for item in self.DefDict.values():
            if item.status and item.ObjectType == 0:
                item.updateText(Mode,Char)

        TempDict = self.DymDict if self.Mode else self.FixDict
        for item in TempDict.values():
            if item.status and item.ObjectType == 0:
                item.updateText(Mode,Char)
        if not self.Mode and self.FixDict['Recurrent'].Tick_Status:
            for item in self.RecurDict.values():
                if item.status and item.ObjectType == 0:
                    item.updateText(Mode,Char)

    def ScrollDD(self, Mode, MousePos):
        for item in self.DefDict.values():
            self.ScrollFunc(item)

        TempDict = self.DymDict if self.Mode else self.FixDict
        for item in TempDict.values():
            self.ScrollFunc(item)
        if not self.Mode and self.FixDict['Recurrent'].Tick_Status:
            for item in self.RecurDict.values():
                self.ScrollFunc(item)

        self.UpdateDay()

    def ScrollFunc(self,item):
        if item.status and item.ObjectType == 1:
            if item.CheckDayMon():
                return
            if self.Mode == 4:  # Scroll Up
                item.Cycle -= 1
            else:  # Scroll Down
                item.Cycle += 1
            if item.Cycle == item.ScrollSen * item.MaxCycle:  # Cycle from last to first
                item.Cycle = 0
            if item.Cycle == -1:  # Cycle from first to last
                item.Cycle = item.ScrollSen * item.MaxCycle - 1

    def UpdateDay(self):
        Year = self.DefDict.get('Year')
        Month = self.DefDict.get('Month')
        Day = self.DefDict.get('Day')
        if not Year or not Month:
            return
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
                Day.text = '01'
            else:
                Day.MaxCycle = 0
                Day.Cycle = 0

    def UpdateEventType(self):
        if self.DefDict['Dynamic Event'].Tick_Status:
            self.Mode = 1
        else:
            self.Mode = 0
        return

    def Update(self):
        self.UpdateEventType()
        self.UpdateDay()

    def DeactiveAll(self):
        for item in self.DefDict.values():
            item.status = False

    def CheckFilled(self):
        for item in self.DefDict.values():
            if item.ObjectType != 2 and item.text == '':
                return 1

        TempDict = self.DymDict if self.Mode else self.FixDict
        for item in TempDict.values():
            if item.ObjectType != 2 and item.text == '':
                return 1


        if not self.Mode and self.FixDict['Recurrent'].Tick_Status:
            for item in self.RecurDict.values():
                if item.ObjectType != 2 and item.text == '':
                    return 1
        return 0

    def CreateEvent(self):
        if self.CheckFilled():
            print("Please Fill Boxes")
            return
        EventName = self.DefDict['Event'].text
        EventLoc = self.DefDict['Location'].text
        EventDes = self.DefDict['Description'].text
        _Priority = Priority(int(self.DefDict['Priority'].text))
        Date = datetime.date(int(self.DefDict['Year'].text),int(self.DefDict['Month'].text),int(self.DefDict['Day'].text))

        if self.Mode:
            EventDur = datetime.time(int(self.DymDict['DurHr'].text),int(self.DymDict['DurMin'].text))

            Event = DynamicEvent(EventName,EventDur,Date,EventLoc,EventDes,Priority)

            #Event = DynamicEvent(name=EventName,
            #                     location=EventLoc,
            #                     description=EventDes,
            #                     expiry_date=Date,
            #                     duration=EventDur,
            #                     priority_tag=Priority)

        else:
            Period = int(self.RecurDict['Period'].text)
            Cycle = int(self.RecurDict['Cycle'].text)
            StartTime = datetime.time(int(self.FixDict['StartHr'].text),int(self.FixDict['StartMin'].text))
            EndTime = datetime.time(int(self.FixDict['EndHr'].text), int(self.FixDict['EndMin'].text))


            Event = FixedEvent(EventName,StartTime,EndTime,Date,Period,Cycle,EventLoc,EventDes,Priority)

            #Event = FixedEvent(name=EventName,
            #                   location=EventLoc,
            #                   description=EventDes,
            #                   date=Date,
            #                   start_time=StartTime,
            #                   end_time=EndTime,
            #                   recur_period=Period,
            #                   recur_cycle=Cycle,
            #                   priority_tag=Priority)

        return Event




screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()

Small_font = pygame.font.Font(None, int(0.8 * font_size))
test_font = pygame.font.Font(None, font_size)

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
                    Value = Test.UserClick(event.pos)
                    if Value == 1:
                        UserEventGUI = False
                    elif Value == 2:
                        Event = Test.CreateEvent()
                        print(Event.get_name())
                        UserEventGUI = False

                if event.button in [4,5]:
                    #print(event.button)
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
