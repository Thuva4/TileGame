import tkinter as tk
import random
from tkinter import messagebox
import time
from src.gui.Tile import Tile


class MemoryTile:
    def __init__(self, parent):
        self.parent = parent
        self.first = None
        self.timer_value = 60
        self.score = 0
        self.tilesCount = 0
        self.game_level = 1
        self.tile_frame = tk.Frame(root, width=100, height=50, pady=3, padx=20)
        self.known_frame = tk.Frame(root,  width=100, height=50, pady=3, padx=20)
        self.timer_label = tk.Label(self.known_frame, text=str(self.timer_value), height=1, width=20)
        self.tile_frame.grid(row=3, sticky="ew")
        self.known_frame.grid(row=0, sticky="ew")
        self.btm_frame = tk.Frame(root, width=400, height=45)
        self.btm_frame.grid(row=8, column=0)
        self.buttons = [[tk.Button(self.tile_frame,
                                   width=8,
                                   height=4,
                                   command=lambda row=row, column=column: self.choose_tile(row, column)
                                   ) for column in range(4)] for row in range(3)]

        self.known_label = tk.Label(self.known_frame, text="", height=2, width=13)
        self.score_label = tk.Label(self.known_frame, text=str(0), height=2, width=13)
        self.start_button = tk.Button(self.btm_frame, text="Start", width=8, height=2, command=self.start_game)
        self.close_button = tk.Button(self.btm_frame, text="Quit", width=8, height=2, command=root.destroy)
        self.level_up = False
        for row in range(1, 4):
            for column in range(0, 4):
                self.buttons[row - 1][column].grid(row=row, column=column)
        self.draw_board()

    def update_score(self):
        self.score_label.config(text=self.score)

    def draw_board(self):
        self.known_label.grid(row=0, column=0)
        self.timer_label.grid(row=0, column=7)
        self.score_label.grid(row=0, column=4)
        self.start_button.grid(row=9, column=2)
        self.close_button.grid(row=9, column=4)
        self.start_button.configure(state=tk.NORMAL)
        for row in self.buttons:
            for button in row:
                button.config(text='', state=tk.DISABLED)

    def restart_game(self):
        self.timer_label.after_cancel(self.timer_event)
        self.start_game()

    def start_game(self):
        self.reset_game()
        self.update_clock()
        if not self.level_up or self.game_level==2:
            self.answer_text = list('AAAABBBBCCCC')
            random.shuffle(self.answer_text)
            self.answer = [[Tile(self.answer_text[row * 4 + column], row, column) for column in range(4)] for row in
                            range(3)]
        if self.game_level == 1:
            for row in self.buttons:
                for button in row:
                    button.config(text='', state=tk.NORMAL)
            self.start_time = time.monotonic()
            self.start_button.configure(text='Restart', command=self.restart_game)
        else:
            for row_index, row in enumerate(self.buttons):
                for column_index, button in enumerate(row):
                    button.config(text=self.answer_text[row_index * 4 + column_index], state=tk.DISABLED)
            self.start_time = time.monotonic()
            self.start_button.configure(text='Restart')

    def choose_tile(self, row, column):
        self.buttons[row][column].config(text=self.answer[row][column].get_text())
        self.buttons[row][column].config(state=tk.DISABLED)
        if not self.first:
            self.first = (row, column)
            for known_tiles in self.answer:
                for known_tile in known_tiles:
                    if known_tile.get_known() and not known_tile.get_matched():
                        if not (
                                known_tile.get_row() == row and known_tile.get_column() == column) and known_tile.get_text() == \
                                self.answer[row][column].get_text():
                            self.known_label.config(text='Match known')
            self.answer[row][column].set_known()

        else:
            a, b = self.first
            if self.answer[row][column].get_text() == self.answer[a][b].get_text():
                self.score += self.answer[row][column].calculate_score()
                self.score += self.answer[a][b].calculate_score()
                self.answer[a][b].set_text('')
                self.known_label.config(text='')
                self.tilesCount += 2
                if self.tilesCount == 12:
                    duration = time.monotonic() - self.start_time
                    self.timer_label.after_cancel(self.timer_event)
                    if self.game_level < 2 and not self.level_up:
                        if messagebox.askyesno(title='Success!',
                                               message='You win! Time: {:.1f} Score:{}, Do you want to play Next Level'.format(
                                                   duration, self.score)):
                            self.game_level = 2
                            self.level_up = True
                            self.start_game()
                    else:
                        messagebox.showinfo(title='Success!', message='You win! Time: {:.1f} Score:{}, Do you want to '
                                                                      'play Next Level. You  have successfully '
                                                                      'completed all levels'.format(duration,
                                                                                                    self.score))
                        self.parent.after(1000, self.draw_board)
            else:
                self.known_label.config(text='')
                self.answer[row][column].increase_seen()
                self.answer[a][b].increase_seen()
                self.parent.after(1000, self.hide_tiles, row, column, a, b)
                self.answer[row][column].set_known()
            self.first = None
            self.score += (self.answer[row][column].calculate_penalty() + self.answer[a][b].calculate_penalty())
        self.update_score()

    def hide_tiles(self, x1, y1, x2, y2):
        self.buttons[x1][y1].config(text='', state=tk.NORMAL)
        self.buttons[x2][y2].config(text='', state=tk.NORMAL)

    def update_clock(self):
        if (self.timer_value > 0):
            self.timer_value -= 1
            self.timer_label.configure(text=str(self.timer_value))
            self.timer_event = self.timer_label.after(1000, self.update_clock)
        else:
            if self.game_level == 1:
                messagebox.showinfo(title='Failed!',
                                    message='You Lose!')
                self.parent.after(0, self.draw_board)
                self.timer_label.after_cancel(self.timer_event)
            else:
                self.game_level = 1
                self.parent.after(0, self.start_game())
                self.timer_label.after_cancel(self.timer_event)

    def reset_game(self):
        self.score = 0
        self.tilesCount = 0
        self.timer_value = 60
        self.update_score()


root = tk.Tk()
memory_tile = MemoryTile(root)
root.mainloop()
