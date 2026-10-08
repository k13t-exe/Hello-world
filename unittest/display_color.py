import os
import sys
import unittest

RESET = "\033[0m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"

class ColorResult(unittest.TextTestResult):
    def getDescription(self, test):
        lines = super().getDescription(test).split("\n")
        lines[1:] = [f"{CYAN}{line}{RESET}" for line in lines[1:]]
        return "\n".join(lines)

    def _write_status(self, test, status):
        if status == "ok":
            color = GREEN
        elif status in ("FAIL", "ERROR"):
            color = RED
        else:
            color = YELLOW
        super()._write_status(test, f"{color}{status}{RESET}")


use_color = (sys.stdout.isatty() or os.environ.get("FORCE_COLOR")) \
    and not os.environ.get("NO_COLOR")
if use_color:
    unittest.TextTestRunner.resultclass = ColorResult
