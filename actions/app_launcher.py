import os
import subprocess
import glob

class AppLauncher:
    @staticmethod
    def find_and_open_app(app_query):
        app_query = app_query.lower().strip()
        if "chrome" in app_query:
            os.system("start chrome")
            return "Launching Google Chrome, sir."
        elif "code" in app_query or "vscode" in app_query:
            os.system("code")
            return "Launching Visual Studio Code, sir."
        elif "davinci" in app_query or "resolve" in app_query:
            resolve_path = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"
            if os.path.exists(resolve_path):
                subprocess.Popen([resolve_path])
                return "Launching DaVinci Resolve."
        search_paths = [
            os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs\**\*.lnk"),
            os.path.expandvars(r"%AppData%\Microsoft\Windows\Start Menu\Programs\**\*.lnk")
        ]
        for pattern in search_paths:
            for lnk in glob.glob(pattern, recursive=True):
                filename = os.path.basename(lnk).lower()
                if app_query in filename:
                    try:
                        os.startfile(lnk)
                        return f"Launching {os.path.splitext(os.path.basename(lnk))[0]}, sir."
                    except Exception:
                        pass
        try:
            subprocess.Popen(f"start {app_query}", shell=True)
            return f"Executing system request for {app_query}."
        except Exception as e:
            return f"Could not find or launch application matching '{app_query}': {str(e)}"

    @staticmethod
    def locate_downloaded_media(file_query):
        downloads_path = os.path.expandvars(r"%USERPROFILE%\Downloads")
        file_query = file_query.lower().strip()
        pattern = os.path.join(downloads_path, f"*{file_query}*")
        matches = glob.glob(pattern)
        if matches:
            found_file = matches[0]
            file_size_mb = os.path.getsize(found_file) / (1024 * 1024)
            return f"Found media file: {os.path.basename(found_file)} ({file_size_mb:.1f} MB)\nLocated at: {found_file}"
        else:
            return f"Could not find any file matching '{file_query}' in your Downloads folder."
