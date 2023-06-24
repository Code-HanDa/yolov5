from win32gui import *
import ctypes, win32process, win32api, pygame
# python窗口绘制，文字绘制，绘制矩形，yolo绘制方框，自瞄，绘制源码
version = "1.0.0"
STANDARD_RIGHTS_REQUIRED = 0x000F0000
SYNCHRONIZE = 0x00100000
TH32CS_SNAPMODULE = 0x00000008


class PROCESS_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ('ExitStatus', ctypes.c_ulonglong),
        ('PebBaseAddress', ctypes.c_ulonglong),
        ('AffinityMask', ctypes.c_ulonglong),
        ('BasePriority', ctypes.c_ulonglong),
        ('UniqueProcessId', ctypes.c_ulonglong),
        ('InheritedFromUniqueProcessId', ctypes.c_ulonglong)]


class MODULEENTRY32(ctypes.Structure):
    _fields_ = [
        ('dwSize', ctypes.c_long),
        ('th32ModuleID', ctypes.c_long),
        ('th32ProcessID', ctypes.c_long),
        ('GlblcntUsage', ctypes.c_long),
        ('ProccntUsage', ctypes.c_long),
        ('modBaseAddr', ctypes.c_long),
        ('modBaseSize', ctypes.c_long),
        ('hModule', ctypes.c_void_p),
        ('szModule', ctypes.c_char * 256),
        ('szExePath', ctypes.c_char * 260)]


kernel32 = ctypes.windll.LoadLibrary("kernel32.dll")
user32 = ctypes.windll.LoadLibrary("user32.dll")

GetLastError = kernel32.GetLastError
GetLastError.rettype = ctypes.c_long
GetLastError = ctypes.windll.kernel32.GetLastError

Module32First = ctypes.windll.kernel32.Module32First
Module32First.argtypes = [ctypes.c_void_p, ctypes.POINTER(MODULEENTRY32)]
Module32First.rettype = ctypes.c_int

Module32Next = ctypes.windll.kernel32.Module32Next
Module32Next.argtypes = [ctypes.c_void_p, ctypes.POINTER(MODULEENTRY32)]
Module32Next.rettype = ctypes.c_int

CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
PROCESS_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFF)


def FindWindowPid(ClassName, WindowName):
    hWindow = FindWindow(ClassName, WindowName)
    return win32process.GetWindowThreadProcessId(hWindow)[1]


def MessageBoxTimeoutA(hwnd, title, cont, dwtimeout, state):
    return user32.MessageBoxTimeoutA(hwnd, cont, title, state, 0, dwtimeout)


def GetMousePos(hwnd):
    return user32.SetCapture(hwnd)


def MonitorHotkeys(hotkey):
    return user32.GetAsyncKeyState(hotkey)


def GetWindRect(hwnd):
    left, top, right, bottom = GetWindowRect(hwnd)
    Width = right - left
    Height = bottom - top
    return (Width, Height)


