import sys
import os

import pythoncom
pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon
from keyboard import add_hotkey, remove_hotkey
from core.input_recovery import InputRecovery
from core.window_manager import WindowManager
from utils.logger import Logger

def get_icon_path(size):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, 'resources', 'icons', f'app_icon_{size}.png')

class PinyinRecoveryApp:
    def __init__(self):
        """
        初始化应用程序
        - QApplication 实例
        - 窗口管理器
        - 输入恢复器
        - 日志记录器
        """
        self.app = QApplication(sys.argv)
        self.window_manager = WindowManager()  # 窗口管理器
        self.input_recovery = InputRecovery(self.window_manager)  # 输入恢复核心功能
        self.logger = Logger()  # 日志记录器
        
        self.app.setQuitOnLastWindowClosed(False)
        
        icon_path = get_icon_path(128)
        app_icon = QIcon(icon_path)
        self.app.setWindowIcon(app_icon)
        
        self.logger.info("应用程序启动")
        self.setup_tray()
        self.setup_hotkey()
        
    ## 设置系统托盘图标
    def setup_tray(self):
        self.tray = QSystemTrayIcon()
        icon_path = get_icon_path(32)
        self.tray.setIcon(QIcon(icon_path))
        self.tray_menu = QMenu()
        
        quit_action = self.tray_menu.addAction("退出")
        quit_action.triggered.connect(self.quit_app)
        
        self.tray.setContextMenu(self.tray_menu)
        self.tray.show()

    ## 设置固定快捷键 Ctrl+~
    def setup_hotkey(self):
        add_hotkey('ctrl+~', self.recover_input)
        self.logger.info("已设置快捷键: ctrl+~")
        
    ## 恢复输入
    def recover_input(self):
        self.logger.info("触发快捷键，开始恢复输入...")
        self.input_recovery.recover()
        
    def quit_app(self):
        try:
            remove_hotkey('ctrl+~')
        except:
            self.logger.warning("移除快捷键失败")
            
        self.tray.hide()
        self.app.quit()
        
    def run(self):
        return self.app.exec_()

if __name__ == "__main__":
    try:
        if not os.path.exists('logs'):
            os.makedirs('logs')
        app = PinyinRecoveryApp()
        sys.exit(app.run())
    finally:
        pythoncom.CoUninitialize() 