import ctypes

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

WINDOW_TITLE = "lucario on cursor"

hwnd = user32.FindWindowW(None, WINDOW_TITLE)
if hwnd:
    pid = ctypes.c_ulong()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    h = kernel32.OpenProcess(1, False, pid.value)
    kernel32.TerminateProcess(h, 0)
