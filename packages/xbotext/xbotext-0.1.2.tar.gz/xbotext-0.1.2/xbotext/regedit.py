import winreg


def is_show_file_ext():
    """检查是否显示文件扩展名"""
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced')
    value, _ = winreg.QueryValueEx(key, 'HideFileExt')
    winreg.CloseKey(key)
    return value == 0


def set_show_file_ext():
    """设置显示文件扩展名"""
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', 0, winreg.KEY_WRITE)
    winreg.SetValueEx(key, 'HideFileExt', 0, winreg.REG_DWORD, 0)
    winreg.CloseKey(key)




