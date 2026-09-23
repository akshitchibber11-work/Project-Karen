class SlangNormalizer:
    # Dictionary mapping casual user inputs / slang to formal system targets
    SLANG_MAP = {
        # Apps & Editors
        "da vinchi": "davinci resolve",
        "davinci": "davinci resolve",
        "resolve": "davinci resolve",
        "vsc": "vscode",
        "code": "vscode",
        "vs code": "vscode",
        "chrome": "chrome",
        "browser": "chrome",
        "notepad": "notepad",
        "spotify": "spotify",
        "music": "spotify",
        
        # System Actions
        "ram": "memory",
        "stats": "diagnostics",
        "diag": "diagnostics",
        "hw": "diagnostics",
        "files": "list files",
        "directory": "list files"
    }

    @staticmethod
    def normalize(text):
        """Takes raw user input, strips it, and checks if any slang/shorthand matches."""
        text_lower = text.lower().strip()
        
        # Check direct match first
        if text_lower in SlangNormalizer.SLANG_MAP:
            return SlangNormalizer.SLANG_MAP[text_lower]
            
        # Check substring matches (e.g. "open da vinchi" -> clean to "open davinci resolve")
        for slang, target in SlangNormalizer.SLANG_MAP.items():
            if slang in text_lower:
                text_lower = text_lower.replace(slang, target)
                
        return text_lower