import random

import wx

first_click = True
base_id = 10000

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800, 600))
        self.SetBackgroundColour((255, 255, 255))
        self.Grid = wx.GridSizer(10, 10, 0, 0)
        self.Buttons = [wx.Button] * 100
        self.Mines = [int] * 100
        font = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)
        for x in range(10):
            for y in range(10):
                new_button = wx.Button(self, id=base_id + (y * 10 + x), label='')
                new_button.SetFont(font)
                new_button.Bind(wx.EVT_BUTTON, self.OnClick)
                self.Buttons[y * 10 + x] = new_button
                self.Mines[y * 10 + x] = 0
                self.Grid.Add(new_button, flag=wx.EXPAND)
        self.Grid.Layout()
        self.SetSizer(self.Grid)
        self.Show(True)

    def OnClick(self, event):
        button_id = event.GetEventObject().GetId()
        x, y = int((button_id - base_id) % 10), int((button_id - base_id) / 10)
        global first_click, frame
        if first_click:
            no_mines = 20
            while no_mines > 0:
                rx, ry = random.randint(0, 9), random.randint(0, 9)
                if frame.Mines[ry * 10 + rx] == 0 and rx != x and ry != y:
                    frame.Mines[ry * 10 + rx] = -1
                    no_mines -= 1
            first_click = False
        current_button = frame.Buttons[y * 10 + x]
        current_button.Enable(enable=False)

        if frame.Mines[y * 10 + x] == -1:
            for ix in range(10):
                for iy in range(10):
                    if frame.Mines[iy * 10 + ix] == -1:
                        frame.Buttons[iy * 10 + ix].SetLabel('X')
            wx.MessageBox(message="You have landed on a mine!", caption="You lost!", style=wx.ICON_EXCLAMATION)
            first_click = True
            for ix in range(10):
                for iy in range(10):
                    frame.Mines[iy * 10 + ix] = 0
                    frame.Buttons[iy * 10 + ix].SetLabel('')
                    frame.Buttons[iy * 10 + ix].Enable(enable=True)
        else:
            near_mine_count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= x + i < 10 and 0 <= y + j < 10:
                        if frame.Mines[(y + j) * 10 + (x + i)] == -1:
                            near_mine_count += 1
            if near_mine_count == 0:
                current_button.SetLabel(":)")
            else:
                current_button.SetLabel(str(near_mine_count))
                
app = wx.App(False)
frame = MainFrame(None, "wxMines 1.0 Python Rewrite")
app.MainLoop()