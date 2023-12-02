import sys
import cli.start as cli
import gui.start as gui

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        cli.run()
    else:
        gui.run()
