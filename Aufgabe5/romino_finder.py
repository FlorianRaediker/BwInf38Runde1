import sys
import os
from typing import Tuple

try:
    from tqdm import tqdm
except ModuleNotFoundError:
    tqdm = lambda x: x

try:
    from aufgabe5 import Romino
except ModuleNotFoundError:
    from Aufgabe5.aufgabe5_2 import Romino

import numpy as np

from PySide2.QtWidgets import QWidget, QApplication, QMessageBox
from PySide2.QtGui import QMouseEvent, QKeyEvent, QPaintEvent, QPainter, QColor, QBrush, QIcon
from PySide2.QtCore import Qt


def trim_zeros_2D(array, axis):
    """
    Thanks to Eddmik: https://stackoverflow.com/a/50699907
    """
    mask = ~(array == 0).all(axis=axis)
    inv_mask = mask[::-1]
    start_idx = np.argmax(mask == True)
    end_idx = len(inv_mask) - np.argmax(inv_mask == True)
    if axis:
        return array[start_idx:end_idx,:]
    else:
        return array[:, start_idx:end_idx]


class RominoCreationWidget(QWidget):
    def __init__(self, parent=None, grid_size=(1, 1), cell_size=10, cell_padding=5, new_romino_callback=lambda w, a: None):
        super().__init__(parent)
        self._cell_size = cell_size
        self._cell_padding = cell_padding
        self.set_grid_size(grid_size)
        self._new_romino_callback = new_romino_callback
        self._color = QColor("black")
        self.setFocus()
        self.highlighted_cell = None
        self.setWindowIcon(QIcon("romino_finder.ico"))
        self.setWindowTitle("RominoFinder")

    def set_grid_size(self, size: Tuple[int, int]):
        self._grid_size = size
        self.setFixedSize(size[0] * self._cell_size, size[1] * self._cell_size)
        self._array = np.zeros(self._grid_size, dtype=np.bool_)

    def set_color(self, color):
        self._color = QColor(color)

    def mousePressEvent(self, event: QMouseEvent):
        x_pos = event.x() // self._cell_size
        y_pos = event.y() // self._cell_size
        self.highlighted_cell = None
        self.switch_square(x_pos, y_pos)

    def switch_square(self, x_pos, y_pos):
        self._array[y_pos, x_pos] = not self._array[y_pos, x_pos]
        self._new_romino_callback(self, self._array)
        self.update()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Space:
            if self.highlighted_cell is not None:
                self.switch_square(self.highlighted_cell[0], self.highlighted_cell[1])
        if self.highlighted_cell is not None:
            if event.key() == Qt.Key_Up:
                if self.highlighted_cell[1] > 0:
                    self.highlighted_cell = (self.highlighted_cell[0], self.highlighted_cell[1] - 1)
                    self.update()
            elif event.key() == Qt.Key_Down:
                if self.highlighted_cell[1] < self._array.shape[0]-1:
                    self.highlighted_cell = (self.highlighted_cell[0], self.highlighted_cell[1] + 1)
                    self.update()
            elif event.key() == Qt.Key_Left:
                if self.highlighted_cell[0] > 0:
                    self.highlighted_cell = (self.highlighted_cell[0] - 1, self.highlighted_cell[1])
                    self.update()
            elif event.key() == Qt.Key_Right:
                if self.highlighted_cell[0] < self._array.shape[1]-1:
                    self.highlighted_cell = (self.highlighted_cell[0] + 1, self.highlighted_cell[1])
                    self.update()
        else:
            if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down or event.key() == Qt.Key_Left or event.key() == Qt.Key_Right:
                self.highlighted_cell = (0, 0)
                self.update()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor(self._color)))
        painter.setPen(QColor("black"))
        # draw grid
        for x in range(1, self._grid_size[1]):
            x_pos = x*self._cell_size
            painter.drawLine(x_pos, 0, x_pos, self.height())
        for y in range(1, self._grid_size[0]):
            y_pos = y*self._cell_size
            painter.drawLine(0, y_pos, self.width(), y_pos)
        if self.highlighted_cell is not None:
            painter.save()
            painter.setBrush(QBrush(QColor("#D2FFFF")))
            painter.setPen(Qt.transparent)
            painter.drawRect(self.highlighted_cell[0] * self._cell_size + 1,
                             self.highlighted_cell[1] * self._cell_size + 1,
                             self._cell_size - 1, self._cell_size - 1)
            painter.restore()
        # draw cells
        for y in range(self._grid_size[0]):
            for x in range(self._grid_size[1]):
                if self._array[y, x]:
                    painter.drawRect(x * self._cell_size + self._cell_padding,
                                     y * self._cell_size + self._cell_padding,
                                     self._cell_size - self._cell_padding * 2,
                                     self._cell_size - self._cell_padding * 2)
        painter.end()


