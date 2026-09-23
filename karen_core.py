import os

class KarenCore:
    APP_NAME = "KAREN"
    VERSION = "2.0.0-modular"
    DEFAULT_MODEL = "phi4-mini"
    BASE_DIR = r"D:\Project-Karen"
    
    @staticmethod
    def initialize_environment():
        os.makedirs(os.path.join(KarenCore.BASE_DIR, "actions"), exist_ok=True)
        os.makedirs(os.path.join(KarenCore.BASE_DIR, "ui_modules"), exist_ok=True)