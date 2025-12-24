import ctypes
from ctypes import wintypes
import threading
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CoInitialize

user32 = ctypes.WinDLL('user32', use_last_error=True)
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
VK_VOLUME_UP = 0xAF
VK_VOLUME_DOWN = 0xAE

com_initialized = False
volume_adjustment_lock = threading.Lock()

def ensure_com_initialized():
    global com_initialized
    if not com_initialized:
        CoInitialize()
        com_initialized = True

def get_spotify_volume():
    try:
        ensure_com_initialized()
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name() == "Spotify.exe":
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                return volume
    except Exception:
        pass
    return None

def adjust_spotify_volume(direction):
    with volume_adjustment_lock:
        volume = get_spotify_volume()
        if volume:
            try:
                current = volume.GetMasterVolume()
                step = 0.02
                
                if direction == "up":
                    new_volume = min(1.0, current + step)
                else:
                    new_volume = max(0.0, current - step)
                
                volume.SetMasterVolume(new_volume, None)
            except Exception:
                pass

class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", wintypes.DWORD),
        ("scanCode", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG))
    ]

def low_level_keyboard_handler(nCode, wParam, lParam):
    if nCode >= 0:
        kb = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
        
        if wParam == WM_KEYDOWN:
            if kb.vkCode == VK_VOLUME_UP:
                threading.Thread(target=adjust_spotify_volume, args=("up",), daemon=True).start()
                return 1
            elif kb.vkCode == VK_VOLUME_DOWN:
                threading.Thread(target=adjust_spotify_volume, args=("down",), daemon=True).start()
                return 1
    
    return user32.CallNextHookEx(None, nCode, wParam, lParam)

HOOKPROC = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p))
keyboard_callback = HOOKPROC(low_level_keyboard_handler)

hook = user32.SetWindowsHookExA(WH_KEYBOARD_LL, keyboard_callback, None, 0)

msg = wintypes.MSG()
while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
    user32.TranslateMessage(ctypes.byref(msg))
    user32.DispatchMessageW(ctypes.byref(msg))

user32.UnhookWindowsHookEx(hook)