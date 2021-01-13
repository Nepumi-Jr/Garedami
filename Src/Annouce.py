"""
    Use for print
"""

from sys import platform


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def printWarning(text):
    if platform == "linux" or platform == "linux2":
        print(f"{bcolors.WARNING}/!\\ Warnning:{text}{bcolors.ENDC}")
    elif platform == "darwin":
        print(f"{bcolors.WARNING}/!\\ Warnning:{text}{bcolors.ENDC}")
    else:
        print(f"/!\\ Warnning : {text}")

def printError(text):
    if platform == "linux" or platform == "linux2":
        print(f"{bcolors.FAIL}\a(X) Warnning:{text}{bcolors.ENDC}")
    elif platform == "darwin":
        print(f"{bcolors.FAIL}\a(X) Warnning:{text}{bcolors.ENDC}")
    else:
        print(f"\a(X) Warnning : {text}")

if __name__ == "__main__":
    printWarning("Test Warnning")
    printError("Test Error")