class SetupProcess():
    def __init__(self, pid):
        self.ntdll = ctypes.WinDLL("ntdll.dll")
        self.hProcess = win32api.OpenProcess(PROCESS_ALL_ACCESS, 0, pid)

    # ReadMemory62 Method -------------------------------------------------------------------------------

    def ReadMemory64(self, addr, n=4):
        addr = ctypes.c_ulonglong(addr)
        retn = ctypes.c_ulonglong()
        BufferLength = ctypes.c_ulonglong(n)
        self.ntdll.NtWow64ReadVirtualMemory64(int(self.hProcess), addr, ctypes.byref(retn), BufferLength, 0)
        return retn.value

    def ReadMemory64_float(self, addr, n=4):
        addr = ctypes.c_ulonglong(addr)
        retn = ctypes.c_float()
        BufferLength = ctypes.c_ulonglong(n)
        self.ntdll.NtWow64ReadVirtualMemory64(int(self.hProcess), addr, ctypes.byref(retn), BufferLength, 0)
        return retn.value

    def ReadMemory64_double(self, addr, n=8):
        addr = ctypes.c_ulonglong(addr)
        retn = ctypes.c_double()
        BufferLength = ctypes.c_ulonglong(n)
        self.ntdll.NtWow64ReadVirtualMemory64(int(self.hProcess), addr, ctypes.byref(retn), BufferLength, 0)
        return retn.value

    def ReadMemory64_byte(self, addr, n=8):
        addr = ctypes.c_int(addr)
        retn = ctypes.c_byte()
        BufferLength = ctypes.c_int(n)
        self.ntdll.NtWow64ReadVirtualMemory64(int(self.hProcess), addr, ctypes.byref(retn), BufferLength, 0)
        return retn.value

    def ReadMemory64_Wchar(self, addr, n, length):
        addr = ctypes.c_ulonglong(addr)
        retn = ctypes.c_wchar_p("0" * length)
        BufferLength = ctypes.c_ulonglong(n)
        self.ntdll.NtWow64ReadVirtualMemory64(int(self.hProcess), addr, retn, BufferLength, 0)
        return retn.value

    # WriteMemory62 Method -------------------------------------------------------------------------------

    def WriteMemory64(self, addr, s, n=4):
        addr = ctypes.c_ulonglong(addr)
        retn = ctypes.c_ulonglong(s)
        BufferLength = ctypes.c_ulonglong(n)
        self.ntdll.NtWow64WriteVirtualMemory64(int(self.hProcess), addr, ctypes.byref(retn), BufferLength, 0)

    def WriteMemory64_float(self, addr, s, n=4):
        addr = ctypes.c_ulonglong(addr)
        retn = ctypes.c_float(s)
        BufferLength = ctypes.c_ulonglong(n)
        self.ntdll.NtWow64WriteVirtualMemory64(int(self.hProcess), addr, ctypes.byref(retn), BufferLength, 0)

    def WriteMemory64_double(self, addr, s, n=8):
        addr = ctypes.c_ulonglong(addr)
        retn = ctypes.c_double(s)
        BufferLength = ctypes.c_ulonglong(n)
        self.ntdll.NtWow64WriteVirtualMemory64(int(self.hProcess), addr, ctypes.byref(retn), BufferLength, 0)

    def WriteMemory64_byte(self, addr, s, n=8):
        addr = ctypes.c_ulonglong(addr)
        retn = ctypes.c_byte(s)
        BufferLength = ctypes.c_ulonglong(n)
        self.ntdll.NtWow64WriteVirtualMemory64(int(self.hProcess), addr, ctypes.byref(retn), BufferLength, 0)

    def GetBaseAddr64(self, ModuleName):
        NumberOfBytesRead = ctypes.c_ulong()
        Buffer = PROCESS_BASIC_INFORMATION()
        Size = ctypes.c_ulong(48)
        name_len = len(ModuleName)
        self.ntdll.NtWow64QueryInformationProcess64(int(self.hProcess), 0, ctypes.byref(Buffer), Size,
                                                    ctypes.byref(NumberOfBytesRead))
        ret = self.ReadMemory64(Buffer.PebBaseAddress + 24, 8)
        ret = self.ReadMemory64(ret + 24, 8)
        for i in range(100000):
            modulehandle = self.ReadMemory64(ret + 48, 8)
            if modulehandle == 0:
                break
            nameaddr = self.ReadMemory64(ret + 96, 8)
            name = self.ReadMemory64_Wchar(nameaddr, name_len * 2 + 1, name_len)
            if name == ModuleName:
                return modulehandle
            ret = self.ReadMemory64(ret + 8, 8)

    # ReadMemory32 Method -------------------------------------------------------------------------------

    def ReadMemory32(self, addr, n=4):
        addr = ctypes.c_int32(addr)
        retn = ctypes.c_int()
        BufferLength = ctypes.c_int32(n)
        kernel32.ReadProcessMemory(int(self.hProcess), addr, ctypes.byref(retn), BufferLength, 0)
        return retn.value

    def ReadMemory32_float(self, addr, n=4):
        addr = ctypes.c_int(addr)
        retn = ctypes.c_float()
        BufferLength = ctypes.c_int(n)
        kernel32.ReadProcessMemory(int(self.hProcess), addr, ctypes.byref(retn), BufferLength, 0)
        return retn.value

    def ReadMemory32_double(self, addr, n=8):
        addr = ctypes.c_int(addr)
        retn = ctypes.c_double()
        BufferLength = ctypes.c_int(n)
        kernel32.ReadProcessMemory(int(self.hProcess), addr, ctypes.byref(retn), BufferLength, 0)
        return retn.value

    def ReadMemory32_byte(self, addr, n=8):
        addr = ctypes.c_int(addr)
        retn = ctypes.c_byte()
        BufferLength = ctypes.c_int(n)
        kernel32.ReadProcessMemory(int(self.hProcess), addr, ctypes.byref(retn), BufferLength, 0)
        return retn.value

    # WriteMemory32 Method -------------------------------------------------------------------------------

    def WriteMemory32(self, addr, s, n=4):
        addr = ctypes.c_int(addr)
        retn = ctypes.c_int(s)
        BufferLength = ctypes.c_int(n)
        kernel32.WriteProcessMemory(int(self.hProcess), addr, ctypes.byref(retn), BufferLength, 0)

    def WriteMemory32_float(self, addr, s, n=4):
        addr = ctypes.c_int(addr)
        retn = ctypes.c_float(s)
        BufferLength = ctypes.c_int(n)
        kernel32.WriteProcessMemory(int(self.hProcess), addr, ctypes.byref(retn), BufferLength, 0)

    def WriteMemory32_double(self, addr, s, n=8):
        addr = ctypes.c_int(addr)
        retn = ctypes.c_double(s)
        BufferLength = ctypes.c_int(n)
        kernel32.WriteProcessMemory(int(self.hProcess), addr, ctypes.byref(retn), BufferLength, 0)

    def WriteMemory32_byte(self, addr, s, n=8):
        addr = ctypes.c_int(addr)
        retn = ctypes.c_byte(s)
        BufferLength = ctypes.c_int(n)
        kernel32.WriteProcessMemory(int(self.hProcess), addr, ctypes.byref(retn), BufferLength, 0)

    def GetModlueAddr32(self, ProcessId, moduleName):
        me32 = MODULEENTRY32()
        me32.dwSize = ctypes.sizeof(MODULEENTRY32)
        hModuleSnap = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, ProcessId)
        if GetLastError() != 0:
            print("hModuleSnap: %d" % hModuleSnap)
            print('Handle Error %s' % GetLastError())
            win32api.CloseHandle(hModuleSnap)
            return 'Not Find Modlue.'
        else:
            if Module32First(hModuleSnap, ctypes.pointer(me32)):
                if me32.szModule.decode() == moduleName:
                    win32api.CloseHandle(hModuleSnap)
                    return me32.modBaseAddr
                else:

                    Module32Next(hModuleSnap, ctypes.pointer(me32))
                    while int(GetLastError()) != 18:
                        if me32.szModule.decode() == moduleName:
                            win32api.CloseHandle(hModuleSnap)
                            return me32.modBaseAddr
                        else:
                            Module32Next(hModuleSnap, ctypes.pointer(me32))
                    win32api.CloseHandle(hModuleSnap)
                    print('Couldn\'t find Process with name %s' % moduleName)
            else:
                print('Module32 First is False %s' % GetLastError())
                win32api.CloseHandle(hModuleSnap)


