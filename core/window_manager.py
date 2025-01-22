import pygetwindow as gw
from pywinauto import Desktop
from utils.logger import Logger

class WindowManager:
    def __init__(self):
        self.last_active_window = None
        self.logger = Logger()
        
    ## 获取最后活动的窗口
    def get_last_active_window(self):
        try:
            window = gw.getActiveWindow()
            if window:
                self.last_active_window = window
                self.logger.info(f"当前活动窗口: {window.title}")
                return window
            if self.last_active_window:
                self.logger.info(f"使用上一个活动窗口: {self.last_active_window.title}")
            else:
                self.logger.warning("没有找到活动窗口")
            return self.last_active_window
        except Exception as e:
            self.logger.error(f"获取窗口失败: {str(e)}")
            return self.last_active_window
            
    ## 将焦点设置到指定窗口
    def focus_window(self, window):
        try:
            if window:
                window.activate()
                self.logger.info(f"已激活窗口: {window.title}")
                return True
            self.logger.warning("无法激活空窗口")
        except Exception as e:
            self.logger.error(f"窗口激活失败: {str(e)}")
        return False 