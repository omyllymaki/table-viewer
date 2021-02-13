import re

from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QLineEdit


class SearchField(QLineEdit):

    def __init__(self, *args, options=None):
        super().__init__(*args)
        self.options = options

    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self._handle_tab_pressed()
            return True
        else:
            return QLineEdit.event(self, event)

    def _handle_tab_pressed(self):
        cursor_position = self.cursorPosition()
        full_text = self.text()
        text_to_cursor = full_text[:cursor_position]
        words = text_to_cursor.split()
        cursor_word = words[-1]
        if cursor_word.startswith("["):
            cursor_word_cleaned = cursor_word.replace("[", "").replace("]", "")
            for candidate in self.options:
                if re.match(cursor_word_cleaned, candidate):
                    full_text_new = full_text.replace(cursor_word, "[" + candidate + "]")
                    self.setText(full_text_new)

    def set_red_background(self):
        self.setStyleSheet("QLineEdit"
                           "{"
                           "background : red;"
                           "}")

    def set_white_background(self):
        self.setStyleSheet("QLineEdit"
                           "{"
                           "background : white;"
                           "}")