class FindWinDraw():
    def __init__(self, ClassName, WindowName):
        self.hwndsr = FindWindow(ClassName, WindowName)
        # hwnd = FindWindow(None, 'C:/Windows/system32/cmd.exe')
        self.LONGARG = (-20, 524288)

    def SetupExGui(self):
        pygame.init()
        left, top, right, bottom = GetWindowRect(self.hwndsr)
        Width = right - left
        Height = bottom - top
        self.screen = pygame.display.set_mode([Width, Height], pygame.NOFRAME)
        self.hwnd = FindWindow("pygame", None)
        SetWindowPos(self.hwnd, -1, left, top, Width, Height, 1)
        SetWindowLong(self.hwnd, self.LONGARG[0], self.LONGARG[1])
        SetLayeredWindowAttributes(self.hwnd, 0, 0, 1)

    def SetupExGui_1(self, left, top, Width, Height):
        pygame.init()
        # left, top, right, bottom = GetWindowRect(self.hwndsr)
        # Width = right - left
        # Height = bottom - top
        self.screen = pygame.display.set_mode([Width, Height], pygame.NOFRAME)
        self.hwnd = FindWindow("pygame", None)
        SetWindowPos(self.hwnd, -1, left, top, Width, Height, 1)
        SetWindowLong(self.hwnd, self.LONGARG[0], self.LONGARG[1])
        SetLayeredWindowAttributes(self.hwnd, 0, 0, 1)

    def DrawText(self, text, size, x, y, color):
        textr = pygame.font.SysFont("simhei", size)
        text_fmt = textr.render(text, 1, color)
        self.screen.blit(text_fmt, (x, y))

    def DrawRect(self, x, y, width, height, c, color):
        pygame.draw.rect(self.screen, color, (x, y, width, height), c)

    def DrawLine(self, startX, startY, endX, endY, width, color):
        pygame.draw.line(self.screen, color, (startX, startY), (endX, endY), width)

    def DrawCircle(self, x, y, c, color):
        pygame.draw.circle(self.screen, color, (x, y), c)

    def StartLoop(self):
        self.screen.fill((0, 0, 0))

    def EndLoop(self):
        for _ in pygame.event.get():
            pass
        left, top, right, bottom = GetWindowRect(self.hwndsr)
        Width = right - left
        Height = bottom - top
        SetWindowPos(self.hwnd, -1, left, top, Width, Height, 1)
        pygame.display.flip()

# The End -------------------------------------------------------------------------------