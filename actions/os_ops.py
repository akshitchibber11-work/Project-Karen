import os
import psutil

class OSOps:
    @staticmethod
    def close_application(app_name):
        app_name = app_name.lower().strip()
        killed = False
        for proc in psutil.process_iter(['name']):
            try:
                if app_name in proc.info['name'].lower():
                    proc.kill()
                    killed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        if killed:
            return f"Terminated processes matching '{app_name}'."
        return f"No active process found matching '{app_name}'."

    @staticmethod
    def list_directory(path="D:\\Project-Karen"):
        try:
            files = os.listdir(path)
            return f"Files in {path}:\n" + "\n".join([f" - {f}" for f in files])
        except Exception as e:
            return f"Could not read directory: {str(e)}"
