import json
import os
from pathlib import Path
import sys

class ConfigManager:
    def __init__(self):
        self.default_config = {
            "max_pinyin_length": 100,
            "auto_start": True
        }
        
        self.config_path = Path(self.get_config_path())
        
        self.config = self._load_config()
    
    def get_config_path(self):
        if getattr(sys, 'frozen', False):
            return os.path.join(os.path.dirname(sys.executable), 'config.json')
        else:
            return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    
    def _load_config(self) -> dict:
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                return {**self.default_config, **config}
            else:
                self.save_config(self.default_config)
                return self.default_config
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return self.default_config
    
    def save_config(self, config=None):
        if config:
            self.config = config
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get_hotkey(self) -> str:
        return self.config.get("hotkey", self.default_config["hotkey"])
    
    def set_hotkey(self, hotkey: str):
        self.config["hotkey"] = hotkey
        self.save_config() 