ROMINO_GENERATIONS = []


def on_new_romino(widget, array: np.ndarray):
    array = trim_zeros_2D(trim_zeros_2D(array, 0), 1)
    if array.shape == (1, 1) and array.all():
        # only one square
        print("one square")
        widget.set_color(QColor("black"))
        return
    r = 0
    square_count = 0
    should_break = False
    for y in range(array.shape[0]):
        for x in range(array.shape[1]):
            if array[y, x]:
                filled_squares = np.zeros(array.shape, dtype=np.bool_)
                
                def search(y, x):
                    nonlocal square_count
                    nonlocal filled_squares
                    nonlocal r
                    square_count += 1
                    filled_squares[y, x] = True
                    r |= 1 << (y * array.shape[1] + x)
                    for y_, x_ in [
                        (y - 1, x - 1), (y - 1, x), (y - 1, x + 1),
                        (y, x - 1), (y, x + 1),
                        (y + 1, x - 1), (y + 1, x), (y + 1, x + 1)
                    ]:
                        if y_ != -1 and x_ != -1 and y_ < array.shape[0] and x_ < array.shape[1] and \
                                array[y_, x_] and not filled_squares[y_, x_]:
                            search(y_, x_)
                search(y, x)
                if not np.array_equal(filled_squares, array):
                    # loop did not break, (y, x) has no neighbor squares
                    widget.set_color(QColor("red"))
                    print("invalid array", end="\n\n")
                    return
                should_break = True
                break
        if should_break:
            break
    romino = Romino.new(array.shape, r)
    print(romino)
    if romino is not None:
        try:
            generation = ROMINO_GENERATIONS[square_count-1]
        except IndexError:
            print("too much squares:", square_count, end="\n\n")
        else:
            if romino not in generation:
                print("FOUND NEW ROMINO", end="\n\n")
                QMessageBox.information(widget, "Neues Romino gefunden",
                                        "Du hast ein bisher unbekanntes Romino endeckt!")
            else:
                widget.set_color("#006400")
                print()
                return
    widget.set_color(QColor("black"))


def get_number(text):
    while True:
        try:
            return int(input(text))
        except ValueError:
            print("Bitte eine Ganzzahl eingeben")


if __name__ == "__main__":
    print(sys.path)
    os.chdir(sys.path[-1])
    max_square_count = get_number("Bitte maximale Anzahl von Quadraten eingeben, für die Rominos geprüft werden: ")
    ROMINO_GENERATIONS = [{Romino.new((1, 1), 1)}]
    for i in range(2, max_square_count+1):
        new_generation = set()
        for romino in tqdm(ROMINO_GENERATIONS[-1]):
            new_generation.update(romino.grow())
        ROMINO_GENERATIONS.append(new_generation)
        print(f"{len(new_generation)} {i}-Rominos", end="\n\n")
    app = QApplication(sys.argv)
    main = RominoCreationWidget(grid_size=(max_square_count, max_square_count), cell_size=50,
                                new_romino_callback=on_new_romino)
    main.show()
    main.activateWindow()
    main.raise_()
    app.exec_()
    sys.exit()
