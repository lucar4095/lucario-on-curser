import ctypes

user32 = ctypes.windll.user32

WINDOW_TITLE = "lucario on curser window"
WM_CLOSE = 0x0010

hwnd = user32.FindWindowW(None, WINDOW_TITLE)

if hwnd:
    user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)