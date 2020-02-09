# Stubs for syllabipy.legalipy (Python 3)

from typing import List

def LegaliPy(word: str, onsets: List[str]) -> List[str]: ...
def getOnsets(
    text: str, threshold: float = 0.0002, clean: bool = True
) -> List[str]: ...
