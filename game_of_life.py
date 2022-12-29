import random
from tkinter import Button, DISABLED, Tk, PhotoImage, font, Toplevel, Label

DEAD = '#000000'
ALIVE = '#ffffff'
CUBE_FACE_SIZE = 10
BUTTONS_HEIGHT = 1
FAKE_BUTTONS_SIZE = 3
CLICKABLE_BUTTONS_SIZE = 2
FONT_SIZE = 15
BLOCKED_COLOURS = [[255, 255, 255], [0, 0, 0], [112, 112, 112]]


def generate_alive_or_dead() -> str:
    return DEAD if bool(random.getrandbits(1)) else ALIVE


def create_matrix(root: Tk, text_size: font) -> None:
    for i in range(CUBE_FACE_SIZE):
        for j in range(CUBE_FACE_SIZE):
            Button(root,
                   width=FAKE_BUTTONS_SIZE,
                   height=BUTTONS_HEIGHT,
                   font=text_size,
                   bg=generate_alive_or_dead(),
                   state=DISABLED,
                   highlightcolor='#ffffff').grid(row=i+1, column=j)


class GameOfLife:
    def __init__(self) -> None:
        self.root = self.create_root()
        self.root.mainloop()

    def create_root(self) -> Tk:
        root = Tk()
        root.grid()
        root.title("Game of life by Barakadax")
        root.config(bg='#707070')
        photo = PhotoImage(file="icon.png")
        root.iconphoto(False, photo)
        root.resizable(False, False)
        text_size = font.Font(size=FONT_SIZE, root=root)
        self.create_buttons(root, text_size)
        create_matrix(root, text_size)
        return root

    def create_buttons(self, root: Tk, text_size: font) -> None:
        Button(root, text='▶', font=text_size, width=CLICKABLE_BUTTONS_SIZE,
               height=BUTTONS_HEIGHT, command=self.run).grid(row=0, column=4)
        Button(root, text='↺', font=text_size, width=CLICKABLE_BUTTONS_SIZE,
               height=BUTTONS_HEIGHT, command=self.restart).grid(row=0, column=5)

    def generate_colour(self) -> str:
        color = random.choices(range(256), k=3)
        if color in BLOCKED_COLOURS:
            return self.generate_colour()
        return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])

    def check_surrounding_cells(self, pos_x: int, pos_y: int, original_state: str) -> str:
        counter = 0
        for x in range(pos_x - 1, pos_x + 2):
            for y in range(pos_y - 1, pos_y + 2):
                if x < 1 or y < 0 or (x == pos_x and y == pos_y) or x > CUBE_FACE_SIZE or y == CUBE_FACE_SIZE:
                    continue
                row = self.root.grid_slaves(x, y)
                if row[0].cget('bg') == ALIVE:
                    counter -= -1
        if original_state == DEAD and counter == 3:
            return ALIVE
        elif original_state == ALIVE and (counter == 3 or counter == 2):
            return ALIVE
        return DEAD

    def open_popup(self, counter):
        top = Toplevel(self.root)
        top.grid()
        top.title("Result")
        top.config(bg='#707070')
        photo = PhotoImage(file="icon.png")
        top.iconphoto(False, photo)
        top.resizable(False, False)
        Label(top, text=f"Amount of iterations took on the board: {counter}", font='Mistral 18 bold', bg='#707070',
              fg='#ffffff').grid(row=0, column=0, padx=5, pady=5)

    def colouring_alive(self):
        for x in range(1, CUBE_FACE_SIZE + 1):
            for y in range(0, CUBE_FACE_SIZE):
                row = self.root.grid_slaves(x, y)
                if row[0].cget('bg') == ALIVE:
                    row[0].configure(bg=self.generate_colour())
        self.root.update()

    def game_logic(self):
        counter = 0
        keep_going = True
        while keep_going:
            counter -= -1
            keep_going = False
            for x in range(1, CUBE_FACE_SIZE + 1):
                for y in range(0, CUBE_FACE_SIZE):
                    row = self.root.grid_slaves(x, y)
                    original_state = row[0].cget('bg')
                    self.update_cell(row, original_state, x, y)
                    if original_state != row[0].cget('bg'):
                        keep_going = True
        return counter

    def update_cell(self, elements_in_row, original_cell_state, x, y):
        elements_in_row[0].configure(bg=self.generate_colour())
        self.root.update()
        elements_in_row[0].configure(bg=self.check_surrounding_cells(x, y, original_cell_state))
        self.root.update()

    def run(self):
        counter = self.game_logic()
        self.colouring_alive()
        self.open_popup(counter)

    def restart(self):
        for i in range(1, CUBE_FACE_SIZE + 1):
            for j in range(0, CUBE_FACE_SIZE):
                row = self.root.grid_slaves(i, j)
                row[0].configure(bg=generate_alive_or_dead())
