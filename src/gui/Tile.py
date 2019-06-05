import tkinter as tk


class Tile():
    def __init__(self, text, row, column):
        self.score = 20
        self.seen = 0
        self.row = row
        self.column = column
        self.text = text
        self.known = False
        self.matched = False

    def calculate_score(self):
        return self.score

    def get_text(self):
        return self.text

    def increase_seen(self):
        self.seen += 1

    def set_text(self, text):
        self.text = text

    def get_row(self):
        return self.row

    def get_column(self):
        return self.column

    def get_known(self):
        return self.known

    def set_known(self):
        self.known = not self.known

    def get_matched(self):
        return self.matched

    def set_matched(self):
        self.matched = True

    def calculate_penalty(self):
        penalty = -5 * self.seen
        return penalty
