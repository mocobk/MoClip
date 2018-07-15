from ctypes import windll, create_unicode_buffer, c_void_p, c_uint, c_wchar_p
import win32con
import win32clipboard as wc
from PIL import ImageGrab, Image

kernel32 = windll.kernel32
GlobalLock = kernel32.GlobalLock
GlobalLock.argtypes = [c_void_p]
GlobalLock.restype = c_void_p
GlobalUnlock = kernel32.GlobalUnlock
GlobalUnlock.argtypes = [c_void_p]

user32 = windll.user32
GetClipboardData = user32.GetClipboardData
GetClipboardData.restype = c_void_p

DragQueryFile = windll.shell32.DragQueryFileW
DragQueryFile.argtypes = [c_void_p, c_uint, c_wchar_p, c_uint]

CF_HDROP = 15


def get_clipboard_files() -> list:
    """get clipboard files path list"""
    file_list = []
    if user32.OpenClipboard(None):
        hGlobal = user32.GetClipboardData(CF_HDROP)
        if hGlobal:
            hDrop = GlobalLock(hGlobal)
            if hDrop:
                count = DragQueryFile(hDrop, 0xFFFFFFFF, None, 0)
                for i in range(count):
                    length = DragQueryFile(hDrop, i, None, 0)
                    buffer = create_unicode_buffer(length)
                    DragQueryFile(hDrop, i, buffer, length + 1)
                    file_list.append(buffer.value)
                GlobalUnlock(hGlobal)
        user32.CloseClipboard()
    return file_list


def get_clipboard_text() -> str:
    """get clipboard plaintext"""
    wc.OpenClipboard()
    text = None
    try:
        text = wc.GetClipboardData(win32con.CF_UNICODETEXT)
    except TypeError:
        pass
    wc.CloseClipboard()
    return text


def get_clipboard_image() -> Image.Image:
    """get clipboard Image Object"""
    img_obj = ImageGrab.grabclipboard()
    if isinstance(img_obj, Image.Image):
        return img_obj


def set_clipboard_text(text: str) -> None:
    """set clipboard plaintext"""
    wc.OpenClipboard()
    wc.EmptyClipboard()
    wc.SetClipboardData(win32con.CF_UNICODETEXT, text)
    wc.CloseClipboard()


if __name__ == '__main__':
    print(get_clipboard_files())
    print(get_clipboard_text())
    # set_clipboard_text('hahahaahha')
    img = get_clipboard_image()
    print(img)
