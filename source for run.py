import sys
import ctypes
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt, QTimer

WINDOW_WIDTH = 200
WINDOW_HEIGHT = 200
IDLE_IMAGE = "idle.png"
CLICK_IMAGE = "click.png"

app = QApplication(sys.argv)

user32 = ctypes.windll.user32
VK_LBUTTON = 0x01
VK_RBUTTON = 0x02

class CursorFollower(QLabel):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(Qt.BlankCursor)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.setWindowTitle("Lucario on cursor")

        self.idle_pixmap = QPixmap(IDLE_IMAGE).scaled(
            WINDOW_WIDTH, WINDOW_HEIGHT,
            Qt.KeepAspectRatio, Qt.FastTransformation
        )
        self.click_pixmap = QPixmap(CLICK_IMAGE).scaled(
            WINDOW_WIDTH, WINDOW_HEIGHT,
            Qt.KeepAspectRatio, Qt.FastTransformation
        )

        self.setPixmap(self.idle_pixmap)
        self.show()

        self.frame_count = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_all)
        self.timer.start(5)
        
        try:
            hwnd = int(self.winId())
            WS_EX_LAYERED = 0x80000
            WS_EX_TRANSPARENT = 0x20
            GWL_EXSTYLE = -20
            style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            user32.SetWindowLongW(
                hwnd,
                GWL_EXSTYLE,
                style | WS_EX_LAYERED | WS_EX_TRANSPARENT
            )
        except Exception:
            pass

    def update_all(self):
        self.frame_count += 1
        
        pos = QCursor.pos()
        self.move(
            pos.x() - WINDOW_WIDTH // 2,
            pos.y() - WINDOW_HEIGHT // 2
        )
        
        if self.is_mouse_pressed():
            self.setPixmap(self.click_pixmap)
        else:
            self.setPixmap(self.idle_pixmap)
        if self.is_cursor_visible():
            self.show()
        else:
            self.hide()
        if self.frame_count % 5 == 0:
            self.raise_()

    @staticmethod
    def is_mouse_pressed():
        return (
            user32.GetAsyncKeyState(VK_LBUTTON) & 0x8000 or
            user32.GetAsyncKeyState(VK_RBUTTON) & 0x8000
        )
        
    @staticmethod
    def is_cursor_visible():
        class CURSORINFO(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.c_uint),
                ("flags", ctypes.c_uint),
                ("hCursor", ctypes.c_void_p),
                ("ptScreenPos", ctypes.c_long * 2)
            ]

        ci = CURSORINFO()
        ci.cbSize = ctypes.sizeof(CURSORINFO)
        ctypes.windll.user32.GetCursorInfo(ctypes.byref(ci))
        return bool(ci.flags & 1)

follower = CursorFollower()
sys.exit(app.exec_())
