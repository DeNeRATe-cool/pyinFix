import win32clipboard
import win32con
import keyboard
import time
import win32gui
from utils.logger import Logger
from core.pinyin_utils import translate_pinyin_to_Chinese

class InputRecovery:
    def __init__(self, window_manager):
        self.window_manager = window_manager
        self.logger = Logger()
        
    ## 获取输入框内容
    def get_input_text(self, window):
        try:
            self.logger.info("开始获取输入文本...")
            
            old_clipboard = self.get_clipboard_text()
            
            self.clear_clipboard()
            
            hwnd = win32gui.GetForegroundWindow()
            self.logger.info(f"当前窗口句柄: {hwnd}")
            
            keyboard.press('ctrl+a')
            time.sleep(0.1)
            keyboard.release('ctrl+a')
            time.sleep(0.1)
            keyboard.press('ctrl+c')
            time.sleep(0.1)
            keyboard.release('ctrl+c')
            time.sleep(0.2)
            
            text = self.get_clipboard_text()
            self.logger.info(f"获取到的文本: {text}")
            
            if old_clipboard:
                self.set_clipboard_text(old_clipboard)
            
            return text
            
        except Exception as e:
            self.logger.error(f"获取输入文本失败: {str(e)}")
            return None
            
    ## 获取剪贴板文本
    def get_clipboard_text(self):
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                text = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
            else:
                text = ""
            win32clipboard.CloseClipboard()
            return text
        except:
            return ""
            
    ## 清空剪贴板
    def clear_clipboard(self):
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.CloseClipboard()
        except:
            pass
            
    ## 设置剪贴板文本
    def set_clipboard_text(self, text):
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text, win32con.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
        except:
            pass

    ## 恢复输入状态并逐个输入汉字
    def restore_input_state(self, window, pinyin):
        try:
            self.window_manager.focus_window(window)
            time.sleep(0.1)

            for char in pinyin:
                keyboard.write(char)
                self.logger.info(f"输入汉字: {char}")
                time.sleep(0.1)
            
            return True
        except Exception as e:
            self.logger.error(f"恢复输入状态失败: {str(e)}")
            return False
            
    ## 恢复拼音输入状态
    def recover(self):
        try:
            window = self.window_manager.get_last_active_window()
            if not window:
                self.logger.error("未找到活动窗口")
                return False
                
            text = self.get_input_text(window)
            self.logger.info(f"获取到的文本: {text}")
            if not text:
                return False
            
            chinese_text = self.replace_pinyin_with_chinese(text)
            self.logger.info(f"替换后的中文文本: {chinese_text}")
            
            self.restore_input_state(window, chinese_text)
            return True
            
        except Exception as e:
            self.logger.error(f"恢复输入失败: {str(e)}")
            return False

    def replace_pinyin_with_chinese(self, input_text):
        return translate_pinyin_to_Chinese(input_text)