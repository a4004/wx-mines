import random
import wx

# global variables declared and assigned a default value
first_click = True
# the base value for widget id's (good practice)
base_id = 10000

# custom class that inherits the wx.Frame base class
class MainFrame(wx.Frame):
    # class constructor, taking in a parent and title variable (self is used because of Python convention)
    def __init__(self, parent, title):
        # call the base constructor to do the important set-up
        wx.Frame.__init__(self, parent, title=title, size=(800, 600))
        # set some basic properties of our Frame such as bg colour and grid layout (because it's minesweeper)
        self.SetBackgroundColour((255, 255, 255))
        self.Grid = wx.GridSizer(10, 10, 0, 0)
        # create a list of fixed length of the needed types - indexes will be used for assignment rather than list.append()
        self.Buttons = [wx.Button] * 100
        self.Mines = [int] * 100
        # create a wxFont object because we want big text
        font = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)
        # loop through each of the proposed buttons and create them (10x10 grid, hence the nested loop)
        for x in range(10):
            for y in range(10):
                # create the button object with empty text and a unique id that allows its position to be found later
                # e.g. current button is at (3, 5) so 10000 + (5 * 10 + x) = 10053
                # we can return to (3, 5) by first (see line 56 for code) doing:
                # 10053 - 1000 (base_id) = 53
                # and to find x, we do 53 mod 10 (which is return remainder after division, so we get 3)
                # and to find y, we divide 53 by 10 = 5.3 (but this must be an integer, so we drop the decimal = 5)
                # clever, huh?
                new_button = wx.Button(self, id=base_id + (y * 10 + x), label='')
                # set the font of our button to the one we created with larger text
                new_button.SetFont(font)
                # bind a click event handler to the button to receive a message when it is pressed so we can take action
                new_button.Bind(wx.EVT_BUTTON, self.OnClick)
                # add the button to our list in the correct position
                self.Buttons[y * 10 + x] = new_button
                # set the corresponding mine to zero (it should already be zero but we can never be sure)
                self.Mines[y * 10 + x] = 0
                # also add the button to the grid, with the expand flag so it fills its cell completely (will adjust when window is resized)
                self.Grid.Add(new_button, flag=wx.EXPAND)
        # request the grid to update its layout of buttons
        self.Grid.Layout()
        # assign the grid sizer to the frame
        self.SetSizer(self.Grid)
        # show the frame to the user
        self.Show(True)

    # onclick event handler
    def OnClick(self, event):
        # get the button id we set
        button_id = event.GetEventObject().GetId()
        # do the clever maths we described before (line 27)
        x, y = int((button_id - base_id) % 10), int((button_id - base_id) / 10)
        # declare that we will be using the global variables, first_click and frame (declared below)
        global first_click, frame
        if first_click:
            # the number of mines in the field
            no_mines = 20
            # could've used for loop here, but this is nicer :P
            while no_mines > 0:
                # create random x,y coordinate for the mine
                rx, ry = random.randint(0, 9), random.randint(0, 9)
                # verify it hasn't already been used and it's not the current position where the user just clicked
                if frame.Mines[ry * 10 + rx] == 0 and rx != x and ry != y:
                    # -1 means armed (but this can be any number)
                    frame.Mines[ry * 10 + rx] = -1
                    # decrement mine count as we placed one out of the 20 (or how ever many we need to)
                    no_mines -= 1
            # the click is no longer the first one
            first_click = False
        # get the current button object from the list (makes it easier to adjust its properties)
        current_button = frame.Buttons[y * 10 + x]
        # disable the button (prevents it being clicked again, also it will become greyed out)
        current_button.Enable(enable=False)
        # check if it's a mine, if it is, the user has lost
        if frame.Mines[y * 10 + x] == -1:
            # loop through each element in the minefield and label each corresponding button as a mine with an 'X'
            for ix in range(10):
                for iy in range(10):
                    if frame.Mines[iy * 10 + ix] == -1:
                        frame.Buttons[iy * 10 + ix].SetLabel('X')
            # tell the user they've lost the game
            wx.MessageBox(message="You have landed on a mine!", caption="You lost!", style=wx.ICON_EXCLAMATION)
            # reset the game
            first_click = True
            # loop through each element in the minefield, resetting all the mines and corresponding buttons
            for ix in range(10):
                for iy in range(10):
                    frame.Mines[iy * 10 + ix] = 0
                    frame.Buttons[iy * 10 + ix].SetLabel('')
                    frame.Buttons[iy * 10 + ix].Enable(enable=True)
        else: # the user has not lost yet, display mine count around the button they've pressed
            near_mine_count = 0
            # check the surrounding buttons to see if they're mines
            # this works like this, where (0, 0) is the current button they've clicked (won't be checked of course):
            # [-1,-1] [0,-1] [1,-1]
            # [-1, 0] [0, 0] [1, 0]
            # [-1, 1] [0, 1] [1, 1]
            for i in range(-1, 2):
                for j in range(-1, 2):
                    # also check if outside of boundaries, if not then proceed to the actual check
                    if 0 <= x + i < 10 and 0 <= y + j < 10:
                        if frame.Mines[(y + j) * 10 + (x + i)] == -1:
                            near_mine_count += 1 
            # if there are no mines them show a smiley on the button
            if near_mine_count == 0:
                current_button.SetLabel(":)")
            # otherwise display the number of mines in proximity
            else:
                current_button.SetLabel(str(near_mine_count))
                
# create an instance of a wxWidgets application
app = wx.App(False)
# create a main window with the title given
frame = MainFrame(None, "wxMines 1.0 Python Rewrite")
# execute the application message loop that will run indefinitely until the user exits the program or we choose to as a result of an event
app.MainLoop()
