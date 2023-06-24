import win32gui
from Demos.print_desktop import hwnd
from win32api import GetSystemMetrics

m=win32gui.GetCursorPos()
dc = win32gui.GetDC(0)

while True:
    n=win32gui.GetCursorPos()
    win32gui.InvalidateRect(hwnd, (m[0], m[1], GetSystemMetrics(0), GetSystemMetrics(1)), True)
    back=[]
    for i in range((n[0]-m[0])//4):
        win32gui.SetPixel(dc, m[0]+4*i, m[1], 0)
        win32gui.SetPixel(dc, m[0]+4*i, n[1], 0)
    for i in range((n[1]-m[1])//4):
        win32gui.SetPixel(dc, m[0], m[1]+4*i, 0)
        win32gui.SetPixel(dc, n[0], m[1]+4*i, 0)