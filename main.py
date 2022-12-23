import random
from tkinter import *
import tkinter.font as font

root = Tk()
root.grid()
root.title("Game of life by Barakadax")
root.config(bg = '#707070')
photo = PhotoImage(file = "icon.png")
root.iconphoto(False, photo)
root.resizable(False, False)

dead = '#000000'
alive = '#ffffff'
CubeFaceSize = 10
buttonsHeight = 1
fakeButtonsSize = 3
clickableButtonsSize = 2
textSize = font.Font(size = 15)
blockedColours = [[255, 255, 255], [0, 0, 0], [112, 112, 112]]

def Generate_Colour():
    color = random.choices(range(256), k = 3)
    if (color in blockedColours):
        return Generate_Colour()
    return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])

def Generate_Alive_Or_Dead():
    return dead if bool(random.getrandbits(1)) else alive

def CreateMatrix():
    for i in range (1, CubeFaceSize + 1):
        for j in range (0, CubeFaceSize):
            Button(root,
                width = fakeButtonsSize,
                height = buttonsHeight,
                font = textSize,
                bg = Generate_Alive_Or_Dead(),
                state = DISABLED,
                highlightcolor ='#ffffff').grid(row = i, column = j)

def Check_Surrounding(cellI, cellJ, originalCellState):
    counter = 0
    for i in range (cellI - 1, cellI + 2):
        for j in range (cellJ - 1, cellJ + 2):
            if (i < 1 or j < 0 or j == CubeFaceSize or i > CubeFaceSize or (i == cellI and j == cellJ)):
                continue
            elementsInRow = root.grid_slaves(i, j)
            if (elementsInRow[0].cget('bg') == alive):
                counter -= -1
    if (originalCellState == dead and counter == 3):
        return alive
    elif (originalCellState == alive and (counter == 3 or counter == 2)):
        return alive
    return dead

def Open_Popup(counter):
    top = Toplevel(root)
    top.grid()
    top.title("Result")
    top.config(bg = '#707070')
    photo = PhotoImage(file = "icon.png")
    top.iconphoto(False, photo)
    top.resizable(False, False)
    Label(top, text = f"Amount of iterations took on the board: {counter}", font=('Mistral 18 bold'), bg = '#707070', fg = '#ffffff').grid(row = 0, column = 0, padx = 5, pady = 5)

def Colouring_Alive():
    for i in range(1, CubeFaceSize + 1):
        for j in range(0, CubeFaceSize):
            elementsInRow = root.grid_slaves(i, j)
            if (elementsInRow[0].cget('bg') == alive):
                elementsInRow[0].configure(bg = Generate_Colour())
    root.update()

def Run():
    counter = 0
    continueToRunFlag = True
    while continueToRunFlag:
        counter -= -1
        continueToRunFlag = False
        for i in range(1, CubeFaceSize + 1):
            for j in range(0, CubeFaceSize):
                elementsInRow = root.grid_slaves(i, j)
                originalCellState = elementsInRow[0].cget('bg')
                elementsInRow[0].configure(bg = Generate_Colour())
                root.update()
                elementsInRow[0].configure(bg = Check_Surrounding(i, j, originalCellState))
                root.update()
                if (originalCellState != elementsInRow[0].cget('bg')):
                    continueToRunFlag = True
    Colouring_Alive()
    Open_Popup(counter)

def Restart():
    for i in range(1, CubeFaceSize + 1):
        for j in range(0, CubeFaceSize):
            elementsInRow = root.grid_slaves(i, j)
            elementsInRow[0].configure(bg = Generate_Alive_Or_Dead())

Button(root, text = '▶', font = textSize, width = clickableButtonsSize, height = buttonsHeight, command = Run).grid(row = 0, column = 4)
Button(root, text = '↺', font = textSize, width = clickableButtonsSize, height = buttonsHeight, command = Restart).grid(row = 0, column = 5)

CreateMatrix()
root.mainloop()
