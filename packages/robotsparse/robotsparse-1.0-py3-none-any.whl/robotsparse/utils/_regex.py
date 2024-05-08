import re

def searchForGroup(pattern: str, text: str, group: str, case_sensitive: bool = True):
    flags = re.DOTALL | re.MULTILINE if case_sensitive else re.DOTALL | re.MULTILINE | re.IGNORECASE
    searchedText = re.search(pattern, text, flags=flags)
    try:
        return searchedText.group(group)
    except:
        return None


