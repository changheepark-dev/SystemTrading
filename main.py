from strategy.RSIStrategy import *
import sys
import os

from api.Kiwoom import *

def main():
    app = QApplication(sys.argv)

    rsi_strategy = RSIStrategy()

    rsi_strategy.start()

    app.exec_()

if __name__ == "__main__":
    main()
    os.execl(sys.executable, sys.executable, *sys.argv)
